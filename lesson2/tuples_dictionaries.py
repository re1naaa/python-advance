grades = {
    ("Melina", "Math"): 2,
    ("Dion", "Physics"): 3.5,
    ("Festa", "Biology"): 5,
    ("Reina", "English"): 4
}

melina_math = grades[("Melina", "Math")]
print("Melina's grade in math is", melina_math)

grades[("Dion", "Physics")] = 3
print(grades)

keys = list(grades.keys())

student , subject = keys[0]
print(student, "'s grade is", subject, "is", medina_math)