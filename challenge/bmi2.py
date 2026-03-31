from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def print_info(self):
        bmi = self.calculate_bmi()
        category = self.get_bmi_category()
        print("\n--- Person Info ---")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"BMI: {bmi:.2f}")
        print(f"Category: {category}")


class Adult(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        else:
            return "Overweight"


class Child(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2) * 1.3

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 14:
            return "Underweight"
        elif bmi < 18:
            return "Normal weight"
        else:
            return "Overweight"


class BMIApp:
    def __init__(self):
        self.people = []

    def get_number(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("❌ Please enter a valid number!")

    def collect_user_data(self):
        name = input("Enter name: ")

        age = int(self.get_number("Enter age: "))
        weight = self.get_number("Enter weight (kg): ")

        print("Enter height in METERS (example: 1.75)")
        height = self.get_number("Enter height: ")

        if age >= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        self.people.append(person)
        print("✅ Person added successfully!")

    def show_all(self):
        if not self.people:
            print("No people added yet.")
            return

        for person in self.people:
            person.print_info()


# RUN
app = BMIApp()

while True:
    print("\n1. Add Person")
    print("2. Show All")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        app.collect_user_data()
    elif choice == "2":
        app.show_all()
    elif choice == "3":
        break
    else:
        print("❌ Invalid choice")