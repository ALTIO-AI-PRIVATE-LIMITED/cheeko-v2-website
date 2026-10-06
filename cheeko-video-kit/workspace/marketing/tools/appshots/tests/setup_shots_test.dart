// Custom card (with the recorder open, mid-take) and the pairing code step.
//
//   flutter test test/appshots/setup_shots_test.dart
import 'dart:io';

import 'package:cheekoai_parent_app/controllers/voice_recording_controller.dart';
import 'package:cheekoai_parent_app/models/custom_card.dart';
import 'package:cheekoai_parent_app/providers/data/custom_card_providers.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/create_custom_card_screen.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/toy_image_editor_screen.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/voice_recorder_sheet.dart';
import 'package:cheekoai_parent_app/screens/home/toy_activation_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../controllers/voice_recording_controller_test.dart'
    show FakePreviewPlayer, FakeVoiceRecorder;
import 'support/sample_data.dart';
import 'support/sample_shell.dart';
import 'support/shots.dart';

void _noop() {}
void _noopItem(CustomCardItem _) {}
void _noopIndex(int _) {}

void main() {
  setUpAll(setUpShots);

  testWidgets('08 custom card and recorder', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    final kid = sampleKid();

    await tester.pumpWidget(
      app.wrap(
        Builder(
          builder:
              (context) => CreateCustomCardView(
                kid: kid,
                kidLabel: kKidName,
                packVersion: '4',
                items: const <CustomCardItem>[
                  CustomCardItem(
                    itemNumber: 1,
                    title: 'Goodnight from Mumma',
                    imageUrl: '$kCdn/imagine/im-13.jpg',
                    sizeBytes: 1437279,
                  ),
                  CustomCardItem(
                    itemNumber: 2,
                    title: 'Dadi’s mango tree story',
                    imageUrl: '$kCdn/imagine/im-10.jpg',
                    sizeBytes: 2598070,
                  ),
                  CustomCardItem(
                    itemNumber: 3,
                    title: 'Counting to 20 with Papa',
                    imageUrl: '$kCdn/imagine/im-11.jpg',
                    sizeBytes: 912004,
                  ),
                ],
                // Live callbacks so every control shows its enabled state.
                onPickFile: _noop,
                onRecord: _noop,
                onOpenItem: _noopItem,
                onUploadImage: _noop,
                onTakePhoto: _noop,
                onPickImageForSelection: _noopIndex,
                onClearImageForSelection: _noopIndex,
              ),
        ),
      ),
    );
    await settle(tester, rounds: 10);
    await snap(tester, '08_custom_card');

    // The recorder sheet exactly as showVoiceRecorderSheet opens it, on a
    // pretend microphone.
    final recorder = FakeVoiceRecorder();
    final controller = VoiceRecordingController(
      maxDuration: CustomCardNotifier.maxRecordingDuration,
      maxBytes: CustomCardNotifier.maxFileSizeBytes,
      recorder: recorder,
      player: FakePreviewPlayer(),
      newTakePath: () async => '/takes/Recording.m4a',
      sizeOf: (_) async => 180 * 1024,
      deleteTake: (_) async {},
    );
    final context = tester.element(find.byType(CreateCustomCardView));
    // ignore: unawaited_futures
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      isDismissible: false,
      enableDrag: false,
      backgroundColor: Colors.transparent,
      builder:
          (_) => VoiceRecorderSheet(
            maxDuration: CustomCardNotifier.maxRecordingDuration,
            maxBytes: CustomCardNotifier.maxFileSizeBytes,
            controller: controller,
          ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    await snap(tester, '08_custom_card_recorder_ready');

    await tester.tap(find.byTooltip('Start recording'));
    await tester.pump();
    // Fourteen seconds of a parent's voice: levels rise and fall like speech.
    const speech = <double>[
      -30, -18, -12, -20, -9, -15, -26, -40, -14, -8, -11, -22, -35, -17,
      -10, -13, -24, -19, -7, -16, -28, -45, -12, -9, -21, -14, -18, -11,
    ];
    for (var i = 0; i < 140; i++) {
      recorder.levelEvents.add(speech[i % speech.length]);
      await tester.pump(const Duration(milliseconds: 100));
    }
    await snap(tester, '08_custom_card_recording');

    await tester.pumpWidget(const SizedBox.shrink());
    controller.dispose();
    await finish(tester);
  });

  testWidgets('09 pairing code step', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(ToyActivationScreen(initialStep: 2, kid: sampleKid())),
    );
    await settle(tester, rounds: 10);
    await snap(tester, '09_pairing_code');

    // The parent types what Cheeko just said. Filling the boxes only stores
    // the code; nothing is sent until "Activate Cheeko" is tapped.
    await tester.enterText(find.byType(EditableText).first, '482915');
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '09_pairing_code_entered');
    printRequests('pairing');
    await finish(tester);
  });

  // ---------------------------------------------------------------------
  // Walkthrough-video additions (2026-09-29)
  // ---------------------------------------------------------------------

  Widget customCardView(List<CustomCardItem> items) => Builder(
    builder:
        (context) => CreateCustomCardView(
          kid: sampleKid(),
          kidLabel: kKidName,
          packVersion: '4',
          items: items,
          onPickFile: _noop,
          onRecord: _noop,
          onOpenItem: _noopItem,
          onUploadImage: _noop,
          onTakePhoto: _noop,
          onPickImageForSelection: _noopIndex,
          onClearImageForSelection: _noopIndex,
        ),
  );

  testWidgets('08 custom card with three recordings', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(
      app.wrap(
        customCardView(const <CustomCardItem>[
          CustomCardItem(
            itemNumber: 1,
            title: 'Grandma’s lullaby',
            imageUrl: '$kCdn/imagine/im-13.jpg',
            sizeBytes: 2143552,
          ),
          CustomCardItem(
            itemNumber: 2,
            title: 'Good morning song',
            imageUrl: '$kCdn/imagine/im-16.jpg',
            sizeBytes: 1387221,
          ),
          CustomCardItem(
            itemNumber: 3,
            title: 'Story: the thirsty crow',
            imageUrl: '$kCdn/custom/cc-crow.jpg',
            sizeBytes: 3012876,
          ),
        ]),
      ),
    );
    await settle(tester, rounds: 10);
    await snap(tester, '08_custom_card_list');
    await finish(tester);
  });

  testWidgets('08 image editor (Sepia)', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(customCardView(const <CustomCardItem>[])));
    await settle(tester, rounds: 4);

    // What the Gallery tile does once the photo picker returns a file: the
    // app's own showToyImageEditor, full-screen, on the picked picture.
    final picked = File(
      '${Directory.current.path}/test/appshots/media/im-10.jpg',
    );
    final context = tester.element(find.byType(CreateCustomCardView));
    // ignore: unawaited_futures
    showToyImageEditor(context, source: picked);
    await tester.pump();
    for (var i = 0; i < 6; i++) {
      await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 150)),
      );
      await tester.pump(const Duration(milliseconds: 200));
    }
    await settle(tester, rounds: 4);

    // At 393 x 852 the crop frame and the filter strip do not fit on one
    // screen. Scrolled so the whole strip (tiles and names) sits just above
    // the Cancel / Use This Picture bar, as a parent scrolls to reach it.
    final list = find
        .descendant(
          of: find.byType(ToyImageEditorScreen),
          matching: find.byType(Scrollable),
        )
        .first;
    final position = tester.state<ScrollableState>(list).position;
    final viewportBottom = tester.getBottomLeft(list).dy;
    final sepia = find.text('Sepia').first;
    position.jumpTo(
      (position.pixels + tester.getBottomLeft(sepia).dy + 10 - viewportBottom)
          .clamp(0, position.maxScrollExtent),
    );
    await tester.pump();
    await settle(tester, rounds: 2);

    // Pick the Sepia look from the filter strip.
    debugPrint('sepia tile at ${tester.getCenter(sepia)}, list ends $viewportBottom');
    await tester.tap(sepia);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, '08_image_editor');

    // Back to the top: the whole crop frame, now in sepia.
    position.jumpTo(0);
    await tester.pump();
    await settle(tester, rounds: 2);
    await snap(tester, '08_image_editor_top');
    await growToFit(tester, list);
    await settle(tester, rounds: 2);
    await snap(tester, '08_image_editor_full');
    await finish(tester);
  });
}
