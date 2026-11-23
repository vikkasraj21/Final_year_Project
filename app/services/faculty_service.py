from app.database.connection import get_connection

def get_all_faculty():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                f.faculty_id,
                f.faculty_name,
                f.faculty_email,
                f.department_id,
                d.department_name
            FROM faculty AS f
            JOIN departments AS d
                ON f.department_id = d.department_id
            ORDER BY f.faculty_id
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def add_faculty(faculty_name, faculty_email, department_id):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO faculty
                (faculty_name, faculty_email, department_id)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (faculty_name, faculty_email, department_id)
        )

        connection.commit()
        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def update_faculty(faculty_id, faculty_name, faculty_email, department_id):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE faculty
            SET faculty_name = %s,
                faculty_email = %s,
                department_id = %s
            WHERE faculty_id = %s
        """

        cursor.execute(
            query,
            (faculty_name, faculty_email, department_id, faculty_id)
        )

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def delete_faculty(faculty_id):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM faculty
            WHERE faculty_id = %s
        """

        cursor.execute(query, (faculty_id,))

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()