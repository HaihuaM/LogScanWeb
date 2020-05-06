from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
      return self.user.username
# Create your models here.

class LogFile(models.Model):
    LogPath = models.CharField(max_length=512)
    FileName = models.CharField(max_length=512)
    PostedDate = models.DateField(auto_now_add=True)
    PostedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    AnalyzeStatus = models.CharField(max_length=20)


