from django.urls import path
from .import views

app_name = "userauth"

urlpatterns = [
    path("signup/", views.RegisterView, name="signup"),
    path("signin/", views.SignInView, name="signin"),
    path("signout/", views.SignOutView, name="signout"),
    path('reset/', views.password_reset, name="resetpassword")
]
