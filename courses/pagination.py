from rest_framework.pagination import PageNumberPagination

# custom pagination configuration for course
class CoursePagination(PageNumberPagination):
    page_size = 10 # set size of the page
    page_size_query_param = "s"
    page_query_param = "p"
    max_page_size = 100

