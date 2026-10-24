
from db import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()
            print("Database connection successful!")
            print(result[0])

except Exception as error:
    print("Database connection failed.")
    print(error)
