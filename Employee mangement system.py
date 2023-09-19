from flask import Flask, render_template, redirect, request
import cx_Oracle
from prettytable import PrettyTable

app = Flask(__name__)

# Database connection details
dsn = cx_Oracle.makedsn("localhost", own db, service_name="ur name")
connection = cx_Oracle.connect("system", "students", dsn=dsn)
cursor = connection.cursor()


def fetch_all_employees():
    query = "SELECT * FROM employee"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


@app.route('/')
def display_employee_data():
    # Fetch all employees from the database
    rows = fetch_all_employees()

    table = PrettyTable(['Employee ID', 'Name', 'Salary', 'Age', 'Role'])

    for row in rows:
        table.add_row(row)

    html_table = table.get_html_string()

    html_content = f"""
    <html>
        <head>
            <title>Employee Data</title>
            
            <style>
                /* Styles */
            </style>
        </head>
        <body style="background-color:lavender;">
        </body>
            <h1>Employee Data</h1>
            {html_table}
            <h2>Add Employee</h2>
            
            <form method="POST" action="/add_employee">
                <label for="add_emp_id">Employee ID:</label>
                <input type="text" id="add_emp_id" name="add_emp_id" required><br><br>
                <label for="add_name">Name:</label>
                <input type="text" id="add_name" name="add_name" required><br><br>
                <label for="add_salary">Salary:</label>
                <input type="text" id="add_salary" name="add_salary" required><br><br>
                <label for="add_age">Age:</label>
                <input type="text" id="add_age" name="add_age" required><br><br>
                <label for="add_role">Role:</label>
                <input type="text" id="add_role" name="add_role" required><br><br>
                <input type="submit" value="Add Employee">
            </form>
            <h2>Delete Employee</h2>
            <form method="POST" action="/delete_employee">
                <label for="delete_emp_id">Employee ID:</label>
                <input type="text" id="delete_emp_id" name="delete_emp_id" required><br><br>
                <input type="submit" value="Delete">
            </form>
            <h2>Update Employee</h2>
            <form method="POST" action="/update_employee">
    <label for="update_emp_id">Employee ID:</label>
    <input type="text" id="update_emp_id" name="update_emp_id" required><br><br>
    <label for="update_job_title">New Job Title:</label>
    <input type="text" id="update_job_title" name="update_job_title" required><br><br>
    <label for="update_role">New Role:</label>
    <input type="text" id="update_role" name="update_role" required><br><br>
    <input type="submit" value="Update">
</form>

            </form>
            <h2>Search Employee</h2>
            <form method="POST" action="/search_employee">
                <label for="search_emp_id">Employee ID:</label>
                <input type="text" id="search_emp_id" name="search_emp_id" required><br><br>
                <input type="submit" value="Search">
            </form>
        </body>
    </html>
    """

    return html_content


@app.route('/add_employee', methods=['POST'])
def add_employee():
    # Retrieve the employee data from the form
    emp_id = request.form['add_emp_id']
    name = request.form['add_name']
    salary = request.form['add_salary']
    age = request.form['add_age']
    role = request.form['add_role']

    query = "INSERT INTO employee (emp_id, name, salary, age, role) VALUES (:1, :2, :3, :4, :5)"
    cursor.execute(query, (emp_id, name, salary, age, role))
    connection.commit()

    return redirect('/')


@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    emp_id = request.form['delete_emp_id']

    query = "DELETE FROM employee WHERE emp_id = :1"
    cursor.execute(query, (emp_id,))
    connection.commit()

    return redirect('/')


@app.route('/update_employee', methods=['POST'])
@app.route('/update_employee', methods=['POST'])
def update_employee():
    emp_id = request.form['update_emp_id']
    new_role = request.form.get('update_role')

    query = "UPDATE employee SET role = :1 WHERE emp_id = :2"
    cursor.execute(query, (new_role, emp_id))
    connection.commit()

    return redirect('/')




@app.route('/search_employee', methods=['POST'])
def search_employee():
    emp_id = request.form['search_emp_id']

    query = "SELECT * FROM employee WHERE emp_id = :1"
    cursor.execute(query, (emp_id,))
    rows = cursor.fetchall()

    table = PrettyTable(['Employee ID', 'Name', 'Salary', 'Age', 'Role'])
    for row in rows:
        table.add_row(row)

    html_table = table.get_html_string()

    html_content = f"""
    <html>
        <head>
            <title>Search Results</title>
            <style>
                /* Styles */
            </style>
        </head>
        <body>
            <h1>Search Results</h1>
            {html_table}
        </body>
    </html>
    """

    return html_content


if __name__ == '__main__':
    app.run(debug=True)

