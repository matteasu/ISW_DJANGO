from django.db import models

# Create your models here.
TIPOEQUIPAGGIAMENTO = [

	("P", "ArmaPrimaria"),
	("S", "ArmaSecondaria"),
	("A", "Armatura"),
]


class Boss(models.Model):
	nome = models.CharField(max_length=50, unique=True)
	luogo = models.CharField(max_length=100, null=True)
	vita = models.IntegerField(default=10)
	abilitato = models.BooleanField(default=False)

	vitalita = models.IntegerField(default=0)
	forza = models.IntegerField(default=0)
	destrezza = models.IntegerField(default=0)
	intelligenza = models.IntegerField(default=0)
	tempra = models.IntegerField(default=0)

	def __str__(self):
		return self.nome


class Equipaggiamento(models.Model):
	nome = models.CharField(max_length=50, unique=True)
	tipo = models.CharField(max_length=1, choices=TIPOEQUIPAGGIAMENTO, null=True)
	abilitato = models.BooleanField(default=True)
	boss = models.ForeignKey("Boss", on_delete=models.CASCADE, blank=True, null=True)

	vitalita = models.IntegerField(default=0)
	forza = models.IntegerField(default=0)
	destrezza = models.IntegerField(default=0)
	intelligenza = models.IntegerField(default=0)
	tempra = models.IntegerField(default=0)

	def __str__(self):
		return self.nome


class Personaggio(models.Model):
	armaPrimaria = models.ForeignKey(Equipaggiamento, null=True, on_delete=models.CASCADE, blank=True, related_name='+')
	armaSecondaria = models.ForeignKey(Equipaggiamento, null=True, on_delete=models.CASCADE, blank=True,
									   related_name='+')
	armatura = models.ForeignKey(Equipaggiamento, null=True, on_delete=models.CASCADE, blank=True, related_name='+')

	vita = models.IntegerField(default=10)

	vitalita = models.IntegerField(default=0)
	forza = models.IntegerField(default=0)
	destrezza = models.IntegerField(default=0)
	intelligenza = models.IntegerField(default=0)
	tempra = models.IntegerField(default=0)


class Inventario(models.Model):
	personaggio = models.ForeignKey(Personaggio, null=False, on_delete=models.CASCADE)
	equipaggiamento = models.ForeignKey(Equipaggiamento, null=False, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('personaggio', 'equipaggiamento')
