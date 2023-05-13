libMemoryManager.a: MemoryManager.cpp MemoryManager.h
	g++ -c MemoryManager.cpp
	ar cr libMemoryManager.a MemoryManager.o
