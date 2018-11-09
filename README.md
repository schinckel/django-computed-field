# django-computed-field

ComputedField() for django


A very common pattern, at least in code I've written and seen, is to use `.annotate()` to add on a field that is based upon one or more real fields, that in many cases is used as frequently as the real fields. A toy example might be:


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

(Yes, I'm aware of falsehoods programmers believe about names, this is just a really neat example).

In order to get access to the name "field", we must ensure we use the ``Person.objects.with_name()`` queryset method each time we need it; alternatively we could look at overriding a manager's `get_queryset()` to always apply this.

However, it would be neat if it we could define this field directly on the model, and it would always be fetched, never be written, and follow django's normal rules with respect to defer/only.


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
