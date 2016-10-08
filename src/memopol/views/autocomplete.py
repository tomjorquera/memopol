# coding: utf-8

from dal import autocomplete

from django.db.models import Q

from representatives.models import Representative
from representatives_votes.models import Proposal


class RepresentativeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Representative.objects.all()

        if self.q:
            qs = qs.filter(
                Q(full_name__icontains=self.q)
            )

        return qs


class ProposalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Proposal.objects.all()

        if self.q:
            qs = qs.filter(
                Q(dossier__title__icontains=self.q) |
                Q(title__icontains=self.q) |
                Q(reference__icontains=self.q)
            )

        return qs
