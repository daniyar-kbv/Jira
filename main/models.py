from authe.models import MainUser
from constants import PROJECT_STATUSES, PROJECT_IN_PROCESS, PROJECT_TYPES, PROJECT_DEVELOPMENT, PROJECT_DONE, \
    PROJECT_FROZEN, PROJECT_OPTIMIZATION, BLOCK_TYPES, BLOCK_BACKLOG
from django.db import models
from django.db.models import F, Q, Count, Avg, Max, Min, Sum
from utils.upload import document_path
from utils.validators import validate_extension, validate_file_size

import datetime as dt


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(project_type=PROJECT_OPTIMIZATION)

    def optimization_projects(self):
        return self.filter(project_type=PROJECT_OPTIMIZATION)

    def development_projects(self):
        return self.filter(project_type=PROJECT_DEVELOPMENT)

    def filter_by_project_type(self, project_type):
        return self.filter(project_type=project_type)

    def frozen_projects(self):
        return self.filter(status=PROJECT_FROZEN)

    def in_process_projects(self):
        return self.filter(status=PROJECT_IN_PROCESS)

    def done_projects(self):
        return self.filter(status=PROJECT_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)

    def avg_blocks(self):
        return self.aggregate(Avg('blocks'))


class DescBase(models.Model):
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        abstract = True


class Project(DescBase):
    name = models.CharField(max_length=100, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=PROJECT_STATUSES, default=PROJECT_IN_PROCESS)
    project_type = models.PositiveSmallIntegerField(choices=PROJECT_TYPES, default=PROJECT_DEVELOPMENT)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='projects')

    objects = ProjectManager()

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    block_type = models.PositiveSmallIntegerField(choices=BLOCK_TYPES, default=BLOCK_BACKLOG)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')

    def __str__(self):
        return self.name


class TaskManager(models.Manager):
    def done_user(self, user):
        return self.filter(executor=user, block__block_type=4)

    def not_done_user(self, user):
        return self.filter(Q(executor=user) & ~Q(block__block_type=4))

    def today_user(self, user):
        return self.filter(Q(block__block_type__in=[2, 3]) & Q(executor=user))

    def unassigned_tasks(self):
        return self.filter(executor__isnull=True)

    def high_priority(self):
        return self.filter(priority__gte=7)

    def documents_count(self):
        return self.annotate(documents_count=Count('documents'))

    def documents_comments_count(self):
        return self.annotate(Count('documents'), Count('comments'))

    def comments_grouped_by_name(self):
        return self.values('name').annotate(Count('comments'))

    def documents_gte_comments(self):
        return self.filter(documents_count__gte=F('comments_count'))


class Task(DescBase):
    name = models.CharField(max_length=100, blank=False, null=False)
    priority = IntegerRangeField(min_value=1, max_value=10, null=False)
    order = models.IntegerField(null=False)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_creator')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_executor', null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')

    objects = TaskManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskDocument(models.Model):
    document = models.FileField(upload_to=document_path, validators=[validate_file_size, validate_extension])
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='documents')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')

    class Meta:
        verbose_name = 'TaskDocument'
        verbose_name_plural = 'TaskDocuments'


class TaskCommentManager(models.Manager):
    def last_month(self):
        today = dt.datetime.now()
        month_ago = today - dt.timedelta(days=30)
        return self.filter(Q(created_at__year=today.year)
                           & ((Q(created_at__month=month_ago.month) & Q(created_at__day__gte=today.day))
                              | (Q(created_at__month=today.month) & Q(created_at__day__lte=today.day))))

    def by_date(self):
        return self.all().order_by('-created_at')


class TaskComment(models.Model):
    body = models.CharField(max_length=300, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    objects = TaskCommentManager()

