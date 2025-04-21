from ..core.database_connection import connect_to_db

def do(query: str) -> str:
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                if cursor.description:  
                    result = cursor.fetchall()
                    response = "Результат:\n" + "\n".join(str(row) for row in result)
                else:  
                    conn.commit()
                    response = f"Успешно. Затронуто строк: {cursor.rowcount}"
    
    except Exception as e:
        response = f"Ошибка: {str(e)}"
    
    return response  