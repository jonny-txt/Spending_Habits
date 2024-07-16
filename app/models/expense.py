from app.config.mysqlconnection import connectToMySQL

class Expense:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cost = data['cost']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO expenses (name, cost, date, user_id)
            VALUES (%(name)s, %(cost)s, %(date)s, %(user_id)s)
        """
        return connectToMySQL('spending').query_db(query, data)

    @classmethod
    def get_all(cls, user_id):
        query = """
            SELECT * FROM expenses 
            WHERE user_id = %(user_id)s
        """
        results = connectToMySQL('spending').query_db(query, {'user_id': user_id})
        expenses = []
        for result in results:
            expenses.append(cls(result))
        return expenses

    @classmethod
    def get_by_id(cls, expense_id, user_id):
        query = """
            SELECT * FROM expenses 
            WHERE id = %(expense_id)s AND user_id = %(user_id)s
        """
        result = connectToMySQL('spending').query_db(query, {'expense_id': expense_id, 'user_id': user_id})
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE expenses 
            SET name = %(name)s, cost = %(cost)s, date = %(date)s 
            WHERE id = %(id)s AND user_id = %(user_id)s
        """
        return connectToMySQL('spending').query_db(query, data)

    @classmethod
    def delete(cls, expense_id, user_id):
        query = "DELETE FROM expenses WHERE id = %(expense_id)s AND user_id = %(user_id)s"
        return connectToMySQL('spending').query_db(query, {'expense_id': expense_id, 'user_id': user_id})
