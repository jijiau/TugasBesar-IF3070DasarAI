import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file
file_path = '/Users/nasywaanaa/Documents/nasywaa/ccc/5thsemester/Mata Kuliah/Coding/DAI/Tubes 1/Genetic-Algorithm/3_Genetic8527.csv'
data = pd.read_csv(file_path)

# Calculate max and average values across each row (iteration)
data['Max Objective'] = data.max(axis=1)
data['Avg Objective'] = data.mean(axis=1)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Max Objective'], label='Maximum Objective Function', color='purple')
plt.plot(data.index, data['Avg Objective'], label='Average Objective Function', color='orange')
plt.xlabel("Iteration")
plt.ylabel("Objective Value")
plt.title("Plot of Maximum and Average Objective Function Values Over Iterations")
plt.legend()
plt.grid()
plt.show()
