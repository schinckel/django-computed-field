from ..models import Person, User, Group, Location


def test_empty_lookup():
    assert not Person.objects.filter(username=None).exists()


def test_null_lookup():
    Person.objects.create(first_name='foo', last_name='bar')
    assert Person.objects.get().username is None
    assert Person.objects.filter(username=None).exists()


def test_value_lookup():
    Person.objects.create(
        first_name='foo',
        last_name='bar',
        user=User.objects.create(username='baz')
    )
    assert Person.objects.get().username == 'baz'
    assert Person.objects.filter(username='baz').exists()
    assert not Person.objects.filter(username=None).exists()


def test_multiple_lookups():
    Person.objects.create(
        first_name='foo',
        last_name='bar',
        user=User.objects.create(username='baz', group=Group.objects.create(name='qux'))
    )

    assert Person.objects.get().group == 'qux'
    assert Person.objects.filter(group='qux').exists()
    assert not Person.objects.filter(group=None).exists()


def test_many_to_many():
    alice = Person.objects.create(first_name='Alice', last_name='A')
    bob = Person.objects.create(first_name='Bob', last_name='B')
    carol = Person.objects.create(first_name='Carol', last_name='C')

    one = Location.objects.create(name='One')
    two = Location.objects.create(name='Two')
    three = Location.objects.create(name='Three')

    one.people.add(alice, bob)
    two.people.add(carol, alice, bob)

    locations = Location.objects.order_by('person_count')
    assert False == str(locations.query)
    assert len(locations) == 3
    assert locations[0] == three
    assert locations[1] == one
    assert locations[2] == two
