// Onboarding video batch: Cheeko setup, screen by screen, into appshots/setup.
//
//   flutter test test/appshots/onboarding_shots_test.dart
import 'dart:async';

import 'package:cheekoai_parent_app/controllers/toy_activation_controller.dart';
import 'package:cheekoai_parent_app/core/themes/app_colors.dart';
import 'package:cheekoai_parent_app/models/provisioning_models.dart';
import 'package:cheekoai_parent_app/core/themes/app_typography.dart'
    show kHomeBackgroundGradient;
import 'package:cheekoai_parent_app/screens/home/toy_activation_screen.dart';
import 'package:cheekoai_parent_app/screens/main_navigation_screen.dart';
import 'package:cheekoai_parent_app/services/ble_provisioning_service.dart';
import 'package:cheekoai_parent_app/widgets/toy_activation/ble_provisioning_step_widget.dart';
import 'package:cheekoai_parent_app/widgets/toy_activation/provisioning_method_step_widget.dart';
import 'package:cheekoai_parent_app/widgets/toy_activation/wifi_configuration_step_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:smooth_page_indicator/smooth_page_indicator.dart';

import 'support/sample_data.dart';
import 'support/sample_shell.dart';
import 'support/shots.dart';

/// A pretend Bluetooth radio. Every step waits on a completer the test
/// releases, so each in-between state can be photographed.
class _SampleBle extends BleProvisioningService {
  _SampleBle() : super(shouldEnsureBluetoothEnabled: false);

  final scan = Completer<List<ProvisioningDevice>>();
  final connect = Completer<ProvisioningResult>();
  final configure = Completer<ProvisioningResult>();

  static const devices = <ProvisioningDevice>[
    ProvisioningDevice(name: 'Cheeko-7F3A', address: 'A4:CF:12:3B:7F:3A', rssi: -48),
    ProvisioningDevice(name: 'Cheeko-21C9', address: 'A4:CF:12:3B:21:C9', rssi: -71),
  ];

  @override
  Future<List<ProvisioningDevice>> scanForDevices({
    void Function(List<ProvisioningDevice> devices)? onDevicesChanged,
  }) => scan.future;

  @override
  Future<ProvisioningResult> connectToDevice(ProvisioningDevice device) =>
      connect.future;

  @override
  Future<List<ProvisioningWifiNetwork>> scanDeviceWifiNetworks({
    void Function(List<ProvisioningWifiNetwork>)? onNetworksChanged,
  }) async => <ProvisioningWifiNetwork>[
    for (final n in sampleCheekoScan())
      ProvisioningWifiNetwork(ssid: n['ssid'] as String, rssi: n['rssi'] as int),
  ];

  @override
  Future<void> keepConnectionAlive() async {}

  @override
  Future<ProvisioningResult> configureConnectedDevice(
    ProvisioningCredentials credentials,
  ) => configure.future;

  @override
  Future<void> cancel() async {}
}

/// ToyActivationScreen's own page chrome (gradient, dot indicator, PageView)
/// around one step, for the steps whose service the screen cannot be handed.
Widget _activationChrome({
  required ToyActivationController controller,
  required int step,
  required int count,
  required Widget child,
}) {
  final pageController = PageController(initialPage: step);
  return ChangeNotifierProvider<ToyActivationController>.value(
    value: controller,
    child: Scaffold(
      backgroundColor: AppColors.homeBgTop,
      body: DecoratedBox(
        decoration: const BoxDecoration(gradient: kHomeBackgroundGradient),
        child: SafeArea(
          top: false,
          bottom: false,
          child: Builder(
            builder:
                (context) => Column(
                  children: [
                    if (step > 0)
                      Padding(
                        padding: EdgeInsets.fromLTRB(
                          16,
                          MediaQuery.of(context).padding.top + 8,
                          16,
                          8,
                        ),
                        child: Row(
                          children: [
                            Expanded(
                              child: SmoothPageIndicator(
                                controller: pageController,
                                count: count,
                                effect: ExpandingDotsEffect(
                                  activeDotColor: AppColors.orange,
                                  dotColor: AppColors.orange.withValues(
                                    alpha: 0.25,
                                  ),
                                  dotHeight: 8,
                                  dotWidth: 18,
                                  expansionFactor: 4,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    Expanded(
                      child: PageView(
                        controller: pageController,
                        physics: const NeverScrollableScrollPhysics(),
                        children: [
                          for (var i = 0; i < count; i++)
                            i == step ? child : const SizedBox.shrink(),
                        ],
                      ),
                    ),
                  ],
                ),
          ),
        ),
      ),
    ),
  );
}

Future<void> _frames(WidgetTester tester, int n) async {
  for (var i = 0; i < n; i++) {
    await tester.pump(const Duration(milliseconds: 100));
  }
}

void main() {
  setUpAll(setUpShots);

  testWidgets('s04 setup checklist', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(ToyActivationScreen(initialStep: 0, kid: sampleKid())),
    );
    await settle(tester, rounds: 6);
    await snap(tester, 'setup/s04_setup_checklist_empty');
    for (final item in const [
      'Phone Bluetooth is ON',
      'Location Services Enabled',
      'Turn ON Cheeko',
    ]) {
      final finder = find.text(item);
      if (finder.evaluate().isEmpty) {
        debugPrint('checklist item not on screen: $item');
        continue;
      }
      await tester.ensureVisible(finder.first);
      await tester.pump();
      await tester.tap(finder.first);
      await tester.pump();
      await _frames(tester, 3);
    }
    // Scrolled so both ticked items, the Cheeko hint and the (now enabled)
    // Continue button share the screen.
    final list = find
        .byWidgetPredicate(
          (w) => w is Scrollable && w.axisDirection == AxisDirection.down,
        )
        .first;
    final position = tester.state<ScrollableState>(list).position;
    position.jumpTo(position.maxScrollExtent);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, 'setup/s04_setup_checklist');
    await finish(tester);
  });

  testWidgets('s05 setup method', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    final controller = ToyActivationController(
      kid: sampleKid(),
      initialStep: 1,
      autoInitialize: false,
    );
    await tester.pumpWidget(
      app.wrap(
        _activationChrome(
          controller: controller,
          step: 1,
          count: 3,
          child: ProvisioningMethodStepWidget(onBack: () {}, onContinue: () {}),
        ),
      ),
    );
    await settle(tester, rounds: 4);
    await snap(tester, 'setup/s05_setup_method');
    await finish(tester);
  });

  testWidgets('s06-s08 bluetooth setup', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    final ble = _SampleBle();
    final controller = ToyActivationController(
      kid: sampleKid(),
      initialStep: 1,
      autoInitialize: false,
    );
    await tester.pumpWidget(
      app.wrap(
        _activationChrome(
          controller: controller,
          step: 1,
          count: 3,
          child: BleProvisioningStepWidget(
            onBack: () {},
            onUseWifiFallback: () {},
            onProvisioned: controller.moveToActivationStep,
            service: ble,
            loadConnectedDevices: () async => const <ProvisioningDevice>[],
            showActivationShortcut: true,
          ),
        ),
      ),
    );
    await _frames(tester, 12);
    await snap(tester, 'setup/s06_scanning');

    ble.scan.complete(_SampleBle.devices);
    await _frames(tester, 8);
    await snap(tester, 'setup/s06b_found');

    ble.connect.complete(const ProvisioningResult.success());
    await _frames(tester, 12);
    await snap(tester, 'setup/s07_wifi_list');

    await tester.tap(find.text('Sharma Home WiFi').first);
    await _frames(tester, 4);
    await tester.enterText(find.byType(TextField).last, 'aarav@2020');
    await _frames(tester, 4);
    await snap(tester, 'setup/s07b_wifi_password');

    await tester.tap(find.text('Connect').last);
    await _frames(tester, 10);
    await snap(tester, 'setup/s08_sending_bluetooth');

    ble.configure.complete(const ProvisioningResult.success());
    await _frames(tester, 10);
    debugPrint('after success, step=${controller.currentStep}');
    await finish(tester);
  });

  testWidgets('s07-s08 wifi method (Cheeko hotspot)', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    final controller = ToyActivationController(
      kid: sampleKid(),
      initialStep: 2,
      initialProvisioningMethod: ProvisioningMethod.wifi,
      autoInitialize: false,
    );
    final submit = Completer<void>();
    backend.gate =
        (method, uri) => uri.path == '/submit' ? submit.future : null;
    addTearDown(() => backend.gate = null);

    await tester.pumpWidget(
      app.wrap(
        _activationChrome(
          controller: controller,
          step: 2,
          count: 4,
          child: WifiConfigurationStepWidget(onBack: () {}),
        ),
      ),
    );
    await settle(tester, rounds: 4);
    await snap(tester, 'setup/s07_wifi_list_hotspot_method');

    await tester.tap(find.text('Sharma Home WiFi').first);
    await _frames(tester, 4);
    final fields = find.byType(TextField);
    if (fields.evaluate().isNotEmpty) {
      await tester.enterText(fields.last, 'aarav@2020');
      await _frames(tester, 4);
    }
    await snap(tester, 'setup/s07b_wifi_password_hotspot_method');

    final connect = find.textContaining('Connect');
    await tester.tap(connect.last);
    await _frames(tester, 6);
    await snap(tester, 'setup/s08_sending');

    submit.complete();
    await _frames(tester, 6);
    await snap(tester, 'setup/s08b_success');
    printRequests('hotspot');
    await finish(tester);
  });

  testWidgets('s10 setup complete', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(const MainNavigationScreen()));
    await settle(tester, rounds: 10);
    // What ToyActivationController.completeRegisteredDeviceProvisioning
    // shows: its own SnackBar, over Home.
    final context = tester.element(find.byType(MainNavigationScreen));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(controllerSuccessMessage())),
    );
    await _frames(tester, 6);
    await snap(tester, 'setup/s10_setup_complete');
    await finish(tester);
  });
}

String controllerSuccessMessage() =>
    ToyActivationController(autoInitialize: false).provisioningSuccessMessage;
