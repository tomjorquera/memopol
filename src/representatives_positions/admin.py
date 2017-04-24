from django import forms
from django.contrib import admin

from dal.autocomplete import ModelSelect2Multiple

from representatives.models import Representative
from .models import Position


def publish_positions(modeladmin, request, queryset):
    """Set published to True for the queryset"""
    queryset.update(published=True)


publish_positions.short_description = 'Publish selected positions'


def unpublish_positions(modeladmin, request, queryset):
    """Set published to False for the queryset"""
    queryset.update(published=False)


unpublish_positions.short_description = 'Unpublish selected positions'


class PositionAdminForm(forms.ModelForm):
    representatives = forms.ModelMultipleChoiceField(
        queryset=Representative.objects.all(),
        required=False,
        widget=ModelSelect2Multiple(
            url='representative-autocomplete',
        )
    )

    def __init__(self, *args, **kwargs):
        super(PositionAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['representatives'].initial = \
                self.instance.representatives.all()

    def save(self, commit=True):
        item = super(PositionAdminForm, self).save(commit=False)
        item.save()

        item.representatives = self.cleaned_data['representatives']
        if commit:
            self.save_m2m()

        return item


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'kind',
        'short_title',
        'short_text',
        'score',
        'datetime',
        'link',
        'published')
    list_display_links = ('short_title', 'short_text')
    list_editable = ('published',)
    list_filter = ('published',)
    actions = (publish_positions, unpublish_positions)

    form = PositionAdminForm


admin.site.register(Position, PositionAdmin)
