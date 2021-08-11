# from django.core.exceptions import ValidationError
from django.test import TestCase, Client
# from django.contrib.auth import login, authenticate, logout
from account.models import Account
import unittest


# Create your tests here.
# Tutte le funzioni di test devono iniziare con test_<qualcosa>
class AccountTest(TestCase):
	def setUp(self):
		self.account = Account.objects.create_user(playerID='Riccardo', password='Fallito234')
		self.superAccount = Account.objects.create_superuser(playerID="Asu", password="Fantastico123")

	# creazione utente di prova per il test unitario
	def test_expected_str_return_value(self):
		self.assertEqual(self.account.__str__(), "Riccardo")

	def test_verifica_username_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_user, playerID='', password='prova123')

	def test_verifica_password_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_user, playerID='dwdw', password='')

	def test_superUser_username_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_superuser, playerID='', password='ddddd')

	def test_superUser_password_registrazione(self):
		self.assertRaises(ValueError, Account.objects.create_superuser, playerID='dwdw', password='')

	def test_superUser_isAdmin(self):
		self.assertTrue(self.superAccount.is_admin)

	# self.assertTrue(self.account.is_admin) fallisce sempre
	def test_superUser_isStaff(self):
		self.assertTrue(self.superAccount.is_staff)

	def test_superUser_isSuperUser(self):
		self.assertTrue(self.superAccount.is_superuser)


if __name__ == "__main__":
	unittest.main()
