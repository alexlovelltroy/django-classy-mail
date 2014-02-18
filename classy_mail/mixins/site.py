from django.contrib.sites.models import Site


class SiteContextMixin(object):
    def get_context(self):
        context = super(SiteContextMixin, self).get_context()
        context.update(dict(site=Site.objects.get_current()))
        return context
