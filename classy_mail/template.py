from django.template.base import (
    Template,
    TemplateDoesNotExist,
    TemplateEncodingError,
)
from django.template.loader import make_origin
from django.template.loaders.filesystem import Loader as FilesystemLoader
from markdown import markdown
import yaml
#from BeautifulSoup import BeautifulSoup


class MarkdownTemplate(Template):
    def __init__(self, template_string, origin=None, name=None):
        split_template = template_string.split("---\n")
        if len(split_template) == 3:
            context = yaml.load(split_template[1])
            if isinstance(context, type({})):
                template_string = split_template[2]
                self.frontmatter = context
        try:
            template_string = markdown(template_string)
            super(Template, self).__init__(
                template_string,
                origin=origin,
                name=name
            )
        except UnicodeDecodeError:
            raise TemplateEncodingError("Templates can only be constructed "
                                        "from unicode or UTF-8 strings.")


class MarkdownTemplateLoader(FilesystemLoader):

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


def get_template_from_string(source, origin=None, name=None):
    """
    Returns a compiled Template object for the given template code,
    handling template inheritance recursively.
    """
    return MarkdownTemplate(source, origin, name)
