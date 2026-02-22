from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserProfileListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('country/', CountryListAPIView.as_view(), name='country_list'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_detail'),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('university/', UniversityListAPIView.as_view(), name='university_list'),
    path('university/<int:pk>/', UniversityDetailAPIView.as_view(), name='university_detail'),
    path('review/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review/<int:pk>/', ReviewEditView.as_view(), name='review_edit'),
    path('news/', NewsListAPIView.as_view(), name='news_list'),
    path('news/create/', NewsCreateAPIView.as_view(), name='news_create'),
    path('news/<int:pk>/', NewsDetailAPIView.as_view(), name='news_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
    ]
