from django.urls import path
from main.views.viewsets import ProjectListCreate, ProjectRetrieveUpdateDelete, BlockViewSet, ProjectViewSet, TaskViewSet, \
    TaskCommentViewSet, TaskDocumentViewSet
from rest_framework import routers

urlpatterns = [
    path('projects/', ProjectListCreate.as_view()),
    path('projects_ud/<int:pk>/', ProjectRetrieveUpdateDelete.as_view())
]

router = routers.DefaultRouter()
router.register('blocks', BlockViewSet, basename='main')
router.register('projects', ProjectViewSet, basename='main')
router.register('tasks', TaskViewSet, basename='main')
router.register('task_comments', TaskCommentViewSet, basename='main')
router.register('task_documents', TaskDocumentViewSet, basename='main')

urlpatterns += router.urls