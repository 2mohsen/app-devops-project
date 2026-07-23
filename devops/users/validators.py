from django.utils.translation import gettext_lazy as _

import re
from django.core.exceptions import ValidationError

def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
            _("Password must include numbers"),
            code="password_must_include_number"
        )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
            _("Password must include letters"),
            code="password_must_include_letter"
        )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
            _("Password must include special charecter"),
            code="password_must_include_special_char "
        )