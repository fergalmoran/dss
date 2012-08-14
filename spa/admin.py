from django.contrib import admin
from spa.models.Release import Release
from spa.models.Event import Event
from spa.models.Label import Label
from spa.models.Mix import Mix
from spa.models.MixLike import MixLike
from spa.models.Release import ReleaseAudio
from spa.models.Venue import Venue

class DefaultAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user.get_profile()
        obj.save()

admin.site.register(Mix)
admin.site.register(MixLike)
#admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Release, DefaultAdmin)
admin.site.register(ReleaseAudio)
admin.site.register(Venue)
admin.site.register(Event)
