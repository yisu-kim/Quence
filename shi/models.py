from django.db import models
from django.utils import timezone


class Shi(models.Model):
    input_text = models.CharField(max_length=200)
    output_text = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.input_text


class Choice(models.Model):
    input = models.ForeignKey(Shi, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
