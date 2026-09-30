#pragma once
#include "freertos/FreeRTOS.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef enum { eRunning, eReady, eBlocked, eSuspended, eDeleted, eInvalid } eTaskState;
typedef enum { eNoAction, eSetBits, eIncrement, eSetValueWithOverwrite, eSetValueWithoutOverwrite } eNotifyAction;
BaseType_t xTaskCreate(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h);
BaseType_t xTaskCreatePinnedToCore(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, BaseType_t c);
BaseType_t xTaskCreateWithCaps(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, uint32_t caps);
BaseType_t xTaskCreatePinnedToCoreWithCaps(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, TaskHandle_t *h, BaseType_t c, uint32_t caps);
TaskHandle_t xTaskCreateStatic(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, StackType_t *st, StaticTask_t *tb);
TaskHandle_t xTaskCreateStaticPinnedToCore(TaskFunction_t f, const char *n, uint32_t s, void *a, UBaseType_t p, StackType_t *st, StaticTask_t *tb, BaseType_t c);
void vTaskDelete(TaskHandle_t h);
void vTaskDeleteWithCaps(TaskHandle_t h);
void vTaskDelay(TickType_t t);
void vTaskSuspend(TaskHandle_t h);
void vTaskResume(TaskHandle_t h);
TaskHandle_t xTaskGetCurrentTaskHandle(void);
UBaseType_t uxTaskGetStackHighWaterMark(TaskHandle_t h);
UBaseType_t uxTaskPriorityGet(TaskHandle_t h);
void vTaskPrioritySet(TaskHandle_t h, UBaseType_t p);
eTaskState eTaskGetState(TaskHandle_t h);
const char *pcTaskGetName(TaskHandle_t h);
BaseType_t xTaskNotifyGive(TaskHandle_t h);
uint32_t ulTaskNotifyTake(BaseType_t clear, TickType_t t);
BaseType_t xTaskNotify(TaskHandle_t h, uint32_t v, eNotifyAction a);
BaseType_t xTaskNotifyWait(uint32_t a, uint32_t b, uint32_t *v, TickType_t t);
void vTaskList(char *buf);
UBaseType_t uxTaskGetNumberOfTasks(void);
#ifdef __cplusplus
}
#endif
