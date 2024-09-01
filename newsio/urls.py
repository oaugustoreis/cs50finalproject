from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("layout/", views.index, name="index"),
    path('search/', views.search_view, name='search'),

]