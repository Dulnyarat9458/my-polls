from django.db import models


class Poll(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.choice_text
