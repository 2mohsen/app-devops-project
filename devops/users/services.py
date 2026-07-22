
from devops.users.models import BaseUser, Profile
from django.db.models import QuerySet
from django.db.transaction import atomic
def create_user(*, email:str, password:str) -> QuerySet[BaseUser]:
    return BaseUser.objects.create_user(email=email, password=password)


def create_profile(*, user:BaseUser, bio:str | None) -> QuerySet[Profile]:
    return Profile.objects.create(user=user, bio=bio)
    
@atomic
def register(bio:str | None, email:str, password:str) -> QuerySet[BaseUser]:
    user = create_user(email=email, password=password)
    create_profile(user=user, bio=bio)
    return user 