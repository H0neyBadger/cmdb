from django.db import models
from django.contrib.auth.models import User, Group


class Team(Group):
    snow_name  = models.CharField(max_length=100)
    email  = models.CharField(max_length=100, help_text="E-mail distribution list")
    phone = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User, 
        null=True, 
        related_name="manager",
        on_delete=models.PROTECT
    )
    technical_contact = models.ForeignKey(
        User, 
        null=True, 
        related_name="technical_contact", 
        on_delete=models.PROTECT
    )
    ciso = models.ForeignKey(
        User, 
        null=True, 
        related_name="ciso", 
        help_text="chief information security officer", 
        on_delete=models.PROTECT
    )

