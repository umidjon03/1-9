from rest_framework import serializers
from .models import Task, Attachment


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "task_summary", "task_context", "completed", "timestamp", "updated", "user"]


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'

