import os
import psycopg2
import pytest
from contextlib import contextmanager
from dotenv import load_dotenv
import time

# Load environment variables from .env file
def setup_test_environment():
    """Load environment variables from .env or .env.test if available"""
    if os.path.exists('.env.test'):
        load_dotenv('.env.test')
    else:
        load_dotenv()

@contextmanager
def get_db_connection():
    """Create a database connection using environment variables."""
    setup_test_environment()
    
    # Get connection parameters from environment variables
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB", "piksel_db")
    user = os.getenv("POSTGRES_USER", "piksel_user")
    password = os.getenv("POSTGRES_PASSWORD", "passwordPiksel")
    
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        yield conn
    except Exception as e:
        pytest.skip(f"Database connection failed: {str(e)}")
    finally:
        if conn:
            conn.close()

def test_database_connection():
    """Test that we can connect to the database with retries."""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()
                    assert result[0] == 1
                return  # Success
        except Exception as e:
            print(f"Connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                # Exponential backoff
                sleep_time = retry_delay * (2 ** attempt)
                time.sleep(sleep_time)
            else:
                raise  # Re-raise on final attempt