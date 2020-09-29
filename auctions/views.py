from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listings, Bid, ListingComment, Categories, WatchList
from . import helpers


def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listings.objects.filter(isClosed=False),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if (not request.user.is_authenticated):
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        url = request.POST["url"]
        category = None
        if request.POST["category"] != '':
            newcategory = Categories(Categories=request.POST["category"])
            newcategory.save()
            category = newcategory


        listing = Listings(title=title, description=description, bid=bid, url=url, by=request.user.username, category=category)
        listing.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/createListing.html")

def listing(request, listing_id):

    try:
        listing = Listings.objects.get(id=listing_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    if listing.by == request.user.username:
        isCurrent = True
    else:
        isCurrent = False

    bidInfo = helpers.getBidInfo(Bid, listing, request)
    comments = helpers.getComments(ListingComment, listing, request)
    isWatched = helpers.checkWatching(WatchList, listing, request)

    if request.method == "POST":
        if 'watchlist' in request.POST:
            if(request.POST['watchlist'] == "add"):
                if (not isWatched):
                    added = WatchList(listing=listing, savedby=request.user.username)
                    added.save()
                    isWatched = True
            else:
                if (isWatched):
                    removed = WatchList.objects.get(listing=listing, savedby=request.user.username)
                    removed.delete()
                    isWatched = False

            return render(request, "auctions/listing.html", {
                'data': listing,
                "bidInfo": bidInfo,
                "isCurrent": isCurrent,
                "comments": comments,
                "isWatched": isWatched,
            })

        if "finish" in request.POST and request.POST["finish"] == 'end':
            bidInfo = helpers.getBidInfo(Bid, listing, request)
            winner = bidInfo["winner"]
            if winner == None:
                winner = request.user.username
                
            Listings.objects.filter(pk=listing_id).update(isClosed=True, winner=winner)
            listing=Listings.objects.get(id=listing_id)
            return render(request, "auctions/listing.html", {
                'data': listing,
                "success": "This Auction has Been Finished",
                "comments": comments,
                "isWatched": isWatched,
            })
        
        if "comment" in request.POST:
            newComment = ListingComment(by=request.user.username, listing=listing, message=request.POST["comment"])
            newComment.save()
            bidInfo = helpers.getBidInfo(Bid, listing, request)
            comments = helpers.getComments(ListingComment, listing, request)
            return render(request, "auctions/listing.html", {
                'data': listing,
                "bidInfo": bidInfo,
                "isCurrent": isCurrent,
                "comments": comments,
                "isWatched": isWatched,
            })
        

        amount = request.POST["bid"]
        if float(amount) <= float(listing.bid):
            return render(request, "auctions/listing.html", {
                'data': listing,
                "message": "You're Bidding Too Less",
                "bidInfo": bidInfo,
                "isCurrent": isCurrent,
                "comments": comments,
                "isWatched": isWatched,
            })

        Listings.objects.filter(pk=listing_id).update(bid=amount)
        listing=Listings.objects.get(id=listing_id)

        by = request.user.username
        newBid = Bid(by=by, amount=amount, listing=listing)
        newBid.save()

        bidInfo = helpers.getBidInfo(Bid, listing, request)

        return render(request, "auctions/listing.html", {
            'data': listing,
            "success": "Success!",
            "bidInfo": bidInfo,
            "isCurrent": isCurrent,
            "comments": comments,
            "isWatched": isWatched,
        })

    return render(request, "auctions/listing.html", {
        'data': listing,
        "bidInfo": bidInfo,
        "isCurrent": isCurrent,
        "comments": comments,
        "isWatched": isWatched,
    })

def watchList(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    
    watched = WatchList.objects.filter(savedby=request.user.username)

    return render(request, 'auctions/watchList.html', {
        "list": watched
    })

def categories(request):
    allcategories = Categories.objects.all()

    return render(request, 'auctions/categories.html', {
        'catlist' : allcategories
    })

def catListings(request, catname):
    obtained = Categories.objects.get(Categories=catname)
    all = Listings.objects.filter(category=obtained)

    return render(request, 'auctions/catListings.html', {
        'name': catname,
        'list': all,
    })