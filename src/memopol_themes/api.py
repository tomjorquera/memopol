from rest_framework import (
    filters,
    viewsets,
)

from representatives.api import DefaultWebPagination

from rql_filter.backend import RQLFilterBackend

from .models import Theme
from .serializers import ThemeSerializer


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view themes
    """
    queryset = Theme.objects.all()
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    search_fields = ('name',)
    ordering_fields = ('name',)
    pagination_class = DefaultWebPagination
    serializer_class = ThemeSerializer
