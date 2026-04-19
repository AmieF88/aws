from database_config import get_connection


def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Connected successfully!")
        print("PostgreSQL version:", db_version[0])

        cursor.close()
        conn.close()
    except Exception as e:
        print("Connection failed:")
        print(e)


if __name__ == "__main__":
    test_connection()