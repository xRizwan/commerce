from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    Categories = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.Categories}"

class Listings(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    title = models.CharField(max_length=150)
    description = models.TextField()
    bid = models.FloatField()
    url = models.URLField(blank=True, null=True)
    by = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categorys", blank=True, null=True)
    isClosed = models.BooleanField(default=False)
    winner = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"""
        {self.id}\n
        title: {self.title},\n
        description: {self.description},\n
        bid: {self.bid},\n
        by: {self.by},\n
        url: {self.url},\n
        category: {self.category}
        """

class Bid(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
    by = models.CharField(max_length=120)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.id} : {self.listing}"

class ListingComment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
    by = models.CharField(max_length=120)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listingComments")

    def __str__(self):
        return f"by : {self.by}\n message: {self.message}\n for: {self.listing}\n"

class WatchList(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    savedby = models.CharField(max_length=150)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchedListings")

    def __str__(self):
        return f"savedby: {self.savedby}\n for: {self.listing}\n"