from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.
def current_user(req):
    return User.objects.get(id = req.session['user_id'])

def index(req):
    return render(req, 'main/index.html')

def register(req):
    valid = User.objects.validateUser(req.POST)
    if valid[0]:
        pw_hash = bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=req.POST['name'], username=req.POST['username'], email=req.POST['email'], password=pw_hash, dob=req.POST['dob'])
        messages.success(req, "Finished registration, please log in")
    else:
        for error in valid[1]:
            messages.error(req, error)
    return redirect("/")

def login(req):
	user = User.objects.filter(email = req.POST.get('email')).first()
	if user and bcrypt.checkpw(req.POST.get('password').encode(), user.password.encode()):
		req.session['user_id'] = user.id
		return redirect('/quotes')
	else:
		messages.error(req, "Password or Email does not match")
		return redirect('/')
	return redirect('/quotes')

def logout(req):
    req.session.clear()
    return redirect("/")

def quotes(req):
    user = current_user(req)

    context = {
            'user': user,
            'quotable_quotes': Quote.objects.exclude(favorites = user),
            'favorites': user.favorites.all()
    }
    return render(req, "main/home.html", context)

def create(req):
        valid = Quote.objects.validateQuote(req.POST)
        if valid[0]:
            Quote.objects.create(content=req.POST['content'], author=req.POST['author'], poster=current_user(req))
            return redirect("/quotes")
        else:
            for error in valid[1]:
                messages.error(req, error)
            return redirect("/quotes")

def add_favorite(req, id):
    user = current_user(req)
    favorite = Quote.objects.get(id=id)

    user.favorites.add(favorite)

    return redirect("/quotes")

def remove_favorite(req, id):
    user = current_user(req)
    favorite = Quote.objects.get(id=id)

    user.favorites.remove(favorite)

    return redirect("/quotes")

def show_user(req, id):
    user = User.objects.get(id=id)
    context = {
            'user': user,
            'favorites': user.favorites.all()
    }
    return render(req, 'main/userpage.html', context)
