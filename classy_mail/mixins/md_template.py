from django.template.base import (
    Template,
    TemplateDoesNotExist,
    TemplateEncodingError,
)
from django.template.loader import make_origin
from django.template.loaders.app_directories import Loader as AppDirectoriesLoader
from markdown import markdown
import yaml
from BeautifulSoup import BeautifulSoup
from .base import BaseTemplateMixin, resolve_template


class MarkdownTemplate(Template):
    def __init__(self, template_string, origin=None, name=None):
        split_template = template_string.split("---\n")
        if len(split_template) == 3:
            context = yaml.load(split_template[1])
            if isinstance(context, type({})):
                template_string = split_template[2]
                self.frontmatter = {}
                for k, v in context.iteritems():
                    self.frontmatter[k.lower()] = v
            template_string = markdown(template_string)
            self.text_template = ''.join(
                BeautifulSoup(
                    template_string
                ).findAll(
                    text=True
                )
            )
        super(MarkdownTemplate, self).__init__(
            template_string,
            origin=origin,
            name=name
        )


class MarkdownTemplateLoader(AppDirectoriesLoader):

    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(template_name,
                                                         template_dirs)
        origin = make_origin(display_name, self.load_template_source,
                             template_name, template_dirs)
        try:
            template = get_template_from_string(source, origin, template_name)
            return template, None
        except TemplateDoesNotExist:
            # If compiling the template we found raises TemplateDoesNotExist,
            # back off to returning the source and display name for the
            # template we were asked to load. This allows for correct
            # identification (later) of the actual template that does not
            # exist.
            return source, display_name


class MarkdownTemplateMixin(BaseTemplateMixin):
    markdown_template = None

    def get_md_template(self):
        if self.markdown_template is None:
            loader = MarkdownTemplateLoader()
            self.template, origin = loader.load_template(
                "%s.md" % self.get_template_name()
            )
        return self.markdown_template

    def get_subject_template(self):
        return Template(self.get_md_template().frontmatter['Subject'])

    def get_text_template(self):
        return Template(self.get_md_template().text_template)

    def get_html_template(self):
        return self.get_md_template()

    def get_context_object(self):
        if self._context_obj is None:
            template_context = self.get_md_template().frontmatter
            instance_context = self.get_context()
            instance_context.update(template_context)
            self._context_obj = Context(instance_context)
        return self._context_obj


def get_template_from_string(source, origin=None, name=None):
    """
    Returns a compiled Template object for the given template code,
    handling template inheritance recursively.
    """
    return MarkdownTemplate(source, origin, name)
