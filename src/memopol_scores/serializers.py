from rest_framework import serializers

from memopol_themes.serializers import ThemeSerializer
from representatives.serializers import RepresentativeSimpleSerializer

from .models import (
    DossierScore,
    RepresentativeScore,
    ThemeScore,
    VoteScore
)


class DossierScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DossierScore
        fields = ('representative', 'dossier', 'score')
        extra_kwargs = {
            'representative': {'view_name': 'api-representative-detail'},
            'dossier': {'view_name': 'api-dossier-detail'},
        }


class RepresentativeScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RepresentativeScore
        fields = ('representative', 'score')
        extra_kwargs = {
            'representative': {'view_name': 'api-representative-detail'},
        }


class ThemeScoreSerializer(serializers.HyperlinkedModelSerializer):
    theme = ThemeSerializer()
    representative = RepresentativeSimpleSerializer()

    class Meta:
        model = ThemeScore
        fields = ('representative', 'theme', 'score')


class VoteScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VoteScore
        fields = ('vote', 'score')
        extra_kwargs = {
            'vote': {'view_name': 'api-vote-detail'},
        }
