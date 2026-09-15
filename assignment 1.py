# Student Data Management Using Dictionary, Tuple and List

# List of student attributes
student1 = [101, "Sarthak", "CSE", 85]
student2 = [102, "Rahul", "IT", 78]
student3 = [103, "Aman", "AI & DS", 91]

# Dictionary storing student records
students = {
    student1[0]: tuple(student1[1:]),
    student2[0]: tuple(student2[1:]),
    student3[0]: tuple(student3[1:])
}

# 1. Add a new student record
new_student = [104, "Priya", "CSE", 88]
students[new_student[0]] = tuple(new_student[1:])

# 2. Delete an existing student record
del students[102]

# 3. Update details of a student
updated_student = [103, "Aman", "AI & DS", 95]
students[updated_student[0]] = tuple(updated_student[1:])

# 4. Display final student records
print("Final Student Records:")
print("-" * 50)

for roll_no, details in students.items():
    print("Roll Number:", roll_no)
    print("Name:", details[0])
    print("Branch:", details[1])
    print("Marks:", details[2])
    print("-" * 50)