
from rest_framework import viewsets, generics,status
from .serializer import (UserProfileListSerializer,ReviewCreateSerializer,
                         ReviewSerializer,CountryDetailSerializer,NewsDetailSerializer,NewsCreateSerializer,
                         UserProfileDetailSerializer,CountryListSerializer,CityListSerializer,
                         UniversityListSerializer,UniversityDetailSerializer,NewsListSerializer,NewsCreateSerializer,
                         FavoriteSerializer,UserLoginSerializer,UserRegisterSerializer)

from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CreateUniversityPermission,CheckRolePermission
from .pagination import NewsPagination,UniversityPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken



class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

class UniversityListAPIView(generics.ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['world_rank', 'tuition_fee_average']
    pagination_class = UniversityPagination

class UniversityDetailAPIView(generics.RetrieveAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityDetailSerializer

class UniversityCreateAPIView(generics.CreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversityDetailSerializer
    permission_classes = [CreateUniversityPermission]

    def get_queryset(self):
        return University.objects.filter(owner=self.request.user)

class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer

class CountryDetailAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckRolePermission]

    def get_queryset(self):
        return Review.objects.filter(student=self.request.user)

class ReviewEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CheckRolePermission]

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    pagination_class = NewsPagination

class NewsDetailAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer

class NewsCreateAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer
    permission_classes = [CreateUniversityPermission]

    def get_queryset(self):
        return News.objects.filter(owner=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
