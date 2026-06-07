from django.urls import path
from courses.views import *


urlpatterns = [
    path('courses', ListCoursesAPIView.as_view(), name='courses')
]

