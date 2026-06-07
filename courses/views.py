from rest_framework.response import Response
from rest_framework.viewsets import generics
from accounts.authentication import HttpOnlyJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from courses.models import Course, Lesson, UserProgress
from courses.serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer, UserProgressSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery
from courses.pagination import CoursePagination
import logging
logger = logging.getLogger()

# Get list of courses or search
class ListCoursesAPIView(generics.ListAPIView):
    logger.log('Retriving course list')
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class  = CoursePagination

    def get(self, request):
        if query := request.GET.get('s') is not None: # full text search for course
            logger.log(f'user searched for query-{query}- in course')
            query = "|".join(query.split(' '))
            search_query = SearchQuery(query, search_type='raw')
            search = SearchVector('title', 'topic', 'primary_language', 'secondary_language')
            queryset = Course.objects.annotate(search).filter(search=search_query)
        else:
            # default result
            queryset = self.queryset
        try:
            if queryset.count() < 1:
                logger.info('courses served with zero results.')
                return Response(
                    {
                        'status': False,
                        'message': 'No courses available.',
                        'data': None,
                        'error_message': None
                    }
                )
            serializer = self.serializer_class(queryset.order_by('-subscriptions'), many=True)
            data = serializer.data
            logger.info('Courses retrived successfully.')
            return Response(
                {
                    'status': True,
                    'message': 'Courses retrived successfully.',
                    'data': data,
                    'error_message': None
                }
            )

        except Exception as e:
            logger.error(f'Error occured while retriving courses. error-{str(e)}')
            return Response(
                {
                    'status': False,
                    'message': 'Someting unexcepted happened.',
                    'data': None,
                    'error_message': 'An unidentified error occured during fetching list of courses.'
                }
            )


class GetCourseAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class GetLessonAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class ListUserProgressAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [HttpOnlyJWTAuthentication]
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

    def get(self, request):
        try:
            user = request.user
            queryset = self.queryset.filter(user=user)
            
            if not queryset.exists():
                return Response(
                    {
                        'status': False,
                        'message': 'No progress.',
                        'data': None,
                        'error_message': None
                    }
                )

            serializer = self.serializer_class(queryset, many=True)
            return Response(
                {
                    'status': True,
                    'message': 'List of progress recived successfully.',
                    'data': serializer.data,
                    'error_message': None
                }
            )
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'message': 'Something unexcepted happened.',
                    'data': None,
                    'error_message': 'Something unexcepted happened.'
                }
            )
