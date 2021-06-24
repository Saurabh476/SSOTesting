from django.contrib import admin
from .models import Post,StudentProfiles
from .models import Profile
# Register your models here.
# registering database for the admin page

admin.site.register(Post)
admin.site.register(StudentProfiles)
admin.site.register(Profile)