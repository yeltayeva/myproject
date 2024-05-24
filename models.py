from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)  # Явное определение первичного ключа
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    # Дополнительные поля профиля пользователя

    def __str__(self):
        return self.username

class Document(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('signed', 'Signed'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='signed_documents')
    signed_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_documents', default=1)
    is_sent = models.BooleanField(default=False)
    is_viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    is_viewed_by_recipient = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Department(models.Model): #отдел
    id = models.AutoField(primary_key=True)  # Явное определение первичного ключа
    name = models.CharField(max_length=100)
    # Другие поля, такие как описание и руководитель

    def __str__(self):
        return self.name

class AccessPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    # Другие поля, определяющие права доступа
