from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from locations.models import Location
from achievements.models import Achievement
# from taggit.managers import TaggableManager



    # username = models.CharField(max_length=150, null=False)

class User(models.Model):
    username = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    image = models.TextField(max_length=50, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    followers = models.ManyToManyField("self" )
    following = models.ManyToManyField("self")
    # message_threads = models.ManyToManyField("terp_messages.MessageThread", null=True, blank=True)
    creation_date = models.DateTimeField(null=True, default=now)
    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(null=True, default=now)

# #the action to take on the report, passing report history. only called when scheduled
# class ReportAction(CodeModel):
#     # name= models.CharField(max_length=150, null=False)
#     # creation_date = models.DateTimeField(default=now())
#     # attributes=models.TextField(null=False, default='{}', help_text='json attributes')
#     # code=models.TextField(null=True, help_text='Python Code To Execute')
#     def __str__(self):
#         return f"{self.name}: {self.description}"
#
#
# class ReportActionHistory(models.Model):
#     creation_date = models.DateTimeField(default=now)
#     attributes = models.TextField(null=False, default='{}', help_text='json attributes')
#     status = models.CharField(choices=(('Running', 'Running'), ('Completed', 'Completed'), ('Completed With Errors', 'Completed With Errors')),default='Running', max_length=150)
#     report_action=models.ForeignKey(ReportAction,null=False, blank=True,on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.report_action.name} {self.status} {self.creation_date}"
# class Report(CodeModel):
#     short_name=models.CharField(max_length=25, default="report_name", help_text="the short name of the report (used when downloading multiple reports)")
#     creation_date = models.DateTimeField(null=True, default=now)
#     connection = models.ForeignKey(Connection,blank=False, null=True, on_delete=models.CASCADE)
#     code = models.TextField(null=False)
#     type = models.CharField(null=False, default='basic', max_length=50)
#     xaxis_label = models.CharField(null=True,blank=True,max_length=50)
#     yaxis_label = models.CharField(null=True,blank=True,max_length=50)
#     attributes = models.TextField(default='{}')
#     alert_trigger =models.ForeignKey(ReportTrigger,null=True,blank=True, on_delete=models.CASCADE)
#     group = models.ForeignKey("auth.Group", null=True, blank=True,on_delete=models.CASCADE)
#     action = models.ForeignKey(ReportAction, null=True, blank=True,on_delete=models.CASCADE)
#     tags = TaggableManager(blank=True)
#
#     def __str__(self):
#         return f"{self.name}: {self.description}"
#
#     #todo add scheduling piece
#     #schedule = models.Choices(choices=(("), ("Hourly", "Hourly"),("Daily", "Daily")))