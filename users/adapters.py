from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if hasattr(user, 'profile'):
            if not user.profile.role:
                user.profile.role = 'APPLICANT'  # Default role if not set
                user.profile.save()

            if user.profile.role == 'RECRUITER':
                return '/users/recruiter/dashboard/'
            elif user.profile.role == 'APPLICANT':
                return '/users/applicant/dashboard/'
        
        return super().get_login_redirect_url(request)


    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Sends the confirmation email.
        """
        current_site = request.site
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)

        subject = f"{settings.ACCOUNT_EMAIL_SUBJECT_PREFIX}Please Confirm Your Email Address"
        message = f"""
        Hello from {current_site.name}!

        You're receiving this email because you or someone else has requested email verification for your account.
        
        To confirm, please visit: {activate_url}
        
        If you did not request this, you can safely ignore this email.
        """
        
        send_mail(
            subject=subject,
            message=message.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[emailconfirmation.email_address.email],
            fail_silently=False,
        )

    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        """
        Customizes email confirmation message.
        """
        if 'email confirmation' in message_template.lower():
            message_template = "Verification email sent. Please check your email to verify your account."
        super().add_message(request, level, message_template, message_context, extra_tags)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        # Always redirect to home after connection
        return reverse('home')

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        role_from_next = request.GET.get('next', '')
        if role_from_next and 'RECRUITER' in role_from_next:
            user.profile.role = 'RECRUITER'
        elif role_from_next and 'APPLICANT' in role_from_next:
            user.profile.role = 'APPLICANT'
        elif not user.profile.role:
            user.profile.role = 'APPLICANT'  # Default fallback

            user.profile.save()
        return user


