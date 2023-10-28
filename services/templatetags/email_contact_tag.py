from django import template
from services.forms import ContactForm, EmailForm

register = template.Library()


@register.simple_tag()
def email_form():
    return EmailForm()


@register.simple_tag()
def contact_form():
    return ContactForm()

