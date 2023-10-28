from django import template
from services.models import Testimonial

register = template.Library()


@register.simple_tag
def show_testimonials():
    testimonial_lst = []
    testimonials = Testimonial.objects.all()

    for i in range(0, len(testimonials), 2):
        testimonial_lst.append(testimonials[i:i+2])
    return testimonial_lst
