#!/bin/bash

for puzzle in puzzle*.txt; do
	solution="solution"$(echo $puzzle | tr -dc "0-9")".txt"
	python3 main.py $puzzle $solution
done