from app.database.connection import get_connection

connection = get_connection()

if connection:
    print("Connection test passed!")
    connection.close()
else:
    print("Connection test failed!")