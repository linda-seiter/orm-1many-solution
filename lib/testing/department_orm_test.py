from department import Department, CONN, CURSOR
import pytest

class TestDepartment:
    '''Class Department in department.py'''
    
    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''drop tables prior to each test.'''
        
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "departments" if it does not exist.'''
        
        Department.create_table()
        assert (CURSOR.execute("SELECT * FROM departments"))

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "departments" if it exists.'''
        
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
        
        Department.drop_table()

        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='departments'
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_department(self):
        '''contains method "save()" that saves a Department instance to the db and assigns the instance an id.'''
        
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        
        sql = """
            SELECT * FROM departments
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (department.id, department.name, department.location) == 
                (row[0], "Payroll", "Building A, 5th Floor" ))

    def test_creates_department(self):
        '''contains method "create()" that creates a new row in the db using parameter data and returns a Department instance.'''
        
        Department.create_table()
        department = Department.create("Payroll", "Building A, 5th Floor")
        
        sql = """
            SELECT * FROM departments
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2]) ==
                (department.id, department.name, department.location) == 
                (row[0], "Payroll", "Building A, 5th Floor" ))

    def test_creates_new_instance_from_db(self):
        '''contains method "new_from_db()" that takes a table row and creates a Department instance.'''
        
        Department.create_table()
        Department.create("Payroll", "Building A, 5th Floor")
        
        sql = """
            SELECT * FROM departments
        """
        row = CURSOR.execute(sql).fetchone()
        department = Department.new_from_db(row)
        
        assert ((row[0], row[1], row[2]) ==
                (department.id, department.name, department.location) == 
                (row[0], "Payroll", "Building A, 5th Floor" ))

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Department instances for every row in the db.'''
        
        Department.create_table()
        
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        departments = Department.get_all()
        
        assert (len(departments) == 2)
        assert (
            (departments[0].id, departments[0].name, departments[0].location) ==
            (department1.id, "Human Resources", "Building C, East Wing"))
        assert ((departments[1].id, departments[1].name, departments[1].location) ==
                (department2.id, "Marketing", "Building B, 3rd Floor")
        )

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns a Department instance corresponding to the db row retrieved by name.'''
        
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        department = Department.find_by_name("Human Resources")
        assert (
            (department.id, department.name, department.location) ==
            (department1.id, "Human Resources", "Building C, East Wing")
        )
        
        department = Department.find_by_name("Marketing")
        assert (
            (department.id, department.name, department.location) ==
            (department2.id, "Marketing", "Building B, 3rd Floor")
        )
        department = Department.find_by_name("Unknown")
        assert (department is None)

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Department instance corresponding to the db row retrieved by id.'''
        
        Department.create_table()
        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        department = Department.find_by_id(department1.id)
        assert (
            (department.id, department.name, department.location) ==
            (department1.id, "Human Resources", "Building C, East Wing")
        )
        department = Department.find_by_id(department2.id)
        assert (
            (department.id, department.name, department.location) ==
            (department2.id, "Marketing", "Building B, 3rd Floor")
        )
        department = Department.find_by_id(0)
        assert (department is None)

    def test_updates_record(self):
        '''contains a method "update()" that updates an instance's corresponding db row to match its new attribute values.'''
        Department.create_table()

        department1 = Department.create("Human Resources", "Building C, East Wing")
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        id1 = department1.id
        id2 = department2.id
        department2.name = "Sales and Marketing"
        department2.location = "Building B, 4th Floor"
        department2.update()

        # assert row not updated
        department = Department.find_by_id(id1)
        assert ((department.id, department.name, department.location) == (id1,"Human Resources","Building C, East Wing"))
    
        # assert row updated
        department = Department.find_by_id(id2)
        assert ((department.id, department.name, department.location) == (id2,"Sales and Marketing","Building B, 4th Floor"))
    

    def test_deletes_record(self):
        '''contains a method "delete()" that deletes the instance's corresponding db row'''
        Department.create_table()

        department1 = Department.create("Human Resources", "Building C, East Wing")
        id = department1.id
        department2 = Department.create("Marketing", "Building B, 3rd Floor")

        department = Department.find_by_id(id)
        department.delete()
        assert (Department.find_by_id(id) is None)  # assert row deleted
        assert (Department.find_by_id(department2.id)) # assert row not deleted

    def test_get_employees(self):
        '''contain a method "employees" that gets the employees for the current Department instance '''
        
        from employee import Employee #avoid circular import issue
        
        Department.create_table()
        department1 = Department.create("Payroll", "Building A, 5th Floor")
        department2 = Department.create("Human Resources", "Building C, 2nd Floor")
        
        Employee.create_table()
        employee1 = Employee.create("Raha", "Accountant", department1.id)
        employee2 = Employee.create("Tal", "Benefits Coordinator", department1.id)
        
        employees = department1.employees()
        assert(len(employees) == 2)
        assert((employees[0].id, employees[0].name, employees[0].job_title, employees[0].department_id) ==
               (employee1.id, employee1.name, employee1.job_title, employee1.department_id)  )      
        assert((employees[1].id, employees[1].name, employees[1].job_title, employees[1].department_id) ==
               (employee2.id, employee2.name, employee2.job_title, employee2.department_id)  )      