from django.contrib import admin

from .models import Category, Listings, User, Bid, Comments
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Bid)
admin.site.register(Comments)
