from django.db.models import QuerySet
from devops.users.models import Profile, BaseUser


def get_profile(user:BaseUser) -> QuerySet[Profile]:
    return Profile.objects.get(user=user)