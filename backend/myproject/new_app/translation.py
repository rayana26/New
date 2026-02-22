from .models import University,Country,Faculty,Grant,Course,News
from modeltranslation.translator import TranslationOptions,register

@register(University)
class UniversityTranslationOptions(TranslationOptions):
    fields = ('name','description',)

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)

@register(Faculty)
class FacultyTranslationOptions(TranslationOptions):
    fields = ('faculty_name','description',)

@register(Grant)
class FacultyTranslationOptions(TranslationOptions):
    fields = ('title','description',)

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title',)