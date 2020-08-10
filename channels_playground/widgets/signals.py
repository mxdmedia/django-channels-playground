from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Widget

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=Widget)
def widget_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if created:
        action = 'CREATED'
    else:
        action = 'UPDATED'

    async_to_sync(channel_layer.group_send)('widgets', {
        'type': 'widget.crud',
        'data': {
            'model': 'Widget',
            'id': instance.id,
            'action': action,
            'message': f'Widget [pk={instance.id}]: {instance.name} {action.lower()}.'
        }
    })


@receiver(post_delete, sender=Widget)
def widget_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)('widgets', {
        'type': 'widget.crud',
        'data': {
            'model': 'Widget',
            'id': instance.id,
            'action': 'DELETED',
            'message': f'Widget [pk={instance.id}]: {instance.name} deleted.'
        }
    })
