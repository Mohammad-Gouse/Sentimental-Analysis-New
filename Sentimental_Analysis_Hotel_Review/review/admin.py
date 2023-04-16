from django.contrib import admin

from review.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display=('user_name', 'description', 'response')

admin.site.register(Review, ReviewAdmin)

# Register your models here.
