import openai
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status #, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins
# from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.permissions import AllowAny
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


from .models import Task, Attachment
from .serializers import TaskSerializer, AttachmentSerializer


class TaskListApiView(ListAPIView):
    serializer_class = TaskSerializer
    # filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend] comment: they are set in settings as default
    pagination_class = PageNumberPagination
    ordering_fields = ['id', 'task_summary', 'timestamp', 'updated'] # id and timestamp ordering return almost the same queryset
    ordering = ['id'] # default
    search_fields = ['task_summary', 'task_context', 'completed']
    filterset_fields = ['completed']

    def get_queryset(self):
        return self.filter_queryset(
            Task.objects.filter(
                user = self.request.user.id
            ).order_by('id').only('id', 'task_summary') # default
        )
    
    @method_decorator(cache_page(60*60*5)) # 5 hour caching
    def get(self, request, *args, **kwargs):
        '''
        We request to get all our tasks frequently, so caching 
        this API call optimizes API performance more
        '''
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data.copy() # to make QueryDict mutable, copy of the date is gotten
        data['user'] = request.user.id
        serializer = TaskSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskRUDApiView(APIView):

    def get_object(self, task_id, user_id):
        try:
            return Task.objects.get(id=task_id, user = user_id)
        except Task.DoesNotExist:
            return None
    # Read
    @cache_page(60*60*10) # 10 hour caching (since, it retrieves only a task, there wont be no huge consumption of storage/memory)
    def get(self, request, task_id):
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {'error': 'Object with task id does not exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update
    def put(self, request, task_id):
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {'error': 'Object with task id does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskSerializer(instance=task_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, task_id):
        task_instance = self.get_object(task_id, request.user.id)
        if not task_instance:
            return Response(
                {'res': 'Object with task id does not exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_204_NO_CONTENT
        )


class AttachmentViewSet(mixins.CreateModelMixin, # for creation of a Attachment instance
                  mixins.RetrieveModelMixin,     # for retriving (download) of a attached file
                  viewsets.GenericViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        task_id = int(request.data.get('task'))
        task = get_object_or_404(Task, id=task_id)

        if task.user != request.user:
            return HttpResponseForbidden('You do not have permission to upload attachments for this task')
        return super().create(request, *args, **kwargs)

    def retrieve(self, request):
        instance = self.get_object()
        task = instance.task
        if task.user != request.user:
            return HttpResponseForbidden('You do not have permission to access this attachment')
        file_path = instance.file.path
        file_name = instance.file.name.split('/')[-1]

        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response


def task_support(request, task_id):
    task =  get_object_or_404(Task, id=task_id)
    openai.api_key = settings.OPENAI_KEY

    if settings.OPENAI_KEY != '':
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant. Help me with my tasks.'},
                    {'role': 'user', 'content': f'My task summary: "{task.task_summary}" and\
                                                  body of the task: "{task.task_context}"'},
                ]
            )
    else:
        response = {'error': 'OpenAI key not configured'}
    return HttpResponse(json.dumps(response), content_type='application/json')


# to test if caching is working:
# └─$ curl -H 'Authorization: Token 4ebe840fe80635f1834e5dd9bf5676798276d8cf' -i http://localhost:8080/tasks/my-tasks/

