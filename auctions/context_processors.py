from .models import WatchList

def add_variable_to_context(request):
    watching = 0
    if (request.user.is_authenticated):
        watching = WatchList.objects.filter(savedby=request.user.username).count()

    return {
        'watching': watching,
    }