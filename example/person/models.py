from django.db import models
from django.db.models.expressions import Value
from django.db.models.functions import Concat, Lower

from computed_field.fields import ComputedField


class ComputedIndex(models.Index):
    def __init__(self, computed_field, name=None, db_tablespace=None):
        self.expression = computed_field.expression
        self.name = name or ''
        if self.name:
            errors = self.check_name()
            if len(self.name) > self.max_name_length:
                errors.append('Index names cannot be longer than %s characters', self.max_name_length)
            if errors:
                raise ValueError(errors)
        self.db_tablespace = db_tablespace


class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    active = models.BooleanField()

    name = ComputedField(Concat(
        models.F('first_name'), Value(' '), models.F('last_name'),
        output_field=models.TextField()
    ))

    lower_name = ComputedField(Lower(models.F('name')))

    class Meta:
        verbose_name_plural = 'people'
    #     indexes = [
    #         models.Index(name='lower_name', fields=['lower_name']),
    #     ]

    def __str__(self):
        return self.name
