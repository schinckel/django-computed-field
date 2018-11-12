from django.db import models
from django.db.models.expressions import Value
from django.db.models.functions import Concat, Lower

from computed_field.fields import ComputedField


class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    name = ComputedField(Concat(
        models.F('first_name'), Value(' '), models.F('last_name'),
        output_field=models.TextField()
    ))

    lower_name = ComputedField(Lower(models.F('name')), db_index=True)

    class Meta:
        indexes = [
            # models.Index(fields=['lower_name']),
        ]
