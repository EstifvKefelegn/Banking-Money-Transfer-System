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
           return redirect("account:kyc-reg")
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


    if request.user.is_authenticated:
        messages.warning(request, "You are already loggedin")
        return redirect("account:account")

    return render(request, "userauth/signin.html")

def password_reset(request):
    current_user  = request.user
    # username = User.objects.get(username=current_user)
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get("confirm_password")
        print(f"Current User: {current_user.username}")
        print(f"Current Password: {current_password}")
        print(f"New Password: {new_password}")
        print(f"Confirm Password: {confirm_password}")
        if current_user.check_password(current_password):
            if new_password == confirm_password:
                current_user.set_password(new_password)
                current_user.save()
                messages.success(request, "You have succesfully changed your password")
                return redirect("account:account")
            else:
                messages.warning(request, "The password you entered doesnot match")
                # return redirect("account:account")
        else:
            messages.warning(request, "Incorrect password")
            # return redirect("account:account")

    return render(request, "account/account.html")


def SignOutView(request):
    logout(request)
    return redirect("core:index")