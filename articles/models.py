from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import User
from categories.models import Category


class Article(TimeStampedModel):
    owner = models.ForeignKey(User)
    title = models.TextField(default='no title')
    body = models.TextField()
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    body = models.TextField()

    def __str__(self):
        return self.body


class Tag(TimeStampedModel):
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
