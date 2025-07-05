from django.db import models

# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    choice = models.ForeignKey('polls.Choice', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')

    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"