"""Template mixins for Zinnia views"""
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.views.generic.base import TemplateResponseMixin


class EntryQuerysetTemplateResponseMixin(TemplateResponseMixin):
    """
    Return a custom template name for views returning
    a queryset of Entry filtered by another model.
    """
    model_type = None
    model_name = None

    def get_model_type(self):
        """
        Return the model type for templates.
        """
        if self.model_type is None:
            raise ImproperlyConfigured(
                "%s requires either a definition of "
                "'model_type' or an implementation of 'get_model_type()'" %
                self.__class__.__name__)
        return self.model_type

    def get_model_name(self):
        """
        Return the model name for templates.
        """
        if self.model_name is None:
            raise ImproperlyConfigured(
                "%s requires either a definition of "
                "'model_name' or an implementation of 'get_model_name()'" %
                self.__class__.__name__)
        return self.model_name

    def get_template_names(self):
        """
        Return a list of template names to be used for the view.
        """
        model_type = self.get_model_type()
        model_name = self.get_model_name()
        templates = [
            f'zinnia/{model_type}/{model_name}/entry_list.html',
            f'zinnia/{model_type}/{model_name}_entry_list.html',
            f'zinnia/{model_type}/entry_list.html',
            'zinnia/entry_list.html']

        if self.template_name is not None:
            templates.insert(0, self.template_name)
        return templates


class EntryQuerysetArchiveTemplateResponseMixin(TemplateResponseMixin):
    """
    Return a custom template name for the archive views based
    on the type of the archives and the value of the date.
    """
    template_name_suffix = '_archive'

    def get_archive_part_value(self, part):
        """
        Method for accessing to the value of
        self.get_year(), self.get_month(), etc methods
        if they exists.
        """
        try:
            return getattr(self, f'get_{part}')()
        except AttributeError:
            return None

    def get_default_base_template_names(self):
        """
        Return a list of default base templates used
        to build the full list of templates.
        """
        return [f'entry{self.template_name_suffix}.html']

    def get_template_names(self):
        """
        Return a list of template names to be used for the view.
        """
        year = self.get_archive_part_value('year')
        week = self.get_archive_part_value('week')
        month = self.get_archive_part_value('month')
        day = self.get_archive_part_value('day')

        templates = []
        path = 'zinnia/archives'
        template_names = self.get_default_base_template_names()
        for template_name in template_names:
            templates.extend([template_name,
                              f'zinnia/{template_name}',
                              f'{path}/{template_name}'])
        if year is not None:
            templates.extend(f'{path}/{year}/{template_name}' for template_name in template_names)

        if week is not None:
            for template_name in template_names:
                templates.extend([
                        f'{path}/week/{week}/{template_name}',
                        f'{path}/{year}/week/{week}/{template_name}'])

        if month is not None:
            for template_name in template_names:
                templates.extend([
                    f'{path}/month/{month}/{template_name}',
                    f'{path}/{year}/month/{month}/{template_name}'])

        if day is not None:
            for template_name in template_names:
                templates.extend([
                    f'{path}/day/{day}/{template_name}',
                    f'{path}/{year}/day/{day}/{template_name}',
                    f'{path}/month/{month}/day/{day}/{template_name}',
                    f'{path}/{year}/{month}/{day}/{template_name}'])

        if self.template_name is not None:
            templates.append(self.template_name)

        templates.reverse()
        return templates


class EntryQuerysetArchiveTodayTemplateResponseMixin(
        EntryQuerysetArchiveTemplateResponseMixin):
    """
    Same as EntryQuerysetArchiveTemplateResponseMixin
    but use the current date of the day when getting
    archive part values.
    """
    today = None

    def get_archive_part_value(self, part):
        """Return archive part for today"""
        parts_dict = {'year': '%Y',
                      'month': self.month_format,
                      'week': self.week_format,
                      'day': '%d'}
        if self.today is None:
            today = timezone.now()
            if timezone.is_aware(today):
                today = timezone.localtime(today)
            self.today = today
        return self.today.strftime(parts_dict[part])


class EntryArchiveTemplateResponseMixin(
        EntryQuerysetArchiveTemplateResponseMixin):
    """
    Same as EntryQuerysetArchiveTemplateResponseMixin
    but use the template defined in the Entry instance
    as the base template name.
    """

    def get_default_base_template_names(self):
        """
        Return the Entry.template value.
        """
        return [self.object.detail_template,
                f'{self.object.slug}.html',
                f'{self.object.slug}_{self.object.detail_template}']
