from datetime import datetime


from rest_framework.filters import BaseFilterBackend
from django.db.models import Q
from django.conf import settings


from .models import Mandate


class ActiveMandateQueryFilterBackend(BaseFilterBackend):
    """
    A filter which check if a mandate is active for a reprensentative

    the parameter used in the query to filter is, by default mandates_active
    and it list a list of mandates among which one should be active.
    """
    query_param = getattr(settings, 'ACTIVE_MANDATES_PARAM', 'active_mandates')

    def filter_queryset(self, request, queryset, view):
        qs = queryset

        if self.query_param in request.GET:
            if len(request.GET[self.query_param]):
                # We want to check for params in a list of mandates
                mandates = request.GET[self.query_param].split(',')
                qs = qs.filter(mandates__in=Mandate.objects.filter(
                    Q(end_date__gte=datetime.today) |
                    Q(end_date__isnull=True)).filter(
                        Q(group__name__in=mandates) |
                        Q(group__abbreviation__in=mandates)
                )).distinct()
                return qs
        return qs
