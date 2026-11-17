from app.database.connection import get_connection


def get_all_departments():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            raise ConnectionError("Unable to connect to MySQL.")

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT department_id, department_code, department_name
            FROM departments
            ORDER BY department_id
            """
        )

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def add_department(department_code, department_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            raise ConnectionError("Unable to connect to MySQL.")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO departments (
                department_code,
                department_name
            )
            VALUES (%s, %s)
            """,
            (department_code, department_name)
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def update_department(department_id, department_code, department_name):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            raise ConnectionError("Unable to connect to MySQL.")

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE departments
            SET department_code = %s,
                department_name = %s
            WHERE department_id = %s
            """,
            (department_code, department_name, department_id)
        )

        connection.commit()
        return cursor.rowcount

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

def delete_department(department_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            raise ConnectionError("Unable to connect to MySQL.")

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM departments
            WHERE department_id = %s
            """,
            (department_id,)
        )

        connection.commit()
        return cursor.rowcount

    except Exception:
        if connection is not None:
            connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()