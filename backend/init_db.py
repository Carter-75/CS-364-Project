import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
# Force loading from the file in the same directory to ensure we get the right values
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"Loaded configuration from {dotenv_path}")
else:
    print("Warning: .env file not found!")
    load_dotenv() # Fallback

def init_db():
    # Get DB config from .env
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME")
    
    if not db_name:
        print("Error: DB_NAME is not set in .env file.")
        return

    print(f"Connecting to MySQL at {host}:{port} as {user}...")
    print(f"Target Database: {db_name}")

    # Connect to MySQL server (no database selected yet)
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Read schema.sql
        with open("app/schema.sql", "r") as f:
            schema_sql = f.read()

        # Replace the hardcoded database name in schema.sql with the one from .env
        # This handles the mismatch where schema.sql says 'mediawatchlist' but .env says 'CS-364-Project'
        schema_sql = schema_sql.replace("mediawatchlist", f"`{db_name}`")
        
        # Execute statements
        print(f"Initializing database '{db_name}'...")
        
        # Split by semicolon, but be careful with delimiters if any (simple split works for this schema)
        statements = schema_sql.split(';')
        
        for statement in statements:
            stmt = statement.strip()
            if not stmt:
                continue

            try:
                cursor.execute(stmt)
                
                # If we just created the database, force the connection to use it
                # This ensures subsequent queries know where to go
                if "CREATE DATABASE" in stmt.upper():
                    conn.database = db_name  # type: ignore
                    
            except mysql.connector.Error as err:
                # If error is "No database selected" (1046), try selecting it and retrying
                if err.errno == 1046:
                    try:
                        print(f"Encountered 'No database selected'. Switching to {db_name} and retrying...")
                        conn.database = db_name  # type: ignore
                        cursor.execute(stmt)
                    except Exception as retry_err:
                        print(f"Retry failed: {retry_err}")
                else:
                    print(f"Error executing statement: {err}")
                    print(f"Statement: {stmt[:50]}...")
                    # Ignore "database exists" or similar harmless errors if you want, 
                    # but usually we want to see them. 
                    # However, the script drops and recreates, so it should be fine.
                    print(f"Error executing statement: {err}")
                    print(f"Statement: {statement[:50]}...")

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialization complete!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    init_db()
