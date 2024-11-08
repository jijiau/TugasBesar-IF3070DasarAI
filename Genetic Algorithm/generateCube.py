import numpy as np
import random

# Generate a list of unique random numbers from 1 to 125
numbers = random.sample(range(1, 126), 125)

# Reshape the list into a 5x5x5 cube
cube_5x5x5 = np.array(numbers).reshape((5, 5, 5))

# Print the cube
print(cube_5x5x5)
