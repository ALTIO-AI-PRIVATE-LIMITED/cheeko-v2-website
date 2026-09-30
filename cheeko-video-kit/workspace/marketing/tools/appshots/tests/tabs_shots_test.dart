// Device and Analytics tabs of the real nav shell, and House rules.
//
//   flutter test test/appshots/tabs_shots_test.dart
import 'dart:async';

import 'package:cheekoai_parent_app/models/kid.dart';
import 'package:cheekoai_parent_app/screens/analytics/analytics_screen.dart';
import 'package:cheekoai_parent_app/screens/device/device_tab_screen.dart';
import 'package:cheekoai_parent_app/screens/main_navigation_screen.dart';
import 'package:cheekoai_parent_app/screens/profile/house_rules_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'support/fake_http.dart';
import 'support/sample_data.dart';
import 'support/sample_shell.dart';
import 'support/shots.dart';

/// Scrolls [scrollable] so [target]'s top sits [fromTop] points below the
/// status bar, building lazily-built content on the way.
Future<void> scrollToTarget(
  WidgetTester tester,
  Finder scrollable,
  Finder target, {
  double fromTop = 16,
}) async {
  if (target.evaluate().isEmpty) {
    await tester.scrollUntilVisible(target, 300, scrollable: scrollable);
    await tester.pump();
  }
  final position = tester.state<ScrollableState>(scrollable).position;
  final dy = tester.getTopLeft(target.first).dy;
  position.jumpTo(
    (position.pixels + dy - kTopInset - fromTop).clamp(
      0,
      position.maxScrollExtent,
    ),
  );
  await tester.pump();
  await settle(tester, rounds: 4);
}

Finder scrollableIn(Type screen) => find
    .descendant(of: find.byType(screen), matching: find.byType(Scrollable))
    .first;

void main() {
  setUpAll(setUpShots);

  testWidgets('03 device tab', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    await snap(tester, '03_device');

    final list = scrollableIn(DeviceTabScreen);
    await scrollToTarget(tester, list, find.text('Controls'));
    await snap(tester, '03_device_controls');

    // The parent turns the volume down to 30 and switches sleep mode on.
    // Both go through the app's own handlers; the Save button lights up.
    final volume = find.byType(Slider).first;
    tester.widget<Slider>(volume).onChanged!(30);
    await tester.pump();
    final sleepRow = find.ancestor(
      of: find.text('Sleep mode'),
      matching: find.byType(Row),
    );
    await tester.tap(
      find.descendant(of: sleepRow.first, matching: find.byType(Switch)),
    );
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_controls_adjusted');

    printRequests('device');
    await finish(tester);
  });

  testWidgets('06 analytics tab', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 2)),
    );
    await settle(tester, rounds: 12);
    await snap(tester, '06_analytics_day');

    final list = scrollableIn(AnalyticsScreen);
    await scrollToTarget(tester, list, find.text('Quiz progress'));
    await snap(tester, '06_analytics_day_quiz');
    tester.state<ScrollableState>(list).position.jumpTo(0);
    await tester.pump();

    await growToFit(tester, list);
    await settle(tester, rounds: 6);
    await snap(tester, '06_analytics_day_full');

    setViewHeight(tester, kPhone.height);
    await tester.pump();
    tester.state<ScrollableState>(list).position.jumpTo(0);
    await tester.pump();

    await tester.tap(find.text('Week'));
    await tester.pump();
    await settle(tester, rounds: 6);
    // Two weeks back: a finished Monday-Sunday week (see sample_data.dart).
    for (var i = 0; i < 2; i++) {
      await tester.tap(find.byTooltip('Previous week'));
      await tester.pump();
      await settle(tester, rounds: 6);
    }
    await snap(tester, '06_analytics_week');
    await scrollToTarget(tester, list, find.text('Activity'));
    await snap(tester, '06_analytics_week_breakdown');
    tester.state<ScrollableState>(list).position.jumpTo(0);
    await tester.pump();
    await growToFit(tester, list);
    await settle(tester, rounds: 6);
    await snap(tester, '06_analytics_week_full');

    printRequests('analytics');
    debugPrint('api calls: ${app.api.calls}');
    await finish(tester);
  });

  testWidgets('04 house rules', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(HouseRulesScreen(kid: sampleKid())));
    await settle(tester, rounds: 10);
    await snap(tester, '04_house_rules');

    final list = scrollableIn(HouseRulesScreen);
    final position = tester.state<ScrollableState>(list).position;
    position.jumpTo(position.maxScrollExtent);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '04_house_rules_events');
    printRequests('house rules');
    await finish(tester);
  });

  // ---------------------------------------------------------------------
  // Walkthrough-video additions (2026-09-29)
  // ---------------------------------------------------------------------

  testWidgets('03 device: full page, actions, theme picker', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    final list = scrollableIn(DeviceTabScreen);

    // The whole tab in one tall capture.
    await growToFit(tester, list);
    await settle(tester, rounds: 6);
    await snap(tester, '03_device_full');
    setViewHeight(tester, kPhone.height);
    await tester.pump();

    // Scrolled to the bottom: "Device actions" and Remove Device.
    final position = tester.state<ScrollableState>(list).position;
    position.jumpTo(position.maxScrollExtent);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_actions');

    // Controls on screen, then the Theme row tapped: the app's own dialog.
    await scrollToTarget(tester, list, find.text('Controls'));
    await tester.tap(find.text('Theme'));
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_theme_picker');
    Navigator.of(tester.element(find.text('Select theme'))).pop();
    await tester.pump();
    await settle(tester, rounds: 2);
    await finish(tester);
  });

  testWidgets('03 device controls changed (Save lit)', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    final list = scrollableIn(DeviceTabScreen);

    // Volume down to 35, brightness to 50, sleep mode on, each through the
    // page's own handlers, which is what lights the header's Save.
    final sliders = find.byType(Slider);
    tester.widget<Slider>(sliders.at(0)).onChanged!(35);
    await tester.pump();
    tester.widget<Slider>(sliders.at(1)).onChanged!(50);
    await tester.pump();
    await scrollToTarget(tester, list, find.text('Controls'));
    final sleepRow = find.ancestor(
      of: find.text('Sleep mode'),
      matching: find.byType(Row),
    );
    await tester.tap(
      find.descendant(of: sleepRow.first, matching: find.byType(Switch)),
    );
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_controls_changed_switches');

    // Back to the top: Save is now the solid orange pill.
    tester.state<ScrollableState>(list).position.jumpTo(0);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_controls_changed');

    await growToFit(tester, list);
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_controls_changed_full');
    printRequests('device changed');
    await finish(tester);
  });

  testWidgets('03 device with two toys: switcher open', (tester) async {
    await preparePhone(tester);
    sampleTwoToys = true;
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    await snap(tester, '03_device_two_toys_closed');
    await tester.tap(find.byWidgetPredicate((w) => w is PopupMenuButton));
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_two_toys');
    printRequests('two toys');
    await finish(tester);
  });

  testWidgets('03 device with two toys, one child: switcher open', (tester) async {
    // One child per Cheeko for now: the account has only Aarav, and the
    // second toy has no child yet, so the child quick switch does not render.
    await preparePhone(tester);
    sampleTwoToys = true;
    sampleSecondKid = false;
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    expect(find.text("Who's using it now?"), findsNothing);
    await snap(tester, '03_device_two_toys_1kid_closed');
    await tester.tap(find.byWidgetPredicate((w) => w is PopupMenuButton));
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_device_two_toys_1kid');
    printRequests('two toys, one child');
    await finish(tester);
  });

  testWidgets('03 ctl: controls changed one step at a time', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 1)),
    );
    await settle(tester, rounds: 12);
    final list = scrollableIn(DeviceTabScreen);

    // Exactly the scroll of 03_device_controls, held for ctl_1..ctl_5.
    await scrollToTarget(tester, list, find.text('Controls'));
    final position = tester.state<ScrollableState>(list).position;
    final offset = position.pixels;
    Future<void> shot(String name) async {
      if (position.pixels != offset) position.jumpTo(offset);
      await tester.pump();
      await settle(tester, rounds: 4);
      debugPrint('$name at offset ${position.pixels} (want $offset)');
      await snap(tester, name);
    }

    final sliders = find.byType(Slider);
    tester.widget<Slider>(sliders.at(0)).onChanged!(35);
    await shot('03_ctl_1_vol35');

    tester.widget<Slider>(sliders.at(1)).onChanged!(50);
    await shot('03_ctl_2_bri50');

    await tester.tap(find.text('Theme'));
    await tester.pump();
    await shot('03_ctl_3_picker');

    await tester.tap(find.text('Night'));
    await tester.pump();
    await settle(tester, rounds: 4);
    expect(find.text('Select theme'), findsNothing);
    await shot('03_ctl_4_night');

    final sleepRow = find.ancestor(
      of: find.text('Sleep mode'),
      matching: find.byType(Row),
    );
    await tester.tap(
      find.descendant(of: sleepRow.first, matching: find.byType(Switch)),
    );
    await tester.pump();
    await shot('03_ctl_5_sleep');

    // The top of the tab in that state: Save lit.
    position.jumpTo(0);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_ctl_6_save');

    // Tap Save. The fake settings endpoint accepts the PATCH the way the
    // server does (merged settings, next version, synced); held open first
    // so the in-flight pill can be seen.
    final settings = app.settingsService;
    settings.patchGate = Completer<void>();
    await tester.tap(find.text('Save'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 150));
    await snap(tester, '03_ctl_7_saving');
    settings.patchGate!.complete();
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '03_ctl_7_saved');
    debugPrint('PATCH bodies: ${settings.patches}');
    debugPrint('saved: vol ${settings.payload.volume}, bri '
        '${settings.payload.brightness}, theme ${settings.payload.theme}, '
        'sleep ${settings.payload.sleepEnabled}');
    await finish(tester);
  });

  testWidgets('06 analytics: activity detail and week picker', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(const MainNavigationScreen(initialIndex: 2)),
    );
    await settle(tester, rounds: 12);
    final list = scrollableIn(AnalyticsScreen);

    // "Tap a section to view full details": Games, then Interactions.
    for (final section in const ['Games', 'Interactions']) {
      // Both tiles are on the first screen, so the page stays at the top.
      await tester.tap(find.text(section).first);
      await tester.pump();
      await settle(tester, rounds: 6);
      await snap(
        tester,
        section == 'Games'
            ? '06_analytics_activity_detail'
            : '06_analytics_activity_detail_interactions',
      );
      await tester.tap(find.byIcon(Icons.close_rounded).last);
      await tester.pump();
      await settle(tester, rounds: 4);
    }

    tester.state<ScrollableState>(list).position.jumpTo(0);
    await tester.pump();
    await tester.tap(find.text('Week'));
    await tester.pump();
    await settle(tester, rounds: 6);
    for (var i = 0; i < 2; i++) {
      await tester.tap(find.byTooltip('Previous week'));
      await tester.pump();
      await settle(tester, rounds: 6);
    }
    await tester.tap(find.byKey(const ValueKey('analytics-week-label')));
    await tester.pump();
    await settle(tester, rounds: 6);
    await snap(tester, '06_analytics_week_picker');
    await finish(tester);
  });

  testWidgets('04 house rules: bedtime 8, upcoming events', (tester) async {
    await preparePhone(tester);
    backend.handler = (method, uri, body) {
      if (uri.path.endsWith('/kids/$kKidId/events')) {
        return FakeReply.envelope(sampleUpcomingEventsJson());
      }
      return sampleBackend(method, uri, body);
    };
    final app = SampleApp();
    // As saved on the server: 8 PM, no scary stories, English + Hindi, and
    // the topics typed the way a parent types them.
    final kid = sampleKid().copyWith(
      parentRules: const ParentRules(
        bedtime: '20:00',
        noScaryStories: true,
        languages: <String>['English', 'Hindi'],
        avoidTopics: <String>['ghosts', 'horror'],
        focus: 'English words',
        note: 'Loves animals and space. Keep answers short and simple.',
      ),
    );
    await tester.pumpWidget(app.wrap(HouseRulesScreen(kid: kid)));
    await settle(tester, rounds: 10);
    await snap(tester, '04_house_rules_bedtime8');

    final list = scrollableIn(HouseRulesScreen);
    final position = tester.state<ScrollableState>(list).position;
    position.jumpTo(position.maxScrollExtent);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '04_house_rules_upcoming');
    printRequests('house rules upcoming');
    await finish(tester);
  });
}
