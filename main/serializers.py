from main.models import Project, Block, Task, TaskComment, TaskDocument
from rest_framework import serializers
from authe.serializers import UserSerializer
from constants import PROJECT_STATUSES, PROJECT_TYPES, BLOCK_TYPES


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField()
    project_type_name = serializers.SerializerMethodField()
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'status_name', 'project_type_name', 'creator_name')

    def get_status_name(self, obj):
        if obj.status is not None:
            return PROJECT_STATUSES[obj.status-1][1]
        return ''

    def get_project_type_name(self, obj):
        if obj.project_type is not None:
            return PROJECT_TYPES[obj.project_type-1][1]
        return ''

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ProjectCreateSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField()
    project_type = serializers.IntegerField()
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def validate_status(self, value):
        if value > 3 or value < 1:
            raise serializers.ValidationError('Status options: [1, 2, 3]')
        return value

    def validate_project_type(self, value):
        if value > 2 or value < 1:
            raise serializers.ValidationError('Project type options: [1, 2]')
        return value

    def validate_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('Name 100 char max')
        return value


class ProjectDetailedSerializer(ProjectListSerializer):
    creator = UserSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'status_name', 'project_type_name', 'creator')


class BlockListSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    block_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = ('id', 'name', 'block_type_name', 'project_name')

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''

    def get_block_type_name(self, obj):
        if obj.block_type is not None:
            return BLOCK_TYPES[obj.block_type-1][1]
        return ''


class BlockCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    project = ProjectSerializer(read_only=True)
    block_type = serializers.IntegerField()

    def validate_block_type(self, value):
        if value > 4 or value < 1:
            raise serializers.ValidationError('Block type options: [1, 2, 3, 4]')
        return value

    def validate_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('Name 100 char max')
        return value


class BlockDetailSerializer(BlockListSerializer):
    project = ProjectListSerializer(read_only=True)

    class Meta:
        model = Block
        fields = ('id', 'name', 'block_type_name', 'project')


class TaskListSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    block_name = serializers.SerializerMethodField()
    executor_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'priority', 'order', 'block_name', 'creator_name', 'executor_name')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def get_executor_name(self, obj):
        if obj.executor is not None:
            return obj.executor.username
        return ''

    def get_block_name(self, obj):
        if obj.block is not None:
            return obj.block.name
        return ''


class TaskCreateSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField()
    creator = UserSerializer(read_only=True)
    block = BlockListSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def validate_priority(self, value):
        if value > 10 or value < 1:
            raise serializers.ValidationError('Task priority can be between 1 and 10')
        return value

    def validate_name(self, value):
        if len(value) > 100:
            raise serializers.ValidationError('Name 100 char max')
        return value


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    block = BlockListSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCommentListSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    task_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskComment
        fields = ('id', 'body', 'creator_name', 'task_name', 'created_at')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return  obj.creator.username
        return ''

    def get_task_name(self, obj):
        if obj.task is not None:
            return obj.task.name
        return ''


class TaskCommentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = '__all__'


class TaskDocumentListSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    task_name = serializers.SerializerMethodField()
    document_full = serializers.SerializerMethodField()

    class Meta:
        model = TaskDocument
        fields = ('id', 'document_full', 'creator_name', 'task_name')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def get_task_name(self, obj):
        if obj.task is not None:
            return obj.task.name
        return ''

    def get_document_full(self, obj):
        return self.context.get('base_url')[:-1] + obj.document.url


class TaskDocumentSerializer(serializers.Serializer):
    creator = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    document = serializers.FileField()