from django.db import models
from authentication.models import User
# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=20,blank=True,null=True)
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title