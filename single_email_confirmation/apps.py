from django.apps import AppConfig

class SingleEmailConfirmationConfig(AppConfig): # Our app config class
    name  = 'single_email_confirmation'
    label = 'single_email'
    verbose_name = "Single Email Confirmation"