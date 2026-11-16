from app.database.connection import get_connection
from app.utils.password_utils import verify_password


def authenticate_admin(username, password):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT password_hash
            FROM admin_users
            WHERE username = %s AND is_active = TRUE
            """,
            (username,)
        )

        admin = cursor.fetchone()

        if admin is None:
            return False

        return verify_password(password, admin["password_hash"])

    except Exception as error:
        print(f"Authentication error: {type(error).__name__}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()