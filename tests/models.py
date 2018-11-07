from django.db import models
from django.db.models.expressions import Value
from django.db.models.functions import Concat, Lower

from annotate_field.fields import AnnotateField


class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    name = AnnotateField(Concat(
        models.F('first_name'), Value(' '), models.F('last_name'),
        output_field=models.TextField()
    ))

    lower_name = AnnotateField(Lower(models.F('name')))
