import random
from department import Department
from employee import Employee
from faker import Faker

Employee.drop_table()
Department.drop_table()
Department.create_table()
Employee.create_table()

# Create seed data
payroll = Department.create("Payroll", "Building A, 5th Floor")
human_resources = Department.create("Human Resources", "Building C, East Wing")
departments = [payroll, human_resources]

fake = Faker()
jobs = ["Database Administrator", "Manager",
        "Full-stack Engineer", "Web Designer"]
for i in range(10):
    Employee.create(fake.name(), random.choice(jobs), random.choice(departments).id)


