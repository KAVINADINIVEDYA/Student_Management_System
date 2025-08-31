


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_auth', '0002_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',

            field=models.CharField(default='CXRJqUCE6uZqLCHBFvb9UaieK4H9aNw5', editable=False, max_length=32, unique=True),
            field=models.CharField(default='PZFrwTHmTYrwcUCTTf6HYt5xJmINg0go', editable=False, max_length=32, unique=True),

          
        ),
    ]
