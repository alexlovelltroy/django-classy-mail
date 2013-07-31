django-classy-mail
==================

Class Based Email for Django, built on Mixins to support many common use cases

All e-mails are based on a BaseEmail class that builds the MultiPartEmail class
that django provides.  This means that you can still use any backend you want.
I like [django-ses](https://github.com/hmarr/django-ses), but you may like
something else.

The simplest usage of the class is to send a one-off e-mail like this:

    from classy_mail.generic import SimpleEmail

    #create the email
    email = SimpleEmail(subject=u'Welcome to mycoolwebsite',to_addr=u'user@example.com', text_content=u'Hello World', from_email=u'Friendly Admin <administrator@mycoolwebsite.io>'')
    #Everything gets validated and templated when build_msg is called by send()
    email.send()
    #You can check things like send status on the object
    print email.status


Some other mixins to play with:

### FileTemplateMixin
Applies templates stored in your project templates directories

### ModelTemplateMixin
Using the included TemplatedEmail model, you can store templates in the database instead

### SiteContextMixin
Adds the site to the context that will be used to render any template

