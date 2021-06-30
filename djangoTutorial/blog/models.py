from django.db import models
from django.utils import timezone

# this statements imports the User table from admin
from django.contrib.auth.models import User

# Create your models here.
# save data to database
# each class in a database
# each attribute in class is attribute in database

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class StudentProfiles(models.Model):
    cseusername = models.TextField()
    firstname = models.TextField()
    lastname = models.TextField()
    rollnumber = models.TextField()
    section = models.TextField()


    # defines what will the query return
    # def __str__(self):
    #     return((self.cseusername,self.firstname, self.lastname,self.rollnumber,self.section))
    
    class Meta:
        db_table = 'StudentProfiles'
        verbose_name = 'StudentProfiles'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # this tells when we call any profile object, what we mean is defined in this function
    def __str__(self):
        return f'{self.user.username} Profile'