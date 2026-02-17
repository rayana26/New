from django.db import models
from  django.contrib.auth.models import  AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_img = models.ImageField(upload_to="country_img", blank=True, null=True)
    country_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.country_name

class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MaxValueValidator(80),
                                                  MinValueValidator(18)], null=True, blank=True)
    user_img = models.ImageField(upload_to='user_photo', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True)
    RoleChoices = (
    ('student','student'),
    ('owner','owner')
    )
    role_user = models.CharField(max_length=20, choices=RoleChoices, default='student')

    def __str__(self):
        return f'{self.username},{self.first_name},{self.last_name}'

class EducationProfile(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('school', 'Школа'),
        ('college', 'Колледж'),
        ('bachelor', 'Бакалавриат'),
    ]
    EXAM_TYPE_CHOICES = [
        ('ielts', 'IELTS'),
        ('toefl', 'TOEFL'),
        ('sat', 'SAT'),
        ('ort', 'ОРТ / ЕНТ / ЕГЭ'),
        ('none', 'Нет сертификата'),
    ]
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='education')
    education_level = models.CharField(max_length=20,choices=EDUCATION_LEVEL_CHOICES,verbose_name="Уровень образования")
    institution_name = models.CharField(max_length=255, verbose_name="Название учебного заведения")
    graduation_year = models.PositiveIntegerField(verbose_name="Год окончания")
    exam_type = models.CharField(max_length=10,choices=EXAM_TYPE_CHOICES,default='none',verbose_name="Тип экзамена" )
    exam_score = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name="Балл за экзамен")



class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_img = models.ImageField(upload_to='city_photo', null=True,blank=True)
    city_name = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE,related_name='country_university')
    description = models.TextField()
    world_rank = models.PositiveIntegerField(null=True, blank=True)
    tuition_fee_average = models.DecimalField(max_digits=10, decimal_places=2)
    website = models.URLField()
    image = models.ImageField(upload_to='uni_logos/')


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='faculties',
    )
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField()


class Grant(models.Model):
    COVERAGE_CHOICES = [
        ('full', 'full'),
        ('partial', 'partial'),
        ('one-time', 'one_time'),
    ]

    title = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    coverage_type = models.CharField(max_length=20, choices=COVERAGE_CHOICES)
    deadline = models.DateField()
    description = models.TextField()
    is_international = models.BooleanField(default=True, verbose_name="Для иностранцев")

class Course(models.Model):
    DEGREE_CHOICES = [
        ('bachelor', 'bachelor'),
        ('master', 'master'),
        ('phd', 'phd'),
    ]
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    duration_years = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.degree_type})"


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,11)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorites')
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    new_url = models.URLField()
    content = models.TextField()
    image = models.ImageField(upload_to='news_photos/')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='news')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published = models.BooleanField(default=True, verbose_name="Опубликовано")


