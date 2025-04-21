from .database_connection import connect_to_db

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

def get_user_name_by_id(user_id: int) -> str:
    query = "SELECT name FROM users WHERE telegram_id = %s"
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))           
                result = cursor.fetchone()
                response = result[0] if result else None
    except Exception as e:
        response = f"Ошибка: {str(e)}"
    
    return response

def is_moder(user_id: int) -> bool:
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = %s AND is_moder = %s)",
                (user_id, True))
            return cursor.fetchone()[0] 