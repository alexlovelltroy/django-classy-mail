from django.core.mail import EmailMultiAlternatives
from django.template.base import Context, TemplateDoesNotExist
from django.template import loader


def resolve_template(template):
    "Accepts a template object, path-to-template or list of paths"
    if isinstance(template, (list, tuple)):
        return loader.select_template(template)
    elif isinstance(template, basestring):
        try:
            return loader.get_template(template)
        except TemplateDoesNotExist:
            return None
    else:
        return template


class BaseTemplateMixin(object):
    _context_obj = None

    def get_template_name(self):
        return self.template_name

    def get_context(self):
        return self.context

    def get_context_object(self):
        if self._context_obj is None:
            self._context_obj = Context(self.get_context())
        return self._context_obj

    def render_subject_template(self):
        return self.get_subject_template().render(
            self.get_context_object()
        ).lstrip().rstrip().replace('\n', '')

    def render_text_template(self):
        return self.get_text_template().render(self.get_context_object())

    def render_html_template(self):
        return self.get_html_template().render(
            self.get_context_object()
        ).replace("\n", "")

    def build_msg(self):
        if self._msg is None:
            try:
                subject = self.subject.lstrip().rstrip().replace('\n', '')
            except AttributeError:
                subject = self.render_subject_template()
            self._msg = EmailMultiAlternatives(
                subject    = subject,
                body       = self.render_text_template(),
                from_email = self.get_from_email(),
                to         = self.get_to(),
                bcc        = self.get_bcc(),
                cc         = self.get_cc(),
                headers    = self.get_headers()
            )
            if self.get_html_template() is not None:
                self._msg.attach_alternative(
                    self.render_html_template(),
                    'text/html'
                )
        return self._msg
