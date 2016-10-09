from memopol_settings.models import Setting
from representatives.models import Chamber, Group


def search_form_options(request):
    d = {}
    # Note: Those queries needs to be eval in the template so that we can cache
    # it efficiently

    d['chambers'] = Chamber.objects.all()
    d['countries'] = Group.objects.filter(kind='country')
    d['parties'] = Group.objects.filter(kind='group')
    d['delegations'] = Group.objects.filter(kind='delegation')
    d['committees'] = Group.objects.filter(kind='committee')

    return d


def intro_text(request):
    d = {}

    for s in Setting.objects.filter(pk__in=['HOMEPAGE_INTRO_TEXT',
                                            'HOMEPAGE_INSTANCE_TEXT']):
        d[s.pk] = s.comment

    return d
