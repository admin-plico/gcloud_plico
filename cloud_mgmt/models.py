from django.db import models
import re

from fernet_fields import EncryptedTextField
from django.contrib.auth.models import User
from aSync_utils.project_mgm_constants import *
from aSync_utils.asana_api import *
from aSync_utils.db_utils import *

# Create your models here.


from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField
import json


class GoogleCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()

    def to_dict(self):
        return {
            'token': self.token,
            'refresh_token': self.refresh_token,
            'token_uri': self.token_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scopes': json.loads(self.scopes),
        }


class GoogleServiceAccount(models.Model):
    name = models.CharField(max_lenght=100, unique=True)
    credentials = EncryptedTextField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AsanaCredentials(models.Model):
    # todo:adjust credentials savings to asana's need
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.TextField()
    token_type = models.TextField()


class DriveFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=128)
    name = models.CharField(max_length=512)
    last_updated = models.DateTimeField(auto_now=True)


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_serial = models.CharField(max_length=5, unique=True)
    project_gid = models.CharField(max_length=200, null=True, blank=True)
    milestone_gid = models.CharField(max_length=200, null=True, blank=True)
    file_id = models.CharField(max_length=200, null=True, blank=True)
    start_on = models.DateField("project Starts", null=True, blank=True)
    due_on = models.DateField("project Due", null=True, blank=True)

    def save(self, *args, **kwargs):
        s_pat = r"^\d{5}"
        s = re.match(s_pat, str(self.project_name))
        if s and not self.project_serial:

            self.project_serial = s[0]
        else:
            next_serial = int(Project.objects.order_by('-project_serial').first()) + 1
            self.project_serial = next_serial
            pn = f"{next_serial} {self.project_name}"
            self.project_name = pn
            # sync_project(self) # Only turn this part on during production !!!

        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_name


class Folder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=200)

    def __str__(self):
        return self.folder_name


class Portfolio(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.portfolio_name
from django.db import models

# Create your models here.
