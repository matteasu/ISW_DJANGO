import os

from struttureGioco.storage import OverwriteStorage
from django.db import models

# Create your models here.
from django.urls import reverse

TIPOEQUIPAGGIAMENTO = [

	("P", "ArmaPrimaria"),
	("S", "ArmaSecondaria"),
	("A", "Armatura"),
]


class Boss(models.Model):
	nome = models.CharField(max_length = 50, unique = True)
	luogo = models.CharField(max_length = 100, null = True, unique = True)
	vita = models.IntegerField(default = 10)
	abilitato = models.BooleanField(default = False)

	vitalita = models.IntegerField(default = 0)
	forza = models.IntegerField(default = 0)
	destrezza = models.IntegerField(default = 0)
	intelligenza = models.IntegerField(default = 0)
	tempra = models.IntegerField(default = 0)

	def upload_location(instance, filename):
		filebase, extension = filename.split('.')
		return 'static/imgB/%s.%s' % (instance.nome, extension)

	image = models.ImageField(upload_to = upload_location, null = True, storage = OverwriteStorage())

	def __str__(self):
		return self.nome

	def get_absolute_url(self):
		return reverse('dettaglioBoss', args = [self.luogo])

	def filename(self):
		return os.path.basename(self.file.name)

class Equipaggiamento(models.Model):
	nome = models.CharField(max_length = 50, unique = True)
	tipo = models.CharField(max_length = 1, choices = TIPOEQUIPAGGIAMENTO, null = True)
	abilitato = models.BooleanField(default = True)
	boss = models.ForeignKey("Boss", on_delete = models.CASCADE, blank = True, null = True)

	vitalita = models.IntegerField(default = 0)
	forza = models.IntegerField(default = 0)
	destrezza = models.IntegerField(default = 0)
	intelligenza = models.IntegerField(default = 0)
	tempra = models.IntegerField(default = 0)

	def __str__(self):
		return self.nome


class Personaggio(models.Model):
	nome = models.CharField(max_length = 50, null = True)
	armaPrimaria = models.ForeignKey(Equipaggiamento, null = True, on_delete = models.CASCADE, blank = True,
	                                 related_name = '+')
	armaSecondaria = models.ForeignKey(Equipaggiamento, null = True, on_delete = models.CASCADE, blank = True,
	                                   related_name = '+')
	armatura = models.ForeignKey(Equipaggiamento, null = True, on_delete = models.CASCADE, blank = True,
	                             related_name = '+')

	vita = models.IntegerField(default = 10)
	vitalita = models.IntegerField(default = 1)
	forza = models.IntegerField(default = 1)
	destrezza = models.IntegerField(default = 1)
	intelligenza = models.IntegerField(default = 1)
	tempra = models.IntegerField(default = 1)
	zaino = models.ManyToManyField(Equipaggiamento, through = 'Inventario')

	def __str__(self):
		return self.nome


class Inventario(models.Model):
	personaggio = models.ForeignKey(Personaggio, null = False, on_delete = models.CASCADE)
	equipaggiamento = models.ForeignKey(Equipaggiamento, null = False, on_delete = models.CASCADE)

	def __str__(self):
		return self.personaggio.__str__() + ' --> ' + self.equipaggiamento.__str__()

	class Meta:
		unique_together = ('personaggio', 'equipaggiamento')
