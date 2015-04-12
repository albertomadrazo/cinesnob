from django.contrib import admin
from califas.models import Director, Title, UserProfile, Friend

class DirectorAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('director_name',)}

class TitleAdmin(admin.ModelAdmin):
	list_display = ('movie_name', 'director')

admin.site.register(Director, DirectorAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(UserProfile)
admin.site.register(Friend)
