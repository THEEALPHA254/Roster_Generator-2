from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Member(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    roles = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, default=1)  # Ensure default value exists in Role table
    contact = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class Roster(models.Model):
    sunday_date = models.DateField()
    members = models.ManyToManyField(Member, related_name='rosters')
    roles = models.ManyToManyField(Role, related_name='rosters')

    def __str__(self):
        return f"Roster for {self.sunday_date}"
