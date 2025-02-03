from sqlalchemy import create_engine, text
import os

# Get the database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def query_database():
    try:
        # Establish a connection
        with engine.connect() as connection:
            # Query 1: Get the schema of the 'users' table
            print("Schema of 'users' table:")
            schema_query = text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
            """)
            schema_result = connection.execute(schema_query)
            schema = schema_result.fetchall()
            
            if schema:
                for column in schema:
                    print(f"{column[0]}: {column[1]}")
            else:
                print("No 'users' table found!")

            # Query 2: Select all data from the 'users' table
            print("\nData in 'users' table:")
            data_query = text("SELECT * FROM users")
            rows = connection.execute(data_query)
            
            user_data = rows.fetchall()
            if user_data:
                for row in user_data:
                    print(row)
            else:
                print("No data found in 'users' table.")
    
    except Exception as e:
        print(f"Error reading from database: {e}")

# Run the query if the script is executed directly
if __name__ == "__main__":
    query_database()


