# Generated by Django 5.1.3 on 2024-12-17 15:57

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_input', models.TextField()),
                ('generated_response', models.TextField()),
                ('response_time', models.DurationField()),
                ('chat_session_title', models.CharField(blank=True, max_length=255, null=True)),
                ('chat_session_end_timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('response_feedback', models.IntegerField(blank=True, choices=[(1, 'Bad'), (2, 'Average'), (3, 'Good'), (4, 'Excellent')], null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'session_id'], name='chat_chathi_user_id_f2b261_idx')],
            },
        ),
    ]