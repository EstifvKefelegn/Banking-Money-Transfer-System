from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .form import RegisterForm
from .models import User
# Create your views here.
def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
           nw_user = form.save()
           username = form.cleaned_data["username"]
           messages.success(request, f"Hey {username}, you are successfully registered")
           new_user = authenticate(username=form.cleaned_data["email"],
                                   password=form.cleaned_data["password1"])
           login(request, new_user)
           return redirect("core:index")

    # if request.user.is_authenticated:
    #     messages.warning(request, "You are already loggedin")
    #     return redirect("core:index")
    else:
        form = RegisterForm()

    context = {
        "form":form
    } 
    return render(request, 'userauth/signup.html', context)

def SignInView(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged")
                return redirect("core:index")
            else:
                messages.warning(request, f"username or passwrd is not correct")    
                return redirect("userauth:signin")

        except:
            messages.warning(request, "User does not exist")


    return render(request, "userauth/signin.html")

def SignOutView(request):
    logout(request)
    return redirect("core:index")