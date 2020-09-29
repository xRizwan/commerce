from django.contrib import admin
from .models import Listings, Bid, User, ListingComment, Categories, WatchList

# Register your models here.
admin.site.register(Listings)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(ListingComment)
admin.site.register(Categories)
admin.site.register(WatchList)