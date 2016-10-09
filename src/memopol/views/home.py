# coding: utf-8

import datetime
import random

from django.db.models import Q
from django.views import generic

from representatives.models import Representative
from representatives_positions.views import PositionFormMixin

from .representative_mixin import RepresentativeViewMixin


class HomeView(PositionFormMixin, RepresentativeViewMixin,
               generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        c = super(HomeView, self).get_context_data(**kwargs)

        qs = Representative.objects
        qs = qs.filter(Q(representative_score__score__lt=0) |
                       Q(representative_score__score__gt=0))
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)

        random.seed(datetime.date.today().isoformat())
        index = random.randint(0, qs.count() - 1)
        c['todays_mep'] = qs.all()[index]

        self.add_representative_country_and_main_mandate(c['todays_mep'])

        return c
