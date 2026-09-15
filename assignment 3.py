# Program to check whether a triangle is right-angled

def is_right_angled(a, b, c):
    # Find the largest side
    sides = [a, b, c]
    sides.sort()

    # Pythagoras theorem
    if sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2:
        return True
    else:
        return False


# Accept three sides
a = float(input("Enter first side: "))
b = float(input("Enter second side: "))
c = float(input("Enter third side: "))

# Check the triangle
if is_right_angled(a, b, c):
    print("The triangle is a right-angled triangle.")
else:
    print("The triangle is not a right-angled triangle.")