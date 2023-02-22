import sqlite3
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()


# Функция для изменение лимита у пользователей
def set_user_gen_limit(user_name, new_limit):
    # проверяем, есть ли пользователь в базе данных
    target_user = cursor.execute('SELECT id FROM users WHERE name=?', (user_name,)).fetchone()
    if target_user is None:
        return f"Пользователь {user_name} не найден в базе данных."

    # обновляем лимит пользователя в базе данных
    cursor.execute('UPDATE users SET gen_limit=? WHERE id=?', (new_limit, target_user[0]))
    conn.commit()
    return f"Лимит пользователя {user_name} изменен на {new_limit}."
