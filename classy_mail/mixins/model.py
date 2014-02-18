from .base import BaseTemplateMixin
from classy_mail.models import EmailTemplate
from django.template.base import Template


class ModelTemplateMixin(BaseTemplateMixin):
    _template = None

    def _get_template(self):
        if self._template is None:
            self._template = EmailTemplate.objects.get(
                name=self.get_template_name()
            )
        return self._template

    def get_subject_template(self):
        return Template(self._get_template().subject_content)

    def get_text_template(self):
        return Template(self._get_template().text_content)

    def get_html_template(self):
        template_content = self._get_template().html_content
        if template_content != '':
            return Template(template_content)
        return None
