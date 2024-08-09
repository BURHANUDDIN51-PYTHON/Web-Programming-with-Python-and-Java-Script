from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.category}'
    
    
    
class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    url = models.CharField(blank=True, max_length=6000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='categories')
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True, blank=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name='users_watchlist')
    
    def __str__(self):
        return f'Title: {self.title}, Description: {self.description}, Category:{Category}, {self.watchlist}'
    
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10,decimal_places=2)
    listing = models.ForeignKey(Listings, blank=True, null=True, related_name="bids", on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, blank=True, null=True, related_name="bidder", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Listing: {self.listing.title} Bid: {self.bid} Bidder:{self.bidder}"
    

class Comments(models.Model):
    comment = models.CharField(max_length=600)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='user_comments' )
    
    def __str__(self):
        return f"{self.user}: {self.comment}"