from django.shortcuts import render, redirect
import random
# Create your views here.
from struttureGioco.models import Equipaggiamento, Boss
from struttureGioco.funzioni import aggiungiStatistiche, rimuoviStatistiche, combattiBoss


def homeView(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")

	if user.personaggio.vitalita > 0:
		vitaEffettiva = user.personaggio.vita * user.personaggio.vitalita
	else:
		vitaEffettiva = user.personaggio.vita

	user.personaggio.save()
	return render(request, "index.html", {'vitaEffettiva': vitaEffettiva})


def inventarioView(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")
	if request.POST:

		itemID = request.POST.get("idItem")
		item = Equipaggiamento.objects.get(pk = itemID)
		if item.tipo == "P":
			# controllo che il personaggio abbia equipaggiata un'arma primaria
			if user.personaggio.armaPrimaria is not None:
				primariaAttuale = Equipaggiamento.objects.get(nome = user.personaggio.armaPrimaria)
				rimuoviStatistiche(user, primariaAttuale)
			# assegno il nuovo equipaggiamento
			user.personaggio.armaPrimaria = item
			aggiungiStatistiche(user, item)
		# user.personaggio.save()
		elif item.tipo == "S":
			# controllo che il personaggio abbia equipaggiata un'arma secondaria
			if user.personaggio.armaSecondaria is not None:
				secondariaAttuale = Equipaggiamento.objects.get(nome = user.personaggio.armaSecondaria)
				rimuoviStatistiche(user, secondariaAttuale)
			# assegno il nuovo equipaggiamento
			user.personaggio.armaSecondaria = item
			aggiungiStatistiche(user, item)

		else:
			# controllo che il personaggio abbia equipaggiata un'armatura
			if user.personaggio.armatura is not None:
				armaturaAttuale = Equipaggiamento.objects.get(nome = user.personaggio.armatura)
				rimuoviStatistiche(user, armaturaAttuale)
			# assegno il nuovo equipaggiamento
			user.personaggio.armatura = item
			aggiungiStatistiche(user, item)

	# aggiornamento statistiche personaggio per ogni equipaggiamento

	if user.personaggio.vitalita > 0:
		vitaEffettiva = user.personaggio.vita * user.personaggio.vitalita
	else:
		vitaEffettiva = user.personaggio.vita

	user.personaggio.save()

	if not user.is_authenticated:
		return redirect("login")

	if user.personaggio.zaino.all():
		zaino = user.personaggio.zaino.all()
	else:
		zaino = None

	print(zaino)

	return render(request, "inventario.html", {'zaino': zaino, 'vitaEffettiva': vitaEffettiva})


def luoghiView(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")

	boss = Boss.objects.all().filter(abilitato = True)
	print(boss)
	return render(request, "luoghi.html", {'listaBoss': boss})


def dettaglioBossView(request, nomeLuogo):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")
	try:
		boss = Boss.objects.get(luogo = nomeLuogo)
		vitaboss = boss.vita * boss.vitalita
		listaDrop = Equipaggiamento.objects.filter(boss = boss).order_by('nome')

		if request.POST:
			print("hehehehe")
			flag = True
			vittoria=False
			drop = Equipaggiamento.objects.filter(boss = boss).order_by('nome').values_list('nome', flat = True)
			try:
				indiceElemento = random.randint(0, len(drop) - 1)
				print(indiceElemento)
				elementoVinto = Equipaggiamento.objects.get(nome = drop[indiceElemento])
				print(elementoVinto)

				vittoria = combattiBoss(request.user, boss)

				if not user.personaggio.zaino.filter(nome=drop[indiceElemento]) and drop != None:
					user.personaggio.zaino.add(elementoVinto)
					user.personaggio.save()
					elementoGiaVinto = False
				else:
					elementoGiaVinto=True
			except:
				print("Boss no loot bad")
				elementoGiaVinto = None
				flag = False
				vittoria = None
				elementoVinto = None

		else:
			print("nonono")
			elementoGiaVinto = None
			flag = False
			vittoria = None
			elementoVinto = None

	except Boss.DoesNotExist:
		return redirect("luoghi")

	return render(request, "dettaglioBoss.html",
	              {'boss': boss, 'listaDrop': listaDrop, 'flag': flag, 'vittoria': vittoria,
	               'elementoVinto': elementoVinto,'elementoGiaVinto':elementoGiaVinto, 'vitaboss':vitaboss})
