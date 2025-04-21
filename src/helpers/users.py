from ..core.database_connection import connect_to_db

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

def register_user(user_id, user_name):
    query = """
        INSERT INTO users (id, name) 
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
    """
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, user_name))
                conn.commit()
                return cursor.fetchone() is not None
    except:
        return False
