
# stackoverflow changes 23-06-2021
from datetime import datetime
from django.utils.timezone import make_aware

def store_token(user, token):
    user.access_token = token["access_token"]
    user.id_token = token["id_token"]
    user.token_expires = make_aware(datetime.fromtimestamp(token["expires_at"]))
    user.save()