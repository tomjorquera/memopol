from django.db import models

from .models import (
    Document,
    Dossier,
    Proposal,
    Vote
)

from rest_framework import (
    filters,
    viewsets,
)

from representatives.api import DefaultWebPagination

from representatives_votes.serializers import (
    DossierDetailSerializer,
    DossierSerializer,
    ProposalDetailSerializer,
    ProposalSerializer,
    VoteSerializer,
)


class DossierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows dossiers to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Dossier.objects.order_by('id')
    serializer_class = DossierSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'title': ['exact', 'icontains'],
        'reference': ['exact', 'icontains'],
    }

    search_fields = (
        'title',
        'reference',
        'text',
        'proposals__title'
    )

    def retrieve(self, request, pk=None):
        self.serializer_class = DossierDetailSerializer
        self.queryset = self.queryset.prefetch_related(
            models.Prefetch(
                'proposals',
                queryset=Proposal.objects.order_by('id')
            ),
            models.Prefetch(
                'documents',
                queryset=Document.objects.order_by('id')
            )
        )
        return super(DossierViewSet, self).retrieve(request, pk)


class ProposalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows proposals to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Proposal.objects.order_by('id')
    serializer_class = ProposalSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'title': ['exact', 'icontains'],
        'description': ['icontains'],
        'reference': ['exact', 'icontains'],
        'datetime': ['exact', 'gte', 'lte'],
        'kind': ['exact'],
    }

    search_fields = (
        'title',
        'reference',
        'dossier__title',
        'dossier__reference'
    )

    def retrieve(self, request, pk=None):
        self.serializer_class = ProposalDetailSerializer
        self.queryset = self.queryset.prefetch_related(
            models.Prefetch(
                'votes',
                queryset=Vote.objects.order_by('representative_id')
            )
        )
        return super(ProposalViewSet, self).retrieve(request, pk)


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows proposals to be viewed.
    """

    pagination_class = DefaultWebPagination
    queryset = Vote.objects.select_related('representative', 'proposal') \
                           .order_by('proposal_id', 'representative__slug')
    serializer_class = VoteSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    filter_fields = {
        'position': ['exact'],
        'representative_name': ['exact', 'icontains'],
        'representative': ['exact']
    }
