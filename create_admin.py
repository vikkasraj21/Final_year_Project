import getpass

from app.database.connection import get_connection
from app.utils.password_utils import hash_password


def create_admin():
    username = input("Enter admin username: ").strip()
    password = getpass.getpass("Enter admin password: ")

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    if len(password) < 12:
        print("Password must contain at least 12 characters.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO admin_users (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, hash_password(password))
        )

        connection.commit()
        print("Admin account created successfully!")

    except Exception as error:
        print(f"Could not create admin account: {type(error).__name__}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    create_admin()