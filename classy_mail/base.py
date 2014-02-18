from django.conf import settings


# Exceptions
class ImpossibleEmail(Exception):
    pass


class NoFromAddress(ImpossibleEmail):
    pass


class NoToAddress(ImpossibleEmail):
    pass


class NoSubject(ImpossibleEmail):
    pass


class NoBody(ImpossibleEmail):
    pass


# Utility Functions
def _makelist(arg):
    if isinstance(arg, list):
        return arg
    if isinstance(arg, basestring):
        return [arg]
    raise TypeError('%s is not a string or a list' % unicode(arg))


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

