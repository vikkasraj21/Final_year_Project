from app.database.connection import get_connection


def get_dashboard_stats():
    stats = {
        "departments": 0,
        "faculty": 0,
        "subjects": 0,
        "classrooms": 0,
        "class_sections": 0,
        "timetable_entries": 0
    }

    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return stats

        cursor = connection.cursor()

        for table in stats:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            stats[table] = cursor.fetchone()[0]

    except Exception as error:
        print(f"Dashboard statistics error: {type(error).__name__}")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

    return stats