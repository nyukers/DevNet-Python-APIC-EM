#
# Author: Zibnitskii Aleksandr
# Condition: Create a script that asks for four pieces of information such
# as: first name, last name, location, and age. After then - print data to
# screen

space = " "

firstName = input("What is your first name? ")
lastName = input("What is your last name? ")
location = input("What is your location? ")
age = input("What is your age? ")
print('-'*38)
print(space.join(["Hi,",firstName,lastName,"! Your location is",location,"and you are",str(age),"years old."]))
