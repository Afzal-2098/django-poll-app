from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(User):
    phone = PhoneNumberField(null=False, blank=False, unique=True)

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class Question(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Choice(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text

class Vote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'