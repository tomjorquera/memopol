# coding: utf-8

from dal import autocomplete

from django.db.models import Q

from representatives.models import Representative, Chamber, Group
from representatives_votes.models import Proposal
from memopol_themes.models import Theme
from ..templatetags import memopol_tags


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


class ThemeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Theme.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class ChamberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Chamber.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) |
                           Q(abbreviation__icontains=self.q))

        return qs

    def get_result_label(self, item):
        icon = memopol_tags.chamber_icon(item)

        return (u'<div class="select2-icon-result">%s'
                u'<span class="select2-label">%s</span></div>' % (
                    icon, item))


class GroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Group.objects.select_related('chamber')

        kind = self.forwarded.get('kind', None)
        if kind:
            qs = qs.filter(kind=kind)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs

    def get_result_label(self, item):
        icon = None

        if item.kind == 'group':
            icon = memopol_tags.group_icon(item)
        elif item.kind == 'country':
            icon = memopol_tags.country_flag(item)
        elif item.kind == 'committee' or item.kind == 'delegation':
            icon = memopol_tags.chamber_icon(item.chamber)

        if icon:
            return (u'<div class="select2-icon-result">%s'
                    u'<span class="select2-label">%s</span></div>' % (
                        icon, item))
        else:
            return u'%s' % item
