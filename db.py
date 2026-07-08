import sqlite3


DATABASE = "search_history.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS search_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            query TEXT,

            file_name TEXT,

            total_results INTEGER,

            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    connection.commit()

    connection.close()


def save_search(

    query,

    file_name,

    total_results

):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(

        """

        INSERT INTO search_history

        (

            query,

            file_name,

            total_results

        )

        VALUES

        (?, ?, ?)

        """,

        (

            query,

            file_name,

            total_results

        )

    )

    connection.commit()

    connection.close()


def get_history():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(

        """

        SELECT *

        FROM search_history

        ORDER BY searched_at DESC

        """

    )

    data = cursor.fetchall()

    connection.close()

    return data