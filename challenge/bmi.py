from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age, weight, height):
        self.__name = name
        self.__age = age
        self.__weight = weight
        self.__height = height


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name=name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age=age

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight= value
        else:
            raise ValueError("Weight is okay")

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if value > 0:
            self.__height = value
        else:
            raise ValueError("Height is okay")

    @abstractmethod
    def calculate_bmi(self):
        pass

    @abstractmethod
    def get_bmi_category(self):
        pass

    def print_info(self):
        bmi = self.calculate_bmi()
        categoty = self.get_bmi_category()
        print(f"\nName: {self.name}")
        print(f"Age: {self.age}")
        print(f"BMI: {bmi: ,2f}")
        print(f"category: {self.category}")

class Adult(Person):
    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18:
            return "Underweight"
        elif bmi < 24:
            return "Normal weight"
        else :
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
        elif bmi < 24:
            return "Normal weight"
        else :
            return "Overweight"

class BMIApp:
    def __init__(self):
        self.person = []

    def add_person(self, person):
        self.person.append(person)

    def collect_user_data(self):
        name = input("Enter Name:")
        age = int(input("Enter Age:"))
        weight = float(input("Enter your weight (kg):"))
        height = float(input("Enter your height (m):"))

        if age>= 18:
            person = Adult(name, age, weight, height)
        else:
            person = Child(name, age, weight, height)

        self.add_person(person)






