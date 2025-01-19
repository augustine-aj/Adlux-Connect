# Generated by Django 5.1.3 on 2024-12-19 03:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chathistory_has_interaction_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='chathistory',
            name='chat_chathi_user_id_f2b261_idx',
        ),
        migrations.RenameField(
            model_name='chathistory',
            old_name='session_id',
            new_name='chat_session_id',
        ),
        migrations.AddIndex(
            model_name='chathistory',
            index=models.Index(fields=['user', 'chat_session_id'], name='chat_chathi_user_id_1f5582_idx'),
        ),
        migrations.AddIndex(
            model_name='chathistory',
            index=models.Index(fields=['user', 'chat_session_start_timestamp'], name='chat_chathi_user_id_62ece0_idx'),
        ),
    ]
