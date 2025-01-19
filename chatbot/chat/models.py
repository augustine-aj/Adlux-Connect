from django.db import models
import uuid
from login.models import CustomUser
from django.utils import timezone

class ChatSession(models.Model):
    """
    Represents a chat session for a user. Only one session can be active for a user at a time.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)  # Chat title initialized from first input
    is_active = models.BooleanField(default=True)  # Only one active session per user
    created_at = models.DateTimeField(auto_now_add=True)  # Session start time
    ended_at = models.DateTimeField(null=True, blank=True)  # Session end time

    def deactivate(self):
        """
        Deactivates the current session.
        """
        self.is_active = False
        self.ended_at = timezone.now()
        self.save()

    @staticmethod
    def manage_user_session(user):
        """
        Ensures only one active session exists per user. Deactivates other sessions if necessary.
        """
        active_sessions = ChatSession.objects.filter(user=user, is_active=True)
        if active_sessions.exists():
            active_sessions.update(is_active=False, ended_at=timezone.now())
        return ChatSession.objects.create(user=user)  # Create a new active session without a title initially


class Interaction(models.Model):
    interaction_id = models.UUIDField(
        default=uuid.uuid4,  # Ensures a unique default value for every new row
        unique=True,
        editable=False
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='interactions')
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.IntegerField(
        blank=True, null=True,
        choices=[
            (1, 'Bad'),
            (2, 'Average'),
            (3, 'Good'),
            (4, 'Excellent'),
        ]
    )
