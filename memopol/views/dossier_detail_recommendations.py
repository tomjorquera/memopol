# coding: utf-8

from django.db import models

from representatives_votes.models import Proposal

from .dossier_detail_base import DossierDetailBase


class DossierDetailRecommendations(DossierDetailBase):
    template_name = 'representatives_votes/dossier_detail_recommendations.html'

    def get_queryset(self):
        qs = super(DossierDetailRecommendations, self).get_queryset()
        qs = qs.prefetch_related(
            models.Prefetch(
                'proposals',
                Proposal.objects.filter(recommendation__isnull=False)
                .select_related('recommendation')
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        c = super(DossierDetailRecommendations,
                  self).get_context_data(**kwargs)

        c['tab'] = 'recommendations'
        c['proposals'] = c['object'].proposals.all()

        return c
