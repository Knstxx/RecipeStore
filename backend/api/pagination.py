from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    offset_query_param = 'page'
    page_size_query_param = 'limit'
    default_limit = 6
