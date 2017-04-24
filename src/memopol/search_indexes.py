import datetime
from haystack import indexes
from representatives.models import Representative

class RepresentativeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    slug = indexes.CharField(model_attr='slug', faceted=True)
    first_name = indexes.CharField(model_attr='first_name', faceted=True)
    last_name = indexes.CharField(model_attr='last_name', faceted=True)
    full_name = indexes.EdgeNgramField(model_attr='full_name')
    ascii_name = indexes.NgramField(model_attr='ascii_name')

    def get_model(self):
        return Representative

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
