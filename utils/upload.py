import shutil
import os


def document_path(instance, filename):
    from main.models import TaskDocument
    if type(instance) == TaskDocument:
        return f'{instance._meta.verbose_name_plural}/Task: {instance.task.id}/{filename}'
    return f'{instance._meta.verbose_name_plural}/{instance.id}/{filename}'


def avatar_path(instance, filename):
    return f'avatars/{instance.id}/{filename}'


def task_delete_path(document):
    path = os.path.abspath(os.path.join(document.path, '..'))
    if os.path.isdir(path):
        shutil.rmtree(path)