from django import template
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def password_help_html():
    # Return the same HTML AllAuth/Django shows for password rules
    return mark_safe(password_validators_help_text_html())