
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Open a connection to the project database."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "business_ai"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
    )
