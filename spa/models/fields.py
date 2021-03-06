import sys

import django

from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

if sys.version_info[0] == 2:
    string_type = unicode
else:
    string_type = str

# Code from six egg https://bitbucket.org/gutworth/six/src/a3641cb211cc360848f1e2dd92e9ae6cd1de55dd/six.py?at=default


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def get_max_length(choices, max_length, default=200):
    if max_length is None:
        if choices:
            return len(','.join([string_type(key) for key, label in choices]))
        else:
            return default
    return max_length


class MultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices):
        choices_selected = []
        for choice_selected in arr_choices:
            choices_selected.append(string_type(choice_selected[0]))
        return choices_selected

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if opt_select not in arr_choices:
                if django.VERSION[0] >= 1 and django.VERSION[1] >= 6:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})
                else:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = string_type(default)
        return default

    def get_prep_value(self, value):
        return ",".join(value)

    def to_python(self, value):
        if value is not None:
            return value if isinstance(value, list) else value.split(',')
        return ''

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(MultiSelectField, self).contribute_to_class(cls, name, virtual_only)
        if self.choices:
            def get_display(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                for value in getattr(obj, fieldname):
                    item_display = choicedict.get(value, None)
                    if item_display is None:
                        try:
                            item_display = choicedict.get(int(value), value)
                        except (ValueError, TypeError):
                            item_display = value
                    display.append(string_type(item_display))
                return ", ".join(display)
            setattr(cls, 'get_%s_display' % self.name, get_display)

MultiSelectField = add_metaclass(models.SubfieldBase)(MultiSelectField)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^spa\.models.fields\.MultiSelectField'])
except ImportError:
    pass