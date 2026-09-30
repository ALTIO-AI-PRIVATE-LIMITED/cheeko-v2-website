// Phone-sized PNG captures of real app widgets.
//
// ignore_for_file: depend_on_referenced_packages, implementation_imports
import 'dart:io';
import 'dart:ui' as ui;

import 'package:cheekoai_parent_app/core/themes/app_theme.dart';
import 'package:cheekoai_parent_app/routes/routes.dart';
import 'package:firebase_auth_platform_interface/src/pigeon/messages.pigeon.dart'
    show FirebaseAuthUserHostApi, PigeonIdTokenResult;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../support/shell_harness.dart' show setUpSignedInFirebase;
import 'fake_http.dart';
import 'sample_data.dart';

/// iPhone 15 / 15 Pro class: 393 x 852 points at 3x, so 1179 x 2556 pixels.
const Size kPhone = Size(393, 852);
const double kDpr = 3;

/// The notch/status-bar and home-indicator insets of that phone, so every
/// SafeArea lays out exactly as it would on the device.
const double kTopInset = 59;
const double kBottomInset = 34;

String get outDir =>
    Platform.environment['APPSHOTS_OUT'] ??
    '/private/tmp/claude-501/-Users-ravikumar-Cheeko-Master/'
        'ef8c9f57-8a38-4b1f-8166-dc9ced55db03/scratchpad/appshots';

final FakeBackend backend = FakeBackend(
  mediaDir: '${Directory.current.path}/test/appshots/media',
)..handler = sampleBackend;

/// Once per file: real fonts, a signed-in parent, the fake network.
Future<void> setUpShots() async {
  TestWidgetsFlutterBinding.ensureInitialized();

  final flutterRoot = Platform.environment['FLUTTER_ROOT'];
  final fonts = <String, List<String>>{
    'Nunito': ['assets/fonts/nunito-variable.ttf'],
    'SwitzerVariable': ['assets/fonts/switzer-variable.ttf'],
    'Switzer': ['assets/fonts/switzer-variable.ttf'],
  };
  for (final entry in fonts.entries) {
    final loader = FontLoader(entry.key);
    for (final asset in entry.value) {
      loader.addFont(rootBundle.load(asset));
    }
    await loader.load();
  }
  if (flutterRoot != null) {
    final dir = '$flutterRoot/bin/cache/artifacts/material_fonts';
    Future<void> fileFont(String family, List<String> files) async {
      final loader = FontLoader(family);
      for (final name in files) {
        final file = File('$dir/$name');
        if (!file.existsSync()) continue;
        loader.addFont(
          Future.value(file.readAsBytesSync().buffer.asByteData()),
        );
      }
      await loader.load();
    }

    await fileFont('MaterialIcons', ['MaterialIcons-Regular.otf']);
    // Android's system font, for the few widgets that fall outside the app
    // theme (dialog defaults, the time picker).
    await fileFont('Roboto', [
      'Roboto-Regular.ttf',
      'Roboto-Medium.ttf',
      'Roboto-Bold.ttf',
      'Roboto-Light.ttf',
    ]);
  }

  // A phone falls back to its system fonts for glyphs the app's fonts do not
  // have (emoji, arrows, check marks). The test engine has no system fonts,
  // so the Mac's own stand in: Apple Color Emoji and Arial Unicode.
  // Screens are rendered as iPhone (Ravi, 2026-09-29), so Apple's system font is the fallback. iOS-mode Material widgets
  // ask for it under its Cupertino names; the Mac's SF (SFNS.ttf) stands in for all of them.
  for (final family in const ['SFPro', 'CupertinoSystemText', 'CupertinoSystemDisplay', '.SF UI Text', '.SF UI Display']) {
    final file = File('/System/Library/Fonts/SFNS.ttf');
    if (!file.existsSync()) break;
    final loader = FontLoader(family)..addFont(Future.value(file.readAsBytesSync().buffer.asByteData()));
    await loader.load();
  }
  for (final entry in const {
    'AppleColorEmoji': '/System/Library/Fonts/Apple Color Emoji.ttc',
    'ArialUnicode': '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
  }.entries) {
    final file = File(entry.value);
    if (!file.existsSync()) continue;
    final loader = FontLoader(entry.key)
      ..addFont(Future.value(file.readAsBytesSync().buffer.asByteData()));
    await loader.load();
  }

  // Never loaded from disk: the base URL points at a host the fake network
  // answers in-process.
  dotenv.loadFromString(envString: 'MOBILE_API_BASE_URL=$kApiBase');

  await setUpSignedInFirebase();
  _mockIdToken();
  _mockConnectivity();
  HttpOverrides.global = FakeHttpOverrides(backend);
}

/// `currentUser.getIdToken()` for the services that sign their own requests.
void _mockIdToken() {
  final messenger =
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
  messenger.setMockDecodedMessageHandler<Object?>(
    BasicMessageChannel<Object?>(
      'dev.flutter.pigeon.firebase_auth_platform_interface.'
      'FirebaseAuthUserHostApi.getIdToken',
      FirebaseAuthUserHostApi.pigeonChannelCodec,
    ),
    (message) async => <Object?>[PigeonIdTokenResult(token: 'fake-token')],
  );
}

/// The phone is on Wi-Fi. connectivity_plus asks once and then listens.
void _mockConnectivity() {
  final messenger =
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
  messenger.setMockMethodCallHandler(
    const MethodChannel('dev.fluttercommunity.plus/connectivity'),
    (call) async => <String>['wifi'],
  );
  messenger.setMockStreamHandler(
    const EventChannel('dev.fluttercommunity.plus/connectivity_status'),
    MockStreamHandler.inline(
      onListen: (arguments, events) => events.success(<String>['wifi']),
    ),
  );
}

/// Grows the phone until [scrollable] has nothing left to scroll, so one
/// capture holds the whole page. Lazy lists only know their true length once
/// every child has been laid out, hence the loop.
Future<double> growToFit(WidgetTester tester, Finder scrollable) async {
  var height = kPhone.height;
  for (var i = 0; i < 8; i++) {
    final position = tester.state<ScrollableState>(scrollable).position;
    if (position.maxScrollExtent <= 0.5) break;
    height += position.maxScrollExtent;
    setViewHeight(tester, height);
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 100));
  }
  return height;
}

/// Per test: fresh preferences with every guided tour already seen, and the
/// phone's size and insets.
Future<void> preparePhone(WidgetTester tester, {double height = 852}) async {
  SharedPreferences.setMockInitialValues(<String, Object>{
    'home_tour_completed_v1_parent-1': true,
    'home_tour_completed_v1': true,
    'selected_home_device_mac_address': kMac,
  });
  // Real soft shadows, not the flat outlines tests draw by default. Put back
  // by [finish] so the binding's end-of-test check still passes.
  debugDisableShadows = false;
  // iPhone: iOS switches, back chevrons and page transitions. Reset by [finish].
  debugDefaultTargetPlatformOverride = TargetPlatform.iOS;
  // Every test starts on the one-toy family and the default fake backend; a
  // test that needs something else sets it after this call.
  sampleTwoToys = false;
  sampleSecondKid = true;
  backend
    ..handler = sampleBackend
    ..gate = null;
  HttpOverrides.global = FakeHttpOverrides(backend);
  // The app version the Profile tab shows: pubspec.yaml at d49af42.
  PackageInfo.setMockInitialValues(
    appName: 'CheekoAI',
    packageName: 'com.cheekoai.in',
    version: '3.8.36',
    buildNumber: '140',
    buildSignature: '',
  );

  setViewHeight(tester, height);
  tester.view.padding = const FakeViewPadding(
    top: kTopInset * kDpr,
    bottom: kBottomInset * kDpr,
  );
  tester.view.viewPadding = const FakeViewPadding(
    top: kTopInset * kDpr,
    bottom: kBottomInset * kDpr,
  );
  tester.platformDispatcher.textScaleFactorTestValue = 1.0;
}

void setViewHeight(WidgetTester tester, double height) {
  tester.view.devicePixelRatio = kDpr;
  tester.view.physicalSize = Size(kPhone.width * kDpr, height * kDpr);
}

/// Stand-ins for the phone's system font fallback (see [setUpShots]).
const List<String> kSystemFallback = <String>[
  'SFPro',
  'AppleColorEmoji',
  'ArialUnicode',
];

/// The app's theme with the system fallback fonts attached. Only glyphs the
/// app's own fonts lack are affected.
ThemeData get appTheme {
  final base = AppTheme.lightTheme;
  return base.copyWith(
    textTheme: base.textTheme.apply(fontFamilyFallback: kSystemFallback),
    primaryTextTheme: base.primaryTextTheme.apply(
      fontFamilyFallback: kSystemFallback,
    ),
  );
}

/// The app's own MaterialApp configuration (main.dart), minus the splash.
Widget appShell({required Widget home}) => MaterialApp(
  debugShowCheckedModeBanner: false,
  theme: appTheme,
  title: 'CheekoAI Parent App',
  onGenerateRoute: AppRoutes.onGenerateRoute,
  home: home,
);

/// Lets real image decoding finish (it runs outside the fake clock) and
/// advances the fake clock past entry animations.
Future<void> settle(
  WidgetTester tester, {
  int rounds = 8,
  Duration step = const Duration(milliseconds: 250),
}) async {
  for (var i = 0; i < rounds; i++) {
    await tester.runAsync(() async {
      await precacheVisibleImages(tester);
      await Future<void>.delayed(const Duration(milliseconds: 40));
    });
    await tester.pump(step);
  }
}

Future<void> precacheVisibleImages(WidgetTester tester) async {
  final futures = <Future<void>>[];
  for (final element in find.byType(Image).evaluate()) {
    final image = (element.widget as Image).image;
    futures.add(
      precacheImage(image, element, onError: (_, _) {}),
    );
  }
  for (final element in find.byType(DecoratedBox).evaluate()) {
    final decoration = (element.widget as DecoratedBox).decoration;
    if (decoration is BoxDecoration && decoration.image != null) {
      futures.add(
        precacheImage(decoration.image!.image, element, onError: (_, _) {}),
      );
    }
  }
  for (final element in find.byType(Container).evaluate()) {
    final decoration = (element.widget as Container).decoration;
    if (decoration is BoxDecoration && decoration.image != null) {
      futures.add(
        precacheImage(decoration.image!.image, element, onError: (_, _) {}),
      );
    }
  }
  // Bounded: a load that needs the fake clock to advance cannot finish in
  // here, and the next pump will pick it up.
  await Future.wait(futures).timeout(
    const Duration(seconds: 2),
    onTimeout: () => <void>[],
  );
}

/// Writes what is on the phone right now to `<outDir>/<name>.png`.
Future<void> snap(WidgetTester tester, String name) async {
  await tester.runAsync(() async {
    final view = tester.binding.renderViews.first;
    final layer = view.debugLayer! as OffsetLayer;
    final image = await layer.toImage(view.paintBounds);
    final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
    final file = File('$outDir/$name.png');
    file.parent.createSync(recursive: true);
    file.writeAsBytesSync(bytes!.buffer.asUint8List());
    image.dispose();
  });
  debugPrint('📸 wrote $name.png');
}

/// Unmounts the app so its timers stop, then runs the clock out.
Future<void> finish(WidgetTester tester) async {
  await tester.pumpWidget(const SizedBox.shrink());
  await tester.pump(const Duration(seconds: 70));
  debugDisableShadows = true;
  debugDefaultTargetPlatformOverride = null;
  tester.view.reset();
  tester.platformDispatcher.clearAllTestValues();
}

/// Scrolls the first scrollable under [finder] to [offset] and lets the frame
/// land.
Future<void> scrollTo(
  WidgetTester tester,
  Finder scrollable,
  double offset,
) async {
  final state = tester.state<ScrollableState>(scrollable);
  state.position.jumpTo(offset);
  await tester.pump();
}

void printRequests(String label) {
  debugPrint('--- requests during $label (${backend.requests.length})');
  for (final request in backend.requests) {
    debugPrint('    $request');
  }
  backend.requests.clear();
}
