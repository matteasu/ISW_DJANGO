from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, playerID, password = None):
		if not playerID:
			raise ValueError("L'utente deve avere uno username")
		user = self.model(
			playerID=playerID
		)

		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, playerID, password):

		if not playerID:
			raise ValueError("L'utente deve avere uno username")
		user = self.create_user(
			playerID=playerID,
			password = password,

		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user


class Account(AbstractBaseUser):
	playerID = models.CharField(max_length = 50, unique = True)
	date_joined = models.DateTimeField(verbose_name = 'date joined', auto_now_add = True)
	last_login = models.DateTimeField(verbose_name = 'last login', auto_now = True)
	is_admin = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)

	# indico con che campo farò il login
	USERNAME_FIELD = "playerID"

	# campi obbligatori



	objects = MyAccountManager()

	def __str__(self):
		return self.playerID

	def has_perm(self, perm, obj = None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
