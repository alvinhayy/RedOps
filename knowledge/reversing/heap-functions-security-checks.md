---
title: "Heap Functions Security Checks"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/binary-exploitation/libc-heap/heap-memory-functions/heap-functions-security-checks.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: reversing
---

## unlink

For more info check:

This is a summary of the performed checks:

- Check if the indicated size of the chunk is the same as the `prev_size` indicated in the next chunk
  - Error message: `corrupted size vs. prev_size`
- Error message:
- Check also that `P->fd->bk == P` and`P->bk->fd == P`  - Error message: `corrupted double-linked list`
- Error message:
- If the chunk is not small, check that `P->fd_nextsize->bk_nextsize == P` and`P->bk_nextsize->fd_nextsize == P`  - Error message: `corrupted double-linked list (not small)`
- Error message:

## _int_malloc

For more info check:

- **Checks during fast bin search:**  - If the chunk is misaligned:
    - Error message: `malloc(): unaligned fastbin chunk detected 2`
  - Error message:
  - If the forward chunk is misaligned:
    - Error message: `malloc(): unaligned fastbin chunk detected`
  - Error message:
  - If the returned chunk has a size that isn’t correct because of it’s index in the fast bin:
    - Error message: `malloc(): memory corruption (fast)`
  - Error message:
  - If any chunk used to fill the tcache is misaligned:
    - Error message: `malloc(): unaligned fastbin chunk detected 3`
  - Error message:
- If the chunk is misaligned:
- **Checks during small bin search:**  - If `victim->bk->fd != victim` :
    - Error message: `malloc(): smallbin double linked list corrupted`
  - Error message:
- If
- **Checks during consolidate** performed for each fast bin chunk:
  - If the chunk is unaligned trigger:
    - Error message: `malloc_consolidate(): unaligned fastbin chunk detected`
  - Error message:
  - If the chunk has a different size that the one it should because of the index it’s in:
    - Error message: `malloc_consolidate(): invalid chunk size`
  - Error message:
  - If the previous chunk is not in use and the previous chunk has a size different of the one indicated by prev_chunk:
    - Error message: `corrupted size vs. prev_size in fastbins`
  - Error message:
- If the chunk is unaligned trigger:
- **Checks during unsorted bin search** :
  - If the chunk size is weird (too small or too big):
    - Error message: `malloc(): invalid size (unsorted)`
  - Error message:
  - If the next chunk size is weird (too small or too big):
    - Error message: `malloc(): invalid next size (unsorted)`
  - Error message:
  - If the previous size indicated by the next chunk differs from the size of the chunk:
    - Error message: `malloc(): mismatching next->prev_size (unsorted)`
  - Error message:
  - If not `victim->bck->fd == victim` or not`victim->fd == av (arena)` :
    - Error message: `malloc(): unsorted double linked list corrupted`
    - As we are always checking the las one, it’s fd should be pointing always to the arena struct.
  - Error message:
  - If the next chunk isn’t indicating that the previous is in use:
    - Error message: `malloc(): invalid next->prev_inuse (unsorted)`
  - Error message:
  - If `fwd->bk_nextsize->fd_nextsize != fwd` :
    - Error message: `malloc(): largebin double linked list corrupted (nextsize)`
  - Error message:
  - If `fwd->bk->fd != fwd` :
    - Error message: `malloc(): largebin double linked list corrupted (bk)`
  - Error message:
- If the chunk size is weird (too small or too big):
- **Checks during large bin (by index) search:**  - `bck->fd-> bk != bck` :
    - Error message: `malloc(): corrupted unsorted chunks`
  - Error message:
- **Checks during large bin (next bigger) search:**  - `bck->fd-> bk != bck` :
    - Error message: `malloc(): corrupted unsorted chunks2`
  - Error message:
- **Checks during Top chunk use:**  - `chunksize(av->top) > av->system_mem` :
    - Error message: `malloc(): corrupted top size`
  - Error message:

## `tcache_get_n`

`tcache_get_n`
- **Checks in `tcache_get_n`:**  - If chunk is misaligned:
    - Error message: `malloc(): unaligned tcache chunk detected`
  - Error message:
- If chunk is misaligned:

## `tcache_thread_shutdown`

`tcache_thread_shutdown`
- **Checks in `tcache_thread_shutdown`:**  - If chunk is misaligned:
    - Error message: `tcache_thread_shutdown(): unaligned tcache chunk detected`
  - Error message:
- If chunk is misaligned:

## `__libc_realloc`

`__libc_realloc`
- **Checks in `__libc_realloc`:**  - If old pointer is misaligned or the size was incorrect:
    - Error message: `realloc(): invalid pointer`
  - Error message:
- If old pointer is misaligned or the size was incorrect:

## `_int_free`

`_int_free`
For more info check:

- **Checks during the start of `_int_free`:**  - Pointer is aligned:
    - Error message: `free(): invalid pointer`
  - Error message:
  - Size larger than `MINSIZE` and size also aligned:
    - Error message: `free(): invalid size`
  - Error message:
- Pointer is aligned:
- **Checks in `_int_free` tcache:**  - If there are more entries than `mp_.tcache_count` :
    - Error message: `free(): too many chunks detected in tcache`
  - Error message:
  - If the entry is not aligned:
    - Error message: `free(): unaligned chunk detected in tcache 2`
  - Error message:
  - If the freed chunk was already freed and is present as chunk in the tcache:
    - Error message: `free(): double free detected in tcache 2`
  - Error message:
- If there are more entries than
- **Checks in `_int_free` fast bin:**  - If the size of the chunk is invalid (too big or small) trigger:
    - Error message: `free(): invalid next size (fast)`
  - Error message:
  - If the added chunk was already the top of the fast bin:
    - Error message: `double free or corruption (fasttop)`
  - Error message:
  - If the size of the chunk at the top has a different size of the chunk we are adding:
    - Error message: `invalid fastbin entry (free)`
  - Error message:
- If the size of the chunk is invalid (too big or small) trigger:

## **`_int_free_merge_chunk`**

`_int_free_merge_chunk`
- **Checks in `_int_free_merge_chunk`:**  - If the chunk is the top chunk:
    - Error message: `double free or corruption (top)`
  - Error message:
  - If the next chunk is outside of the boundaries of the arena:
    - Error message: `double free or corruption (out)`
  - Error message:
  - If the chunk is not marked as used (in the prev_inuse from the following chunk):
    - Error message: `double free or corruption (!prev)`
  - Error message:
  - If the next chunk has a too little size or too big:
    - Error message: `free(): invalid next size (normal)`
  - Error message:
  - If the previous chunk is not in use, it will try to consolidate. But, if the `prev_size` differs from the size indicated in the previous chunk:
    - Error message: `corrupted size vs. prev_size while consolidating`
  - Error message:
- If the chunk is the top chunk:

## **`_int_free_create_chunk`**

`_int_free_create_chunk`
- **Checks in `_int_free_create_chunk`:**  - Adding a chunk into the unsorted bin, check if `unsorted_chunks(av)->fd->bk == unsorted_chunks(av)` :
    - Error message: `free(): corrupted unsorted chunks`
  - Error message:
- Adding a chunk into the unsorted bin, check if

## `do_check_malloc_state`

`do_check_malloc_state`
- **Checks in `do_check_malloc_state`:**  - If misaligned fast bin chunk:
    - Error message: `do_check_malloc_state(): unaligned fastbin chunk detected`
  - Error message:
- If misaligned fast bin chunk:

## `malloc_consolidate`

`malloc_consolidate`
- **Checks in `malloc_consolidate`:**  - If misaligned fast bin chunk:
    - Error message: `malloc_consolidate(): unaligned fastbin chunk detected`
  - Error message:
  - If incorrect fast bin chunk size:
    - Error message: `malloc_consolidate(): invalid chunk size`
  - Error message:
- If misaligned fast bin chunk:

## `_int_realloc`

`_int_realloc`
- **Checks in `_int_realloc`:**  - Size is too big or too small:
    - Error message: `realloc(): invalid old size`
  - Error message:
  - Size of the next chunk is too big or too small:
    - Error message: `realloc(): invalid next size`
  - Error message:
- Size is too big or too small:

## References
