from PIL.ImageChops import difference

my_set ={1, 2, 3, 3, 4, 5, 5, 6}
print(my_set)

set1 = {1, 2, 3}
set2 = {3, 4, 5}

union_result_method = set1.union(set2)
union_result_operator = set1 | set2

print(union_result_method)
print(union_result_operator)

intersection_result_method= set1.intersection(set2)
intersection_result_operator= set1 & set2

print(intersection_result_method)
print(intersection_result_operator)

difference_result_method = set1.difference(set2)
difference_result_operator = set1 - set2

print(difference_result_method)
print(difference_result_operator)

symetric_difference_method = set1.symmetric_difference(set2)
symetric_difference_operator = set1 ^ set2

print(symetric_difference_method)
print(symetric_difference_operator)



my_set = {1, 2, 3}

my_set.add(7)

my_set.remove(3)

my_set.discard(8)

print(my_set)

my_set.clear()

print(my_set)

user1_interests = {"music", "movies", "travel"}
user2_interests = {"movies", "reading", "cooking"}
common_interests = user1_interests.intersection(user2_interests)
print(common_interests)

colors = {"red", "green", "blue"}
color = "green"
print(color in colors)
print(color not in colors)
