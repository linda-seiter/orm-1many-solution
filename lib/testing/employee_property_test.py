from department import Department
from employee import Employee
import pytest

class TestEmployeeProperties:
    '''Class Employee in employee.py'''

    def test_name_is_string(self):
        '''validates name property is assigned a string'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            employee = Employee("Lee", "Manager", department.id)
            employee.name = 7
            
    def test_name_string_length(self):
        '''validates name property length > 0'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            employee = Employee("Lee", "Manager", department.id)
            employee.name = ''
                
    def test_location_is_string(self):
        '''validates job_title property is assigned a string'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            employee = Employee("Lee", "Manager", department.id)
            employee.job_title = 7  
            
    def test_location_string_length(self):
        '''validates job_title property length > 0'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            employee = Employee("Lee", "Manager", department.id)
            employee.job_title = ''   
       
    def test_department_id_fk_property_create(self):
        with pytest.raises(ValueError):
            Department.create_table()
            Employee.create_table()
            Employee.create("Raha", "Accountant", 7)
            
    def test_department_id_fk_property_reassignment(self):
        with pytest.raises(ValueError):
            Department.create_table()
            department = Department.create("Payroll", "Building C, 3rd Floor")
            Employee.create_table()
            employee = Employee.create("Raha", "Accountant", department.id)
            employee.department_id = 10