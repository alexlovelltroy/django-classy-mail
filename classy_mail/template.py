from django.template import Template, TemplateEncodingError
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
