from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.utils.functional import curry


class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj, fields=('id', 'name')))
        return JSONEncoder.default(self, obj)

# partial function, we can now use dumps(my_dict) instead
# of dumps(my_dict, cls=DjangoJSONEncoder)
dumps = curry(dumps, cls=DjangoJSONEncoder)


def to_ajax(rows, filter_field, slug_field=None):
    ret = []
    for row in rows:
        ret.append(
            {'id': row.id,
             'description': getattr(row, filter_field),
             'slug': getattr(row, slug_field) if slug_field else ''
            }
        )
    return ret