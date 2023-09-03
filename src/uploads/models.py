from django.db import models
from users.models import CustomUser
# Create your models here.

class Upload(models.Model):

    def get_upload_path(self, file_name):
        return f"submissions/{self.author.email}/{file_name}"

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(null=True, upload_to=get_upload_path)
    state_choices = (("D", "DELETED",), ("E", "EDITED",), ("N", "NEW"))
    state = models.CharField(choices=state_choices, default="N", max_length=10)


