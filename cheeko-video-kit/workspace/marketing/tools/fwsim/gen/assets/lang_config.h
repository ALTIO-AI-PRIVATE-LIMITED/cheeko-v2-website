// Auto-generated language config
// Language: en-US with en-US fallback
#pragma once

#include <string_view>

#ifndef en_us
    #define en_us  // 預設語言
#endif

namespace Lang {
    // 语言元数据
    constexpr const char* CODE = "en-US";

    // 字符串资源 (en-US as fallback for missing keys)
    namespace Strings {
        constexpr const char* ACCESS_VIA_BROWSER = " Config URL: ";
        constexpr const char* ACTIVATION = "Activation";
        constexpr const char* BATTERY_CHARGING = "Charging";
        constexpr const char* BATTERY_FULL = "Battery full";
        constexpr const char* BATTERY_LOW = "Low battery";
        constexpr const char* BATTERY_NEED_CHARGE = "Low battery, please charge";
        constexpr const char* CHECKING_NEW_VERSION = "Checking for new version...";
        constexpr const char* CHECK_NEW_VERSION_FAILED = "Check for new version failed, will retry in %d seconds: %s";
        constexpr const char* CONNECTED_TO = "Connected to ";
        constexpr const char* CONNECTING = "Connecting...";
        constexpr const char* CONNECTING_TO = "Connecting to ";
        constexpr const char* CONNECTION_SUCCESSFUL = "Connection Successful";
        constexpr const char* CONNECT_TO = "Connect to ";
        constexpr const char* CONNECT_TO_HOTSPOT = "Hotspot: ";
        constexpr const char* DETECTING_MODULE = "Detecting module...";
        constexpr const char* DOWNLOAD_ASSETS_FAILED = "Failed to download assets";
        constexpr const char* ENTERING_WIFI_CONFIG_MODE = "Entering Wi-Fi configuration mode...";
        constexpr const char* ERROR = "Error";
        constexpr const char* FLIGHT_MODE_OFF = "Flight mode is off";
        constexpr const char* FLIGHT_MODE_ON = "Flight mode is on";
        constexpr const char* FOUND_NEW_ASSETS = "Found new assets: %s";
        constexpr const char* HELLO_MY_FRIEND = "Hello, my friend!";
        constexpr const char* INFO = "Information";
        constexpr const char* INITIALIZING = "Waking up...";
        constexpr const char* LISTENING = "Listening...";
        constexpr const char* LOADING_ASSETS = "Loading assets...";
        constexpr const char* LOADING_PROTOCOL = "Logging in...";
        constexpr const char* MAX_VOLUME = "Max volume";
        constexpr const char* MODEM_INIT_ERROR = "Modem initialization failed";
        constexpr const char* MUTED = "Muted";
        constexpr const char* NEW_VERSION = "New version ";
        constexpr const char* OTA_UPGRADE = "OTA Upgrade";
        constexpr const char* PIN_ERROR = "Please insert SIM card";
        constexpr const char* PLEASE_WAIT = "Please wait...";
        constexpr const char* REGISTERING_NETWORK = "Waiting for network...";
        constexpr const char* REG_ERROR = "Unable to access network, please check SIM card status";
        constexpr const char* RTC_MODE_OFF = "AEC Off";
        constexpr const char* RTC_MODE_ON = "AEC On";
        constexpr const char* SCANNING_WIFI = "Scanning Wi-Fi...";
        constexpr const char* SERVER_BUSY = "Cheeko is busy, one moment";
        constexpr const char* SERVER_ERROR = "Sending failed, please check the network";
        constexpr const char* SERVER_NOT_CONNECTED = "Unable to connect to service, please try again later";
        constexpr const char* SERVER_NOT_FOUND = "Looking for available service";
        constexpr const char* SERVER_TIMEOUT = "Waiting for response timeout";
        constexpr const char* SPEAKING = "Speaking...";
        constexpr const char* STANDBY = "Standby";
        constexpr const char* SWITCH_TO_4G_NETWORK = "Switching to 4G...";
        constexpr const char* SWITCH_TO_WIFI_NETWORK = "Switching to Wi-Fi...";
        constexpr const char* UPGRADE_FAILED = "Upgrade failed";
        constexpr const char* UPGRADING = "System is upgrading...";
        constexpr const char* VERSION = "Ver ";
        constexpr const char* VOLUME = "Volume ";
        constexpr const char* WARNING = "Warning";
        constexpr const char* WIFI_CONFIG_MODE = "Wi-Fi Configuration Mode";
    }

    // 音效资源 (en-US as fallback for missing audio files)
    namespace Sounds {

        extern const char ogg_0_start[] asm("_binary_0_ogg_start");
        extern const char ogg_0_end[] asm("_binary_0_ogg_end");
        static const std::string_view OGG_0 {
        static_cast<const char*>(ogg_0_start),
        static_cast<size_t>(ogg_0_end - ogg_0_start)
        };

        extern const char ogg_1_start[] asm("_binary_1_ogg_start");
        extern const char ogg_1_end[] asm("_binary_1_ogg_end");
        static const std::string_view OGG_1 {
        static_cast<const char*>(ogg_1_start),
        static_cast<size_t>(ogg_1_end - ogg_1_start)
        };

        extern const char ogg_2_start[] asm("_binary_2_ogg_start");
        extern const char ogg_2_end[] asm("_binary_2_ogg_end");
        static const std::string_view OGG_2 {
        static_cast<const char*>(ogg_2_start),
        static_cast<size_t>(ogg_2_end - ogg_2_start)
        };

        extern const char ogg_3_start[] asm("_binary_3_ogg_start");
        extern const char ogg_3_end[] asm("_binary_3_ogg_end");
        static const std::string_view OGG_3 {
        static_cast<const char*>(ogg_3_start),
        static_cast<size_t>(ogg_3_end - ogg_3_start)
        };

        extern const char ogg_4_start[] asm("_binary_4_ogg_start");
        extern const char ogg_4_end[] asm("_binary_4_ogg_end");
        static const std::string_view OGG_4 {
        static_cast<const char*>(ogg_4_start),
        static_cast<size_t>(ogg_4_end - ogg_4_start)
        };

        extern const char ogg_5_start[] asm("_binary_5_ogg_start");
        extern const char ogg_5_end[] asm("_binary_5_ogg_end");
        static const std::string_view OGG_5 {
        static_cast<const char*>(ogg_5_start),
        static_cast<size_t>(ogg_5_end - ogg_5_start)
        };

        extern const char ogg_6_start[] asm("_binary_6_ogg_start");
        extern const char ogg_6_end[] asm("_binary_6_ogg_end");
        static const std::string_view OGG_6 {
        static_cast<const char*>(ogg_6_start),
        static_cast<size_t>(ogg_6_end - ogg_6_start)
        };

        extern const char ogg_7_start[] asm("_binary_7_ogg_start");
        extern const char ogg_7_end[] asm("_binary_7_ogg_end");
        static const std::string_view OGG_7 {
        static_cast<const char*>(ogg_7_start),
        static_cast<size_t>(ogg_7_end - ogg_7_start)
        };

        extern const char ogg_8_start[] asm("_binary_8_ogg_start");
        extern const char ogg_8_end[] asm("_binary_8_ogg_end");
        static const std::string_view OGG_8 {
        static_cast<const char*>(ogg_8_start),
        static_cast<size_t>(ogg_8_end - ogg_8_start)
        };

        extern const char ogg_9_start[] asm("_binary_9_ogg_start");
        extern const char ogg_9_end[] asm("_binary_9_ogg_end");
        static const std::string_view OGG_9 {
        static_cast<const char*>(ogg_9_start),
        static_cast<size_t>(ogg_9_end - ogg_9_start)
        };

        extern const char ogg_activation_start[] asm("_binary_activation_ogg_start");
        extern const char ogg_activation_end[] asm("_binary_activation_ogg_end");
        static const std::string_view OGG_ACTIVATION {
        static_cast<const char*>(ogg_activation_start),
        static_cast<size_t>(ogg_activation_end - ogg_activation_start)
        };

        extern const char ogg_battery_low_start[] asm("_binary_battery_low_ogg_start");
        extern const char ogg_battery_low_end[] asm("_binary_battery_low_ogg_end");
        static const std::string_view OGG_BATTERY_LOW {
        static_cast<const char*>(ogg_battery_low_start),
        static_cast<size_t>(ogg_battery_low_end - ogg_battery_low_start)
        };

        extern const char ogg_boot_startup_start[] asm("_binary_boot_startup_ogg_start");
        extern const char ogg_boot_startup_end[] asm("_binary_boot_startup_ogg_end");
        static const std::string_view OGG_BOOT_STARTUP {
        static_cast<const char*>(ogg_boot_startup_start),
        static_cast<size_t>(ogg_boot_startup_end - ogg_boot_startup_start)
        };

        extern const char ogg_card_insert_start[] asm("_binary_card_insert_ogg_start");
        extern const char ogg_card_insert_end[] asm("_binary_card_insert_ogg_end");
        static const std::string_view OGG_CARD_INSERT {
        static_cast<const char*>(ogg_card_insert_start),
        static_cast<size_t>(ogg_card_insert_end - ogg_card_insert_start)
        };

        extern const char ogg_charge_connect_start[] asm("_binary_charge_connect_ogg_start");
        extern const char ogg_charge_connect_end[] asm("_binary_charge_connect_ogg_end");
        static const std::string_view OGG_CHARGE_CONNECT {
        static_cast<const char*>(ogg_charge_connect_start),
        static_cast<size_t>(ogg_charge_connect_end - ogg_charge_connect_start)
        };

        extern const char ogg_charge_full_start[] asm("_binary_charge_full_ogg_start");
        extern const char ogg_charge_full_end[] asm("_binary_charge_full_ogg_end");
        static const std::string_view OGG_CHARGE_FULL {
        static_cast<const char*>(ogg_charge_full_start),
        static_cast<size_t>(ogg_charge_full_end - ogg_charge_full_start)
        };

        extern const char ogg_cheeko_intro_start[] asm("_binary_cheeko_intro_ogg_start");
        extern const char ogg_cheeko_intro_end[] asm("_binary_cheeko_intro_ogg_end");
        static const std::string_view OGG_CHEEKO_INTRO {
        static_cast<const char*>(ogg_cheeko_intro_start),
        static_cast<size_t>(ogg_cheeko_intro_end - ogg_cheeko_intro_start)
        };

        extern const char ogg_cheeko_offline_start[] asm("_binary_cheeko_offline_ogg_start");
        extern const char ogg_cheeko_offline_end[] asm("_binary_cheeko_offline_ogg_end");
        static const std::string_view OGG_CHEEKO_OFFLINE {
        static_cast<const char*>(ogg_cheeko_offline_start),
        static_cast<size_t>(ogg_cheeko_offline_end - ogg_cheeko_offline_start)
        };

        extern const char ogg_connecting_network_start[] asm("_binary_connecting_network_ogg_start");
        extern const char ogg_connecting_network_end[] asm("_binary_connecting_network_ogg_end");
        static const std::string_view OGG_CONNECTING_NETWORK {
        static_cast<const char*>(ogg_connecting_network_start),
        static_cast<size_t>(ogg_connecting_network_end - ogg_connecting_network_start)
        };

        extern const char ogg_err_pin_start[] asm("_binary_err_pin_ogg_start");
        extern const char ogg_err_pin_end[] asm("_binary_err_pin_ogg_end");
        static const std::string_view OGG_ERR_PIN {
        static_cast<const char*>(ogg_err_pin_start),
        static_cast<size_t>(ogg_err_pin_end - ogg_err_pin_start)
        };

        extern const char ogg_err_reg_start[] asm("_binary_err_reg_ogg_start");
        extern const char ogg_err_reg_end[] asm("_binary_err_reg_ogg_end");
        static const std::string_view OGG_ERR_REG {
        static_cast<const char*>(ogg_err_reg_start),
        static_cast<size_t>(ogg_err_reg_end - ogg_err_reg_start)
        };

        extern const char ogg_exclamation_start[] asm("_binary_exclamation_ogg_start");
        extern const char ogg_exclamation_end[] asm("_binary_exclamation_ogg_end");
        static const std::string_view OGG_EXCLAMATION {
        static_cast<const char*>(ogg_exclamation_start),
        static_cast<size_t>(ogg_exclamation_end - ogg_exclamation_start)
        };

        extern const char ogg_knob_click_start[] asm("_binary_knob_click_ogg_start");
        extern const char ogg_knob_click_end[] asm("_binary_knob_click_ogg_end");
        static const std::string_view OGG_KNOB_CLICK {
        static_cast<const char*>(ogg_knob_click_start),
        static_cast<size_t>(ogg_knob_click_end - ogg_knob_click_start)
        };

        extern const char ogg_knob_turn_start[] asm("_binary_knob_turn_ogg_start");
        extern const char ogg_knob_turn_end[] asm("_binary_knob_turn_ogg_end");
        static const std::string_view OGG_KNOB_TURN {
        static_cast<const char*>(ogg_knob_turn_start),
        static_cast<size_t>(ogg_knob_turn_end - ogg_knob_turn_start)
        };

        extern const char ogg_low_battery_start[] asm("_binary_low_battery_ogg_start");
        extern const char ogg_low_battery_end[] asm("_binary_low_battery_ogg_end");
        static const std::string_view OGG_LOW_BATTERY {
        static_cast<const char*>(ogg_low_battery_start),
        static_cast<size_t>(ogg_low_battery_end - ogg_low_battery_start)
        };

        extern const char ogg_math_0_start[] asm("_binary_math_0_ogg_start");
        extern const char ogg_math_0_end[] asm("_binary_math_0_ogg_end");
        static const std::string_view OGG_MATH_0 {
        static_cast<const char*>(ogg_math_0_start),
        static_cast<size_t>(ogg_math_0_end - ogg_math_0_start)
        };

        extern const char ogg_math_1_start[] asm("_binary_math_1_ogg_start");
        extern const char ogg_math_1_end[] asm("_binary_math_1_ogg_end");
        static const std::string_view OGG_MATH_1 {
        static_cast<const char*>(ogg_math_1_start),
        static_cast<size_t>(ogg_math_1_end - ogg_math_1_start)
        };

        extern const char ogg_math_2_start[] asm("_binary_math_2_ogg_start");
        extern const char ogg_math_2_end[] asm("_binary_math_2_ogg_end");
        static const std::string_view OGG_MATH_2 {
        static_cast<const char*>(ogg_math_2_start),
        static_cast<size_t>(ogg_math_2_end - ogg_math_2_start)
        };

        extern const char ogg_math_3_start[] asm("_binary_math_3_ogg_start");
        extern const char ogg_math_3_end[] asm("_binary_math_3_ogg_end");
        static const std::string_view OGG_MATH_3 {
        static_cast<const char*>(ogg_math_3_start),
        static_cast<size_t>(ogg_math_3_end - ogg_math_3_start)
        };

        extern const char ogg_math_4_start[] asm("_binary_math_4_ogg_start");
        extern const char ogg_math_4_end[] asm("_binary_math_4_ogg_end");
        static const std::string_view OGG_MATH_4 {
        static_cast<const char*>(ogg_math_4_start),
        static_cast<size_t>(ogg_math_4_end - ogg_math_4_start)
        };

        extern const char ogg_math_5_start[] asm("_binary_math_5_ogg_start");
        extern const char ogg_math_5_end[] asm("_binary_math_5_ogg_end");
        static const std::string_view OGG_MATH_5 {
        static_cast<const char*>(ogg_math_5_start),
        static_cast<size_t>(ogg_math_5_end - ogg_math_5_start)
        };

        extern const char ogg_math_6_start[] asm("_binary_math_6_ogg_start");
        extern const char ogg_math_6_end[] asm("_binary_math_6_ogg_end");
        static const std::string_view OGG_MATH_6 {
        static_cast<const char*>(ogg_math_6_start),
        static_cast<size_t>(ogg_math_6_end - ogg_math_6_start)
        };

        extern const char ogg_math_7_start[] asm("_binary_math_7_ogg_start");
        extern const char ogg_math_7_end[] asm("_binary_math_7_ogg_end");
        static const std::string_view OGG_MATH_7 {
        static_cast<const char*>(ogg_math_7_start),
        static_cast<size_t>(ogg_math_7_end - ogg_math_7_start)
        };

        extern const char ogg_math_8_start[] asm("_binary_math_8_ogg_start");
        extern const char ogg_math_8_end[] asm("_binary_math_8_ogg_end");
        static const std::string_view OGG_MATH_8 {
        static_cast<const char*>(ogg_math_8_start),
        static_cast<size_t>(ogg_math_8_end - ogg_math_8_start)
        };

        extern const char ogg_math_9_start[] asm("_binary_math_9_ogg_start");
        extern const char ogg_math_9_end[] asm("_binary_math_9_ogg_end");
        static const std::string_view OGG_MATH_9 {
        static_cast<const char*>(ogg_math_9_start),
        static_cast<size_t>(ogg_math_9_end - ogg_math_9_start)
        };

        extern const char ogg_onb_back_start[] asm("_binary_onb_back_ogg_start");
        extern const char ogg_onb_back_end[] asm("_binary_onb_back_ogg_end");
        static const std::string_view OGG_ONB_BACK {
        static_cast<const char*>(ogg_onb_back_start),
        static_cast<size_t>(ogg_onb_back_end - ogg_onb_back_start)
        };

        extern const char ogg_onb_card_start[] asm("_binary_onb_card_ogg_start");
        extern const char ogg_onb_card_end[] asm("_binary_onb_card_ogg_end");
        static const std::string_view OGG_ONB_CARD {
        static_cast<const char*>(ogg_onb_card_start),
        static_cast<size_t>(ogg_onb_card_end - ogg_onb_card_start)
        };

        extern const char ogg_onb_cardok_start[] asm("_binary_onb_cardok_ogg_start");
        extern const char ogg_onb_cardok_end[] asm("_binary_onb_cardok_ogg_end");
        static const std::string_view OGG_ONB_CARDOK {
        static_cast<const char*>(ogg_onb_cardok_start),
        static_cast<size_t>(ogg_onb_cardok_end - ogg_onb_cardok_start)
        };

        extern const char ogg_onb_hello_start[] asm("_binary_onb_hello_ogg_start");
        extern const char ogg_onb_hello_end[] asm("_binary_onb_hello_ogg_end");
        static const std::string_view OGG_ONB_HELLO {
        static_cast<const char*>(ogg_onb_hello_start),
        static_cast<size_t>(ogg_onb_hello_end - ogg_onb_hello_start)
        };

        extern const char ogg_onb_later_start[] asm("_binary_onb_later_ogg_start");
        extern const char ogg_onb_later_end[] asm("_binary_onb_later_ogg_end");
        static const std::string_view OGG_ONB_LATER {
        static_cast<const char*>(ogg_onb_later_start),
        static_cast<size_t>(ogg_onb_later_end - ogg_onb_later_start)
        };

        extern const char ogg_onb_press_start[] asm("_binary_onb_press_ogg_start");
        extern const char ogg_onb_press_end[] asm("_binary_onb_press_ogg_end");
        static const std::string_view OGG_ONB_PRESS {
        static_cast<const char*>(ogg_onb_press_start),
        static_cast<size_t>(ogg_onb_press_end - ogg_onb_press_start)
        };

        extern const char ogg_onb_ready_start[] asm("_binary_onb_ready_ogg_start");
        extern const char ogg_onb_ready_end[] asm("_binary_onb_ready_ogg_end");
        static const std::string_view OGG_ONB_READY {
        static_cast<const char*>(ogg_onb_ready_start),
        static_cast<size_t>(ogg_onb_ready_end - ogg_onb_ready_start)
        };

        extern const char ogg_onb_swipe_start[] asm("_binary_onb_swipe_ogg_start");
        extern const char ogg_onb_swipe_end[] asm("_binary_onb_swipe_ogg_end");
        static const std::string_view OGG_ONB_SWIPE {
        static_cast<const char*>(ogg_onb_swipe_start),
        static_cast<size_t>(ogg_onb_swipe_end - ogg_onb_swipe_start)
        };

        extern const char ogg_onb_tap_start[] asm("_binary_onb_tap_ogg_start");
        extern const char ogg_onb_tap_end[] asm("_binary_onb_tap_ogg_end");
        static const std::string_view OGG_ONB_TAP {
        static_cast<const char*>(ogg_onb_tap_start),
        static_cast<size_t>(ogg_onb_tap_end - ogg_onb_tap_start)
        };

        extern const char ogg_onb_turn_start[] asm("_binary_onb_turn_ogg_start");
        extern const char ogg_onb_turn_end[] asm("_binary_onb_turn_ogg_end");
        static const std::string_view OGG_ONB_TURN {
        static_cast<const char*>(ogg_onb_turn_start),
        static_cast<size_t>(ogg_onb_turn_end - ogg_onb_turn_start)
        };

        extern const char ogg_popup_start[] asm("_binary_popup_ogg_start");
        extern const char ogg_popup_end[] asm("_binary_popup_ogg_end");
        static const std::string_view OGG_POPUP {
        static_cast<const char*>(ogg_popup_start),
        static_cast<size_t>(ogg_popup_end - ogg_popup_start)
        };

        extern const char ogg_sleep_bye_start[] asm("_binary_sleep_bye_ogg_start");
        extern const char ogg_sleep_bye_end[] asm("_binary_sleep_bye_ogg_end");
        static const std::string_view OGG_SLEEP_BYE {
        static_cast<const char*>(ogg_sleep_bye_start),
        static_cast<size_t>(ogg_sleep_bye_end - ogg_sleep_bye_start)
        };

        extern const char ogg_success_start[] asm("_binary_success_ogg_start");
        extern const char ogg_success_end[] asm("_binary_success_ogg_end");
        static const std::string_view OGG_SUCCESS {
        static_cast<const char*>(ogg_success_start),
        static_cast<size_t>(ogg_success_end - ogg_success_start)
        };

        extern const char ogg_upgrade_start[] asm("_binary_upgrade_ogg_start");
        extern const char ogg_upgrade_end[] asm("_binary_upgrade_ogg_end");
        static const std::string_view OGG_UPGRADE {
        static_cast<const char*>(ogg_upgrade_start),
        static_cast<size_t>(ogg_upgrade_end - ogg_upgrade_start)
        };

        extern const char ogg_vibration_start[] asm("_binary_vibration_ogg_start");
        extern const char ogg_vibration_end[] asm("_binary_vibration_ogg_end");
        static const std::string_view OGG_VIBRATION {
        static_cast<const char*>(ogg_vibration_start),
        static_cast<size_t>(ogg_vibration_end - ogg_vibration_start)
        };

        extern const char ogg_vol_up_start[] asm("_binary_vol_up_ogg_start");
        extern const char ogg_vol_up_end[] asm("_binary_vol_up_ogg_end");
        static const std::string_view OGG_VOL_UP {
        static_cast<const char*>(ogg_vol_up_start),
        static_cast<size_t>(ogg_vol_up_end - ogg_vol_up_start)
        };

        extern const char ogg_waiting_card_start[] asm("_binary_waiting_card_ogg_start");
        extern const char ogg_waiting_card_end[] asm("_binary_waiting_card_ogg_end");
        static const std::string_view OGG_WAITING_CARD {
        static_cast<const char*>(ogg_waiting_card_start),
        static_cast<size_t>(ogg_waiting_card_end - ogg_waiting_card_start)
        };

        extern const char ogg_welcome_start[] asm("_binary_welcome_ogg_start");
        extern const char ogg_welcome_end[] asm("_binary_welcome_ogg_end");
        static const std::string_view OGG_WELCOME {
        static_cast<const char*>(ogg_welcome_start),
        static_cast<size_t>(ogg_welcome_end - ogg_welcome_start)
        };

        extern const char ogg_wificonfig_start[] asm("_binary_wificonfig_ogg_start");
        extern const char ogg_wificonfig_end[] asm("_binary_wificonfig_ogg_end");
        static const std::string_view OGG_WIFICONFIG {
        static_cast<const char*>(ogg_wificonfig_start),
        static_cast<size_t>(ogg_wificonfig_end - ogg_wificonfig_start)
        };
    }
}
