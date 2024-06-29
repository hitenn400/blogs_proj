from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(ParentInfo)
class ParentInfo(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = (
        "id",
        "name",
        "city",
    )
    list_filter = ("city",)

@admin.register(ChildInfo)
class childInfo(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = (
        "id",
        "name",
        "age",
        "gender",
        "parent_details",
    )
    list_filter = ("parent_details","gender")


@admin.register(Blogs)
class Blogs(admin.ModelAdmin):
    ordering = ["-modified"]
    list_display = (
        "id",
        "title",
        "content",
    )
    list_filter = ("title",)



