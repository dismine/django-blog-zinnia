"""Fields for Zinnia admin"""
from django import forms
from django.utils.encoding import smart_str

# Try to import normalize_choices from Django 5.0, otherwise define a fallback
try:
    from django.utils.choices import normalize_choices
    NORMALIZE_CHOICES_AVAILABLE = True
except ImportError:
    NORMALIZE_CHOICES_AVAILABLE = False


class MPTTModelChoiceIterator(forms.models.ModelChoiceIterator):
    """
    MPTT version of ModelChoiceIterator.
    """

    def choice(self, obj):
        """
        Overloads the choice method to add the position
        of the object in the tree for future sorting.
        """
        tree_id = getattr(obj, self.queryset.model._mptt_meta.tree_id_attr, 0)
        left = getattr(obj, self.queryset.model._mptt_meta.left_attr, 0)
        return super(MPTTModelChoiceIterator,
                     self).choice(obj) + ((tree_id, left),)


class MPTTModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    MPTT version of ModelMultipleChoiceField.
    """

    def __init__(self, level_indicator='|--', *args, **kwargs):
        self.level_indicator = level_indicator
        super(MPTTModelMultipleChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """
        Create labels which represent the tree level of each node
        when generating option labels.
        """
        label = smart_str(obj)
        if prefix := self.level_indicator * getattr(
            obj, obj._mptt_meta.level_attr
        ):
            return f'{prefix} {label}'
        return label

    @property
    def choices(self):
        """
        Override the _get_choices method to use MPTTModelChoiceIterator.
        """
        return MPTTModelChoiceIterator(self)

    @choices.setter
    def choices(self, value):
        if NORMALIZE_CHOICES_AVAILABLE:
            # Setting choices on the field also sets the choices on the widget.
            # Note that the property setter for the widget will re-normalize.
            self._choices = self.widget.choices = normalize_choices(value)
        else:
            forms.ChoiceField._set_choices(self, value)
