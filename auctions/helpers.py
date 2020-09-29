def getBidInfo(Bid, listing, request):
    allBids = Bid.objects.filter(listing=listing)
    lastBid = allBids.last()
    totalBids = allBids.count()
    if lastBid == None:
        result = "No Bids Yet"
        return {
            "result": result,
            "winner": None,
        }
    else:
        result = f"{totalBids} bids so far."
    
    lastBidder = lastBid.by

    if lastBidder == request.user.username:
        result += "Your bid is the current bid!"

    return {
        "result": result,
        "winner": lastBidder,
    }

def getComments(Comment, listing, request):
    allComments = Comment.objects.filter(listing=listing)
    try:
        allComments[0]
    except IndexError:
        allComments = None

    return allComments

def checkWatching(WatchList, listing, request):
    watching = WatchList.objects.filter(savedby=request.user.username, listing=listing).count()
    if (watching > 0):
        return True
    else:
        return False