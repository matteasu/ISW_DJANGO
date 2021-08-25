from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import random
# Create your views here.
from django.urls import reverse

from struttureGioco.models import Equipaggiamento, Boss
from struttureGioco.funzioni import combattiBoss, modificaEquip, sceltaDrop


def homeView(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")

	if user.is_admin:
		pag = "homeAdmin.html"
		equip = Equipaggiamento.objects.all()
		boss = Boss.objects.all()
		bossDrop = []
		for b in boss:
			bossDrop.append({
				'boss': b,
				'drop': Equipaggiamento.objects.filter(boss = b).order_by('nome')
			})
		context = {'equip': equip, 'bossDrop': bossDrop}
	else:
		if user.personaggio.vitalita > 0:
			vitaEffettiva = user.personaggio.vita * user.personaggio.vitalita
		else:
			vitaEffettiva = user.personaggio.vita

		user.personaggio.save()
		context = {'vitaEffettiva': vitaEffettiva}
		pag = "index.html"
	return render(request, pag, context)


def inventarioView(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("login")
	if request.POST:
		itemID = request.POST.get("idItem")
		modificaEquip(user, itemID)

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

	elementoVinto = None
	elementoGiaVinto = None

	if not user.is_authenticated:
		return redirect("login")
	try:
		boss = Boss.objects.get(luogo = nomeLuogo)
		vitaboss = boss.vita * boss.vitalita
		listaDrop = Equipaggiamento.objects.filter(boss = boss).order_by('nome')

		if request.POST:
			print("hehehehe")

			flag = True
			vittoria = False
			try:
				vittoria = combattiBoss(request.user, boss)
				print(vittoria)
				if vittoria:
					elementoVinto = sceltaDrop(boss)
					if not user.personaggio.zaino.filter(nome = elementoVinto.nome):
						user.personaggio.zaino.add(elementoVinto)
						user.personaggio.save()
						elementoGiaVinto = False
					else:
						elementoGiaVinto = True
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
	               'elementoVinto': elementoVinto, 'elementoGiaVinto': elementoGiaVinto, 'vitaboss': vitaboss})
