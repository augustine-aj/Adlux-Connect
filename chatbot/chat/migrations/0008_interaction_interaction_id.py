# Generated by Django 5.1.3 on 2025-01-15 15:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_chatsession_interaction_delete_chathistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='interaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
