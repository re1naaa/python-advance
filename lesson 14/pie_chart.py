import pandas as pd
import matplotlib.pyplot as plt



df = pd.read_csv('avgIQpercountry.csv')

nobel_prizes_by_continent = df.groupby('Continent')['Nobel Prices'].sum()

no_of_continents = nobel_prizes_by_continent.count()

print(no_of_continents)

colors = ['gold','lightcoral', 'yellow', 'red', 'orange', 'lightskyblue', 'purple', 'brown']

plt.figure(figsize=(10,10))

nobel_prizes_by_continent.plot(kind='pie', colors=colors, autopct='%1.1f%%')

plt.title('Distibution of Nobel Prizes by Continent')

plt.axis('equal')

plt.ylabel('')

plt.tight_layout()

plt.show()