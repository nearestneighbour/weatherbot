import psycopg2

class sql:
    def __init__(self, url):
        self.conn = psycopg2.connect(url, sslmode='require')
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get(self, column, chat_id):
        str = "SELECT {} FROM users WHERE chat_id={};".format(column, chat_id)
        self.cur.execute(str)
        result = self.cur.fetchone()
        return result[0] if result else None

    def set(self, column, chat_id, value):
        if self.get('chat_id', chat_id) == None:
            str = insertstr.format(column, chat_id, value)
        else:
            str = updatestr.format(column, value, chat_id)
        self.cur.execute(str)

insertstr = "INSERT INTO users(chat_id,{}) VALUES ({},'{}');"
updatestr = "UPDATE users SET {}='{}' WHERE chat_id={};"
