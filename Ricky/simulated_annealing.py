from datetime import datetime
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from base_solver import CubeSolver

class SimulatedAnnealingSolver(CubeSolver):
    def __init__(self, state=None):
        super().__init__(state)

    def generate_random_neighbor(self, state):
        neighbor = state.copy()
        i, j = random.sample(range(len(state)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

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

    def simulated_annealing(self, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
        current_state = self.state
        initial_state = current_state.copy()
        current_value = self.calculate_objective(current_state)
        best_state = current_state
        best_value = current_value
        temperature = initial_temp
        iteration = 0
        iterations = []
        exp_values = []
        objective_values = []
        stuck_count = 0

        start_time = datetime.now()

        plt.ion()  
        fig = plt.figure(figsize=(14,14))
        gs = fig.add_gridspec(nrows=5, ncols=1, height_ratios=[2,0.5,2,0.5,2])
        ax = fig.add_subplot(gs[0])
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Objective Value')
        ax.set_title('Simulated Annealing Objective Value over Iterations')

        ax2 = fig.add_subplot(gs[2])
        ax2.margins(0.3)
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('e^(ΔE/T)')
        ax2.set_title('Exponential Acceptance Probability over Iterations')
        
        gs2 = gs[4].subgridspec(1, 5)
        cube_axes = [fig.add_subplot(gs2[0, i]) for i in range(5)]

        self.visualize_state(current_state, axes=cube_axes)
        plt.pause(0.1)

        while temperature > min_temp:
            iterations.append(iteration)
            objective_values.append(current_value)
            
            ax.plot(iterations, objective_values, color='red')
            for ax1 in cube_axes:
                ax1.clear()
            self.visualize_state(current_state, axes=cube_axes)
            plt.pause(0.1)
            
            neighbor = self.generate_random_neighbor(current_state)
            neighbor_value = self.calculate_objective(neighbor)
            
            delta_e = neighbor_value - current_value

            if delta_e < 0: 
                capped_delta_e_over_temp = (delta_e / temperature)
                exp_value = math.exp(capped_delta_e_over_temp)
                exp_values.append(exp_value)
            else:
                exp_values.append(None)  
            
            valid_exp_values = [v for v in exp_values if v is not None]
            valid_iterations = [iterations[i] for i, v in enumerate(exp_values) if v is not None]
            ax2.plot(valid_iterations, valid_exp_values, color='blue')
            if delta_e >= 0 or exp_value > random.random():
                current_state = neighbor
                current_value = neighbor_value
                
                if current_value > best_value:
                    best_state = current_state
                    best_value = current_value
            else:
                stuck_count += 1
                  
            temperature *= cooling_rate
            iteration += 1

        plt.ioff()
        fig2 = plt.figure(figsize=(12, 6))
        fig2.suptitle('Initial and Final States')

        gs_init_final = fig2.add_gridspec(2, 5)

        axes_initial = [fig2.add_subplot(gs_init_final[0, i]) for i in range(5)]
        axes_final = [fig2.add_subplot(gs_init_final[1, i]) for i in range(5)]

        self.visualize_state(initial_state, axes=axes_initial)
        self.visualize_state(current_state, axes=axes_final)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() * 1000

        fig2.text(0.5, 0.05, f'Final Objective Value: {current_value} Duration: {duration} ms Stuck Count: {stuck_count}' , ha='center', fontsize=10)

        for ax in axes_initial:
            ax.set_title('Initial State', fontsize=8)
        for ax in axes_final:
            ax.set_title('Final State', fontsize=8)

        plt.show()
        print("Stuck Frequency:", stuck_count)
        
        # Display the final state in array format
        print("Final State (Array Format):")
        self.display_formatted_state(best_state)
        
        return best_state
