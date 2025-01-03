# Generated by Django 5.1.3 on 2024-12-20 03:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_chathistory_chat_session_end_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='chat_session_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
