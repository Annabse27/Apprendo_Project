from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    # Количество элементов на странице по умолчанию
    page_size = 10
    # Параметр, который позволяет клиенту задать количество элементов на странице
    page_size_query_param = 'page_size'
    # Максимальное количество элементов на странице
    max_page_size = 100
