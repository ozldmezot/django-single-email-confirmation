from django.dispatch import Signal

email_confirmed = Signal(providing_args=['email_address'])
confirmed_email_change_requested = Signal(providing_args=['email_address'])
unconfirmed_email_change_requested = Signal(providing_args=['email_address'])
