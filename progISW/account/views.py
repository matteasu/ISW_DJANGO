from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, LoginForm


# Create your views here.

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			playerID = form.cleaned_data.get("playerID")
			raw_psw = form.cleaned_data.get("password1")
			account = authenticate(playerID = playerID, password = raw_psw)
			login(request, account)
			return redirect("home")
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)


def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			playerID = request.POST['playerID']
			password = request.POST['password']
			user = authenticate(playerID = playerID, password = password)
			if user:
				login(request, user)
				return redirect("home")
	else:
		form = LoginForm()
	context['login_form'] = form
	return render(request, 'login.html', context)