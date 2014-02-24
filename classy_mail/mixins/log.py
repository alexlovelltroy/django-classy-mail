from classy_mail.models import EmailMessageLog

class UniqueMailAlreadySent(Exception):
    pass


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

class UniqueMessageMixin(LogMessageMixin):
    def send(self, log_msg=True):
        self.msg = self.build_msg()
        if EmailMessageLog.objects.filter(
            subject      = self.msg.message().get('Subject'),
            to_header    = self.msg.message().get('To'),
            from_header  = self.msg.message().get('From'),
        ).count() > 0:
            raise UniqueMailAlreadySent(
            "Mail found in the log from %s to %s with the subject: %s" % (
                self.msg.message().get('From'),
                self.msg.message().get('To'),
                self.msg.message().get('Subject')
                )
            )
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
