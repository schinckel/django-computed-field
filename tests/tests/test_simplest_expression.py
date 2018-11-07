from ..models import Person

import pytest


@pytest.mark.django_db
def test_create_works():
    Person.objects.create(first_name='Foo', last_name='Bar')


@pytest.mark.django_db
def test_annotated_field_is_set_on_object():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.get().name == 'Foo Bar'


@pytest.mark.django_db
def test_annotated_field_is_set_on_values():
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.values('name')[0] == {'name': 'Foo Bar'}


@pytest.mark.django_db
def test_filter_on_annotate_field():
    assert not Person.objects.filter(name='Foo Bar').exists()
    Person.objects.create(first_name='Foo', last_name='Bar')
    assert Person.objects.filter(name='Foo Bar').exists()
