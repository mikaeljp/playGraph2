from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from lib.bggapi import get_bgg_user, get_bgg_plays
from playgraph.models import BggUser
from playgraph.serializers import BggUserSerializer


class PlayGraphView(View):
    """
    Initial page load will not contain bgg user id
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'playgraph/play_graph_home.html')


class PlayGraphDataView(View):
    """
    This view is used by angular to get cached data (if any) and post data to cache
    It accepts and returns JSON data
    """
    def get(self, request, bgg_id, *args, **kwargs):
        if request.GET.get('refresh'):
            BggUser.objects.filter(pk=bgg_id).delete()
        try:
            user = BggUser.objects.get(pk=bgg_id)
            serializer = BggUserSerializer(user)
        except BggUser.DoesNotExist:
            # the user has not been cached, fetch the details from BGG and cache them
            data = get_bgg_user(bgg_id)
            serializer = BggUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        plays = get_bgg_plays(bgg_id)
        return JsonResponse(plays, safe=False)
