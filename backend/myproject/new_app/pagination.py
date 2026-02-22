from rest_framework.pagination import PageNumberPagination

class NewsPagination(PageNumberPagination):
    page_size = 5

class UniversityPagination(PageNumberPagination):
    page_size = 8