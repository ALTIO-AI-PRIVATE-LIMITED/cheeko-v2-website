#pragma once
#include "freertos/FreeRTOS.h"
#ifdef __cplusplus
extern "C" {
#endif
SemaphoreHandle_t xSemaphoreCreateMutex(void);
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex(void);
SemaphoreHandle_t xSemaphoreCreateBinary(void);
SemaphoreHandle_t xSemaphoreCreateCounting(UBaseType_t m, UBaseType_t i);
SemaphoreHandle_t xSemaphoreCreateMutexStatic(StaticSemaphore_t *b);
SemaphoreHandle_t xSemaphoreCreateBinaryStatic(StaticSemaphore_t *b);
BaseType_t xSemaphoreTake(SemaphoreHandle_t s, TickType_t t);
BaseType_t xSemaphoreGive(SemaphoreHandle_t s);
BaseType_t xSemaphoreTakeRecursive(SemaphoreHandle_t s, TickType_t t);
BaseType_t xSemaphoreGiveRecursive(SemaphoreHandle_t s);
BaseType_t xSemaphoreGiveFromISR(SemaphoreHandle_t s, BaseType_t *w);
void vSemaphoreDelete(SemaphoreHandle_t s);
UBaseType_t uxSemaphoreGetCount(SemaphoreHandle_t s);
#ifdef __cplusplus
}
#endif
