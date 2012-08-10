from django.contrib import admin
from spa.models import Mix, Label, Release, ReleaseAudio, MixLike, Venue, Event

class DefaultAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user.get_profile()
        obj.save()

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Mix)
admin.site.register(MixLike)
#admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Release, DefaultAdmin)
admin.site.register(ReleaseAudio)
