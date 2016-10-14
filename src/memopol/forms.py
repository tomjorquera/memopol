from django import forms
from dal import autocomplete, forward

from representatives.models import Chamber, Group, Representative
from representatives_votes.models import Dossier


class RepresentativeSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    scoremin = forms.FloatField(
        required=False,
        label='Between',
        widget=forms.NumberInput(attrs={'placeholder': 'Min. score'})
    )
    scoremax = forms.FloatField(
        required=False,
        label='and',
        widget=forms.NumberInput(attrs={'placeholder': 'Max. score'})
    )
    chamber = forms.ModelChoiceField(
        queryset=Chamber.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='chamber-autocomplete',
            attrs={'data-html': 'true'}
        )
    )
    country = forms.ModelChoiceField(
        queryset=Group.objects.filter(kind='country'),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='group-autocomplete',
            forward=(forward.Const('country', 'kind'),),
            attrs={'data-html': 'true'}
        )
    )
    party = forms.ModelChoiceField(
        queryset=Group.objects.filter(kind='group'),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='group-autocomplete',
            forward=(forward.Const('group', 'kind'),),
            attrs={'data-html': 'true'}
        )
    )
    committee = forms.ModelChoiceField(
        queryset=Group.objects.filter(kind='committee'),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='group-autocomplete',
            forward=(forward.Const('committee', 'kind'),),
            attrs={'data-html': 'true'}
        )
    )
    delegation = forms.ModelChoiceField(
        queryset=Group.objects.filter(kind='delegation'),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='group-autocomplete',
            forward=(forward.Const('delegation', 'kind'),),
            attrs={'data-html': 'true'}
        )
    )


class DossierSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    chamber = forms.ModelChoiceField(
        queryset=Chamber.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(
            url='chamber-autocomplete',
            attrs={'data-html': 'true'}
        )
    )
