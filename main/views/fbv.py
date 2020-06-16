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

from main.models import Project, Block
from main.serializers import ProjectListSerializer, BlockListSerializer
from main.permissions import BlockPermission

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication, ))
def projects(request):
    projects = Project.objects.all()
    serializer = ProjectListSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((BlockPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
def blocks(request, pk):
    project = get_object_or_404(Project, id=pk)
    blocks = Block.objects.filter(project_id=project.id)
    serializer = BlockListSerializer(blocks, many=True)
    return Response(serializer.data)