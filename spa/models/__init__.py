from _BaseModel import _BaseModel
from UserProfile import UserProfile
from _Activity import _Activity
from Recurrence import Recurrence
from Comment import Comment
from Venue import Venue
from Event import Event
from Label import Label
from Mix import Mix
from MixLike import MixLike
from MixPlay import MixPlay
from Tracklist import Tracklist
from PurchaseLink import PurchaseLink
from Release import Release
from UserFavourite import UserFavourite

from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app

# Prevent interactive question about wanting a superuser created.  (This
# code has to go in this otherwise empty "models" module so that it gets
# processed by the "syncdb" command during database creation.)

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser")