from django.shortcuts import render
from .models import Favorites


def favorites(self, request, pk):
    post = self.get_object()
    user = request.user
    if request.method == 'POST':
        if user.favorites.filter(post=post).exists():
            return Response('This post is already in favorites!',
                            status=400)
        Favorites.objects.create(owner=user, post=post)
        return Response('Added to favorites!', status=201)
    else:
        if user.favorites.filter(post=post).exists():
            user.favorites.filter(post=post).delete()
            return Response('Deleted from favorites!', status=204)
        return Response('Post is not found!', status=400)
