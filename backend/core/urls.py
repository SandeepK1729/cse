from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('search_api', views.search_api, name='search_api'),
    path('search_page', views.search_page, name='search_page'),
    path('feedback', views.feedback, name='feedback'),
    
    path('signup', views.signup, name = 'signup'),
    path('', include('django.contrib.auth.urls')),
]