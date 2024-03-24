from django.urls import path, include
from rest_framework_simplejwt   import views as jwt_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # authentication
    path('api/token/',                  jwt_views.TokenObtainPairView.as_view(),        name ='token_obtain_pair'),
    path('api/token/refresh/',          jwt_views.TokenRefreshView.as_view(),           name ='token_refresh'),

    path('search', views.search, name='search'),
    path('api/search', views.SearchAPIView.as_view(), name='search_api'),
    path('search_page', views.search_page, name='search_page'),
    path('feedback', views.feedback, name='feedback'),
    
    path('signup', views.signup, name = 'signup'),
    path('', include('django.contrib.auth.urls')),
]