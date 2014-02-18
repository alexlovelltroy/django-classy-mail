from classy_mail.models import EmailMessageLog


class LogMessageMixin(object):
    def send(self, log_msg=True):
        self.msg = self.build_msg()
        # Does this need to be a manager method?
        if log_msg:
            log = EmailMessageLog(
                message_text = self.msg.message().as_string(),
                subject      = self.msg.message().get('Subject'),
                from_header  = self.msg.message().get('From'),
                to_header    = self.msg.message().get('To'),
                cc_header    = self.msg.message().get('Cc'),
                bcc_header   = self.msg.message().get('Bcc'),
            )
            self.msg.send()
            log.save()
        else:
            self.msg.send()
