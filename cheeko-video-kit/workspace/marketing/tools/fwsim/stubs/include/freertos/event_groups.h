#pragma once
#include "freertos/FreeRTOS.h"
#ifdef __cplusplus
extern "C" {
#endif
EventGroupHandle_t xEventGroupCreate(void);
EventBits_t xEventGroupSetBits(EventGroupHandle_t g, EventBits_t b);
EventBits_t xEventGroupClearBits(EventGroupHandle_t g, EventBits_t b);
EventBits_t xEventGroupGetBits(EventGroupHandle_t g);
EventBits_t xEventGroupWaitBits(EventGroupHandle_t g, EventBits_t b, BaseType_t c, BaseType_t a, TickType_t t);
void vEventGroupDelete(EventGroupHandle_t g);
#ifdef __cplusplus
}
#endif
