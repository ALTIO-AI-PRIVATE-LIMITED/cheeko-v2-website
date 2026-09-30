#pragma once
#include "freertos/FreeRTOS.h"
typedef enum { RINGBUF_TYPE_NOSPLIT, RINGBUF_TYPE_ALLOWSPLIT, RINGBUF_TYPE_BYTEBUF } RingbufferType_t;
#ifdef __cplusplus
extern "C" {
#endif
RingbufHandle_t xRingbufferCreate(size_t s, RingbufferType_t t);
RingbufHandle_t xRingbufferCreateWithCaps(size_t s, RingbufferType_t t, uint32_t caps);
void vRingbufferDelete(RingbufHandle_t r);
void vRingbufferDeleteWithCaps(RingbufHandle_t r);
BaseType_t xRingbufferSend(RingbufHandle_t r, const void *d, size_t n, TickType_t t);
void *xRingbufferReceive(RingbufHandle_t r, size_t *n, TickType_t t);
void *xRingbufferReceiveUpTo(RingbufHandle_t r, size_t *n, TickType_t t, size_t m);
void vRingbufferReturnItem(RingbufHandle_t r, void *i);
size_t xRingbufferGetCurFreeSize(RingbufHandle_t r);
#ifdef __cplusplus
}
#endif
