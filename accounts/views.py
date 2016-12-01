# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
 

def index(request):
    return render_to_response("index.html")
 
 
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect("/signin/")
        else:
            return render(request, "sign_up.html", {"form": form})

    return render(request, "sign_up.html", {"form": UserCreationForm() })


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect("/")
        else:
            return render(request, "sign_in.html", {"form": form})
    
    return render(request, "sign_in.html", {"form": AuthenticationForm()})
