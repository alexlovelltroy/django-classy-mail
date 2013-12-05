import logging
logger = logging.getLogger("classy_mail")
from django.conf import settings
from django.template import Template, Context ,loader, TemplateDoesNotExist
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from .models import EmailTemplate, EmailMessageLog
from .exceptions import *

# Utility Functions

def _makelist(arg):
    if isinstance(arg, list):
        return arg
    if isinstance(arg, basestring):
        return [arg]
    raise TypeError('%s is not a string or a list' % unicode(arg))

def _resolve_template(template):
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


# The good stuff

class BaseEmail(object):
    _msg = None
    from_email = settings.DEFAULT_FROM_EMAIL
    context = dict()
    #TODO: Separate getting the template from rendering it

    def __init__(self, **kwargs):
        """
        Constructor. Can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_subject(self):
        try:
           return self.subject
        except AttributeError:
            raise NoSubject("Missing a subject.  try adding it as a kwarg")

    def get_to(self):
        try:
            addr = self.to_addr
        except AttributeError:
            raise NoToAddress("Missing a to_addr.  try adding it as a kwarg")
        return _makelist(addr)


    def get_from_email(self):
        try:
           return self.from_email
        except AttributeError:
            raise NoFromAddress("Missing a from_email.  try adding it as a kwarg")

    def get_cc(self):
        return None

    def get_bcc(self):
        return None

    def get_headers(self):
        return None

    def get_text_content(self):
        try:
           return self.text_content
        except AttributeError:
            raise NoBody("Missing text_content.  try adding it as a kwarg")

    def get_html_content(self):
        return None


    def send(self):
        self.msg = self.build_msg()
        self.msg.send()

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
        return self.get_subject_template().render(self.get_context_object()).lstrip().rstrip().replace('\n','')

    def render_text_template(self):
        return self.get_text_template().render(self.get_context_object())

    def render_html_template(self):
        return self.get_html_template().render(self.get_context_object()).replace("\n","")

    def build_msg(self):
        if self._msg is None:
            try:
                subject = self.subject.lstrip().rstrip().replace('\n','')
            except AttributeError:
                subject = self.render_subject_template()
            self._msg = EmailMultiAlternatives(
                subject = subject,
                body = self.render_text_template(),
                from_email = self.get_from_email(),
                to = self.get_to(),
                bcc = self.get_bcc(),
                cc = self.get_cc(),
                headers = self.get_headers(),
            )
            if self.get_html_template() is not None:
                self._msg.attach_alternative(self.render_html_template(), 'text/html')
        return self._msg

class FileTemplateMixin(BaseTemplateMixin):

    def get_subject_template(self):
        template_name = "%s_subject.txt" % self.get_template_name()
        return _resolve_template(template_name)

    def get_text_template(self):
        template_name = "%s_body.txt" % self.get_template_name()
        return _resolve_template(template_name)

    def get_html_template(self):
        template_name = "%s_body.html" % self.get_template_name()
        return _resolve_template(template_name)

class ModelTemplateMixin(BaseTemplateMixin):
    _template = None

    def _get_template(self):
        if self._template is None:
            self._template = EmailTemplate.objects.get(name=self.get_template_name())
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

class SiteContextMixin(object):
    def get_context(self):
        context = super(SiteContextMixin, self).get_context()
        context.update(dict(site = Site.objects.get_current()))
        return context

class LogMessageMixin(object):
    def send(self, log_msg=True):
        self.msg = self.build_msg()
        # Does this need to be a manager method?
        if log_msg:
            log = EmailMessageLog(
                message_text = self.msg.message().as_string(),
                subject = self.msg.message().get('Subject'),
                from_header = self.msg.message().get('From'),
                to_header = self.msg.message().get('To'),
                cc_header = self.msg.message().get('Cc'),
                bcc_header = self.msg.message().get('Bcc'),
            )
            self.msg.send()
            log.save()
        else:
            self.msg.send()

class SimpleEmail(BaseEmail):
    """This email needs everything passed in to init"""

    def build_msg(self):
        if self._msg is None:
            self._msg = EmailMultiAlternatives(
                subject = self.get_subject(),
                body= self.get_text_content(),
                from_email = self.get_from_email(),
                to = self.get_to(),
                bcc = self.get_bcc(),
                cc = self.get_cc(),
                headers = self.get_headers(),
            )
            if self.get_html_content() is not None:
                self._msg.attach_alternative(self.get_html_content(), 'text/html')
        return self._msg

class ModelTemplateEmail(LogMessageMixin, ModelTemplateMixin, BaseEmail):
    pass


class FileTemplateEmail(LogMessageMixin, FileTemplateMixin, BaseEmail):
    pass

