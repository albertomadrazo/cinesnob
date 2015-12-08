from django.contrib import admin
from califas.models import Director, Title, UserProfile, Review, Friend

class DirectorAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

# class TitleAdmin(admin.ModelAdmin):
# 	list_display = ('name', 'director', 'users')

class ReviewAdmin(admin.ModelAdmin):
	list_display = ('user', 'title')

admin.site.register(Director, DirectorAdmin)
admin.site.register(Title)#, TitleAdmin)
admin.site.register(UserProfile)
admin.site.register(Friend)
admin.site.register(Review, ReviewAdmin)