from django.db import models
from django.utils.timezone import now
class Configuration(models.Model):#config class, stores kv pairs
    created = models.DateField(null=False, default=now)
    key = models.CharField(max_length=250, null=False)
    value= models.TextField(null=False)
    description=models.TextField(null=False)
    def __str__(self):
        return f"{self.key}"

class ConfigurationJSON(models.Model):#config class, stores json by name
    created = models.DateField(null=False, default=now)
    name = models.CharField(max_length=250, null=False)
    value= models.TextField(null=False, default="{}")
    description=models.TextField(null=False)
    def __str__(self):
        return f"{self.name}"
class NavigationLink(models.Model):
    name=models.CharField(max_length=100, null=False)
    description=models.TextField(null=False)
    location= models.CharField(max_length=500, null=False)
    group = models.ForeignKey("auth.Group", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.location}"