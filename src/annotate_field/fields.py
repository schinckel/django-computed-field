import inspect

from django.db import models


class AnnotateField(models.Field):
    def __init__(self, expression, *args, **kwargs):
        # We want to trigger the read-only behaviour in the admin.
        kwargs.update(editable=False)
        # Ensure we have an output field on our expression?
        self.expression = expression
        super().__init__(*args, **kwargs)
        # Can we prevent this field from being used in a form?

    def db_type(self, connection):
        # We can easily prevent creation of a field in a migration by returning None here.
        return None

    def from_db_value(self, value, expression, connection):
        # This will always be delegated to the output field of the expression.
        return self.expression.output_field.from_db_value(value, expression, connection)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, [self.expression] + args, kwargs

    def get_col(self, alias, output_field=None):
        # I'd love some way to get the query object without having to peek up the stack...
        query = None
        for frame in inspect.stack():
            if frame.function == 'get_default_columns':
                query = frame.frame.f_locals['self'].query
                break
            if frame.function == 'add_fields':
                query = frame.frame.f_locals['self']
                break

        if query:
            col = self.expression.resolve_expression(query=query)
            col.target = self
            col.alias = alias  # Do we need this?
            return col

    def contribute_to_class(self, cls, name, private_only=True):
        # We use a private field, because that then means it won't be added to the
        # list of local/concrete fields (which would mean we can change how and when
        # it is included in the query).
        super().contribute_to_class(cls, name, True)
