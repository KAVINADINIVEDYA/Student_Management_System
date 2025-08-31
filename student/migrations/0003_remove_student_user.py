

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_user_alter_student_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
