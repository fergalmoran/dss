from django.contrib import admin
from spa.models.genre import Genre
from spa.models.userprofile import UserProfile
from spa.models.chatmessage import ChatMessage
from spa.models.recurrence import Recurrence
from spa.models.release import Release
from spa.models.event import Event
from spa.models.label import Label
from spa.models.mix import Mix
from spa.models.activity import _Activity
from spa.models.mixlike import MixLike
from spa.models.mixplay import MixPlay
from spa.models.mixfavourite import MixFavourite
from spa.models.release import ReleaseAudio
from spa.models.venue import Venue


class DefaultAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user.get_profile()
        obj.save()


admin.site.register(Mix)
admin.site.register(_Activity)
admin.site.register(MixLike)
admin.site.register(MixPlay)
admin.site.register(MixFavourite)
admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Release, DefaultAdmin)
admin.site.register(ReleaseAudio)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Recurrence)
admin.site.register(ChatMessage)
