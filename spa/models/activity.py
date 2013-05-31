from django.db import models
from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel

ACTIVITYTYPES = (
    ('p', 'played'),
    ('d', 'downloaded'),
    ('l', 'liked'),
    ('f', 'favourited'),
)


class Activity(_BaseModel):
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    activity_type = models.CharField(max_length=1, choices=ACTIVITYTYPES)

    def __unicode__(self):
        return "%s" % self.date

    def get_verb_passed(self):
        verb = [item for item in ACTIVITYTYPES if item[0] == self.activity_type][0]
        return str(verb[1])

    def get_object_singular(self):
        return "mix"

    def get_object_name(self):
        return "mix"

    def get_object_url(self):
        return "url"

