// Onboarding video batch, part 2: sign-in, parent profile, adding the child.
//
//   flutter test test/appshots/onboarding_account_shots_test.dart
import 'package:cheekoai_parent_app/screens/onboarding/interactive_kids_onboarding_screen.dart';
import 'package:cheekoai_parent_app/screens/onboarding/parent_profile_setup_screen.dart';
import 'package:cheekoai_parent_app/screens/onboarding/walkthrough_screen.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:syncfusion_flutter_datepicker/datepicker.dart';

import 'support/sample_data.dart';
import 'support/sample_shell.dart';
import 'support/shots.dart';

Future<void> _frames(WidgetTester tester, int n) async {
  for (var i = 0; i < n; i++) {
    await tester.pump(const Duration(milliseconds: 100));
  }
}

Future<void> _tapText(WidgetTester tester, String text) async {
  final finder = find.text(text).first;
  await tester.ensureVisible(finder);
  await tester.pump();
  await tester.tap(finder);
  await _frames(tester, 6);
}

void main() {
  setUpAll(setUpShots);

  testWidgets('s01 walkthrough sign-in (iPhone)', (tester) async {
    await preparePhone(tester);
    // "Continue with Apple" is only offered on iOS.
    debugDefaultTargetPlatformOverride = TargetPlatform.iOS;
    try {
      final app = SampleApp();
      await tester.pumpWidget(app.wrap(const WalkthroughScreen()));
      await settle(tester, rounds: 10);
      await snap(tester, 'setup/s01_walkthrough_signin');
      await finish(tester);
    } finally {
      debugDefaultTargetPlatformOverride = null;
    }
  });

  testWidgets('s02 parent profile and consent', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(
        ParentProfileSetupScreen(
          profileService: SampleProfileApi(),
          initialDisplayName: kParentName,
          initialEmail: 'priya@example.com',
          currentUserId: 'parent-1',
        ),
      ),
    );
    await settle(tester, rounds: 6);
    final phone = find.byWidgetPredicate(
      (w) => w is TextField && w.decoration?.hintText == 'Phone number',
    );
    await tester.enterText(phone, '9876543210');
    await _frames(tester, 3);
    FocusManager.instance.primaryFocus?.unfocus();
    await _frames(tester, 3);
    await snap(tester, 'setup/s02a_parent_profile');

    for (final item in const [
      'I confirm I am the parent/guardian and consent to creating this account.',
      'I accept the Privacy Policy.',
      'I accept the Terms of Service.',
    ]) {
      await _tapText(tester, item);
      await _tapText(tester, 'I have read and accept');
    }
    await tester.ensureVisible(find.text('Continue').first);
    await _frames(tester, 4);
    await settle(tester, rounds: 3);
    await snap(tester, 'setup/s02_parent_consent');
    await finish(tester);
  });

  testWidgets('s03 add child', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(const InteractiveKidsOnboardingScreen()));
    await settle(tester, rounds: 6);
    await snap(tester, 'setup/s03a_intro');

    Future<void> next(String label) async {
      await tester.tap(find.text(label).hitTestable().first);
      await _frames(tester, 10);
    }

    final continueOnIntro = find.textContaining(RegExp('Continue|Get Started|Let'));
    await tester.tap(continueOnIntro.last);
    await _frames(tester, 8);

    // Name
    await tester.enterText(find.byType(TextField).first, kKidName);
    await _frames(tester, 3);
    FocusManager.instance.primaryFocus?.unfocus();
    await _frames(tester, 4);
    await snap(tester, 'setup/s03b_name');
    await next('Continue');

    // Birthday: the app's own picker dialog, with Aarav's date handed to it.
    await _tapText(tester, 'Tap to select birthday');
    await settle(tester, rounds: 3);
    final picker = tester.widget<SfDateRangePicker>(
      find.byType(SfDateRangePicker),
    );
    picker.onSelectionChanged!(
      DateRangePickerSelectionChangedArgs(sampleKid().dateOfBirth),
    );
    await _tapText(tester, 'Select');
    await _frames(tester, 6);
    await snap(tester, 'setup/s03c_birthday');
    await next('Continue');
    // The app confirms the age before moving on.
    await settle(tester, rounds: 3);
    await snap(tester, 'setup/s03c2_age_confirm');
    await tester.tap(find.text('Continue').hitTestable().last);
    await _frames(tester, 12);

    // Gender
    await _tapText(tester, 'Male');
    await snap(tester, 'setup/s03d_gender');
    await next('Continue');

    // Interests
    for (final interest in const ['Dinosaurs', 'Science', 'Animals']) {
      await _tapText(tester, interest);
    }
    tester.state<ScrollableState>(
      find.byWidgetPredicate(
        (w) => w is Scrollable && w.axisDirection == AxisDirection.down,
      ).first,
    ).position.jumpTo(0);
    await _frames(tester, 4);
    await snap(tester, 'setup/s03e_interests');
    await next('Continue');

    // Language (single choice in the app)
    await _tapText(tester, 'English');
    await snap(tester, 'setup/s03f_language');

    // The last page, reached without the save the app makes on
    // "Complete Setup!" (that would create a child on the server).
    final pageView = tester.widget<PageView>(find.byType(PageView).first);
    pageView.controller!.jumpToPage(7);
    await tester.pump();
    await settle(tester, rounds: 6);
    await snap(tester, 'setup/s03g_all_set');
    await finish(tester);
  });
}
