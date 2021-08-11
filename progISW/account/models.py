from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from struttureGioco.models import Personaggio


# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, playerID, password=None):
		# eccezione in caso in cui playerID sia vuoto
		if not playerID:
			raise ValueError("L'utente deve avere uno username")

		# eccezione in caso in cui password sia vuota
		if not password:
			raise ValueError("La password non può essere vuota")
		user = self.model(
			playerID=playerID
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, playerID, password):

		if not playerID:
			raise ValueError("L'utente deve avere uno username")

			# eccezione in caso in cui password sia vuota
		if not password:
			raise ValueError("La password non può essere vuota")

		user = self.create_user(
			playerID=playerID,
			password=password,

		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	playerID = models.CharField(max_length=50, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	personaggio = models.ForeignKey(Personaggio, on_delete=models.CASCADE, null=True)

	# indico con che campo farò il login
	USERNAME_FIELD = "playerID"

	# campi obbligatori

	objects = MyAccountManager()

	def __str__(self):
		return self.playerID

	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
