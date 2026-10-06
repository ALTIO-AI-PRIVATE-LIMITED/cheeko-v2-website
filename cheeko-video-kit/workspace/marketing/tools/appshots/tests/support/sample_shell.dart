// The real four-tab nav shell (MainNavigationScreen) wired the way main.dart
// wires it, with every service swapped for the sample family.
import 'package:cheekoai_parent_app/models/device_settings_payload.dart';
import 'package:cheekoai_parent_app/providers/assistive_button_provider.dart';
import 'package:cheekoai_parent_app/providers/data/home_providers.dart';
import 'package:cheekoai_parent_app/providers/device_provider.dart';
import 'package:cheekoai_parent_app/providers/device_settings_provider.dart';
import 'package:cheekoai_parent_app/providers/infrastructure/api_providers.dart';
import 'package:cheekoai_parent_app/services/chat_history_service.dart';
import 'package:cheekoai_parent_app/services/java_api_service.dart';
import 'package:cheekoai_parent_app/services/profile_api_service.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart' show ProviderScope;
import 'package:provider/provider.dart';

import 'sample_data.dart';
import 'shots.dart';

class SampleApp {
  SampleApp({DeviceSettingsPayload? settings})
    : settingsService =
          settings == null
              ? SampleDeviceSettings()
              : SampleDeviceSettings(payload: settings);

  final SampleJavaApi api = SampleJavaApi();
  final DeviceProvider deviceProvider = DeviceProvider();
  final SampleChatHistory chatHistory = SampleChatHistory();
  final SampleProfileApi profileApi = SampleProfileApi();
  final SampleDeviceSettings settingsService;

  /// Wraps [home] in the providers main.dart puts above MyApp.
  Widget wrap(Widget home) {
    return ProviderScope(
      overrides: [
        javaApiServiceProvider.overrideWithValue(api),
        deviceProviderProvider.overrideWithValue(deviceProvider),
        javaAgentServiceProvider.overrideWithValue(SampleAgents()),
        profileApiServiceProvider.overrideWithValue(profileApi),
        kidsApiServiceProvider.overrideWithValue(SampleKidsApi()),
        analyticsApiServiceProvider.overrideWithValue(SampleAnalyticsApi()),
        chatHistoryServiceProvider.overrideWithValue(chatHistory),
        homeRecommendationServiceProvider.overrideWithValue(
          SampleRecommendations(),
        ),
        parentTimezoneSyncServiceProvider.overrideWithValue(
          SampleTimezoneSync(),
        ),
        homeSessionCheckProvider.overrideWithValue(() => true),
        homeConnectivityProvider.overrideWithValue(() async => true),
      ],
      child: MultiProvider(
        providers: [
          ChangeNotifierProvider<DeviceProvider>.value(value: deviceProvider),
          Provider<JavaApiService>.value(value: api),
          Provider<ChatHistoryService>.value(value: chatHistory),
          ChangeNotifierProvider(
            create: (_) => DeviceSettingsProvider(settingsService),
          ),
          ChangeNotifierProvider(create: (_) => AssistiveButtonProvider()),
          Provider<ProfileApiService>.value(value: profileApi),
        ],
        child: appShell(home: home),
      ),
    );
  }
}
