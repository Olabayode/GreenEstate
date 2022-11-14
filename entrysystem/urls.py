from django.urls import path
from . import views

urlpatterns = [path("", views.home, name="home"),
               path("register/", views.register, name="register"),
               path("login/", views.user_login, name="login"),
               path("logout/", views.user_logout, name="logout"),
               path("base/", views.base, name="base"),
               path("base/<int:code>", views.get_visit, name="get_visit"),
               path("login/register/", views.register, name="signup"),
               path("register/login/", views.user_login, name="signin"),
               ]
