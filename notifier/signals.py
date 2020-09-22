from asgiref.sync import async_to_sync
from channels import DEFAULT_CHANNEL_LAYER
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifier.models import Food


@receiver(post_save, sender=User)
def announce_new_user(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # They have different purposes.async_to_sync turns an awaitable into a synchronous callable
        async_to_sync(channel_layer.group_send)(
            # gossip is group name
            "gossip", {
                "type": "user.gossip",
                "event": "NewUser",
                "username": instance.username
            }
        )


@receiver(post_save, sender=Food)
def announce_new_food(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # They have different purposes.async_to_sync turns an awaitable into a synchronous callable
        async_to_sync(channel_layer.group_send)(
            # gossip is group name
            "gossip", {
                "type": "food.gossip",
                "event": "NewFood",
                "food_name": instance.id
            }
        )
