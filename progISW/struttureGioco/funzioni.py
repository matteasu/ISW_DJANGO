import random

from django.core.exceptions import EmptyResultSet

from struttureGioco.models import Equipaggiamento


def aggiungiStatistiche(user, equipaggiamento):
	user.personaggio.vitalita += equipaggiamento.vitalita
	user.personaggio.destrezza += equipaggiamento.destrezza
	user.personaggio.forza += equipaggiamento.forza
	user.personaggio.intelligenza += equipaggiamento.intelligenza
	user.personaggio.tempra += equipaggiamento.tempra


def rimuoviStatistiche(user, equipaggiamento):
	user.personaggio.vitalita -= equipaggiamento.vitalita
	user.personaggio.destrezza -= equipaggiamento.destrezza
	user.personaggio.forza -= equipaggiamento.forza
	user.personaggio.intelligenza -= equipaggiamento.intelligenza
	user.personaggio.tempra -= equipaggiamento.tempra


def combattiBoss(user, boss):
	win = False

	# Str - attacco
	# Dex - chance critico dex% di fare X2 danno
	# Int - chance diminuzione difesa nemica
	# Tem - dininuzione attacco nemico (resistenza)

	vitapg = user.personaggio.vita * user.personaggio.vitalita
	vitaboss = boss.vita * boss.vitalita

	print(vitaboss, vitapg, user.personaggio.nome)

	while vitapg > 0 and vitaboss > 0:
		# Turno PG
		atk = user.personaggio.forza

		if user.personaggio.destrezza >= 100:
			atk *= 2
		elif random.randint(1, 100) <= user.personaggio.destrezza:
			atk *= 2

		if user.personaggio.intelligenza >= 100:
			danni = atk
		elif random.randint(1, 100) <= user.personaggio.intelligenza:
			danni = atk
		else:
			danni = atk - boss.tempra

		if danni <= 0:
			danni = 50

		vitaboss -= danni

		# Turno Boss
		atk = boss.forza

		if boss.destrezza >= 100:
			atk *= 2
		elif random.randint(1, 100) <= boss.destrezza:
			atk *= 2

		if boss.intelligenza >= 100:
			danni = atk
		elif random.randint(1, 100) <= boss.intelligenza:
			danni = atk
		else:
			danni = atk - user.personaggio.tempra

		if danni <= 0:
			danni = 5

		vitapg -= danni

	if vitapg > vitaboss:
		win = True
	else:
		win = False

	print(vitaboss, vitapg)

	return win


def modificaEquip(user, itemID):
	item = Equipaggiamento.objects.get(pk=itemID)
	if item:
		if user.personaggio.zaino.filter(pk=itemID):
			if item.tipo == "P":
				# controllo che il personaggio abbia equipaggiata un'arma primaria
				if user.personaggio.armaPrimaria is not None:
					primariaAttuale = Equipaggiamento.objects.get(nome=user.personaggio.armaPrimaria)
					rimuoviStatistiche(user, primariaAttuale)
				# assegno il nuovo equipaggiamento
				user.personaggio.armaPrimaria = item
				aggiungiStatistiche(user, item)
			# user.personaggio.save()
			elif item.tipo == "S":
				# controllo che il personaggio abbia equipaggiata un'arma secondaria
				if user.personaggio.armaSecondaria is not None:
					secondariaAttuale = Equipaggiamento.objects.get(nome=user.personaggio.armaSecondaria)
					rimuoviStatistiche(user, secondariaAttuale)
				# assegno il nuovo equipaggiamento
				user.personaggio.armaSecondaria = item
				aggiungiStatistiche(user, item)

			else:
				# controllo che il personaggio abbia equipaggiata un'armatura
				if user.personaggio.armatura is not None:
					armaturaAttuale = Equipaggiamento.objects.get(nome=user.personaggio.armatura)
					rimuoviStatistiche(user, armaturaAttuale)
				# assegno il nuovo equipaggiamento
				user.personaggio.armatura = item
				aggiungiStatistiche(user, item)
		else:
			raise ValueError("Equipaggiamento non presente all'interno dello zaino")
	else:
		raise Equipaggiamento.DoesNotExist("Equipaggiamento inesistente")


def sceltaDrop(boss):
	drop = Equipaggiamento.objects.filter(boss=boss).order_by('nome').values_list('nome', flat=True)
	if drop:
		indiceElemento = random.randint(0, len(drop) - 1)
		print(indiceElemento)
		elementoVinto = Equipaggiamento.objects.get(nome=drop[indiceElemento])
		print(elementoVinto)
	else:
		raise EmptyResultSet("Il boss non ha loot")

	return elementoVinto
