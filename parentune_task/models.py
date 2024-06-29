from django.db import models

# Create your models here.
from django.db import models
from django.db.models import *
from django_extensions.db.models import TimeStampedModel
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User
from parentune_task.model_helpers import ChildGenderChoices

from django.db import models

class AgeGroup(models.Model):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    age_range = models.IntegerField(unique=True)  # Example format: "0-2", "3-5", "6-8", etc.

    def __str__(self):
        return self.age_range


class ParentInfo(TimeStampedModel, models.Model):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    feed_preferences = models.JSONField(default={}, blank=True, null=True)
    class Meta:
        db_table = "parent_info"
        get_latest_by = "modified"

    def __str__(self):
        return str(self.id)


class ChildInfo(TimeStampedModel, models.Model):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=32,blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.CharField(choices=ChildGenderChoices.choices, blank=True, null=True,max_length=6)
    meta_info = models.JSONField(default={}, blank=True, null=True)
    parent_details = models.ForeignKey(ParentInfo,related_name="child_details",on_delete=models.CASCADE)
    class Meta:
        db_table = "child_info"
        get_latest_by = "modified"

    def __str__(self):
        return str(self.id)


class Blogs(TimeStampedModel,models.Model):
    id = ShortUUIDField(
        length=8,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        primary_key=True,
        editable=False,
    )
    title = models.CharField(max_length=60)
    content = models.TextField()
    suitable_for_age = models.ManyToManyField(AgeGroup)
    suitable_for_gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='blog_user', on_delete=models.CASCADE)
    class Meta:
        db_table = "blogs"
        get_latest_by = "modified"

    def __str__(self):
        return str(self.id)