from rest_framework import serializers

from .models import Theme


class ThemeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Theme
        fields = ('name',)
