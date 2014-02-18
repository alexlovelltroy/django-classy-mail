import logging
logger = logging.getLogger("classy_mail")
from mixins.filesystem import FileTemplateMixin
from mixins.models import ModelTemplateMixin
from mixins.log import LogMessageMixin
from mixins.markdown import MarkdownTemplateMixin
from .base import BaseEmail


class ModelTemplateEmail(LogMessageMixin, ModelTemplateMixin, BaseEmail):
    pass


class FileTemplateEmail(LogMessageMixin, FileTemplateMixin, BaseEmail):
    pass


class MarkdownTemplateEmail(LogMessageMixin, MarkdownTemplateMixin, BaseEmail):
    pass
