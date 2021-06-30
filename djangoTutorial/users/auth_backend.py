from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from blog.models import StudentProfiles

class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, rollnumber=None):
        try:
            studentProfile = StudentProfiles.objects.get(rollnumber=rollnumber)
            print(studentProfile)
            user = User.objects.get(username=studentProfile.cseusername)
            if user:
                return user, studentProfile
        except User.DoesNotExist:
            return None

    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None
