#pragma once
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#define MALLOC_CAP_EXEC (1 << 0)
#define MALLOC_CAP_32BIT (1 << 1)
#define MALLOC_CAP_8BIT (1 << 2)
#define MALLOC_CAP_DMA (1 << 3)
#define MALLOC_CAP_SPIRAM (1 << 10)
#define MALLOC_CAP_INTERNAL (1 << 11)
#define MALLOC_CAP_DEFAULT (1 << 12)
#define MALLOC_CAP_IRAM_8BIT (1 << 13)
#define MALLOC_CAP_RETENTION (1 << 14)
#define MALLOC_CAP_RTCRAM (1 << 15)
typedef struct { size_t total_free_bytes, total_allocated_bytes, largest_free_block, minimum_free_bytes, allocated_blocks, free_blocks, total_blocks; } multi_heap_info_t;
#ifdef __cplusplus
extern "C" {
#endif
static inline void *heap_caps_malloc(size_t s, uint32_t c) { (void)c; return malloc(s); }
static inline void *heap_caps_calloc(size_t n, size_t s, uint32_t c) { (void)c; return calloc(n, s); }
static inline void *heap_caps_realloc(void *p, size_t s, uint32_t c) { (void)c; return realloc(p, s); }
static inline void *heap_caps_aligned_alloc(size_t a, size_t s, uint32_t c) { (void)c; void *p = NULL; if (a < sizeof(void*)) a = sizeof(void*); posix_memalign(&p, a, s ? s : 1); return p; }
static inline void *heap_caps_aligned_calloc(size_t a, size_t n, size_t s, uint32_t c) { void *p = heap_caps_aligned_alloc(a, n * s, c); if (p) { unsigned char *q = (unsigned char *)p; for (size_t i = 0; i < n * s; ++i) q[i] = 0; } return p; }
static inline void heap_caps_free(void *p) { free(p); }
static inline void heap_caps_aligned_free(void *p) { free(p); }
static inline size_t heap_caps_get_free_size(uint32_t c) { return (c & MALLOC_CAP_SPIRAM) ? 6u * 1024 * 1024 : 120u * 1024; }
static inline size_t heap_caps_get_total_size(uint32_t c) { return (c & MALLOC_CAP_SPIRAM) ? 8u * 1024 * 1024 : 320u * 1024; }
static inline size_t heap_caps_get_largest_free_block(uint32_t c) { return (c & MALLOC_CAP_SPIRAM) ? 4u * 1024 * 1024 : 64u * 1024; }
static inline size_t heap_caps_get_minimum_free_size(uint32_t c) { return heap_caps_get_free_size(c); }
static inline void heap_caps_get_info(multi_heap_info_t *i, uint32_t c) { i->total_free_bytes = heap_caps_get_free_size(c); i->largest_free_block = heap_caps_get_largest_free_block(c); i->minimum_free_bytes = i->total_free_bytes; i->total_allocated_bytes = 0; i->allocated_blocks = i->free_blocks = i->total_blocks = 0; }
static inline int heap_caps_check_integrity_all(int p) { (void)p; return 1; }
static inline size_t esp_get_free_internal_heap_size(void) { return 120u * 1024; }
#ifdef __cplusplus
}
#endif
