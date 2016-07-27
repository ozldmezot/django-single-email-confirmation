from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .signals import (
    email_confirmed,
    confirmed_email_change_requested, 
    unconfirmed_email_change_requested,
)


from time import time
from django.utils.crypto import get_random_string
class EmailAddressManager(models.Manager):


    def generate_key(self):

        # ensuring its gonna be unique over time
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        t = int( time() )
        stamp = ''
        while t:
            stamp += allowed_chars[t % 62]
            t = int( t / 62 )

        return get_random_string(34) + str(stamp)

    def confirm(self, key):
        "Confirm an email address. Returns the address that was confirmed."
        queryset = self.all()

        email_address = queryset.get(key=key)
        email_address.confirmed_at = timezone.now()
        
        owner = email_address.owner
        owner.set_current_email(email_address.email)
        owner._single_email_confirmation_signal = email_confirmed
        owner.save()

class EmailAddress(models.Model):
    "An email address belonging to a User"

    email = models.EmailField(max_length=255)
    key = models.TextField(unique=True)

    set_at = models.DateTimeField(
        default=timezone.now,
        help_text=_('When the confirmation key expiration was set'),
    )
    confirmed_at = models.DateTimeField(
        blank=True, null=True,
        help_text=_('First time this email was confirmed'),
    )

    objects = EmailAddressManager()

    @property
    def is_confirmed(self):
        return self.confirmed_at is not None

    def reset_confirmation(self, email=None):

        self.key = EmailAddress._default_manager.generate_key()
        self.set_at = timezone.now()
        if email:
            self.email=email
        self.confirmed_at = None


class EmailConfirmationMixin(models.Model):
    """
    Mixin to be used with your django 1.9+ custom User model.
    Provides python-level functionality only.
    """

    """
    Confirmed Email will always be primary email or None, therefore
    supplying get_unconfirmed_email, because this can differentiate from
    primary email
    """

    _single_email_confirmation_signal = None
    email_field_name = 'email'
    email_address    = models.OneToOneField(EmailAddress, related_name='owner', null=True, blank=True)
    
    class Meta:
        abstract = True

    @property
    def email_is_confirmed(self):
        email_address = self.email_address
        if not email_address:
            email_address = EmailAddress()
        return email_address.email != self.email or email_address.is_confirmed

    def get_current_email(self):
        return getattr(self, self.email_field_name)
    
    def set_current_email(self, email):
        setattr(self, self.email_field_name, email)

    def change_email(self, email, commit=True, force=False):

        # email was not changed
        if self.email == email:
            return

        email_address = self.email_address
        # no metadata available, mixin might have been added later
        if not email_address:
            email_address = EmailAddress()

        # this email is already requested for change

        if email == email_address.email and not force:
            return

        if self.email_is_confirmed:
            self._single_email_confirmation_signal = confirmed_email_change_requested
        else:
            self.email_address = email_address
            self.email = email
            self._single_email_confirmation_signal = unconfirmed_email_change_requested

        email_address.reset_confirmation(email)
        if commit:
            self.save()

    def save(self, *args, **kwargs):
        if self.email_address:
            self.email_address.save()
            self.email_address = self.email_address
        saved = super().save(*args, **kwargs)
        if self._single_email_confirmation_signal:
            self._single_email_confirmation_signal.send(sender=self, email_address=self.email_address)
            self._single_email_confirmation_signal = None

        return saved

