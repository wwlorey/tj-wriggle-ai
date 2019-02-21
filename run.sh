#!/bin/bash

# Place your compile and execute script here.
# You can write any bash script that will run on campus linux machines.
# The below script will compile and execute the example.cpp program.

# compile the program
g++ -std=c++11 *.cpp -o sample

# Here's a neat loop to iterate through all puzzle files in the local
# directory and make the appropriate solution filenames.
for puzzle in puzzle*.txt; do
	solution="solution"$(echo $puzzle | tr -dc "0-9")".txt"
	./sample $puzzle $solution
done