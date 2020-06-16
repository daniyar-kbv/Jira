from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from main.models import Task, TaskDocument, Project, Block
from utils.upload import task_delete_path
from utils.other import find_type
from constants import BLOCK_TYPES


@receiver(post_delete, sender=TaskDocument)
def task_deleted(sender, instance, **kwargs):
    if instance:
        task_delete_path(document=instance.document)


@receiver(post_save, sender=Project)
def project_created(sender, instance, created=True, **kwargs):
    for block_type in BLOCK_TYPES:
        Block.objects.create(block_type=block_type[0], project=instance)


@receiver(post_save, sender=Block)
def block_created(sender, instance, created=True, **kwargs):
    if (not instance.name) or instance.name == '':
        if instance.block_type:
            new_name = find_type(BLOCK_TYPES, instance.block_type).lower().replace('_', ' ')
            new_name = f'{new_name[0].upper()}{new_name[1:]}'
            instance.name = new_name
            instance.save()