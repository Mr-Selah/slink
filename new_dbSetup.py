import sqlite3

# Connect to the database
connection = sqlite3.connect("business_card.db")
cursor = connection.cursor()

# Drop the existing 'users' table if it exists
cursor.execute("DROP TABLE IF EXISTS users")

# Create the 'users' table with proper schema
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    website TEXT,
    address TEXT,
    job_title TEXT NOT NULL,
    x_handle TEXT,
    instagram_handle TEXT,
    facebook_handle TEXT,
    photo TEXT,  -- Store photo as file path
    access_token TEXT NOT NULL -- 6-character access token for security
);
""")

connection.commit()
connection.close()
print("✅ Database setup completed successfully!")
