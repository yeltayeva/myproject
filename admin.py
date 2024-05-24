from django.contrib import admin
from .models import Document, UserProfile, Department

admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Department)
