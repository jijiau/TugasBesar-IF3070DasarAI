from simulated_annealing import SimulatedAnnealingSolver

if __name__ == "__main__":
    initial_state = SimulatedAnnealingSolver().generate_test_state_1()
    solver = SimulatedAnnealingSolver(initial_state)
    solution = solver.simulated_annealing()
    print("Final state:", solution)
    print("Objective value:", solver.calculate_objective(solution))



