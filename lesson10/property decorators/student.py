class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    #Getter method for name property
    @property
    def name(self):
        return self.__name

    #Setter method for name property
    @name.setter
    def name(self, name):
        self.__name=name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age=age

#Creating an Instance of Student
student1 = Student("Melina", 17)

print("Name:", student1.name)
print("Age:", student1.age)

student1.name = "Reina"
student1.age = 16

print("Updated Name:", student1.name)
print("Updated Age:", student1.age)