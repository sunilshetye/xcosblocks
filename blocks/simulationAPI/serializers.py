import logging
from rest_framework import serializers
from simulationAPI.models import TaskFile, Task

logger = logging.getLogger(__name__)


class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ('file_id', 'file', 'upload_time', 'task')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    file = TaskFileSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('task_id', 'task_time', 'file')

    def create(self, validated_data):
        # Takes file from request and stores it along with a taskid
        files_data = list(self.context.get(
            'view').request.FILES.getlist("file"))[0]
        logger.info('File Upload')
        task = Task.objects.create()
        logger.info('task: '+str(task))
        TaskFile.objects.create(task=task, file=files_data)
        logger.info('Created Object for:' + files_data.name)
        return task