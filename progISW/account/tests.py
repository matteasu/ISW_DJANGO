from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from account.forms import LoginForm
from account.models import Account
import unittest


# Create your tests here.
# Tutte le funzioni di test devono iniziare con test_<qualcosa>
class AccountTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.account = Account.objects.create_user(playerID = 'Nino Nino', password = 'Paramedico234')
		self.superAccount = Account.objects.create_superuser(playerID = "Asu", password = "Fantastico123")

	# creazione utente di prova per il test unitario
	def test_expected_str_return_value(self):
		self.assertEqual(self.account.__str__(), "Nino Nino")

	def test_verifica_username_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_user, playerID = '', password = 'prova123')

	def test_verifica_password_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_user, playerID = 'dwdw', password = '')

	def test_superUser_username_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_superuser, playerID = '', password = 'ddddd')

	def test_superUser_password_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_superuser, playerID = 'dwdw', password = '')

	def test_superUser_isAdmin(self):
		self.assertTrue(self.superAccount.is_admin)

	# self.assertTrue(self.account.is_admin) fallisce sempre
	def test_superUser_isStaff(self):
		self.assertTrue(self.superAccount.is_staff)

	def test_superUser_isSuperUser(self):
		self.assertTrue(self.superAccount.is_superuser)

	def test_login(self):
		response = self.client.login(playerID = "Nino Nino", password = "Paramedico234")
		self.assertTrue(response)

	def test_login_raises_ValidationError(self):
		form = LoginForm({'player_id': 'Riccardo', 'password': 'a'})
		self.assertRaises(ValidationError, form.clean)

	if __name__ == "__main__":
		unittest.main()
