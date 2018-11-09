from ..models import Person

import pytest


@pytest.mark.django_db
def test_create_works():
    Person.objects.create(first_name='Foo', last_name='Bar')


@pytest.mark.django_db
def test_computed_field_is_set_on_object():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.get().name == 'Foo Bar'


@pytest.mark.django_db
def test_computed_field_is_set_on_values():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.values('name')[0] == {'name': 'Foo Bar'}


@pytest.mark.django_db
def test_filter_on_computed_field():
    assert not Person.objects.filter(name='Foo Bar').exists()
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.filter(name='Foo Bar').exists()


@pytest.mark.django_db
def test_filter_transform_on_computed_field():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.filter(name__icontains='foo').exists()


@pytest.mark.django_db
def test_cascading_field():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.filter(lower_name='foo bar').exists()
