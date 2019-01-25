from django.db import models
from django.db.models.expressions import Value
from django.db.models.functions import Concat, Lower

from computed_field.fields import ComputedField


class Group(models.Model):
    name = models.TextField()


class User(models.Model):
    username = models.TextField()
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)


class Person(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()
    follows = models.ManyToManyField('tests.Person', related_name='followed_by')

    name = ComputedField(Concat(
        models.F('first_name'), Value(' '), models.F('last_name'),
        output_field=models.TextField()
    ))

    lower_name = ComputedField(Lower(models.F('name')), db_index=True)

    username = ComputedField(models.F('user__username'))
    group = ComputedField(models.F('user__group__name'))

    # follower_count = ComputedField(models.Count('follows__name'))

    class Meta:
        indexes = [
            # models.Index(fields=['lower_name']),
        ]


class Address(models.Model):
    person = models.OneToOneField(Person, related_name='address', primary_key=True, on_delete=models.CASCADE)
