import pandas as pd

from lesson13.array_manipulation import total_sum

product = ['Apples', 'Bananas', 'Oranges', 'Grapes', 'Pineapples']

sales = [150,200,180,90,60]

sales_series = pd.Series(sales, index=product)

print(sales_series)

print(sales_series['Grapes'])

total_sales = sales_series.sum()
print(total_sales)

best_selling_product = sales_series.idxmax()
print(f"Best selling product: {best_selling_product}")