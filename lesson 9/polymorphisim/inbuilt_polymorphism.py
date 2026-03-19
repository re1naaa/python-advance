
string_length = len("Hello World")
list_length = len([1, 2, 3, 4, 5])
tuple_length = len((10,20,30))

print(string_length)
print(list_length)
print(tuple_length)

sum_list = sum([1, 2, 3, 4, 5])
sum_tuple = sum((10,2, 3))

print(sum_list)
print(sum_tuple)


max_value = max(5,10,3)
max_float = max(3.14,2.71,3.4)

print(max_value)
print(max_float)

def add(x,y):
    return x + y

def concatenate(x,y):
    return str(x) + str(y)

def operate(operation, x,y):
    return operation(x,y)

result_sum = operate(add,3,5)
result_concatenate = operate(concatenate,'hello','world')

print("Result of sum:", result_sum)
print("Result of concatenate:", result_concatenate)

