CC = g++ -lpthread -std=c++11 --no_warnings

all: main.o FileReader.o
    $(CC) main.o FileReader.o -lpthread -o readFile -g

main.o: main.cpp
    $(CC) main.cpp -c -g

FileReader.o: FileReader.cpp FileReader.h
    $(CC) FileReader.cpp -c -g