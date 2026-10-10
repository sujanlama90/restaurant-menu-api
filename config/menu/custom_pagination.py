from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size=3
    page_query_param='page_num'
    page_size_query_param='records'
    max_page_size =6