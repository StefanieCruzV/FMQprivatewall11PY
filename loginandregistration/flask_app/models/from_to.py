from flask_app.config.mysqlconnection import connectToMySQL

class From_to:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.message = data['message']
        self.message_id = data['message_id']

    @classmethod
    def get_all_user_messages(cls, data):
        query = "SELECT * FROM login JOIN from_to ON login.id = from_id JOIN message ON message_id = message.id WHERE to_id = %(id)s;"
        results = connectToMySQL("login").query_db(query, data)
    
        from_to_list = []
        for row_from_db in results:
            from_to_data = {
                "id": row_from_db["id"],
                "first_name": row_from_db['first_name'],
                "last_name": row_from_db['last_name'],
                "email": row_from_db['email'],
                "message": row_from_db["message"],
                "message_id" : row_from_db['message.id']
            }
            from_to_list.append(cls(from_to_data))

        return from_to_list
    
    @classmethod
    def delete_message(cls, data):
        query = "DELETE FROM from_to WHERE from_id = %(from_id)s and message_id = %(message_id)s;"
        print(query)
        results = connectToMySQL("login").query_db(query, data)
        print(results)
        return
    
    @classmethod
    def create_relation_message(cls, data):
        query = "INSERT INTO from_to (from_id, to_id, message_id) values (%(form_id)s, %(to_id)s, %(message_id)s);"
        result = connectToMySQL("login").query_db(query,data)
        return result