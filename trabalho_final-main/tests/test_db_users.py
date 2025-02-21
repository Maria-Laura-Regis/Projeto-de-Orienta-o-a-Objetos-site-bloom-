import unittest
from app.controllers.db.db_users import DataRecord
from app.models.user_account import UserAccount

class TestDataRecord(unittest.TestCase):
    def test_get_user_account(self):
        # Supondo que o arquivo JSON contenha uma conta de usuário
        db = DataRecord()
        user_account = db.get_user_account(0)  # Obtém o primeiro usuário
        self.assertIsInstance(user_account, UserAccount)
        self.assertEqual(user_account.username, "Guest")
        
    def test_invalid_parameter(self):
        db = DataRecord()
        user_account = db.get_user_account("invalid")  # Parâmetro inválido
        self.assertIsNone(user_account)  # Esperamos que seja None

if __name__ == '__main__':
    unittest.main()