# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from .models import Leave, Status






