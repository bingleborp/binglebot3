from ..core.database_connection import connect_to_db

def add_song(user_id: int, session_id: int, song_name: str, song_url: str) -> bool:
    try:
        # Получаем следующий приоритет для пользователя
        next_priority = get_next_user_priority(user_id, session_id)
        if next_priority is None:  # Если не удалось получить приоритет
            return False
        
        query = """
            INSERT INTO requests (user_id, session_id, title, url, priority, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, session_id, song_name, song_url, next_priority))
                conn.commit()
                return True
    
    except Exception as e:
        print(f"Ошибка при добавлении песни: {str(e)}")
        return False


def get_next_user_priority(user_id: int, session_id: int) -> int | None:
    try:
        query = """
            SELECT COALESCE(MAX(priority), 0) + 1 
            FROM requests 
            WHERE user_id = %s AND session_id = %s
        """
        
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, session_id))
                result = cursor.fetchone()
                return result[0] if result else 1
    
    except Exception as e:
        print(f"Ошибка при получении приоритета: {str(e)}")
        return None