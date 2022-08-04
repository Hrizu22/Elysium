from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination,CursorPagination

class StockListPagination(PageNumberPagination):
    page_size = 1
    page_query_param ='p'
    page_size_query_param='size'
    max_page_size= 4
    last_page_strings = 'end'
    
class StockListLOPagination(LimitOffsetPagination):
    default_limit= 5
    max_limit = 3
    limit_query_param = 'start'
    
class StockListCPagination(CursorPagination):
    page_size = 1
    ordering='-created'