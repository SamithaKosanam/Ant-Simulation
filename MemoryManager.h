//
// Created by samik on 3/24/2023.
//

#ifndef MEMORYMANAGER_MEMORYMANAGER_H
#define MEMORYMANAGER_MEMORYMANAGER_H


#include <functional>
#include <vector>
#include <cstdlib>
#include <map>


//Memory Allocation Algorithms
int bestFit(int sizeInWords, void *list);
//Returns word offset of hole selected by the best fit memory allocation algorithm, and -1 if there is no fit.

int worstFit(int sizeInWords, void *list);
//Returns word offset of hole selected by the worst fit memory allocation algorithm, and -1 if there is no fit.

class MemoryManager {
private:
    unsigned wordSize;
    std::function<int(int, void*)> allocator;
    size_t totalWords;
    std::map<int,void*> addresses;
    int* sizes = nullptr;
    int* memory = nullptr;
    uint64_t* arr = nullptr;
    uint8_t* b_ret = nullptr;
    short* l_ret = nullptr;

public:
    MemoryManager(unsigned wordSize, std::function<int(int, void *)> allocator);
    //Constructor; sets native word size (in bytes, for alignment) and default allocator for finding a memory hole.

    ~MemoryManager();
    //Releases all memory allocated by this object without leaking memory.

    void initialize(size_t sizeInWords);
    //Instantiates block of requested size, no larger than 65535 words; cleans up previous block if applicable.

    void shutdown();
    //Releases memory block acquired during initialization, if any. This should only include memory created for
    //long term use not those that returned such as getList() or getBitmap() as whatever is calling those should
    //delete it instead.

    void *allocate(size_t sizeInBytes);
    //Allocates a memory using the allocator function. If no memory is available or size is invalid, returns nullptr.

    void free(void *address);
    //Frees the memory block within the memory manager so that it can be reused.

    void setAllocator(std::function<int(int, void *)> allocator);
    //Changes the allocation algorithm to identifying the memory hole to use for allocation.

    int dumpMemoryMap(char *filename);
    //Uses standard POSIX calls to write hole list to filename as text, returning -1 on error and 0 if successful.
    //Format: "[START, LENGTH] - [START, LENGTH] …", e.g., "[0, 10] - [12, 2] - [20, 6]"

    void *getList();
    /*Returns an array of information (in decimal) about holes for use by the allocator function (little-Endian).
    Offset and length are in words. If no memory has been allocated, the function should return a NULL pointer.
    Format: Example: [3, 0, 10, 12, 2, 20, 6]*/

    void *getBitmap();
    /*Returns a bit-stream of bits in terms of an array representing whether words are used (1) or free (0). The
        first two bytes are the size of the bitmap (little-Endian); the rest is the bitmap, word-wise.
    Note : In the following example B0, B2, and B4 are holes, B1 and B3 are allocated memory.
              Hole-0 Hole-1 Hole-2 ┌─B4─┐    ┌ B2┐    ┌───B0 ──┐  ┌─Size (4)─┐┌This is Bitmap in Hex┐
    Example: [0,10]-[12,2]-[20,6] [00 00001111 11001100 00000000] [0x04,0x00,0x00,0xCC,0x0F,0x00]
                                        ┕─B3─┙    ┕B1┙
    Returned Array: [0x04,0x00,0x00,0xCC,0x0F,0x00] or [4,0,0,204,15,0]
     Read LEFTMOST TO RIGHTMOST BLOCK, IN DECIMAL FORM*/

    unsigned getWordSize();
    //Returns the word size used for alignment.

    void *getMemoryStart();
    //Returns the byte-wise memory address of the beginning of the memory block.

    unsigned getMemoryLimit();
    //Returns the byte limit of the current memory block.
    //Note: The following two functions should not be part of the Memory Manager Class.
};


//#include "MemoryManager.cpp"

#endif //MEMORYMANAGER_MEMORYMANAGER_H
