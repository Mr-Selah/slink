import sqlite3

# Connect to your database
connection = sqlite3.connect("business_card.db")  # Ensure the database file is in the same folder as this script
cursor = connection.cursor()

# Query 1: Get the schema of the 'users' table
print("Schema of 'users' table:")
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users';")
schema = cursor.fetchone()
if schema:
    print(schema[0])
else:
    print("No 'users' table found!")

print("\nData in 'users' table:")
# Query 2: Select all data from the 'users' table
try:
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found in 'users' table.")
except sqlite3.Error as e:
    print(f"Error reading from database: {e}")

# Close the connection
connection.close()
