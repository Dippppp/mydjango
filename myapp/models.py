from django.db import models

# 用户模型
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
