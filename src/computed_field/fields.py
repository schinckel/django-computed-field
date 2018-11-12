import inspect

from django.db import models
from django.db.models.expressions import Col


class ComputedField(models.Field):
    def __init__(self, expression, *args, **kwargs):
        # We want to trigger the read-only behaviour in the admin.
        kwargs.update(editable=False)
        # Ensure we have an output field on our expression?
        self.expression = expression.copy()
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

        def resolve_f(expression):
            # Because of the fact that F() expressions refer to the "local" table,
            # we need to resolve these to a Col() expression that uses the table
            # alias (supplied to us), and the field that the F() expression refers
            # to. This is then complicated by the fact that we could have an F()
            # expression that refers to a ComputedField - which we just want to
            # resolve the inner F expressions in right now. We'll rely on the
            # fact that resolve_expression() will keep resolving source expressions
            # to handle everything else: this is just a precursor to that.
            if hasattr(expression, 'get_source_expressions'):
                # We want a copy here, because otherwise we'd be mutating objects we
                # really shouldn't, which could affect places where the same expression
                # was shared between different things.
                expression = expression.copy()
                expression.set_source_expressions([
                    resolve_f(expr) for expr in expression.get_source_expressions()
                ])
            if isinstance(expression, models.F):
                # If we are dealing with an F() expression, we want to try to resolve
                # it to a Col(alias, field) for the relevant field on our model.
                # If that is a ComputedField(), then just resolve the F() expressions
                # inside that.
                field = self.model._meta.get_field(expression.name)
                if hasattr(field, 'expression'):
                    return resolve_f(field.expression)
                return Col(alias, field)
            return expression

        # I'd love some way to get the query object without having to peek up the stack...
        query = None
        for frame in inspect.stack():
            if frame.function in ['get_default_columns', 'get_order_by']:
                query = frame.frame.f_locals['self'].query
                break
            if frame.function in ['add_fields', 'build_filter']:
                query = frame.frame.f_locals['self']
                break
        else:
            import pdb; pdb.set_trace()  # NOQA

        col = resolve_f(self.expression).resolve_expression(query=query)
        col.target = self
        col.alias = self.name
        return col

    def contribute_to_class(self, cls, name, private_only=False):
        # We use a private field, because that then means it won't be added to the
        # list of local/concrete fields (which would mean we can change how and when
        # it is included in the query). I think this is the mechanism that is used
        # by inherited fields. Seems to work okay, unless we try to use this field
        # in an index.
        super().contribute_to_class(cls, name, True)
