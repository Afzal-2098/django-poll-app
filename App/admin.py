from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["uid", "owner", "text", "pub_date", "active"]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["uid", "question", "choice_text"]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["uid", "user", "question", "choice"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "phone"]
