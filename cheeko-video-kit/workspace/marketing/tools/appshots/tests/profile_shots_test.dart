// Profile tab and the screens a parent reaches from it, by tapping.
//
//   flutter test test/appshots/profile_shots_test.dart
import 'package:cheekoai_parent_app/screens/home/home_reference_widgets.dart';
import 'package:cheekoai_parent_app/screens/main_navigation_screen.dart';
import 'package:cheekoai_parent_app/screens/profile/child_profile_screen.dart';
import 'package:cheekoai_parent_app/screens/profile/parent_profile.dart';
import 'package:cheekoai_parent_app/services/notification_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import 'support/sample_shell.dart';
import 'support/shots.dart';

Finder _scrollableIn(Type screen) => find
    .descendant(of: find.byType(screen), matching: find.byType(Scrollable))
    .first;

/// The app opens on Home, which reads the family's toys; the parent then
/// taps the Profile tab. (Opening the shell straight on Profile would leave
/// the toy list unread, and "Wifi Setup" would say no Cheeko was found.)
Future<void> _openProfile(WidgetTester tester) async {
  await preparePhone(tester);
  final app = SampleApp();
  await tester.pumpWidget(app.wrap(const MainNavigationScreen()));
  await settle(tester, rounds: 10);
  await tester.tap(find.text('Profile').last);
  await tester.pump();
  await settle(tester, rounds: 10);
}

/// Lets layout overflows through without failing the test, and collects
/// them. Only for screens where the app itself overflows at iPhone width.
List<String> _tolerateOverflows(WidgetTester tester) {
  final seen = <String>[];
  final original = FlutterError.onError;
  FlutterError.onError = (details) {
    final text = details.exceptionAsString();
    if (text.contains('overflowed')) {
      seen.add(text.split('\n').first);
      return;
    }
    original?.call(details);
  };
  addTearDown(() => FlutterError.onError = original);
  return seen;
}

/// Taps a row on the Profile tab, scrolling it into view first when it sits
/// under the floating navigation capsule.
Future<void> _tapRow(WidgetTester tester, String title) async {
  final row = find.text(title).first;
  final list = _scrollableIn(ParentProfileScreen);
  if (tester.getCenter(row).dy > kPhone.height - 140) {
    final position = tester.state<ScrollableState>(list).position;
    position.jumpTo(
      (position.pixels + tester.getCenter(row).dy - kPhone.height / 2).clamp(
        0,
        position.maxScrollExtent,
      ),
    );
    await tester.pump();
  }
  await tester.tap(row);
  await tester.pump();
}

void main() {
  setUpAll(setUpShots);

  testWidgets('10 profile tab', (tester) async {
    await _openProfile(tester);
    await snap(tester, '10_profile');
    final list = _scrollableIn(ParentProfileScreen);
    await growToFit(tester, list);
    await settle(tester, rounds: 6);
    await snap(tester, '10_profile_full');
    printRequests('profile');
    await finish(tester);
  });

  testWidgets('11 kid profile (Profile > Kid Profile)', (tester) async {
    // The "House rules & upcoming" row is wider than the phone: a Row of
    // fixed-width texts with no Expanded, 130 px too wide at 393 pt. On a
    // phone it is clipped; in a test Flutter paints debug stripes over it.
    final overflows = _tolerateOverflows(tester);
    await _openProfile(tester);
    await _tapRow(tester, 'Kid Profile');
    await settle(tester, rounds: 12);
    await snap(tester, '11_kid_profile');

    // A taller capture that stops just above Flutter's debug marker for that
    // overflow. The marker is striped box on the row plus a vertical label
    // (about 225 pt of 7.5 pt test-font glyphs) centred on the row's right
    // edge, so it reaches up into the Rules card and down into Notes.
    // Everything below that point (House rules & upcoming, Notes with its
    // suggestion chips, Save Changes) cannot be captured clean.
    final rowCenter = tester.getCenter(find.text('House rules & upcoming')).dy;
    final contentEnd = rowCenter - 115 - 6;
    debugPrint('kid profile: row centre $rowCenter, capture ends $contentEnd');
    setViewHeight(tester, contentEnd + kBottomInset);
    await tester.pump();
    await settle(tester, rounds: 6);
    await snap(tester, '11_kid_profile_full');
    debugPrint('overflows: $overflows');
    printRequests('kid profile');
    await finish(tester);
  });

  testWidgets('12 notification settings', (tester) async {
    // The controller's real state on a phone that has allowed notifications
    // and registered for push. Firebase Messaging cannot run in a test, so the
    // three public fields it would set are set here.
    NotificationController.instance
      ..enabled = true
      ..permissionGranted = true
      ..registered = true;
    await _openProfile(tester);
    await _tapRow(tester, 'Notifications');
    await settle(tester, rounds: 8);
    await snap(tester, '12_notifications');
    await finish(tester);
  });

  testWidgets('13 add device: who is this Cheeko for', (tester) async {
    await _openProfile(tester);
    await _tapRow(tester, 'Add Device');
    await settle(tester, rounds: 10);
    await snap(tester, '13_add_device_who');
    printRequests('add device');
    await finish(tester);
  });

  testWidgets('13 wifi setup (Bluetooth on)', (tester) async {
    // Bluetooth is switched on, so the app skips its checklist and opens the
    // Bluetooth scan directly (ProvisioningPrerequisites.areReady).
    final messenger =
        TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
    const permissions = MethodChannel(
      'flutter.baseflow.com/permissions/methods',
    );
    messenger.setMockMethodCallHandler(permissions, (call) async {
      if (call.method == 'checkServiceStatus') return 1; // enabled
      if (call.method == 'checkPermissionStatus') return 1; // granted
      if (call.method == 'requestPermissions') {
        return <int, int>{
          for (final p in (call.arguments as List).cast<int>()) p: 1,
        };
      }
      return null;
    });
    // The toy's Bluetooth plugin (esp_blufi): the scan starts and nothing has
    // answered yet, which is the first thing a parent sees.
    const blufi = MethodChannel('esp_blufi');
    messenger.setMockMethodCallHandler(blufi, (call) async => null);
    messenger.setMockStreamHandler(
      const EventChannel('esp_blufi/state'),
      MockStreamHandler.inline(onListen: (arguments, events) {}),
    );
    addTearDown(() {
      messenger.setMockMethodCallHandler(permissions, null);
      messenger.setMockMethodCallHandler(blufi, null);
      messenger.setMockStreamHandler(
        const EventChannel('esp_blufi/state'),
        null,
      );
    });

    await _openProfile(tester);
    await _tapRow(tester, 'Wifi Setup');
    for (var i = 0; i < 12; i++) {
      await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 50)),
      );
      await tester.pump(const Duration(milliseconds: 150));
    }
    await snap(tester, '13_wifi_setup');
    printRequests('wifi setup');
    await finish(tester);
  });
}
