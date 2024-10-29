# urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import CustomLoginView, root_redirect

urlpatterns = [
    path('', root_redirect, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]