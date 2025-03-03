# Generated by Django 5.1.3 on 2024-12-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_chathistory_chat_chathi_user_id_f2b261_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='chat_session_end_timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='chathistory',
            name='chat_session_id',
            field=models.UUIDField(editable=False, unique=True),
        ),
    ]
