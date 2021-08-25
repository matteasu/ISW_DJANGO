from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import random
# Create your views here.
from django.urls import reverse

from struttureGioco.models import Equipaggiamento, Boss
from struttureGioco.funzioni import combattiBoss, modificaEquip, sceltaDrop


def homeView(request):
	user = request.user
	context = {}
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
	context = {}

	if not user.is_authenticated:
		return redirect("login")

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

	if user.personaggio.zaino.all():
		zaino = user.personaggio.zaino.all()
	else:
		zaino = None

	context = {'zaino': zaino, 'vitaEffettiva': vitaEffettiva}

	return render(request, "inventario.html", context)


def luoghiView(request):
	user = request.user
	context = {}
	if not user.is_authenticated:
		return redirect("login")

	boss = Boss.objects.all().filter(abilitato = True)

	context = {'listaBoss': boss}

	print(boss)
	return render(request, "luoghi.html", context)


def dettaglioBossView(request, nomeLuogo):
	user = request.user

	context = {'elementoVinto': None, 'elementoGiaVinto': None, 'vittoria': None, 'flag': False}

	if not user.is_authenticated:
		return redirect("login")
	try:
		boss = Boss.objects.get(luogo = nomeLuogo)
		context['boss'] = boss
		context['vitaboss'] = boss.vita * boss.vitalita
		context['listaDrop'] = Equipaggiamento.objects.filter(boss = boss).order_by('nome')

		if request.POST:
			print("hehehehe")
			context['flag'] = True
			context['vittoria'] = False

			vittoria = combattiBoss(request.user, boss)
			context['vittoria'] = vittoria
			print(vittoria)
			if vittoria:
				elementoVinto = sceltaDrop(boss)
				context['elementoVinto'] = elementoVinto
				if not user.personaggio.zaino.filter(nome = elementoVinto.nome):
					user.personaggio.zaino.add(elementoVinto)
					user.personaggio.save()
					context['elementoGiaVinto'] = False
				else:
					context['elementoGiaVinto'] = True

		else:
			print("nonono")

	except Boss.DoesNotExist:
		return redirect("luoghi")

	return render(request, "dettaglioBoss.html", context)
