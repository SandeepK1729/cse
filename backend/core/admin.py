from django.contrib import admin

from .models import User, Site, SearchHistory


admin.site.register(User)
admin.site.register(Site)
admin.site.register(SearchHistory)
