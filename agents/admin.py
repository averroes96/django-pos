from django.contrib import admin
from django.contrib.auth.models import User

from agents.models import Agent

# Register your models here.

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    
    list_display = ["__str__", "phone", "address", "is_admin"]
    search_fields = ["__str__", "phone", "address"]
    list_filter = ["is_admin"]
    list_per_page = 16