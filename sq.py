import sqlite3 as sq

async def bedin_database():
    global db, cur_n

    db = sq.connect('Phonebook.db')
    cur_n = db.cursor()

    # cur_n.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, photo TEXT, age TEXT, description TEXT, name TEXT)")

    db.commit()


async def create_contact(phone):
    contact = cur_n.execute("SELECT 1 FROM people WHERE surname == '{key}'".format(key=phone)).fetchone()
    if not contact:
        cur_n.execute("INSERT INTO people VALUES(?, ?, ?, ?, ?)", (phone, '', '', '', ''))
        db.commit()


async def edit_contact(state, phone):
    async with state.proxy() as data:
        cur_n.execute("UPDATE people SET name = '{}', surname = '{}', comment = '{}' WHERE phone == '{}'".format(
            data['name'], data['surname'], data['comment'],  phone))
        db.commit()
