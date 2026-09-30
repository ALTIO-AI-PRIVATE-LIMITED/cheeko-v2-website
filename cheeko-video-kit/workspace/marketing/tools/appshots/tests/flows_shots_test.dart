// Screens reached from Home the way a parent reaches them: by tapping.
//
//   flutter test test/appshots/flows_shots_test.dart
import 'package:cheekoai_parent_app/screens/home/home_screen.dart';
import 'package:cheekoai_parent_app/screens/main_navigation_screen.dart';
import 'package:cheekoai_parent_app/widgets/streak_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'support/sample_shell.dart';
import 'support/shots.dart';

Finder get _homeList => find
    .descendant(of: find.byType(HomeScreen), matching: find.byType(Scrollable))
    .first;

Future<void> _openHome(WidgetTester tester) async {
  await preparePhone(tester);
  final app = SampleApp();
  await tester.pumpWidget(app.wrap(const MainNavigationScreen()));
  await settle(tester, rounds: 10);
}

/// Scrolls Home so [target]'s top sits [fromTop] points below the status bar.
Future<void> _scrollHomeTo(
  WidgetTester tester,
  Finder target, {
  double fromTop = 16,
}) async {
  if (target.evaluate().isEmpty) {
    await tester.scrollUntilVisible(target, 300, scrollable: _homeList);
    await tester.pump();
  }
  final position = tester.state<ScrollableState>(_homeList).position;
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

void main() {
  setUpAll(setUpShots);

  testWidgets('02 today chats', (tester) async {
    await _openHome(tester);
    await tester.tap(find.text('Review'));
    await tester.pump();
    await settle(tester, rounds: 10);
    // All the way down to the newest exchange, as a parent would scroll.
    final thread = find.byType(Scrollable).last;
    for (var i = 0; i < 4; i++) {
      final position = tester.state<ScrollableState>(thread).position;
      position.jumpTo(position.maxScrollExtent);
      await tester.pump();
    }
    await settle(tester, rounds: 2);
    await snap(tester, '02_today_chats');
    printRequests('chats');
    await finish(tester);
  });

  testWidgets('05 streak card and streak screen', (tester) async {
    await _openHome(tester);
    // The streak card with the quiz card above it, as a parent scrolls to it.
    await _scrollHomeTo(tester, find.text('Daily Quiz Progress'));
    await snap(tester, '05_streak_card');

    await tester.tap(find.byType(StreakCard));
    await tester.pump();
    await settle(tester, rounds: 10);
    await snap(tester, '05_streak_screen');
    printRequests('streak');
    await finish(tester);
  });

  testWidgets('01b home recent activity (See all)', (tester) async {
    await _openHome(tester);
    await _scrollHomeTo(tester, find.text('Recent activity'), fromTop: 120);
    final seeAll = find.descendant(
      of: find.ancestor(
        of: find.text('Recent activity'),
        matching: find.byType(Row),
      ),
      matching: find.text('See all'),
    );
    await tester.tap(seeAll.first);
    await tester.pump();
    await settle(tester, rounds: 8);
    await snap(tester, '01b_home_recent_activity_all');
    await finish(tester);
  });

  testWidgets('07 imagine gallery', (tester) async {
    await _openHome(tester);
    await _scrollHomeTo(tester, find.text('Gallery'), fromTop: 200);
    final seeAll = find.descendant(
      of: find.ancestor(of: find.text('Gallery'), matching: find.byType(Row)),
      matching: find.text('See all'),
    );
    await tester.tap(seeAll.first);
    await tester.pump();
    await settle(tester, rounds: 10);
    await snap(tester, '07_gallery');
    printRequests('gallery');
    await finish(tester);
  });

  // ---------------------------------------------------------------------
  // Walkthrough-video additions (2026-09-29)
  // ---------------------------------------------------------------------

  testWidgets('02 today chats: Nani picked in the strip', (tester) async {
    await _openHome(tester);
    await tester.tap(find.text('Review'));
    await tester.pump();
    await settle(tester, rounds: 10);
    // The Nani tile, which carries this child's Nani row (agent-nani).
    await tester.tap(find.byKey(const Key('home-chat-character-agent-nani')));
    await tester.pump();
    await settle(tester, rounds: 8);
    final thread = find.byType(Scrollable).last;
    final position = tester.state<ScrollableState>(thread).position;
    position.jumpTo(position.maxScrollExtent);
    await tester.pump();
    await settle(tester, rounds: 2);
    await snap(tester, '02_today_chats_nani');
    await finish(tester);
  });

  testWidgets('07 gallery: viewer and multi-select', (tester) async {
    await _openHome(tester);
    await _scrollHomeTo(tester, find.text('Gallery'), fromTop: 200);
    final seeAll = find.descendant(
      of: find.ancestor(of: find.text('Gallery'), matching: find.byType(Row)),
      matching: find.text('See all'),
    );
    await tester.tap(seeAll.first);
    await tester.pump();
    await settle(tester, rounds: 10);

    // Tap a picture: the full-screen viewer with Save / Share / Details.
    await tester.tap(find.byKey(const ValueKey('gallery-grid-item-0')));
    await tester.pump();
    await settle(tester, rounds: 8);
    await snap(tester, '07_gallery_viewer');
    await tester.pageBack();
    await tester.pump();
    await settle(tester, rounds: 6);

    // Long-press starts selection; two more taps add to it.
    await tester.longPress(find.byKey(const ValueKey('gallery-grid-item-0')));
    await tester.pump();
    for (final i in const [2, 4]) {
      await tester.tap(find.byKey(ValueKey('gallery-grid-item-$i')));
      await tester.pump();
    }
    await settle(tester, rounds: 4);
    await snap(tester, '07_gallery_select');
    await finish(tester);
  });
}
