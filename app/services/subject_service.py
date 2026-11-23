from app.database.connection import get_connection

def get_all_subjects():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                s.subject_id,
                s.subject_code,
                s.subject_name,
                s.department_id,
                d.department_name,
                s.subject_type,
                s.periods_per_week
            FROM subjects AS s
            JOIN departments AS d
                ON s.department_id = d.department_id
            ORDER BY s.subject_id
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def add_subject(
    subject_code,
    subject_name,
    department_id,
    subject_type,
    periods_per_week
):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO subjects (
                subject_code,
                subject_name,
                department_id,
                subject_type,
                periods_per_week
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                subject_code,
                subject_name,
                department_id,
                subject_type,
                periods_per_week
            )
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

def update_subject(
    subject_id,
    subject_code,
    subject_name,
    department_id,
    subject_type,
    periods_per_week
):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE subjects
            SET
                subject_code = %s,
                subject_name = %s,
                department_id = %s,
                subject_type = %s,
                periods_per_week = %s
            WHERE subject_id = %s
        """

        cursor.execute(
            query,
            (
                subject_code,
                subject_name,
                department_id,
                subject_type,
                periods_per_week,
                subject_id
            )
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

def delete_subject(subject_id):
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM subjects
            WHERE subject_id = %s
        """

        cursor.execute(query, (subject_id,))

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()