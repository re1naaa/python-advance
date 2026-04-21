import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset from a CSV file into a DataFrame
df = pd.read_csv('avgIQpercountry.csv')

# Creating a scatter plot of Mean years of schooling vs. Average IQ

# Set the figure size (width=10 inches, height=6 inches)
plt.figure(figsize=(10, 6))

# Create scatter plot
plt.scatter(df['Mean years of schooling - 2021'], df['Average IQ'], color='purple', alpha=0.7)

# Set plot title
plt.title('Scatter Plot of Mean Years of Schooling vs. Average IQ')

# Set label for the x-axis
plt.xlabel('Mean years of schooling - 2021')

# Set label for the y-axis
plt.ylabel('Average IQ')

# Enable grid lines with dashed style and transparency
plt.grid(True, linestyle='--', alpha=0.7)

# Display the plot
plt.show()