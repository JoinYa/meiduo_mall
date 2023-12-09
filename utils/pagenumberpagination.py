from rest_framework.pagination import PageNumberPagination


# 自定义分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10  # 默认每页返回的条数
    page_size_query_param = 'page_size'  # url中设置 page_size的键,默认为page_size
    max_page_size = 100  # 每页返回的最大条数
