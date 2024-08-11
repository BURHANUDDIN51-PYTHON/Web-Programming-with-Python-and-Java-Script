from django.contrib import admin
from .models import User, New_post, Followers, Following

# Register your models here.
admin.site.register(User)
admin.site.register(New_post)
admin.site.register(Followers)
admin.site.register(Following)
