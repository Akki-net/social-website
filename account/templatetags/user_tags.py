from django import template
from ..models import Profile
 
register = template.Library()
@register.inclusion_tag('account/profile.xhtml')
def show_user(user):
    profile = Profile.objects.get(user__id=user.id)
    return {'profile': profile, 'user': user}