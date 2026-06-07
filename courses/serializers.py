from rest_framework import serializers
from courses.models import Course ,Module, Lesson, VideoResource, UserProgress
from uuid import UUID
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializes user model
class UserSerailizer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name']

# serializes course model - for fetching list
class CourseSerializer(serializers.ModelSerializer):
    user = UserSerailizer(required=False)

    class Meta:
        model = Course
        exclude = ['updated_at']

# serializes module model
class ModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Module
        exclude = ['updated_at']


# serializes videoresourse model
class VideoResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoResource
        exclude = ['updated_at']


# serializes lesson model - to GET a Lesson
class LessonSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    videos = VideoResourceSerializer(many=True)

    class Meta:
        model = Lesson
        exclude = ['updated_at']

    def get(self, request, *args, **kwargs):
        lesson_id = request.GET.get('lesson')
        if not lesson_id:
            return {
                'status': False,
                'message': 'Lesson id required.',
                'data': None,
                'error_message': 'Lesson id not recived.'
            }
        
        try:
            lesson_uid = UUID(lesson_id)
        except (TypeError, ValueError):
            return {
                'status': False,
                'message': 'Lesson id is invalid.',
                'data': None,
                'error_message': 'TypeError/ValueError on lesson id.'
            }
        
        try:
            lesson = Lesson.objects.get(uid=lesson_uid)
        except Lesson.DoesNotExist:
            return {
                'status': False,
                'message': 'Lesson does not exist.',
                'data': None,
                'error_message': 'Lesson does not exist.'
            }
        except Exception as e:
            return {
                'status': False,
                'message': 'Somthing unexcepted happened while retriving lesson.',
                'data': None,
                'error_message': 'An unexcpected error occured while retriving lesson.'
            }
        
        serializer = self.__class__(lesson)
        return {
            'status': True,
            'message': 'Lesson fetched successfully.',
            'data': serializer.data,
            'error_message': None
        }
        #  add background progress system
        

# serializes userprogress model - to fetch list of progress in different courses
class UserProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()
    user = UserSerailizer()
    course = CourseSerializer()
    class Meta:
        model = UserProgress
        fields = ['user', 'lesson', 'completed']

# serializes course model - fetch a single Course
class CourseDetailSerializer(serializers.ModelSerializer):
    user = UserSerailizer(required=False)
    modules = ModuleSerializer(many=True)
    lesson = LessonSerializer(many=True)

    class Meta:
        model = Course
        exclude = ['updated_at']
    
    def get(self, request, *args, **kwargs):
        course_id = request.GET.get('course_id')
        if not course_id:
            return {
                'status': False,
                'message': 'Course id required.',
                'data': None,
                'error_message': 'Course id not recived.'
            }
        try:
            course_uid = UUID(course_id)
        except (TypeError, ValueError):
            return {
                'status': False,
                'message': 'Invalid course id.',
                'data': None,
                'error_message': 'TypeError on course_id.'
            }
        try:
            course = Course.objects.get(id=course_uid)
        except Course.DoesNotExist:
            return {
                'status': False,
                'message': 'Course does not exist.',
                'data': None,
                'error_message': 'Invalid course id.'
            }
        try:
            progress = UserProgress.objects.get(user=request.user)
        except:
            progress = None
        serializer = self.__class__(course)
        if progress:
            serializer.data['progress'] = {
                'user': {
                        'id': progress.user.id,
                        'name': progress.user.name
                    },
                'lesson': {
                        'uid': str(progress.lesson.uid),
                        'title': progress.lesson.title
                    },
                'completed': progress.completed
            }

        return {
                'status': True,
                'message': 'Course fetched successfully.',
                'data': serializer.data,
                'error_message': None
            }

