from django.urls import path
import travello.urls
from . import views
urlpatterns = [
    path("register", views.register, name="register"),
path("login",views.login,name="login"),
path("logout",views.logout,name="logout"),
path("book",views.book,name="book"),
]
