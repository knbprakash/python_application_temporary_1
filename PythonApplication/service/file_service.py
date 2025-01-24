import pymysql.cursors

class FileService:
    def get_db_connection():
        """Establish and return a database connection."""
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='makeathon_db',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def getLatestAgreementId(username):
        connection = FileService.get_db_connection()

        try:
            agreement_id = None
            with connection.cursor() as cursor:
                query = """
                    SELECT agreement_id from Agreement
                    WHERE created_by = %s
                    ORDER BY created_at DESC
                    LIMIT 1;
                """
                cursor.execute(query, (username))
                result = cursor.fetchone()

                agreement_id = result['agreement_id']

            return agreement_id
        finally:
            connection.close()

    def createAgreement(username):
        connection = FileService.get_db_connection()

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Agreement (agreement_id, created_at, created_by)
                    VALUES (UUID(), CURRENT_TIMESTAMP(), %s);
                """
                cursor.execute(query, (username))
                connection.commit()
        finally:
            connection.close()

    def saveFile(agreement_id, text):
        connection = FileService.get_db_connection()

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Files (file_id, agreement_id, text)
                    VALUES (UUID(), %s, %s);
                """
                cursor.execute(query, (agreement_id, text))
                connection.commit()
        finally:
            connection.close()

    def getAllSavedTextsByAgreementId(agreement_id):
        connection = FileService.get_db_connection()

        try:
            text_list = []
            with connection.cursor() as cursor:
                query = """
                    SELECT text from Files
                    WHERE agreement_id = %s;
                """
                cursor.execute(query, (agreement_id))
                result = cursor.fetchall()

                text_list = [row['text'] for row in result]

            return text_list
        finally:
            connection.close()
