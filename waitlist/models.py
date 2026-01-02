from django.db import models


class WaitlistApplication(models.Model):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.confirmation_token:
            self.confirmation_token = self.token_urlsafe(16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
