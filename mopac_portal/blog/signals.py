from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post
from django.conf import settings
import shutil
import os


@receiver(post_delete, sender=Post)
def delete_on_post_del(sender, instance, **kwargs):
    try:
        if os.path.isdir(settings.MEDIA_ROOT+'/'+str(instance.id)):
            shutil.rmtree(settings.MEDIA_ROOT+'/'+str(instance.id))
    except:
        print('error deleting file')
        print(settings.MEDIA_ROOT+'/'+str(instance.id))
    
