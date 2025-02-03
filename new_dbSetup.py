from sqlalchemy import create_engine, text
import os

# Get the database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def setup_database():
    try:
        # Establish a connection
        with engine.connect() as connection:
            # Drop existing 'users' table if it exists
            connection.execute(text("DROP TABLE IF EXISTS users"))
            
            # Create the 'users' table with PostgreSQL syntax
            connection.execute(text("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                website TEXT,
                address TEXT,
                job_title TEXT NOT NULL,
                x_handle TEXT,
                instagram_handle TEXT,
                facebook_handle TEXT,
                photo TEXT,
                access_token TEXT NOT NULL
            );
            """))
            
            print("✅ Database setup completed successfully!")
    
    except Exception as e:
        print(f"Error setting up database: {e}")

# Run the setup if the script is executed directly
if __name__ == "__main__":
    setup_database()

