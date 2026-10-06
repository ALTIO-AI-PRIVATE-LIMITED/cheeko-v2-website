// V26 Make Your Own Card: one parent's flow on Aarav's custom card, every
// screen from the app's own widgets. Grandma's lullaby is already on the card;
// the parent adds "Good morning song" with the peacock picture.
//
//   APPSHOTS_OUT=.../app-shots-ios/myo flutter test test/appshots/myo_shots_test.dart
import 'dart:io';

import 'package:cheekoai_parent_app/controllers/voice_recording_controller.dart';
import 'package:cheekoai_parent_app/models/custom_card.dart';
import 'package:cheekoai_parent_app/providers/data/custom_card_providers.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/create_custom_card_screen.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/toy_image_editor_screen.dart';
import 'package:cheekoai_parent_app/screens/custom_cards/voice_recorder_sheet.dart';
import 'package:cheekoai_parent_app/services/content_rights_consent_service.dart';
import 'package:cheekoai_parent_app/widgets/content_rights_dialog.dart';
import 'package:cheekoai_parent_app/widgets/snackbar.dart';
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

const CustomCardItem _lullaby = CustomCardItem(
  itemNumber: 1,
  title: 'Grandma’s lullaby',
  imageUrl: '$kCdn/imagine/im-13.jpg',
  sizeBytes: 2143552,
);
const CustomCardItem _morning = CustomCardItem(
  itemNumber: 2,
  title: 'Good morning song',
  imageUrl: '$kCdn/imagine/im-16.jpg',
  sizeBytes: 1387221,
);
const String _file = 'Good morning song.mp3';

String get _media => '${Directory.current.path}/test/appshots/media';

Widget _card({
  List<CustomCardItem> items = const <CustomCardItem>[_lullaby],
  List<String> selected = const <String>[],
  List<String?> images = const <String?>[],
  File? queued,
  bool uploading = false,
}) => Builder(
  builder:
      (context) => CreateCustomCardView(
        kid: sampleKid(),
        kidLabel: kKidName,
        packVersion: '4',
        items: items,
        selectedFileNames: selected,
        selectedImageNames: images,
        queuedImage: queued,
        isUploading: uploading,
        onPickFile: uploading ? null : _noop,
        onRecord: uploading ? null : _noop,
        onUpload: selected.isEmpty || uploading ? null : _noop,
        onClearSelection: uploading ? null : _noop,
        onOpenItem: _noopItem,
        onUploadImage: _noop,
        onTakePhoto: _noop,
        onEditImage: queued == null ? null : _noop,
        onClearImage: queued == null ? null : _noop,
        onPickImageForSelection: _noopIndex,
        onClearImageForSelection: _noopIndex,
      ),
);

/// The whole scrolling page, as one tall capture, so the video can scroll it.
Future<void> _tall(WidgetTester tester, String name) async {
  final list = find.byType(Scrollable).first;
  await growToFit(tester, list);
  await settle(tester, rounds: 3);
  await snap(tester, name);
}

void main() {
  setUpAll(setUpShots);

  testWidgets('myo card, rights check, selection, saved', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();

    // 1. The card with Grandma's lullaby on it, Add Media below.
    await tester.pumpWidget(app.wrap(_card()));
    await settle(tester, rounds: 10);
    await snap(tester, 'myo_01_card');

    // 2. Upload Audio first asks about content rights; ticked, ready to agree.
    final context = tester.element(find.byType(CreateCustomCardView));
    // ignore: unawaited_futures
    showContentRightsDialog(context);
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    await tester.tap(find.text(kContentRightsAgreementLabel));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    await snap(tester, 'myo_02_rights');
    await finish(tester);
  });

  testWidgets('myo selected file, picture, uploading, saved', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();

    // 3. The picked file waits under Add Media, with room for a picture.
    await tester.pumpWidget(
      app.wrap(_card(selected: const <String>[_file], images: const <String?>[null])),
    );
    await settle(tester, rounds: 10);
    await _tall(tester, 'myo_03_selected_full');

    // 4. With its picture fitted to Cheeko's screen, ready to add.
    await preparePhone(tester);
    final fitted = File('$_media/myo-peacock-fitted.png');
    await tester.pumpWidget(
      app.wrap(
        _card(
          selected: const <String>[_file],
          images: const <String?>['peacock.jpg'],
          queued: fitted,
        ),
      ),
    );
    await settle(tester, rounds: 10);
    await _tall(tester, 'myo_04_ready_full');

    // 5. Add to Custom Card tapped: uploading.
    await preparePhone(tester);
    await tester.pumpWidget(
      app.wrap(
        _card(
          selected: const <String>[_file],
          images: const <String?>['peacock.jpg'],
          queued: fitted,
          uploading: true,
        ),
      ),
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    await _tall(tester, 'myo_05_uploading_full');

    // 6. Saved: two recordings on the card and the app's own message.
    await preparePhone(tester);
    await tester.pumpWidget(
      app.wrap(_card(items: const <CustomCardItem>[_lullaby, _morning])),
    );
    await settle(tester, rounds: 10);
    final context = tester.element(find.byType(CreateCustomCardView));
    showSnackBar(
      context,
      'Saved. Cheeko picks it up the next time the card is tapped.',
    );
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 600));
    await snap(tester, 'myo_06_saved');
    await tester.pump(const Duration(seconds: 6));
    await finish(tester);
  });

  testWidgets('myo recorder', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(_card()));
    await settle(tester, rounds: 10);

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
    await snap(tester, 'myo_07_rec_ready');

    await tester.tap(find.byTooltip('Start recording'));
    await tester.pump();
    const speech = <double>[
      -30, -18, -12, -20, -9, -15, -26, -40, -14, -8, -11, -22, -35, -17,
      -10, -13, -24, -19, -7, -16, -28, -45, -12, -9, -21, -14, -18, -11,
    ];
    for (var i = 0; i < 120; i++) {
      recorder.levelEvents.add(speech[i % speech.length]);
      await tester.pump(const Duration(milliseconds: 100));
    }
    await snap(tester, 'myo_08_recording');

    await tester.tap(find.byTooltip('Stop recording'));
    for (var i = 0; i < 6; i++) {
      await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 60)));
      await tester.pump(const Duration(milliseconds: 150));
    }
    await snap(tester, 'myo_09_rec_done');

    await tester.pumpWidget(const SizedBox.shrink());
    controller.dispose();
    await finish(tester);
  });

  testWidgets('myo picture editor', (tester) async {
    await preparePhone(tester);
    final app = SampleApp();
    await tester.pumpWidget(app.wrap(_card(selected: const <String>[_file], images: const <String?>[null])));
    await settle(tester, rounds: 4);

    final context = tester.element(find.byType(CreateCustomCardView));
    // ignore: unawaited_futures
    showToyImageEditor(context, source: File('$_media/im-16.jpg'));
    await tester.pump();
    for (var i = 0; i < 6; i++) {
      await tester.runAsync(() => Future<void>.delayed(const Duration(milliseconds: 150)));
      await tester.pump(const Duration(milliseconds: 200));
    }
    await settle(tester, rounds: 4);
    await snap(tester, 'myo_10_editor_top');

    final list = find
        .descendant(of: find.byType(ToyImageEditorScreen), matching: find.byType(Scrollable))
        .first;
    final position = tester.state<ScrollableState>(list).position;
    final viewportBottom = tester.getBottomLeft(list).dy;
    final chip = find.text('Brightness').first;
    position.jumpTo(
      (position.pixels + tester.getBottomLeft(chip).dy + 10 - viewportBottom)
          .clamp(0, position.maxScrollExtent),
    );
    await tester.pump();
    await settle(tester, rounds: 2);
    await tester.tap(chip);
    await tester.pump();
    await settle(tester, rounds: 4);
    await snap(tester, 'myo_11_editor_filters');
    await finish(tester);
  });
}
