from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('search/', views.search_view, name='search'),
    path('saved/', views.saved_view, name='saved'),
    path('read_later/', views.read_later, name='read_later'),
    path('delete_saved/', views.delete_saved, name='delete_saved'),

]