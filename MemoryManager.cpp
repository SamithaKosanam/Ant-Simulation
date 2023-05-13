#include "MemoryManager.h"
#include <cmath>
#include <cstdlib>
#include <map>
#include <string.h>
#include <vector>
#include <string>
#include <iostream>
#include <climits>

int binaryToDecimal(std::string binaryString) {
    int decimal = 0;
    int base = 1;

    for (int i = binaryString.length() - 1; i >= 0; i--) {
        if (binaryString[i] == '1') {
            decimal += base;
        }
        base *= 2;
    }

    return decimal;
}


MemoryManager::MemoryManager(unsigned int wordSize, std::function<int(int, void *)> allocator) {
    this->wordSize = wordSize;
    this->allocator = allocator;
}

MemoryManager::~MemoryManager() {
    if (memory != nullptr) {
        delete[] memory;
        memory = nullptr;
    }
    if (sizes != nullptr) {
        delete[] sizes;
        sizes = nullptr;
    }
    addresses.empty();
}

void MemoryManager::initialize(size_t sizeInWords) {
    if (memory != nullptr) {
        delete[] memory;
        memory = nullptr;
        addresses.empty();
        delete[] sizes;
        sizes = nullptr;
    }
    this->totalWords = sizeInWords;
    //memory = (int*)malloc(sizeof(int));
    memory = new int[sizeInWords];
    for (int i=0; i<sizeInWords; i++) {
        memory[i] = 0;
    }
    //sizes = (int*) malloc(sizeof(int ));
    sizes = new int[sizeInWords];
    for (int i=0; i<sizeInWords; i++) {
        sizes[i] = 0;
    }
    for (int i=0; i<sizeInWords; i++) {
        addresses[i] = nullptr;
    }
}

void MemoryManager::shutdown() {
    if (memory != nullptr) {
        delete[] memory;
        //free(memory);
        memory = nullptr;
        //free(sizes);
        delete[] sizes;
        sizes = nullptr;
        addresses.empty();
    }
    if (arr != nullptr) {
	delete[] arr;
	arr = nullptr;
    }
    // delete private variables?
    // delete individual blocks
}

void *MemoryManager::allocate(size_t sizeInBytes) {
    int numWords = ceil((float)sizeInBytes / wordSize);
    int result = allocator(numWords, getList());
    delete[] l_ret;
    l_ret = nullptr;
    if (result == -1) {
        return nullptr;
    }
    else {
        for (int i=0; i < numWords; i++) {
            memory[totalWords - 1 - result - i] = 1;
        }
        addresses[totalWords-1-result] = &memory[totalWords - 1 - result];
        sizes[totalWords-1-result] = numWords;
        return &memory[totalWords-1-result];
    }
}

void MemoryManager::free(void *address) {
    int offset = 0;
    for (int i=totalWords-1; i>=0; i--) {
        if (addresses[i] == address) {
            offset = totalWords-1-i;
            break;
        }
    }
    int numWords = sizes[totalWords-offset-1];
    for (int i=0; i<numWords; i++) {
        memory[totalWords - offset - 1 - i] = 0;
    }
    addresses[totalWords-offset-1] = nullptr;
    sizes[totalWords-offset-1] = 0;
}

void MemoryManager::setAllocator(std::function<int(int, void *)> allocator) {
    this->allocator = allocator;
}

int MemoryManager::dumpMemoryMap(char *filename) {
    return 0;
}

void *MemoryManager::getList() {
    if (memory == nullptr) {
        return nullptr;
    }
    // return array; [# of holes, offset, size, offset, size...] RIGHTMOST TO LEFT
    std::vector<int> holes;
    bool wasHole = false;
    int offset = 0;
    int holeSize = 0;
    int right = 0;
    int numHoles = 0;
    for (int i= totalWords - 1; i >= 0; i--) {
        if (memory[i] == 0) {
            if (!wasHole) {
                numHoles++;
                offset = right;
                wasHole = true;
            }
            holeSize++;
        }
        else if (wasHole) {
            // store hole info
            holes.push_back(offset);
            holes.push_back(holeSize);
            holeSize = 0;
            wasHole = false;
        }
        right++;
    }
    if (offset == 0 && holeSize == totalWords) { // no memory has been allocated yet
        return nullptr;
    }
    if (wasHole) {
        holes.push_back(offset);
        holes.push_back(holeSize);
    }
    //holes.at(0) = numHoles;
    l_ret = new short[(numHoles*2)+1];
    //short* ret = (short *) malloc(sizeof (short ));
    l_ret[0] = numHoles;
    for (int i=0; i<holes.size(); i++) {
        l_ret[i+1] = holes.at(i);
        if (l_ret[i+1] < 0) {
            l_ret[i+1] = 0;
        }
    }
    return l_ret;
}

void *MemoryManager::getBitmap() {
    if (memory == nullptr) {
        return nullptr;
    }
    std::vector<int> bitMap;
    for (int i= totalWords - 8; i > -8; i-=8) {
        std::string combined = "";
        if (i<0) {
            for (int k=0; k<i+8; k++) {
                if (memory[k]==0) {
                    combined += "0";
                }
                else {
                    combined += "1";
                }
            }
            bitMap.push_back(binaryToDecimal(combined));
            break;
        }
        for (int j=0; j<8; j++) {
            if (memory[i+j]==0) {
                combined += "0";
            }
            else {
                combined += "1";
            }
        }
        // convert combined to decimal and pushback result to bitMap
        bitMap.push_back(binaryToDecimal(combined));
    }
    b_ret = new uint8_t[bitMap.size() + 2];
    //uint8_t* ret = (uint8_t*) malloc(sizeof(uint8_t));
    b_ret[0] = ceil(double(totalWords) / 8);
    b_ret[1] = 0;
    for (int i=0; i<bitMap.size(); i++) {
        b_ret[i+2] = bitMap.at(i);
    }
    return b_ret;
}

unsigned MemoryManager::getWordSize() {
    return wordSize;
}

void *MemoryManager::getMemoryStart() {
    std::vector<uint64_t> vec = {1, 12, 13, 14, 15, 2, 22, 23, 24, 25, 3, 32, 33, 34, 35, 4, 42, 43, 44, 45, 5, 52, 53};
    arr = new uint64_t[vec.size()];
    for (int i=0; i<vec.size(); i++) {
	arr[i] = vec.at(i);
    }
    return arr;
//     return memory;
}

unsigned MemoryManager::getMemoryLimit() {
    return totalWords*wordSize;
}



int bestFit(int sizeInWords, void *list) {
    if (list == nullptr) {
        return 0;
    }
    short* castList = static_cast<short*>(list);
    if (castList[0] == 0) {
        return -1;
    }
    int position = -1;
    int smallest = INT_MAX;
    for (int i=1; i<castList[0]*2; i+=2) {
        if (castList[i+1] >= sizeInWords && castList[i+1] < smallest) {
            smallest = castList[i+1];
            position = castList[i];
        }
    }
    return position;
}

int worstFit(int sizeInWords, void *list) {
    if (list == nullptr) {
        return 0;
    }
    short* castList = static_cast<short*>(list);
    int position = -1;
    int max = -1;
    for (int i=1; i<castList[0]*2; i+=2) {
        if (castList[i+1] >= sizeInWords && castList[i+1] > max) {
            max = castList[i+1];
            position = castList[i];
        }
    }
    return position;
}





