from __future__ import unicode_literals

from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def validateUser(self, post_data):
        errors = []
        if len(post_data['name']) == 0:
            errors.append('Name cannot be empty')
        if len(post_data['username']) == 0:
            errors.append('Username cannot be empty')
        if not re.search(r'\w+\@\w+.\w+', post_data.get('email')):
            errors.append('Must enter valid email')
        if len(post_data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if not post_data['password'] == post_data['confirm_password']:
            errors.append('Password must match confirm password')
        if len(errors) == 0:
            return True,
        else:
            return False, errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    favorites = models.ManyToManyField("Quote", related_name= "favorites", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def validateQuote(self, post_data):
        errors = []
        if len(post_data['author']) < 3:
            errors.append('Author must be more than 3 characters')
        if len(post_data['content']) < 10:
            errors.append('Quote must be more than 10 characters')
        if len(errors) == 0:
            return True,
        else:
            return False, errors

class Quote(models.Model):
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name = 'authored_quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
