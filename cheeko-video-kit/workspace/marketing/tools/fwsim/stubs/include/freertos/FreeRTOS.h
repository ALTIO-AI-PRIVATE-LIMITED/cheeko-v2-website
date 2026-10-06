#pragma once
// Single-threaded host stand-in for FreeRTOS: tasks are recorded but never
// run, locks always succeed, time comes from the simulator clock.
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
typedef uint32_t TickType_t;
typedef int BaseType_t;
typedef unsigned int UBaseType_t;
typedef void *TaskHandle_t;
typedef void *SemaphoreHandle_t;
typedef void *QueueHandle_t;
typedef void *EventGroupHandle_t;
typedef void *TimerHandle_t;
typedef void *RingbufHandle_t;
typedef uint32_t EventBits_t;
typedef uint32_t StackType_t;
typedef struct { int dummy; } StaticTask_t;
typedef struct { int dummy; } StaticSemaphore_t;
typedef struct { int dummy; } StaticQueue_t;
typedef void (*TaskFunction_t)(void *);
typedef struct { unsigned int owner; unsigned int count; } portMUX_TYPE;
#define portMUX_INITIALIZER_UNLOCKED {0, 0}
#define pdTRUE 1
#define pdFALSE 0
#define pdPASS 1
#define pdFAIL 0
#define errQUEUE_EMPTY 0
#define errQUEUE_FULL 0
#define portMAX_DELAY 0xffffffffu
#define portTICK_PERIOD_MS 1
#define configTICK_RATE_HZ 1000
#define configMAX_PRIORITIES 25
#define tskNO_AFFINITY 0x7fffffff
#define tskIDLE_PRIORITY 0
#define pdMS_TO_TICKS(ms) ((TickType_t)(ms))
#define pdTICKS_TO_MS(t) ((uint32_t)(t))
#define portENTER_CRITICAL(m) do { (void)(m); } while (0)
#define portEXIT_CRITICAL(m) do { (void)(m); } while (0)
#define taskENTER_CRITICAL(m) do { (void)(m); } while (0)
#define taskEXIT_CRITICAL(m) do { (void)(m); } while (0)
#define portYIELD_FROM_ISR(...) do {} while (0)
#define configASSERT(x) do { (void)(x); } while (0)
#ifdef __cplusplus
extern "C" {
#endif
TickType_t xTaskGetTickCount(void);
#ifdef __cplusplus
}
#endif
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"
