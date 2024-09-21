import sqlite3

# Connect to SQLite
connection = sqlite3.connect("ellucian_products.db")

# Create a cursor object to insert records and create the table
cursor = connection.cursor()

# Create the table with Ellucian product details
table_info = """
CREATE TABLE ELLUCIAN_PRODUCTS (
    PRODUCT_NAME VARCHAR(50),
    SALES_COUNT INT,
    PRICE DECIMAL(10, 2),
    CATEGORY VARCHAR(50)
);
"""
cursor.execute(table_info)

# Insert records for Ellucian products
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Banner', 1000, 20000.00, 'Student Information Systems')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Colleague', 800, 18000.00, 'Student Information Systems')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('PowerCampus', 300, 15000.00, 'Student Information Systems')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('CRM Advance', 500, 22000.00, 'CRM')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('CRM Advise', 450, 21000.00, 'CRM')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('CRM Recruit', 400, 19000.00, 'CRM')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Degree Works', 600, 25000.00, 'Academic Planning')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Ethos', 700, 30000.00, 'Data Integration')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Quercus', 350, 17000.00, 'Student Information Systems')''')
cursor.execute('''INSERT INTO ELLUCIAN_PRODUCTS VALUES('Elevate', 200, 12000.00, 'Student Information Systems')''')

# Display all the records
print("The inserted records are:")
data = cursor.execute('''SELECT * FROM ELLUCIAN_PRODUCTS''')
for row in data:
    print(row)

# Commit your changes to the database
connection.commit()
connection.close()
