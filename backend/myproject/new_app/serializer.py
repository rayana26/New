from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'country')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'faculty_name', 'description', 'website', 'email', 'phone']

class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = '__all__'

class CountryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','user_img']

class UserProfileListSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer()
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'user_img', 'role_user','country']

class EducationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationProfile
        fields = '__all__'

class UserProfileDetailSerializer(serializers.ModelSerializer):
    education = EducationProfileSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'age', 'user_img', 'country', 'phone_number',
            'role_user', 'education', 'register_date'
        ]

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id','country_name']

class UniversityListSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer()
    class Meta:
        model = University
        fields = ['id','image','name','website','world_rank','country']


class CountryDetailSerializer(serializers.ModelSerializer):
    country_university = UniversityListSerializer
    class Meta:
        model = Country
        fields = ['id','country_name']



class CityListSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer()
    class Meta:
        model = City
        fields = ['id', 'city_name', 'city_img','country']


class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['city_name']


class UniversityDetailSerializer(serializers.ModelSerializer):
    country = CountryNameSerializer()
    faculties = FacultySerializer(many=True, read_only=True)
    grants = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = [
            'id', 'name', 'country', 'description', 'world_rank',
            'tuition_fee_average', 'website', 'image', 'faculties',
            'grants', 'average_rating'
        ]


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%H')
    user = UserProfileNameSerializer()
    class Meta:
        model = Review
        fields = ['user', 'comment', 'created_date']
