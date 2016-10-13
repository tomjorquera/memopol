from .forms import DossierSearchForm, RepresentativeSearchForm

from memopol_settings.models import Setting
from representatives.models import Chamber, Group


def search_forms(request):
    return {
        'representative_search_form': RepresentativeSearchForm(request.GET),
        'dossier_search_form': DossierSearchForm(request.GET)
    }


def intro_text(request):
    d = {}

    for s in Setting.objects.filter(pk__in=['HOMEPAGE_INTRO_TEXT',
                                            'HOMEPAGE_INSTANCE_TEXT']):
        d[s.pk] = s.comment

    return d
