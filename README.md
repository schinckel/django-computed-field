# django-computed-field

ComputedField() for django


A very common pattern, at least in code I've written and seen, is to use `.annotate()` to add on a field that is based upon one or more real fields, that in many cases is used as frequently as the real fields. A toy example might be:

```python
class PersonQuerySet(models.query.QuerySet):
    def with_name(self):
        return self.annotate(
            name=Concat(
                models.F('first_name'),
                Value(' '),
                models.F('last_name'),
                output_field=models.TextField(),
            ),
        )


class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    objects = PersonQuerySet.as_manager()
```
(Yes, I'm aware of [falsehoods programmers believe about names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/), this is just a really neat example).

In order to get access to the name "field", we must ensure we use the ``Person.objects.with_name()`` queryset method each time we need it; alternatively we could look at overriding a manager's `get_queryset()` to always apply this.

However, it would be neat if it we could define this field directly on the model, and it would always be fetched, never be written, and follow django's normal rules with respect to defer/only.

```python
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()

    name = ComputedField(
        Concat(
            models.F('first_name'),
            Value(' '),
            models.F('last_name'),
            output_field=models.TextField(),
        ),
    )

    group = ComputedField(
        ExpressionWrapper(models.F('user__group__name')),
        output_field=models.TextField()
    )
```

We can also, as shown in the `group` field, refer to foreign keys. This does require us to use an ExpressionWrapper, and provide the correct output_field.

This is still a proof of concept: whilst it works in the tests I have written so far, it may not work in all cases (and actually still contains a `pdb` breakpoint, sort-of deliberately).

It's also missing major functionality that I think is required before it can be used: the ability to declare that a ComputedField should have an index, and the migrations framework detecting that, and creating one. This currently cannot be done due to the mechanism I have used for avoiding other things happening (like the value being sent to the database when we save) also prevents the field from being used in indices.
