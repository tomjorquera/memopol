import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.core.urlresolvers import reverse
from memopol.utils import strip_accents


def search_autocomplete(request):
    if request.is_ajax():
        q = strip_accents(request.GET.get('term', ''))
        if q is not None:
            json_results = []
            sqs = SearchQuerySet().autocomplete(ascii_name=q)
            for result in sqs:
                result_json = {}
                result_json['id'] = result.id
                result_json['label'] = result.full_name
                result_json['value'] = result.full_name
                result_json['link'] = reverse(
                    'representative-detail', kwargs={'slug': result.slug})
                json_results.append(result_json)
            data = json.dumps(json_results)
    else:
        data = "Fail"
    return HttpResponse(data, "application/json")
