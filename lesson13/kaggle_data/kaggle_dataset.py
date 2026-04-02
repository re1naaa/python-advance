# Importing the Pandas library for data manipulation and analysis
import pandas as pd

# Reading a CSV file into a DataFrame
df = pd.read_csv('avgIQpercountry.csv')

# Printing information about the DataFrame
print(df.info())

# Extracting the first 5 rows using the head() method
first_rows = df.head()

# Displaying the extracted rows to quickly inspect the data
print(first_rows)

# Extracting the 'Country' column from the DataFrame
country_data = df['Country']

# Displaying the 'Column' data to view the countries included in the dataset
print(country_data)

# Select a subset of the dataframe containing only the 'Country' and 'Average IQ' columns
subset = df[['Country', 'Average IQ']]

# Print the subset
print(subset)

# Filtering the subset DataFrame to include only rows where 'Average IQ' is greater than 100
filtered_df = subset[subset['Average IQ'] > 100]

# Printing the filtered DataFrame
print(filtered_df)

# Check for missing values and create a boolean mask where True indicates a missing value
null_mask = df.isnull()

# Count the number of missing values in each column by summing up the True values in the null_mask
null_count = null_mask.sum()

# Print the count of missing values in each column
print("\nCount of null values in each column:")
print(null_count)

# Drop rows with any missing data
df.dropna(inplace=True)

print("\nDataset information after removing null values:")
print(df.info())


# Count the number of duplicate rows in the DataFrame
duplicated_count = df.duplicated().sum()

print("\nCount of duplicate rows:")
print(duplicated_count)

# Group by 'Continent' and calculate average IQ
average_iq_per_continent = df.groupby('Continent')['Average IQ'].mean()

# Printing the average IQ for each continent
print(average_iq_per_continent)

# Sorting the average IQ per continent in descending order
sorted_average_iq_per_continent = average_iq_per_continent.sort_values(ascending=False)

# Printing the sorted average IQ per continent
print(sorted_average_iq_per_continent)

# Convert 'Population - 2023' column from string with commas to float
df['Population - 2023'] = df['Population - 2023'].apply(lambda x: float(x.replace(',', '')))
print(df.info())

# Calculate the total Nobel Prizes by Country
total_nobel_by_country = df.groupby('Country')['Nobel Prices'].sum()

# Sort the total Nobel Prizes by country in descending order
sorted_total_nobel_by_country = total_nobel_by_country.sort_values(ascending=False)

# Print the sorted total Nobel Prizes by country
print("\nTotal Nobel Prizes by country", sorted_total_nobel_by_country)

# Filter out countries with zero Nobel Prizes by country
sorted_total_nobel_nonzero = sorted_total_nobel_by_country[sorted_total_nobel_by_country != 0]

# Print the sorted total Nobel Prizes by country, excluding countries with zero Nobel Prizes
print("\nTotal Nobel Prizes by country, excluding countries with Zero Nobel Prizes\n", sorted_total_nobel_nonzero)
