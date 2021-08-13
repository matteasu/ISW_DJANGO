from django.shortcuts import render, redirect


# Create your views here.

def homeView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    return render(request, "index.html", {})


def inventarioView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    zaino = user.personaggio.zaino.all()

    return render(request, "inventario.html", {'zaino': zaino})
