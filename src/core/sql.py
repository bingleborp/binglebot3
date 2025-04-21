from .database_connection import connect_to_db

def do(query: str) -> str:
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        cursor.execute(query)

        if cursor.description:  
            result = cursor.fetchall()
            response = "Результат:\n" + "\n".join(str(row) for row in result)
        else:  
            conn.commit()
            response = f"Успешно. Затронуто строк: {cursor.rowcount}"

    except Exception as e:
        response = f"Ошибка: {str(e)}"
        
    finally:
        if 'conn' in locals():  
            cursor.close()
            conn.close()

    return response  