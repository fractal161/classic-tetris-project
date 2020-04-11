import factory

from classic_tetris_project.models import *


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
