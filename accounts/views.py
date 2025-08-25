from django.shortcuts import render, redirect
from django.contrib  import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            messages.info(request, 'Invalid credentials.')
            return redirect('login')
    else:
        return render(request, "login.html")


def lo_gout (request):
    logout(request)
    return redirect('login')


def register(request):
    return render(request, "register.html")
