import numpy as np
import sys
from collections import defaultdict

def check_duplicates(array):
    flat_array = array.flatten()
    element_indices = defaultdict(list)
    duplicates = {}

    for idx, value in enumerate(flat_array):
        element_indices[value].append(idx)
    
    for value, indices in element_indices.items():
        if len(indices) > 1:
            duplicates[value] = indices
    
    if duplicates:
        print("Array contains duplicates:")
        for value, indices in duplicates.items():
            print(f"Value {value} is duplicated at indices: {indices}")
    else:
        print("Array has no duplicates.")

input_string = sys.stdin.read()

lines = input_string.strip().splitlines()
array = []

for line in lines:
    if "[" in line:
        line = line.replace("[", "").replace("]", "")
        if line.strip():
            numbers = list(map(int, line.split()))
            array.append(numbers)

array = np.array(array)

check_duplicates(array)