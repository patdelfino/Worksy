from django.shortcuts import redirect
from django.urls import reverse
from .models import UserProfile

def create_user_profile(backend, user, response, *args, **kwargs):
    """
    Create user profile for social auth users if it doesn't exist
    """
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'APPLICANT'}
    )
    
    if backend.name == 'github':
        if response.get('name'):
            names = response['name'].split(' ', 1)
            user.first_name = names[0]
            if len(names) > 1:
                user.last_name = names[1]
        
        if response.get('bio'):
            profile.bio = response['bio']
        
        if response.get('blog'):
            profile.website = response['blog']
        
        if response.get('location'):
            profile.location = response['location']

    # (Optional: Add Google, LinkedIn data parsing here.)

    profile.save()
    user.save()

    return {
        'user': user,
        'is_new': kwargs.get('is_new', False)
    }

def social_auth_role_handler(strategy, details, user=None, *args, **kwargs):
    if user:
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        role = getattr(profile, 'role', None)
        if not role:
            profile.role = 'APPLICANT'
            profile.save()

        if role == 'APPLICANT':
            return {'redirect_url': reverse('users:applicant_dashboard')}
        elif role == 'RECRUITER':
            return {'redirect_url': reverse('users:recruiter_dashboard')}
        else:
            return {'redirect_url': reverse('users:home')}
    
    return None
