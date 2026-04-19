from database_config import get_connection


def create_table():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        with open("create_persons_table.sql", "r") as file:
            sql_script = file.read()

        cursor.execute(sql_script)
        conn.commit()

        print("Table 'persons' created successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print("Error creating table:")
        print(e)


if __name__ == "__main__":
    create_table()