from simulated_annealing import SimulatedAnnealingSolver

def get_solver_choice():
    print("Choose an algorithm to solve the cube:")
    print("1: Hill Climbing")
    print("2: Simulated Annealing")
    print("3: Genetic Algorithm")
    choice = int(input("Enter the number of your choice: "))
    return choice

if __name__ == "__main__":
    initial_state = SimulatedAnnealingSolver().generate_random_initial_state()
    solver = SimulatedAnnealingSolver(initial_state)
    solution = solver.simulated_annealing()
    print("Final state:", solution)
    print("Objective value:", solver.calculate_objective(solution))



