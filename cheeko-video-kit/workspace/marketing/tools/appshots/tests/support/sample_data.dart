// The one sample family every screenshot is filled with: Aarav, 6, and his
// Cheeko. Everything here is invented for the marketing video; none of it is
// read from, or sent to, a real server.
//
// ignore_for_file: depend_on_referenced_packages
import 'dart:async';

import 'package:cheekoai_parent_app/core/utils/ist.dart';
import 'package:cheekoai_parent_app/models/analytics_day.dart';
import 'package:cheekoai_parent_app/models/analytics_overall_stats.dart';
import 'package:cheekoai_parent_app/models/analytics_session.dart';
import 'package:cheekoai_parent_app/models/analytics_user_progress.dart';
import 'package:cheekoai_parent_app/models/character_conversation.dart';
import 'package:cheekoai_parent_app/models/chat_message.dart';
import 'package:cheekoai_parent_app/models/device.dart';
import 'package:cheekoai_parent_app/models/device_runtime_state.dart';
import 'package:cheekoai_parent_app/models/device_settings.dart';
import 'package:cheekoai_parent_app/models/device_settings_payload.dart';
import 'package:cheekoai_parent_app/models/device_sync_event.dart';
import 'package:cheekoai_parent_app/models/homepage_activity.dart';
import 'package:cheekoai_parent_app/models/imagine_image.dart';
import 'package:cheekoai_parent_app/models/kid.dart';
import 'package:cheekoai_parent_app/models/kid_character.dart';
import 'package:cheekoai_parent_app/models/kid_session.dart';
import 'package:cheekoai_parent_app/models/kid_streak.dart';
import 'package:cheekoai_parent_app/models/parent_profile.dart';
import 'package:cheekoai_parent_app/models/quiz_analytics.dart';
import 'package:cheekoai_parent_app/models/session_message_page.dart';
import 'package:cheekoai_parent_app/services/analytics_api_service.dart';
import 'package:cheekoai_parent_app/services/chat_history_service.dart';
import 'package:cheekoai_parent_app/services/device_settings_service.dart';
import 'package:cheekoai_parent_app/services/home_recommendation_service.dart';
import 'package:cheekoai_parent_app/services/java_agent_service.dart';
import 'package:cheekoai_parent_app/services/java_api_service.dart';
import 'package:cheekoai_parent_app/services/kids_api_service.dart';
import 'package:cheekoai_parent_app/services/parent_timezone_sync_service.dart';
import 'package:cheekoai_parent_app/services/profile_api_service.dart';

import 'fake_http.dart';

/// Where the fake CDN "hosts" the sample pictures. The host is never looked
/// up: [FakeHttpOverrides] answers every request in-process.
const String kCdn = 'https://cdn.cheeko.test';
const String kApiBase = 'https://api.cheeko.test';

const String kKidId = 'kid-1';
const String kKidName = 'Aarav';
const String kParentName = 'Priya Sharma';
const String kMac = 'A4:CF:12:3B:7E:01';
const String kDeviceName = 'Cheeko';

/// Aarav's photo on his profile (website photo `live/kid-beanbag.jpg`).
const String kKidAvatar = '$kCdn/avatars/kid-aarav.jpg';

/// A second toy and child, for the one shot that shows a two-toy account
/// (03_device_two_toys). Off everywhere else; [preparePhone] resets it.
bool sampleTwoToys = false;

/// With [sampleTwoToys]: whether the second toy has its own child (Anaya).
/// False leaves the account with one child and the second toy unpaired, so
/// the Device tab's "Who's using it now?" row (not shipping) stays hidden.
bool sampleSecondKid = true;

const String kKid2Id = 'kid-2';
const String kKid2Name = 'Anaya';
const String kMac2 = 'A4:CF:12:3B:21:C9';
const String kDevice2Name = 'Cheeko 2';

/// Today, on the IST calendar the app reads everything in.
DateTime get _todayIst => istNow();

/// An instant today at [hour]:[minute] IST, as the UTC time a server sends.
DateTime todayAt(int hour, int minute) {
  final day = _todayIst;
  return DateTime.utc(
    day.year,
    day.month,
    day.day,
    hour,
    minute,
  ).subtract(const Duration(hours: 5, minutes: 30));
}

DateTime daysAgoAt(int days, int hour, int minute) =>
    todayAt(hour, minute).subtract(Duration(days: days));

String _dateKey(DateTime istDay) =>
    '${istDay.year}-${istDay.month.toString().padLeft(2, '0')}-${istDay.day.toString().padLeft(2, '0')}';

// ---------------------------------------------------------------------------
// Child, parent, toy
// ---------------------------------------------------------------------------

const ParentRules kHouseRules = ParentRules(
  bedtime: '20:00',
  noScaryStories: true,
  languages: <String>['English', 'Hindi'],
  avoidTopics: <String>['Ghosts', 'Monsters'],
  focus: 'English words',
  note: 'Loves animals and space. Keep answers short and simple.',
);

Kid sampleKid() => Kid(
  id: kKidId,
  parentId: 'parent-1',
  name: kKidName,
  // Six years old on the day the screenshots are taken.
  dateOfBirth: DateTime(2020, 4, 2),
  // Capitalised, as the app's own onboarding and profile screens store it
  // (the profile screen reads anything but 'Male' as Female).
  gender: 'Male',
  // The three picked in onboarding (setup/s03e_interests).
  interests: const <String>['Animals', 'Dinosaurs', 'Science'],
  avatarUrl: kKidAvatar,
  primaryLanguage: 'English',
  parentRules: kHouseRules,
  deviceMac: kMac,
  isPaired: true,
  createdAt: DateTime(2026, 5, 10),
  updatedAt: DateTime(2026, 9, 20),
);

Map<String, dynamic> sampleKidJson() => <String, dynamic>{
  'id': kKidId,
  'parent_id': 'parent-1',
  'name': kKidName,
  'date_of_birth': '2020-04-02',
  'gender': 'Male',
  'interests': <String>['Animals', 'Dinosaurs', 'Science'],
  'avatar_url': kKidAvatar,
  'primary_language': 'English',
  'parent_rules': <String, dynamic>{
    'bedtime': '20:00',
    'no_scary_stories': true,
    'languages': <String>['English', 'Hindi'],
    'avoid_topics': <String>['Ghosts', 'Monsters'],
    'focus': 'English words',
    'note': 'Loves animals and space. Keep answers short and simple.',
  },
  'device_mac': kMac,
  'is_paired': true,
  'is_active': true,
  'created_at': '2026-05-10T00:00:00Z',
  'updated_at': '2026-09-20T00:00:00Z',
};

Map<String, dynamic> sampleDeviceJson() => <String, dynamic>{
  'id': 'dev-1',
  'mac_address': kMac,
  'device_name': kDeviceName,
  'agent_id': 'agent-1',
  'kid_id': kKidId,
  'app_version': '2.4.1',
  'board': 'cheeko-s3',
  'battery_level': 80,
  'last_connected_at': todayAt(18, 40).toIso8601String(),
  'create_date': '2026-05-10T00:00:00Z',
  'update_date': '2026-09-28T00:00:00Z',
};

Device sampleDevice() => Device.fromJson(sampleDeviceJson());

/// Anaya, 4 (born 12 Jan 2022), on the second toy.
Map<String, dynamic> sampleKid2Json() => <String, dynamic>{
  'id': kKid2Id,
  'parent_id': 'parent-1',
  'name': kKid2Name,
  'date_of_birth': '2022-01-12',
  'gender': 'Female',
  'interests': <String>['Music', 'Stories', 'Nature'],
  'primary_language': 'English',
  'device_mac': kMac2,
  'is_paired': true,
  'is_active': true,
  'created_at': '2026-08-02T00:00:00Z',
  'updated_at': '2026-09-20T00:00:00Z',
};

Map<String, dynamic> sampleDevice2Json() => <String, dynamic>{
  'id': 'dev-2',
  'mac_address': kMac2,
  'device_name': kDevice2Name,
  'agent_id': 'agent-1',
  'kid_id': sampleSecondKid ? kKid2Id : null,
  'app_version': '2.4.1',
  'board': 'cheeko-s3',
  'battery_level': 64,
  'last_connected_at': todayAt(17, 55).toIso8601String(),
  'create_date': '2026-08-02T00:00:00Z',
  'update_date': '2026-09-28T00:00:00Z',
};

List<Map<String, dynamic>> sampleKidsJson() => <Map<String, dynamic>>[
  sampleKidJson(),
  if (sampleTwoToys && sampleSecondKid) sampleKid2Json(),
];

Map<String, dynamic> sampleRuntimeJson() => <String, dynamic>{
  'online': true,
  'battery': 80,
  'charging': false,
  'discharging': true,
  'network': 'Sharma Home WiFi',
  'mode': 'chat',
  'firmware': '2.4.1',
  'last_seen_at': todayAt(18, 41).toIso8601String(),
};

DeviceRuntimeState sampleRuntimeState() =>
    DeviceRuntimeState.fromApi(sampleRuntimeJson());

// ---------------------------------------------------------------------------
// The calendar every figure hangs off
// ---------------------------------------------------------------------------
//
// Today: 48 min, 5 talks, 4 cards, 3 games, quiz 7/10, streak 5.
// Five days before today is the one quiet day (no play, no quiz) that started
// the current run, so the usage-based "Active streak" on Analytics and the
// quiz streak on Home agree on 5.
//
// The Week tab shows a full Monday-Sunday week picked with the app's own week
// picker: the week two before the current one, so every day has happened and
// the quiet day above is not inside it (keeps the streak honest).

DateTime get _todayDate {
  final t = _todayIst;
  return DateTime(t.year, t.month, t.day);
}

DateTime dayAgo(int ago) {
  final t = _todayDate;
  return DateTime(t.year, t.month, t.day - ago);
}

/// Monday of the week the Week tab is switched to.
DateTime get featuredWeekStart {
  final t = _todayDate;
  return DateTime(t.year, t.month, t.day - (t.weekday - 1) - 14);
}

const List<int> kFeaturedWeekMinutes = <int>[32, 45, 28, 51, 40, 62, 48];
const List<int> kFeaturedWeekQuestions = <int>[6, 9, 5, 12, 8, 14, 11];

const int kTodayMinutes = 48;
const int kTodayTalks = 5;
const int kTodayCards = 4;
const int kTodayGames = 3;

int _agoOf(DateTime date) =>
    _todayDate.difference(DateTime(date.year, date.month, date.day)).inDays;

int? _featuredIndex(DateTime date) {
  final i =
      DateTime(date.year, date.month, date.day).difference(featuredWeekStart).inDays;
  return i >= 0 && i < 7 ? i : null;
}

/// Minutes of play on [date].
int minutesOn(DateTime date) {
  final ago = _agoOf(date);
  if (ago == 0) return kTodayMinutes;
  if (ago == 5) return 0;
  final featured = _featuredIndex(date);
  if (featured != null) return kFeaturedWeekMinutes[featured];
  const cycle = <int>[41, 36, 52, 30, 44, 27, 39, 55, 33, 46];
  return cycle[ago % cycle.length];
}

int questionsOn(DateTime date) {
  final ago = _agoOf(date);
  if (ago == 0) return kTodayTalks;
  if (ago == 5) return 0;
  final featured = _featuredIndex(date);
  if (featured != null) return kFeaturedWeekQuestions[featured];
  return 5 + (ago * 7) % 8;
}

int cardsOn(DateTime date) {
  final ago = _agoOf(date);
  if (ago == 0) return kTodayCards;
  if (ago == 5) return 0;
  return 2 + (ago * 5) % 4;
}

int gamesOn(DateTime date) {
  final ago = _agoOf(date);
  if (ago == 0) return kTodayGames;
  if (ago == 5) return 0;
  return 1 + (ago * 3) % 3;
}

// ---------------------------------------------------------------------------
// Today
// ---------------------------------------------------------------------------

/// Today's five conversations, oldest first — five talks on the Home card.
/// The chat screen opens scrolled to the newest, which are the sky and the
/// tiger.
List<ChatMessage> sampleTodayChat() {
  var n = 0;
  ChatMessage line(int type, DateTime at, String text) => ChatMessage(
    id: 'msg-${++n}',
    content: text,
    timestamp: at,
    chatType: type,
    macAddress: kMac,
    childName: kKidName,
  );

  return <ChatMessage>[
    line(1, todayAt(16, 5), 'How do you say thank you in Hindi?'),
    line(
      2,
      todayAt(16, 5),
      'In Hindi we say “Dhanyavaad”! You can also say “Shukriya”. Who will '
      'you say it to today?',
    ),
    line(1, todayAt(16, 31), 'Why does the moon follow our car?'),
    line(
      2,
      todayAt(16, 31),
      'The moon is so far away that it looks like it moves with you. It is '
      'really staying in the same place in the sky!',
    ),
    line(1, todayAt(17, 10), 'What does enormous mean?'),
    line(
      2,
      todayAt(17, 10),
      'Enormous means very, very big, like an elephant! Can you think of '
      'something else that is enormous?',
    ),
    line(1, todayAt(18, 12), 'Why is the sky blue?'),
    line(
      2,
      todayAt(18, 12),
      'Great question! Sunlight bounces off tiny bits of air, and blue '
      'bounces the most! What colour do you think sunset is?',
    ),
    line(1, todayAt(18, 35), 'Can a tiger ride a bicycle?'),
    line(
      2,
      todayAt(18, 35),
      'Ha ha! A real tiger can’t, its paws are too big for the pedals. But '
      'in a story it could zoom down the road! Shall we make one up?',
    ),
  ];
}

const String kNaniAgentId = 'agent-nani';

/// Aarav and Nani at 3:30 PM, when the Nani card went in (see
/// [sampleRecentActivitiesJson]). Read only through the character strip's
/// Nani tile: the "everyone" thread and the 5-talks count stay as they are.
List<CharacterSessionTranscript> sampleNaniToday() {
  var seq = 0;
  SessionMessage line(String role, DateTime at, String text) =>
      SessionMessage(sequence: ++seq, role: role, content: text, createdAt: at);
  return <CharacterSessionTranscript>[
    CharacterSessionTranscript(
      session: KidSession(
        sessionId: 'sess-nani-1',
        startedAt: todayAt(15, 30),
        endedAt: todayAt(15, 41),
        messageCount: 4,
      ),
      messages: <SessionMessage>[
        line('user', todayAt(15, 30),
            'Nani, tell me a story about a clever crow!'),
        line(
          'assistant',
          todayAt(15, 31),
          'Arre wah, my little one! Once, on a hot summer day, a thirsty crow '
          'found a pot with only a little water at the bottom. His beak could '
          'not reach it. What do you think he did?',
        ),
        line('user', todayAt(15, 33), 'He put stones in the pot!'),
        line(
          'assistant',
          todayAt(15, 34),
          'Shabaash, Aarav! Pebble by pebble the water came up, and the crow '
          'drank happily. When we think calmly, we always find a way, beta.',
        ),
      ],
    ),
  ];
}

Map<String, dynamic> sampleProgressToday() => <String, dynamic>{
  'today_progress': <String, dynamic>{
    'usage_time_seconds': kTodayMinutes * 60,
    'card_tap_count': kTodayCards,
    'games_played': kTodayGames,
    'ai_interaction_count': kTodayTalks,
    'first_activity_date': '2026-05-10',
  },
};

/// Card art as the backend serves it. The pictures are the shipping cards'
/// own art from the website.
String cardArt(String file) => '$kCdn/cards/$file';

Map<String, dynamic> _activity(
  String name,
  String mode,
  String art,
  String description,
  DateTime at,
  int seconds,
) => <String, dynamic>{
  'title': name,
  'content_pack_name': name,
  'mode_type': mode,
  'card_type': 'content',
  'description': description,
  'image_url': cardArt(art),
  'usage_seconds': seconds,
  'created_at': at.toIso8601String(),
};

List<Map<String, dynamic>> sampleRecentActivitiesJson() => <Map<String, dynamic>>[
  _activity('Tales of Kindness', 'story', '01-tales-of-kindness.jpg',
      'Gentle stories about sharing, caring and helping.', todayAt(18, 2), 720),
  _activity('Floor is Lava!', 'game', '02-floor-is-lava.jpg',
      'Jump, freeze and giggle: a movement game.', todayAt(17, 40), 540),
  _activity('Mitthu the Parrot', 'learning', '05-mitthu-the-parrot.jpg',
      'Your English tutor: new words every day.', todayAt(17, 15), 600),
  _activity('Play & Sing Along', 'rhymes', '03-play-and-sing-along.jpg',
      'Rhymes for little explorers.', todayAt(16, 40), 480),
  _activity('Sounds Around Me', 'game', '09-sounds-around-me.jpg',
      'Guess the sound: bells, phones, animals and more.', todayAt(16, 12), 420),
  _activity('Nani', 'story', '10-nani.jpg',
      'Your storytelling grandma.', todayAt(15, 30), 660),
];

Map<String, dynamic> sampleHomepageActivityJson() => <String, dynamic>{
  'recentActivities': sampleRecentActivitiesJson(),
  'momentOfTheDay': <String, dynamic>{
    'questionText': 'Why does the moon follow our car?',
    'replyText':
        'The moon is so far away that it looks like it moves with you.',
    'imageUrl': '$kCdn/imagine/im-07.jpg',
    'createdAt': todayAt(16, 31).toIso8601String(),
  },
};

HomepageActivityDetail sampleCardsToday() => HomepageActivityDetail.fromJson(
  <String, dynamic>{
    'metric': 'cards',
    'period': 'today',
    'period_label': 'Today',
    'total': kTodayCards,
    'items': <Map<String, dynamic>>[
      for (final a in sampleRecentActivitiesJson())
        if (a['mode_type'] != 'game')
          <String, dynamic>{
            'name': a['title'],
            'key': a['title'],
            'image_url': a['image_url'],
            'timestamp': a['created_at'],
            'count': 1,
            'duration_seconds': a['usage_seconds'],
          },
    ],
  },
);

HomepageActivityDetail sampleGamesToday() => HomepageActivityDetail.fromJson(
  <String, dynamic>{
    'metric': 'games',
    'period': 'today',
    'period_label': 'Today',
    'total': kTodayGames,
    'items': <Map<String, dynamic>>[
      <String, dynamic>{
        'game_name': 'Floor is Lava!',
        'game_id': 'floor_is_lava',
        'duration_seconds': 540,
        'score': 9,
        'level': 2,
        'played_at': todayAt(17, 40).toIso8601String(),
      },
      <String, dynamic>{
        'game_name': 'Sounds Around Me',
        'game_id': 'sounds_around_me',
        'duration_seconds': 420,
        'score': 8,
        'level': 3,
        'played_at': todayAt(16, 12).toIso8601String(),
      },
      <String, dynamic>{
        'game_name': 'Word Ladder',
        'game_id': 'word_ladder',
        'duration_seconds': 300,
        'score': 6,
        'level': 2,
        'played_at': todayAt(15, 5).toIso8601String(),
      },
    ],
  },
);

/// Where the day's (or the featured week's) minutes went, by the keys the
/// usage endpoint documents. Split: cards 41%, games 25%, talk 19%, audio
/// 15%. (Talk is kept under an hour for the week: at 393 pt the app wraps the
/// "Interactions" label when its value reads "1h 23m".)
HomepageActivityDetail sampleUsageDetail(String period, int totalMinutes) {
  final cards = (totalMinutes * 0.41).round();
  final games = (totalMinutes * 0.25).round();
  final talk = (totalMinutes * 0.19).round();
  final audio = totalMinutes - cards - talk - games;
  Map<String, dynamic> item(String key, String name, int minutes) =>
      <String, dynamic>{
        'key': key,
        'name': name,
        'duration_seconds': minutes * 60,
        'count': 1,
      };
  return HomepageActivityDetail.fromJson(<String, dynamic>{
    'metric': 'usage',
    'period': period,
    'total_seconds': totalMinutes * 60,
    'items': <Map<String, dynamic>>[
      item('cards', 'Cards', cards),
      item('ai', 'AI talk', talk),
      item('games', 'Games', games),
      item('radio', 'Radio', audio),
    ],
  });
}

/// The Imagine drawings Aarav asked Cheeko for, newest first.
List<ImagineImage> sampleImagine() => <ImagineImage>[
  ImagineImage(url: '$kCdn/imagine/im-05.jpg', createdAt: todayAt(18, 37)),
  ImagineImage(url: '$kCdn/imagine/im-07.jpg', createdAt: todayAt(16, 33)),
  ImagineImage(url: '$kCdn/imagine/im-16.jpg', createdAt: daysAgoAt(1, 18, 10)),
  ImagineImage(url: '$kCdn/imagine/im-10.jpg', createdAt: daysAgoAt(1, 17, 25)),
  ImagineImage(url: '$kCdn/imagine/im-17.jpg', createdAt: daysAgoAt(2, 16, 50)),
  ImagineImage(url: '$kCdn/imagine/im-11.jpg', createdAt: daysAgoAt(3, 17, 5)),
  ImagineImage(url: '$kCdn/imagine/im-13.jpg', createdAt: daysAgoAt(4, 18, 20)),
  ImagineImage(url: '$kCdn/imagine/im-01.jpg', createdAt: daysAgoAt(6, 16, 40)),
];

// ---------------------------------------------------------------------------
// Quiz
// ---------------------------------------------------------------------------

List<Map<String, dynamic>> _sampleQuestions({DateTime? weekStart}) {
  var n = 0;
  Map<String, dynamic> q(String text, String answer, String result) {
    final day =
        weekStart == null
            ? _todayDate
            : DateTime(weekStart.year, weekStart.month, weekStart.day + (n++ * 7) ~/ 10);
    return <String, dynamic>{
      'question_text': text,
      'correct_answer': answer,
      'result': result,
      'points': result == 'correct' ? 10 : 0,
      'answered_on': _dateKey(day),
    };
  }
  return <Map<String, dynamic>>[
    q('Which animal is called the king of the jungle?', 'Lion', 'correct'),
    q('How many legs does a spider have?', 'Eight', 'correct'),
    q('What colour do you get when you mix blue and yellow?', 'Green', 'correct'),
    q('Which bird is India’s national bird?', 'Peacock', 'correct'),
    q('What shape has three sides?', 'Triangle', 'wrong'),
    q('Which planet do we live on?', 'Earth', 'correct'),
    q('What is the opposite of “hot”?', 'Cold', 'correct'),
    q('How many days are there in a week?', 'Seven', 'wrong'),
    q('What do bees make?', 'Honey', 'correct'),
    q('Which is the biggest ocean?', 'Pacific Ocean', 'revealed'),
  ];
}

QuizAnalytics sampleQuiz(String period, {String? weekStart}) {
  final isDay = period == 'today' || period == 'day';
  final today = _todayDate;
  final week =
      isDay
          ? null
          : weekStart != null
          ? DateTime.parse(weekStart)
          : DateTime(today.year, today.month, today.day - (today.weekday - 1));
  final attempted = isDay ? 10 : 52;
  final correct = isDay ? 7 : 44;
  final accuracy = (correct * 100 / attempted).round();
  return QuizAnalytics.fromJson(<String, dynamic>{
    'period': period,
    'banks': <Map<String, dynamic>>[
      <String, dynamic>{
        'bank': 'quiz',
        'available': true,
        'current_level': 3,
        'attempted': attempted,
        'correct': correct,
        'points': correct * 10,
        'levels': <Map<String, dynamic>>[
          if (!isDay)
            <String, dynamic>{
              'level': 2,
              'attempted': 30,
              'correct': 27,
              'wrong': 2,
              'revealed': 1,
              'accuracy': 90,
              'points': 270,
              'replay': false,
              'cleared': true,
            },
          <String, dynamic>{
            'level': 3,
            'attempted': isDay ? 10 : 22,
            'correct': isDay ? 7 : 17,
            'wrong': isDay ? 2 : 4,
            'revealed': 1,
            'accuracy': isDay ? 70 : 77,
            'points': isDay ? 70 : 170,
            'replay': false,
            'cleared': false,
            'questions': _sampleQuestions(weekStart: week),
          },
        ],
      },
    ],
    'trend': <String, dynamic>{
      'direction': 'up',
      'accuracy': accuracy,
      'previous_accuracy': accuracy - 8,
      'delta': 8,
    },
  });
}

// ---------------------------------------------------------------------------
// Streak
// ---------------------------------------------------------------------------

/// Five days in a row, today included, after a quiet day five days ago. The
/// longest run (nine days) had a rest day in it.
String _streakStatus(int ago) {
  if (ago <= 4) return 'played';
  if (ago == 5) return 'quiet';
  if (ago == 7) return 'quiet';
  if (ago == 12) return 'rest';
  if (ago == 17 || ago == 24) return 'quiet';
  return 'played';
}

Map<String, dynamic> _streakDay(int ago) {
  final status = _streakStatus(ago);
  return <String, dynamic>{
    'date': _dateKey(dayAgo(ago)),
    'status': status == 'quiet' ? 'missed' : status,
    'questions': status == 'played' ? (ago == 0 ? 10 : 5 + (ago * 3) % 6) : 0,
  };
}

Map<String, dynamic> sampleStreakJson() {
  final monthStart = DateTime(_todayDate.year, _todayDate.month, 1);
  final daysThisMonth = _todayDate.difference(monthStart).inDays;
  return <String, dynamic>{
    'current': 5,
    'longest': 9,
    'todayDone': true,
    'questionsToday': 10,
    'questionsNeeded': 5,
    'restDaysUsedThisWeek': 0,
    'restDaysAllowed': 1,
    'nextMilestone': 7,
    'week': <Map<String, dynamic>>[
      for (var ago = 6; ago >= 0; ago--) _streakDay(ago),
    ],
    'month': <Map<String, dynamic>>[
      for (var ago = daysThisMonth; ago >= 0; ago--) _streakDay(ago),
    ],
  };
}

KidStreak sampleStreak() => KidStreak.fromJson(sampleStreakJson());

// ---------------------------------------------------------------------------
// Trends and sessions for Analytics
// ---------------------------------------------------------------------------

ProgressTrendPoint _pointFor(DateTime d) => ProgressTrendPoint(
  date: _dateKey(d),
  usageTimeSeconds: minutesOn(d) * 60,
  cardTapCount: cardsOn(d),
  gamesPlayed: gamesOn(d),
  aiInteractionCount: questionsOn(d),
);

List<DateTime> _weekOf(DateTime monday) => <DateTime>[
  for (var i = 0; i < 7; i++) DateTime(monday.year, monday.month, monday.day + i),
];

ProgressTrend sampleTrend(String period, {String? weekStart}) {
  final today = _todayDate;
  final List<DateTime> dates;
  if (period == 'week') {
    final monday =
        weekStart != null
            ? DateTime.parse(weekStart)
            : DateTime(today.year, today.month, today.day - (today.weekday - 1));
    dates = _weekOf(monday).where((d) => !d.isAfter(today)).toList();
  } else {
    // The last five weeks, so the month view and the streak both have a
    // history to read.
    dates = <DateTime>[
      for (var ago = 34; ago >= 0; ago--) dayAgo(ago),
    ];
  }
  return ProgressTrend(
    period: period,
    timezone: 'Asia/Kolkata',
    points: <ProgressTrendPoint>[for (final d in dates) _pointFor(d)],
  );
}

HomepageActivity sampleSummary(String period, {String? weekStart}) {
  if (period == 'today') {
    return HomepageActivity.fromJson(sampleProgressToday());
  }
  final trend = sampleTrend(period, weekStart: weekStart);
  var seconds = 0, cards = 0, games = 0, talks = 0;
  for (final p in trend.points) {
    seconds += p.usageTimeSeconds;
    cards += p.cardTapCount;
    games += p.gamesPlayed;
    talks += p.aiInteractionCount;
  }
  return HomepageActivity.fromJson(<String, dynamic>{
    'today_progress': <String, dynamic>{
      'usage_time_seconds': seconds,
      'card_tap_count': cards,
      'games_played': games,
      'ai_interaction_count': talks,
      'first_activity_date': '2026-05-10',
    },
  });
}

int _minutesInWeek(String? weekStart) {
  final trend = sampleTrend('week', weekStart: weekStart);
  return trend.points.fold<int>(0, (s, p) => s + p.usageTimeSeconds) ~/ 60;
}

/// Play sessions, the source of the success rate, the mode split and the
/// recent-sessions list. Today: seven sessions summing to 48 minutes, six
/// finished (86%). Every other day: three sessions, one in seven unfinished.
List<AnalyticsSession> sampleSessions() {
  var id = 0;
  AnalyticsSession s(
    DateTime start,
    String mode,
    int minutes,
    int interactions, {
    bool done = true,
  }) {
    id++;
    return AnalyticsSession.fromJson(<String, dynamic>{
      'id': id,
      'session_id': 'sess-$id',
      'mac_address': kMac,
      'agent_id': 'agent-1',
      'mode_type': mode,
      'started_at': start.toIso8601String(),
      'ended_at': start.add(Duration(minutes: minutes)).toIso8601String(),
      'duration_seconds': minutes * 60,
      'interaction_count': interactions,
      'completion_status': done ? 'completed' : 'abandoned',
    });
  }

  final sessions = <AnalyticsSession>[
    s(todayAt(18, 10), 'conversation', 11, 3),
    s(todayAt(17, 38), 'math_tutor', 7, 6),
    s(todayAt(17, 12), 'story', 9, 2),
    s(todayAt(16, 38), 'music', 6, 1),
    s(todayAt(16, 3), 'conversation', 6, 2),
    s(todayAt(15, 28), 'word_ladder', 5, 8, done: false),
    s(todayAt(15, 2), 'story', 4, 1),
  ];
  const modes = <String>['conversation', 'story', 'math_tutor', 'music', 'word_ladder'];
  for (var ago = 1; ago <= 30; ago++) {
    final day = dayAgo(ago);
    final minutes = minutesOn(day);
    if (minutes == 0) continue;
    final at = todayAt(16, 0).subtract(Duration(days: ago));
    for (var k = 0; k < 3; k++) {
      final share = k == 2 ? minutes - 2 * (minutes ~/ 3) : minutes ~/ 3;
      sessions.add(
        s(
          at.add(Duration(minutes: 40 * k)),
          modes[(ago + k) % modes.length],
          share,
          2 + (ago + k) % 5,
          done: (ago * 3 + k) % 7 != 0,
        ),
      );
    }
  }
  return sessions;
}

// ---------------------------------------------------------------------------
// Fakes: the service layer the screens read through
// ---------------------------------------------------------------------------

/// Everything the Java API answers, from the sample family above.
class SampleJavaApi implements JavaApiService {
  SampleJavaApi({this.imagine});

  final List<ImagineImage>? imagine;
  final List<String> calls = <String>[];

  @override
  Future<List<Map<String, dynamic>>> getUserDevices({
    bool forceRefresh = false,
  }) async => <Map<String, dynamic>>[
    sampleDeviceJson(),
    if (sampleTwoToys) sampleDevice2Json(),
  ];

  @override
  Future<ProgressTrend> getProgressTrend({
    required String period,
    String? mac,
    String? kidId,
    String? weekStart,
  }) async {
    calls.add('trend $period $weekStart');
    return sampleTrend(period, weekStart: weekStart);
  }

  @override
  Future<HomepageActivity> getProgressSummary({
    String period = 'week',
    String? mac,
    String? deviceId,
    String? fallbackDeviceId,
    String? kidId,
    String? weekStart,
  }) async {
    calls.add('summary $period $weekStart');
    return sampleSummary(period, weekStart: weekStart);
  }

  @override
  Future<HomepageActivity> getHomepageActivity({
    String? mac,
    String? deviceId,
    String? kidId,
  }) async => HomepageActivity.fromJson(sampleHomepageActivityJson());

  @override
  Future<HomepageActivityDetail> getProgressDetails({
    required String metric,
    required String period,
    String? mac,
    String? deviceId,
    String? fallbackDeviceId,
    String? kidId,
    String? month,
    String? weekStart,
    int page = 1,
    int limit = 20,
  }) async {
    calls.add('details $metric $period $weekStart');
    if (metric == 'cards' && period == 'today') return sampleCardsToday();
    if (metric == 'games' && period == 'today') return sampleGamesToday();
    if (metric == 'usage' && period == 'today') {
      return sampleUsageDetail('today', kTodayMinutes);
    }
    if (metric == 'usage' && period == 'week') {
      return sampleUsageDetail('week', _minutesInWeek(weekStart));
    }
    return HomepageActivityDetail.fromJson(<String, dynamic>{
      'metric': metric,
      'period': period,
    });
  }

  @override
  Future<Map<String, dynamic>> getDeviceRuntimeState(String mac) async =>
      sampleRuntimeJson();

  @override
  Future<List<ImagineImage>> getDeviceImagineImages(String mac) async =>
      imagine ?? sampleImagine();

  @override
  Future<QuizAnalytics?> getQuizAnalytics({
    String? kidId,
    String period = 'week',
    String? mac,
    String? weekStart,
  }) async => sampleQuiz(period, weekStart: weekStart);

  @override
  Future<List<KidCharacter>> getKidCharacters(String kidId) async =>
      <KidCharacter>[
        KidCharacter(
          agentId: 'agent-1',
          agentName: 'Cheeko',
          sessionCount: 5,
          lastSessionAt: todayAt(18, 35),
        ),
        KidCharacter(
          agentId: kNaniAgentId,
          agentName: 'Nani',
          sessionCount: 1,
          lastSessionAt: todayAt(15, 30),
        ),
      ];

  @override
  dynamic noSuchMethod(Invocation invocation) {
    calls.add('UNFAKED ${invocation.memberName}');
    return super.noSuchMethod(invocation);
  }
}

class SampleDeviceSettings extends DeviceSettingsService {
  SampleDeviceSettings({this.payload = const DeviceSettingsPayload(
    volume: 60,
    brightness: 70,
    sleepEnabled: false,
  )}) : super(JavaApiService(headersProvider: () async => {}));

  /// The toy's current settings. A save replaces it, as the server would.
  DeviceSettingsPayload payload;
  int _version = 7;

  /// Every PATCH body the app sent, for a test to print.
  final List<Map<String, dynamic>> patches = <Map<String, dynamic>>[];

  /// Holds a save in flight until completed, so the "saving" state can be
  /// photographed. Null answers at once.
  Completer<void>? patchGate;

  /// What the settings endpoint answers to a PATCH: the merged settings at
  /// the next version, already acknowledged by a toy that is online.
  @override
  Future<DeviceSettings> patchSettings(
    String mac,
    Map<String, dynamic> patch,
  ) async {
    patches.add(Map<String, dynamic>.from(patch));
    final gate = patchGate;
    if (gate != null) await gate.future;
    payload = payload.mergePatch(patch);
    _version++;
    return DeviceSettings(
      macAddress: mac,
      settingsVersion: _version,
      settings: payload,
      syncStatus: 'synced',
    );
  }

  @override
  Future<DeviceSettings> fetchSettings(String mac) async => DeviceSettings(
    macAddress: mac,
    settingsVersion: _version,
    settings: payload,
    syncStatus: 'synced',
  );

  @override
  Future<List<DeviceSyncEvent>> fetchSyncEvents(
    String mac, {
    int limit = 50,
  }) async => const <DeviceSyncEvent>[];

  @override
  Future<DeviceRuntimeState?> fetchRuntimeState(String mac) async =>
      sampleRuntimeState();
}

class SampleAgents implements JavaAgentService {
  @override
  Future<List<Map<String, dynamic>>> getUserAgents() async =>
      <Map<String, dynamic>>[
        <String, dynamic>{'id': 'agent-1', 'agentName': 'Cheeko'},
      ];

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleProfileApi implements ProfileApiService {
  @override
  Future<ParentProfile?> getParentProfile() async => ParentProfile(
    id: 'parent-1',
    userId: 'user-1',
    fullName: kParentName,
    email: 'priya@example.com',
    createdAt: DateTime(2026, 5, 10),
    updatedAt: DateTime(2026, 5, 10),
  );

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleKidsApi implements KidsApiService {
  @override
  Future<List<Kid>> getKids(String parentId) async =>
      <Kid>[for (final json in sampleKidsJson()) Kid.fromJson(json)];

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleAnalyticsApi implements AnalyticsApiService {
  @override
  Future<AnalyticsOverallStats?> getOverallStats(String macAddress) async =>
      const AnalyticsOverallStats(
        totalSessions: 214,
        totalTimeSeconds: 96 * 3600,
        totalInteractions: 1480,
        successRatePercentage: 86,
        longestStreak: 9,
        totalStreaksCompleted: 6,
        skillLevel: 'Explorer',
        sessionsByMode: <String, int>{
          'conversation': 70,
          'story': 52,
          'math_tutor': 38,
          'music': 30,
          'word_ladder': 24,
        },
      );

  @override
  Future<List<AnalyticsUserProgress>> getUserProgress(
    String macAddress,
  ) async => <AnalyticsUserProgress>[
    AnalyticsUserProgress.fromJson(<String, dynamic>{
      'modeType': 'math_tutor',
      'macAddress': kMac,
      'totalSessions': 38,
      'totalTimeSeconds': 38 * 7 * 60,
      'totalInteractions': 228,
      'successRatePercentage': 84,
      'skillLevel': 'intermediate',
    }),
    AnalyticsUserProgress.fromJson(<String, dynamic>{
      'modeType': 'word_ladder',
      'macAddress': kMac,
      'totalSessions': 24,
      'totalTimeSeconds': 24 * 5 * 60,
      'totalInteractions': 190,
      'successRatePercentage': 72,
      'skillLevel': 'intermediate',
    }),
  ];

  @override
  Future<List<AnalyticsSession>> getRecentSessions(
    String macAddress, {
    int limit = 10,
  }) async => sampleSessions().take(limit).toList();

  @override
  Future<Map<String, dynamic>> getGameAttemptStats(String macAddress) async =>
      const <String, dynamic>{'total': kTodayGames};

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleChatHistory implements ChatHistoryService {
  @override
  Future<List<ChatMessage>> getTodayMessagesForKid(
    String kidId, {
    AnalyticsDay? day,
    DateTime? now,
    int sessionsPerCharacter = 3,
  }) async => sampleTodayChat();

  @override
  Future<List<ChatMessage>> getWeekMessagesForKid(
    String kidId, {
    DateTime? now,
    int sessionsPerCharacter = 50,
  }) async => sampleTodayChat();

  /// What the character strip reads when a face is tapped: today's sessions
  /// with that one character.
  @override
  Future<List<CharacterSessionTranscript>> getTodayCharacterConversation(
    String kidId,
    String agentId, {
    AnalyticsDay? day,
    DateTime? now,
    int sessionsPerPage = 20,
    int maxPages = 3,
    int messagesPerSession = 300,
  }) async {
    if (agentId == kNaniAgentId) return sampleNaniToday();
    return const <CharacterSessionTranscript>[];
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleRecommendations implements HomeRecommendationService {
  static const List<HomeRecommendationItem> items = <HomeRecommendationItem>[
    HomeRecommendationItem(
      id: 'dreamy',
      type: HomeRecommendationType.content,
      title: 'Dreamy Melodies',
      category: 'RFID Content Card',
      thumbnailUrl: '$kCdn/cards/04-dreamy-melodies.jpg',
    ),
    HomeRecommendationItem(
      id: 'clever',
      type: HomeRecommendationType.content,
      title: 'Clever Little Tales',
      category: 'RFID Content Card',
      thumbnailUrl: '$kCdn/cards/07-clever-little-tales.jpg',
    ),
    HomeRecommendationItem(
      id: 'ravi-nila',
      type: HomeRecommendationType.content,
      title: 'The Adventures of Ravi & Nila',
      category: 'RFID Content Card',
      thumbnailUrl: '$kCdn/cards/08-ravi-and-nila.jpg',
    ),
    HomeRecommendationItem(
      id: 'make-your-own',
      type: HomeRecommendationType.content,
      title: 'Make Your Own',
      category: 'RFID Content Card',
      thumbnailUrl: '$kCdn/cards/06-make-your-own.jpg',
    ),
  ];

  @override
  Future<List<HomeRecommendationItem>> getCachedRecommendations({
    Kid? activeKid,
    int limit = 8,
  }) async => items;

  @override
  Future<List<HomeRecommendationItem>> getHomepageRecommendations({
    Device? activeDevice,
    Kid? activeKid,
    int limit = 8,
    bool allowEmptyFallback = false,
  }) async => items;

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class SampleTimezoneSync implements ParentTimezoneSyncService {
  @override
  Future<void> sync(ParentProfile? profile) async {}

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

// ---------------------------------------------------------------------------
// The pretend backend for services that talk HTTP directly
// ---------------------------------------------------------------------------

/// What Cheeko's own setup hotspot (http://192.168.4.1) answers while it is
/// in Wi-Fi setup mode: the networks it can see, strongest first.
List<Map<String, dynamic>> sampleCheekoScan() => <Map<String, dynamic>>[
  <String, dynamic>{'ssid': 'Sharma Home WiFi', 'rssi': -42, 'authmode': 3},
  <String, dynamic>{'ssid': 'Sharma Home WiFi 5G', 'rssi': -55, 'authmode': 3},
  <String, dynamic>{'ssid': 'JioFiber-Mehta', 'rssi': -63, 'authmode': 3},
  <String, dynamic>{'ssid': 'Airtel_Kapoor_Home', 'rssi': -71, 'authmode': 3},
  <String, dynamic>{'ssid': 'TP-Link_4B2C', 'rssi': -80, 'authmode': 4},
];

FakeReply? sampleBackend(String method, Uri uri, String body) {
  final path = uri.path;
  if (uri.host == '192.168.4.1') {
    if (path == '/scan') return FakeReply.json(sampleCheekoScan());
    if (path == '/submit') return FakeReply.json(<String, dynamic>{'success': true});
    if (path == '/reboot') return FakeReply.json(<String, dynamic>{'success': true});
    return FakeReply.json(<String, dynamic>{'status': 'ok'});
  }
  if (path.endsWith('/kids/$kKidId/streak')) {
    return FakeReply.envelope(sampleStreakJson());
  }
  if (path.endsWith('/kids/$kKidId/events')) {
    return FakeReply.envelope(sampleEventsJson());
  }
  if (path.endsWith('/toy/api/mobile/kids') ||
      path.endsWith('/toy/api/mobile/kids/')) {
    return FakeReply.json(sampleKidsJson());
  }
  if (path.endsWith('/kids/$kKidId')) {
    return FakeReply.envelope(sampleKidJson());
  }
  return null;
}

/// The two events on 04_house_rules_upcoming: one the parent added, one Aarav
/// told Cheeko about.
List<Map<String, dynamic>> sampleUpcomingEventsJson() => <Map<String, dynamic>>[
  <String, dynamic>{
    'id': 'evt-2',
    'kid_id': kKidId,
    'title': 'Science exam',
    'event_date': '2026-10-14',
    'source': 'parent',
    'created_at': todayAt(9, 0).toIso8601String(),
  },
  <String, dynamic>{
    'id': 'evt-3',
    'kid_id': kKidId,
    'title': 'Birthday party at Riya’s',
    'event_date': '2026-10-24',
    'source': 'child',
    'times_mentioned': 1,
    'created_at': todayAt(17, 12).toIso8601String(),
  },
];

List<Map<String, dynamic>> sampleEventsJson() {
  final today = _todayIst;
  final todayDate = DateTime(today.year, today.month, today.day);
  // The coming Friday.
  var friday = todayDate;
  while (friday.weekday != DateTime.friday) {
    friday = friday.add(const Duration(days: 1));
  }
  return <Map<String, dynamic>>[
    <String, dynamic>{
      'id': 'evt-1',
      'kid_id': kKidId,
      'title': 'Maths exam',
      'event_date': _dateKey(friday),
      'created_at': todayAt(9, 0).toIso8601String(),
    },
  ];
}
