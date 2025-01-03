from django.db import models
import uuid
from login.models import CustomUser
from django.utils import timezone

class ChatHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_history')
    chat_session_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    user_input = models.TextField()
    generated_response = models.TextField()
    response_time = models.DurationField(blank=True, null=True)
    chat_session_start_timestamp = models.DateTimeField(default=timezone.now)
    chat_session_title = models.CharField(max_length=255, blank=True, null=True)
    chat_session_end_timestamp = models.DateTimeField(null=True)
    has_interaction = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    response_feedback = models.IntegerField(blank=True, null=True, choices=[(1, 'Bad'), (2, 'Average'), (3, 'Good'), (4, 'Excellent')])

    class Meta:
        indexes = [
            models.Index(fields=['user', 'chat_session_id']),
            models.Index(fields=['user', 'chat_session_start_timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username}_{self.chat_session_id}"

    def deactivate_session(self):
        """
        Deactivates this session by setting is_active to False and recording the end timestamp.
        """
        self.is_active = False
        self.chat_session_end_timestamp = timezone.now()
        self.save()

    def start_new_session(self):
        """
        Starts a new chat session with a unique session ID and sets the session start time.
        """
        self.chat_session_id = uuid.uuid4()
        self.is_active = True
        self.chat_session_start_timestamp = timezone.now()
        self.chat_session_title = None
        self.save()

    def set_chat_session_title(self, title=None):
        """
        Updates the chat session title after receiving the first user input or using a default value.
        """
        if not self.chat_session_title:
            self.chat_session_title = title or f"Session_{self.chat_session_id}"
            self.save()