import logging
logger = logging.getLogger("classy_mail")
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class EmailTemplate(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    subject_content = models.CharField(max_length=512)
    text_content = models.TextField()
    html_content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class CampaignAddressee(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    email_address = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)


class EmailCampaign(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    template_name = models.CharField(max_length=128, null=True, blank=True)
    subject_content = models.CharField(max_length=512, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    html_content = models.TextField(null=True, blank=True)
    emails = models.ManyToManyField(CampaignAddressee)


class CampaignMail(models.Model):
    campaign = models.ForeignKey(EmailCampaign)
    adressee = models.ForeignKey(CampaignAddressee)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_opened = models.DateTimeField(null=True, blank=True)
    date_clicked = models.DateTimeField(null=True, blank=True)

# TODO: Add the tracking pixel and a link interceptor

class EmailMessageLog(models.Model):
    message_text = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=512, blank=True, null=True)
    from_header = models.CharField(max_length=512, blank=True, null=True)
    to_header = models.CharField(max_length=512, blank=True, null=True)
    cc_header = models.CharField(max_length=512, blank=True, null=True)
    bcc_header = models.CharField(max_length=512, blank=True, null=True)
    date_header = models.CharField(max_length=512, blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)
