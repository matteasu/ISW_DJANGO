from django.shortcuts import render, redirect

# Create your views here.
from struttureGioco.models import Equipaggiamento


def homeView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    return render(request, "index.html", {})


def inventarioView(request):
    user = request.user
    if request.POST:
        itemID = request.POST.get("idItem")
        item = Equipaggiamento.objects.get(pk=itemID)
        if item.tipo == "P":
            user.personaggio.armaPrimaria = item
            # user.personaggio.save()
        elif item.tipo == "S":
            user.personaggio.armaSecondaria = item
            # user.personaggio.save()
        else:
            user.personaggio.armatura = item

        user.personaggio.save()

    if not user.is_authenticated:
        return redirect("login")

    zaino = user.personaggio.zaino.all()

    return render(request, "inventario.html", {'zaino': zaino})
