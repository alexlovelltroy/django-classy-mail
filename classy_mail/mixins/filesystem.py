from .base import BaseTemplateMixin, resolve_template


class FileTemplateMixin(BaseTemplateMixin):
    def get_subject_template(self):
        template_name = "%s_subject.txt" % self.get_template_name()
        return resolve_template(template_name)

    def get_text_template(self):
        template_name = "%s_body.txt" % self.get_template_name()
        return resolve_template(template_name)

    def get_html_template(self):
        template_name = "%s_body.html" % self.get_template_name()
        return resolve_template(template_name)
