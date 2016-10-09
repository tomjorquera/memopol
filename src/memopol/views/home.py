# coding: utf-8

import datetime
import random

from django.db.models import Q, Count
from django.views import generic

from representatives.models import Representative
from representatives_positions.views import PositionFormMixin
from representatives_votes.models import Proposal

from memopol_settings.models import Setting
from memopol_themes.models import Theme

from .representative_mixin import RepresentativeViewMixin


class HomeView(PositionFormMixin, RepresentativeViewMixin,
               generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        c = super(HomeView, self).get_context_data(**kwargs)

        # Today's mep

        qs = Representative.objects
        qs = qs.filter(Q(representative_score__score__lt=0) |
                       Q(representative_score__score__gt=0))
        qs = self.prefetch_for_representative_country_and_main_mandate(qs)
        qs = qs.select_related('representative_score')

        random.seed(datetime.date.today().isoformat())
        index = random.randint(0, qs.count() - 1)
        c['todays_mep'] = qs.all()[index]

        self.add_representative_country_and_main_mandate(c['todays_mep'])

        # Featured themes

        c['featured_themes'] = Theme.objects \
            .filter(featured=True) \
            .annotate(
                nb_links=Count('links', distinct=True),
                nb_dossiers=Count('dossiers', distinct=True),
                nb_proposals=Count('proposals', distinct=True),
                nb_positions=Count('positions', distinct=True))

        # Last votes

        num = int(Setting.objects.get(pk='HOMEPAGE_LATEST_VOTES').value)
        c['latest_votes'] = Proposal.objects \
            .filter(recommendation__isnull=False) \
            .select_related('dossier', 'recommendation') \
            .prefetch_related('themes', 'dossier__themes',
                              'dossier__documents__chamber') \
            .order_by('-datetime')[0:num]

        return c
