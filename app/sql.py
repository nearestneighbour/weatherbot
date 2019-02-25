from app import cur

def find(chat_id):
    str = "SELECT coord,loc FROM users WHERE chat_id={};".format(chat_id)
    cur.execute(str)
    return cur.fetchone()

def set(chat_id, coord, loc):
    if find(chat_id) == None:
        str = "INSERT INTO users(chat_id,coord,loc) VALUES ({},'{}','{}');".format(chat_id, coord, loc)
    else:
        str = "UPDATE users SET coord='{}',loc='{}' WHERE chat_id={};".format(coord, loc, chat_id)
    cur.execute(str)
