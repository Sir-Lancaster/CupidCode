from django.db import migrations
from django.contrib.auth.hashers import make_password

def dummy_manager(User):
    """
    Create the sample manager.
    User: The model to use for User
    """

    user = User(
        username='manager',
        password=make_password('password'),
        email='manager@cupidcode.com',
        first_name='Mr.',
        last_name='Boss',
        is_staff=True,
        phone_number='0982137894',
        role="manager"
    )

    user.save()


def main(apps, schema_editor):
    """
    Call the functions to actually perform the migrations.
    apps: provided by Django, provides access to models
    schema_editor: provided by Django, currently unused
    """
    # Find models
    User = apps.get_model('api', 'User')

    # Manager only
    dummy_manager(User)


class Migration(migrations.Migration):
    """
    Expected by Django. Makes the migrations happen.
    """

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(main),
    ]