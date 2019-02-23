def find(chat_id):
    return "SELECT * FROM users WHERE chat_id={};".format(chat_id)

def set(chat_id, location):
    return "UPDATE users SET location='{}' WHERE chat_id={};".format(location,chat_id)

def new(chat_id):
    return "INSERT INTO users(chat_id) VALUES ({});".format(chat_id)
