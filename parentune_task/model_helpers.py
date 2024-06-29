from django.db import models

class ChildGenderChoices(models.TextChoices):
    MALE = (
        "MALE",
        "MALE",
    )
    FEMALE = (
        "FEMALE",
        "FEMALE",
    )
    OTHERS = ("OTHERS", "OTHERS",)
