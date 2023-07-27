#include <stdio.h>
#include <assert.h>
#include <stdbool.h>
#define HEAP_CAP 640000
#define HEAP_ALLOCED_CAP 1024
#define HEAP_FREED_CAP 1024

typedef struct {
    void* start;
    size_t size;
} Chunk;

typedef struct {
    size_t count;
    Chunk chunks[HEAP_ALLOCED_CAP]; 
} Chunk_List;

// int chunck_list_find(const Chunk_List* list, void* ptr)
// {
//     "TODO"
//     return -1;
// }

// void chunk_list_remove(Chunk_List* list, size_t index)
// {
//     "TODO"
//     return -1;
// }

// void chunk_list_remove(Chunk_List* list, void* ptr, size_t size)
// {
//     "TODO"
//     return -1;
// }


char heap[HEAP_CAP] = {0};
Chunk_List alloced_chunks = {0};
Chunk_List freed_chunks = {0};

size_t heap_size = 0;
size_t heap_alloced_size = 0;  
size_t heap_freed_size = 0;


void* heap_alloc(size_t size) 
{
    if (size > 0) 
    {
        assert(heap_size + size <= HEAP_CAP);
        void* result = heap + heap_size;
        heap_size += size;

        const Heap_Chunk chunk = {
            .start = result,
            .size = size,
        };
        assert(heap_alloced_size < HEAP_ALLOCED_CAP);
        heap_alloced[heap_alloced_size++] = chunk;

        return result;
    }
    else {
        return NULL;
    }
    
}

void heap_dump_alloced_chunks(void)
{
    printf("Allocated Chunks:(%zu)\n", heap_alloced_size);
    for (size_t i = 0; i < heap_alloced_size; ++i)
    {
        printf("  start: %p, size: %zu\n", 
            heap_alloced[i].start, 
            heap_alloced[i].size);
    }
}

void heap_free(void* ptr)
{
    for (size_t i = 0; i < heap_alloced_size; i++)
    {
        if (heap_alloced[i].start == ptr)
        {

        } 
    }

}

// void heap_collect() 
// {

// }

int main()
{
    // char* root = heap_alloc(26);
    // for (int i = 0; i < 26; ++i)
    // {
    //     root[i] = i;
    // }
    // for (int i = 0; i < 26; ++i)
    // {
    //     printf("%d\n", root[i]);
    // }
    for (int i = 0; i < 10; i++)
    {
        heap_alloc(i);
    }
    heap_dump_alloced_chunks();
    return 0;
}
