import logging

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from main.models import Project, Task, Block, TaskComment
from main.serializers import TaskCommentListSerializer, BlockListSerializer, ProjectListSerializer, \
    TaskListSerializer
from main.permissions import BlockPermission, TaskInsidePermission, TaskPermission


@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True)

        return Response(serializer.data)


@permission_classes((BlockPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
class BlockList(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        blocks = Block.objects.filter(project_id=project.id)
        serializer = BlockListSerializer(blocks, many=True)

        return Response(serializer.data)


@permission_classes((TaskPermission,))
@authentication_classes((JSONWebTokenAuthentication,))
class TaskList(APIView):
    def get(self, request, pk):
        block = get_object_or_404(Block, id=pk)
        tasks = Task.objects.filter(block=block)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


@permission_classes((TaskInsidePermission,))
@authentication_classes((JSONWebTokenAuthentication,))
class TaskCommentList(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        comments = TaskComment.objects.filter(task=task)
        serializer = TaskCommentListSerializer(comments, many=True)
        return Response(serializer.data)