from django.db import models
import uuid
from django.contrib.auth import get_user_model

class Base(models.Model):
    uid = models.fields.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.fields.DateTimeField(auto_now_add=True)
    updated_at = models.fields.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


User = get_user_model()
class Course(Base):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='courses', null=True, blank=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermidiate', 'Intermediate'), ('advanced', 'Advanced')])
    goal = models.TextField(null=True, blank=True)
    primary_language = models.fields.CharField(max_length=25)
    secondary_language = models.fields.CharField(max_length=25)
    subscriptions = models.fields.IntegerField(default=0)


class Module(Base):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.IntegerField()


class Lesson(Base):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    definition = models.TextField()
    order = models.IntegerField()


class VideoResource(Base):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='Videos')
    youtube_url = models.URLField()
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    views = models.BigIntegerField()
    language = models.CharField(max_length=50)
    score = models.FloatField()


class UserProgress(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
