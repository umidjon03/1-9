from django.db import models
from users.models import User

class Task(models.Model):
    task_summary = models.CharField(max_length = 180)
    task_context = models.TextField()
    completed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.task_summary

    class Meta:
        db_table = 'task_tasks'


class Attachment(models.Model):
    file = models.FileField(upload_to='task-attachments')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id} {self.task.task_summary[:10]}'
    
    class Meta:
        db_table = 'task_attachment'
