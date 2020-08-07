from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Widget(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Widget)
def widget_saved(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('widgets', {
        'type': 'widget.save',
        'data': {
            'message': f'Widget [{instance.id}]: {instance.name} saved.'
        }
    })
