from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class ChatGroup(models.Model):
    name = models.CharField(max_length=50)
    participants = models.ManyToManyField(User)


class ChatMessage(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_msgs")
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_msgs", null=True
    )

    def can_be_edited(self, user):
        # Only owner of the message can edit, if it's sent in last 5 minutes
        if user.pk == self.sender.pk:
            return timezone.now() <= self.timestamp + timezone.timedelta(minutes=5)
        return False


class ChatMessageStatus(models.Model):
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'chat_message')
