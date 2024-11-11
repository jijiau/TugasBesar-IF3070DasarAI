import random
import numpy as np
import matplotlib.pyplot as plt

class CubeSolver:
    MAGIC_CONSTANT = 315

    def __init__(self, state=None):
        if state is None:
            self.state = self.generate_random_initial_state()
        else:
            self.state = state

    def calculate_objective(self, state):
        objective = 0
        for layer in range(5):
            for row in range(5):
                row_sum = sum(state[layer * 25 + row * 5 + col] for col in range(5))
                objective += abs(row_sum - self.MAGIC_CONSTANT)

        for layer in range(5):
            for col in range(5):
                col_sum = sum(state[layer * 25 + row * 5 + col] for row in range(5))
                objective += abs(col_sum - self.MAGIC_CONSTANT)

        for row in range(5):
            for col in range(5):
                pillar_sum = sum(state[layer * 25 + row * 5 + col] for layer in range(5))
                objective += abs(pillar_sum - self.MAGIC_CONSTANT)

        for layer in range(5):
            diag1_sum = sum(state[layer * 25 + i * 6] for i in range(5))
            diag2_sum = sum(state[layer * 25 + (i + 1) * 4] for i in range(5))
            objective += abs(diag1_sum - self.MAGIC_CONSTANT)
            objective += abs(diag2_sum - self.MAGIC_CONSTANT)

        for col in range(5):
            diag3_sum = sum(state[layer * 25 + layer * 5 + col] for layer in range(5))
            diag4_sum = sum(state[layer * 25 + (4 - layer) * 5 + col] for layer in range(5))
            objective += abs(diag3_sum - self.MAGIC_CONSTANT)
            objective += abs(diag4_sum - self.MAGIC_CONSTANT)

        for row in range(5):
            diag5_sum = sum(state[layer * 25 + row * 5 + layer] for layer in range(5))
            diag6_sum = sum(state[layer * 25 + row * 5 + (4 - layer)] for layer in range(5))
            objective += abs(diag5_sum - self.MAGIC_CONSTANT)
            objective += abs(diag6_sum - self.MAGIC_CONSTANT)

        triagonal_indices = [
            [i * 31 for i in range(5)],
            [4, 33, 62, 91, 120],
            [20, 41, 62, 83, 104],
            [100, 81, 62, 43, 24]
        ]

        for indices in triagonal_indices:
            triagonal_sum = sum(state[idx] for idx in indices)
            objective += abs(triagonal_sum - self.MAGIC_CONSTANT)

        return objective

    def generate_random_initial_state(self):
        state = list(range(1, 126))
        random.shuffle(state)
        return state

    def visualize_state(self, state, axes=None):
        layers = self.format_state_as_layers(state)
        
        if axes is None:
            fig, axes = plt.subplots(1, 5, figsize=(15, 3))
        
        for i, layer in enumerate(layers):
            ax = axes[i]
            ax.matshow(layer, cmap='gray', vmin=0, vmax=1)
            for (row, col), val in np.ndenumerate(layer):
                ax.text(col, row, f'{val}', va='center', ha='center', color='black', fontsize=6)
            ax.set_title(f'Layer {i + 1}', fontsize=8)
            ax.axis('off')
        
        if axes is None:
            plt.suptitle('5x5x5 Cube Visualization')
            plt.show()

    def format_state_as_layers(self, state):
        """
        Converts a 125-element state list into five 5x5 layers for display.
        """
        return [np.array(state[i * 25:(i + 1) * 25]).reshape(5, 5) for i in range(5)]

    def display_formatted_state(self, state):
        """
        Prints the cube's state in a 5x5 layer format.
        """
        layers = self.format_state_as_layers(state)
        for i, layer in enumerate(layers):
            print(f"Layer {i+1}:\n{layer}\n")

    def generate_test_state_1(self):
        """
        Returns a fixed cube state with a specific order.
        """
        # Example state 1: Sequential order for testing
        return list(range(1, 126))

    def generate_test_state_2(self):
        """
        Returns a fixed cube state with a reversed order.
        """
        # Example state 2: Reversed order for testing
        return list(range(125, 0, -1))

    def generate_test_state_3(self):
        """
        Returns a fixed cube state with a shuffled but specific known order.
        """
        # Example state 3: A predetermined shuffled order for consistent testing
        return [1, 5, 3, 2, 4, 10, 6, 8, 7, 9, 15, 11, 13, 12, 14, 
                20, 16, 18, 17, 19, 25, 21, 23, 22, 24, 30, 26, 28, 
                27, 29, 35, 31, 33, 32, 34, 40, 36, 38, 37, 39, 45, 
                41, 43, 42, 44, 50, 46, 48, 47, 49, 55, 51, 53, 52, 
                54, 60, 56, 58, 57, 59, 65, 61, 63, 62, 64, 70, 66, 
                68, 67, 69, 75, 71, 73, 72, 74, 80, 76, 78, 77, 79, 
                85, 81, 83, 82, 84, 90, 86, 88, 87, 89, 95, 91, 93, 
                92, 94, 100, 96, 98, 97, 99, 105, 101, 103, 102, 104, 
                110, 106, 108, 107, 109, 115, 111, 113, 112, 114, 120, 
                116, 118, 117, 119, 125, 121, 123, 122, 124]




