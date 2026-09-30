// Home tab: first screenful and the whole scroll as one tall image.
//
//   flutter test test/appshots/home_shots_test.dart
import 'package:cheekoai_parent_app/screens/home/home_screen.dart';
import 'package:cheekoai_parent_app/screens/main_navigation_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'support/sample_shell.dart';
import 'support/shots.dart';

void main() {
  setUpAll(setUpShots);

  testWidgets('01 home', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(const MainNavigationScreen()));
    await settle(tester, rounds: 12);
    await snap(tester, '01_home');

    // Full height: measure the page, then grow the phone to fit all of it.
    final list = find
        .descendant(of: find.byType(HomeScreen), matching: find.byType(Scrollable))
        .first;
    final fullHeight = await growToFit(tester, list);
    debugPrint('home content height: $fullHeight');
    await settle(tester, rounds: 8);
    await snap(tester, '01_home_full');

    printRequests('home');
    debugPrint('api calls: ${app.api.calls}');
    await finish(tester);
  });
}
