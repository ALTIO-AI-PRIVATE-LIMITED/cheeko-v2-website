cmake_minimum_required(VERSION 3.16)
project(cheeko_fwsim C CXX)

# Host (macOS) build of the Cheeko firmware's LVGL UI code, rendering into an
# in-memory 296x240 RGB565 framebuffer. The firmware sources come from
# ${FW_ROOT} (an extracted `git archive` of cheeko-os-v2); nothing in the repo
# itself is touched. See render.sh.

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()

set(SIM ${CMAKE_CURRENT_SOURCE_DIR})
if(NOT FW_ROOT)
  set(FW_ROOT ${SIM}/src)
endif()
set(FW ${FW_ROOT}/main)
if(NOT FWSIM_PROJECT_VER)
  file(STRINGS ${FW_ROOT}/CMakeLists.txt _pv REGEX "set\\(PROJECT_VER")
  string(REGEX REPLACE ".*\"(.*)\".*" "\\1" FWSIM_PROJECT_VER "${_pv}")
endif()
message(STATUS "firmware version ${FWSIM_PROJECT_VER}")

# ---------------------------------------------------------------- LVGL (v9)
file(GLOB_RECURSE LVGL_SRC ${SIM}/deps/lvgl/src/*.c)
add_library(lvgl STATIC ${LVGL_SRC})
set(COMMON_DEFS
  LV_CONF_KCONFIG_EXTERNAL_INCLUDE="sdkconfig.h"
  LV_LVGL_H_INCLUDE_SIMPLE=1
  CONFIG_BOARD_TYPE_CHEEKO=1
  FWSIM=1
)
target_compile_definitions(lvgl PUBLIC ${COMMON_DEFS})
target_include_directories(lvgl PUBLIC
  ${SIM}/config
  ${SIM}/deps/lvgl
  ${SIM}/deps/lvgl/src
)
target_compile_options(lvgl PRIVATE -w -O2)

# ---------------------------------------------------------------- firmware UI
file(GLOB FW_OS_SRC ${FW}/cheeko_os/*.cc)
file(GLOB FW_FONT_SRC ${FW}/display/lvgl_display/fonts/*.c)
file(GLOB FW_IMG_SRC ${FW}/display/lvgl_display/images/*.c)
set(FW_SRC
  ${FW_OS_SRC}
  ${FW_FONT_SRC}
  ${FW_IMG_SRC}
  ${FW}/display/display.cc
  ${FW}/display/lcd_display.cc
  ${FW}/display/cheeko_face.cc
  ${FW}/display/cheeko_character_art.cc
  ${FW}/display/lvgl_display/lvgl_display.cc
  ${FW}/display/lvgl_display/lvgl_theme.cc
  ${FW}/display/lvgl_display/lvgl_font.cc
  ${FW}/display/lvgl_display/lvgl_image.cc
  ${FW}/display/lvgl_display/emoji_collection.cc
  ${FW}/cheeko_companion/cheeko_companion.cc
  ${FW}/boards/cheeko-v2/cheeko_sd_image_loader.cc
  ${FW}/cheeko_boot_mode.cc
  ${FW}/settings.cc
  ${FW}/boards/common/content_crypto.cc
  ${FW_ROOT}/tests/host/mbedtls_stub/mbedtls_stub.cc
)
set(FONTS ${SIM}/deps/xiaozhi-fonts)
set(FONT_SRC
  ${FONTS}/src/font_awesome_14_1.c
  ${FONTS}/src/font_awesome_20_4.c
  ${FONTS}/src/font_awesome_30_1.c
  ${FONTS}/src/font_awesome_30_4.c
  ${FONTS}/src/font_awesome.c
  ${FONTS}/src/font_puhui_basic_14_1.c
  ${FONTS}/src/font_puhui_basic_20_4.c
  ${FONTS}/src/cbin_font.c
)
file(GLOB EMOJI_SRC ${FONTS}/src/emoji/*.c)
list(APPEND FONT_SRC ${EMOJI_SRC})
file(GLOB STUB_SRC ${SIM}/stubs/*.cc ${SIM}/stubs/*.c)

add_executable(fwsim
  ${FW_SRC}
  ${FONT_SRC}
  ${STUB_SRC}
  ${SIM}/deps/cjson/cJSON.c
  ${SIM}/gen/lang_blobs.c
  ${SIM}/gen/haptics_names.cc
  ${SIM}/harness/main.cc
  ${SIM}/harness/board_display.cc
)
target_include_directories(fwsim PRIVATE
  ${SIM}/stubs/include
  ${SIM}/gen
  ${FW}
  ${FW}/display
  ${FW}/display/lvgl_display
  ${FW}/display/lvgl_display/jpg
  ${FW}/audio
  ${FW}/protocols
  ${FW}/cheeko_companion
  ${FW}/cheeko_os
  ${FW}/radio
  ${FW}/boards/common
  ${FW}/boards/cheeko-v2
  ${FONTS}/include
  ${SIM}/deps/cjson
  ${FW_ROOT}/tests/host/mbedtls_stub
)
target_compile_definitions(fwsim PRIVATE
  BUILTIN_TEXT_FONT=font_puhui_basic_14_1
  BUILTIN_ICON_FONT=font_awesome_20_4
  FWSIM_PROJECT_VER="${FWSIM_PROJECT_VER}"
)
target_compile_options(fwsim PRIVATE
  -Wno-everything
  -fno-omit-frame-pointer
  $<$<COMPILE_LANGUAGE:CXX>:-include ${SIM}/stubs/include/fwsim_prelude.h>
)
set_source_files_properties(${SIM}/harness/main.cc PROPERTIES COMPILE_OPTIONS -fno-access-control)
target_link_libraries(fwsim PRIVATE lvgl z)
