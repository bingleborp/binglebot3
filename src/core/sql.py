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

def get_user_name_by_id(user_id: int) -> str:
    query = "SELECT name FROM users WHERE telegram_id = %s"
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))           
        response = cursor.fetchone()
    except Exception as e:
        response = f"Ошибка!"
    finally:
        if 'conn' in locals():  
            cursor.close()
            conn.close()
    return response

def is_moder(user_id: int) -> bool:
    query = "SELECT 1 FROM users WHERE telegram_id = %s AND is_moder = %s"
    try:
        conn = connect_to_db()
        with conn.cursor() as cursor: 
            cursor.execute(query, (user_id, True))
            return cursor.fetchone() is not None  
            
    except Exception as e:
        print(f"Ошибка при проверке модератора: {e}")
        return False  
        
    finally:
        if 'conn' in locals():
            conn.close()  