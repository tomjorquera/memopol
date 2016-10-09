import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.views import generic

from representatives.models import Chamber, Representative
from memopol_themes.models import Theme
from memopol_scores.models import ThemeScore


class ThemeScoresJSONView(generic.View):
    """
    Returns JSON with all score points for a given theme as follows:

    {
        "theme": "<theme_name>",
        "scores": [-99, -98, -98, ... 100, 102, 102, 102]
    }
    """

    def get(self, request, *args, **kwargs):
        try:
            theme = Theme.objects.get(id=kwargs['theme'])
        except Theme.DoesNotExist:
            return HttpResponseNotFound()

        data = {
            "theme": theme.name,
            "scores": [ts['score'] for ts in
                       ThemeScore.objects.filter(theme=theme).order_by('score').values('score')]
        }

        return HttpResponse(json.dumps(data), content_type='application/json')


class ChamberScoresJSONView(generic.View):
    """
    Returns JSON with all score points for a given chamber as follows:

    {
        "chamber": "<chamber_name>",
        "scores": [-99, -98, -98, ... 100, 102, 102, 102]
    }
    """

    def get(self, request, *args, **kwargs):
        try:
            chamber = Chamber.objects.get(id=kwargs['chamber'])
        except Chamber.DoesNotExist:
            return HttpResponseNotFound()

        today = datetime.date.today()
        meps = Representative.objects.filter(
            Q(mandates__end_date__gte=today) |
            Q(mandates__end_date__isnull=True),
            mandates__group__chamber=chamber
        ).select_related('representative_score') \
         .order_by('representative_score__score') \
         .distinct()

        data = {
            "chamber": chamber.name,
            "scores": [r.representative_score.score for r in meps]
        }

        return HttpResponse(json.dumps(data), content_type='application/json')
