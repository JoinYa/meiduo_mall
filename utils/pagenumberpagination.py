from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


# 自定义分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10  # 默认每页返回的条数
    page_size_query_param = 'page_size'  # url中设置 page_size的键,默认为page_size
    max_page_size = 100  # 每页返回的最大条数

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            max_page_number = len(queryset) // page_size + 1
            if int(page_number) > max_page_number:
                page_number = max_page_number
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
