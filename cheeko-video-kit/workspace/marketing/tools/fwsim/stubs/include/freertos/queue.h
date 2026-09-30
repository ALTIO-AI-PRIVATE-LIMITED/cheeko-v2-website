#pragma once
#include "freertos/FreeRTOS.h"
#ifdef __cplusplus
extern "C" {
#endif
QueueHandle_t xQueueCreate(UBaseType_t len, UBaseType_t item);
BaseType_t xQueueSend(QueueHandle_t q, const void *item, TickType_t t);
BaseType_t xQueueSendToBack(QueueHandle_t q, const void *item, TickType_t t);
BaseType_t xQueueSendFromISR(QueueHandle_t q, const void *item, BaseType_t *w);
BaseType_t xQueueOverwrite(QueueHandle_t q, const void *item);
BaseType_t xQueueReceive(QueueHandle_t q, void *item, TickType_t t);
BaseType_t xQueueReset(QueueHandle_t q);
UBaseType_t uxQueueMessagesWaiting(QueueHandle_t q);
void vQueueDelete(QueueHandle_t q);
#ifdef __cplusplus
}
#endif
