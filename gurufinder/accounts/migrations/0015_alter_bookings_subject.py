# Generated by Django 3.2.9 on 2021-11-07 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_tutorprofile_programming_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='subject',
            field=models.CharField(choices=[('JavaScript', 'JavaScript'), ('Python', 'Python'), ('Swift', 'Swift'), ('Java', 'Java'), ('Sql', 'Sql'), ('PHP', 'PHP'), ('C#', 'C#')], default='JavaScript', max_length=10),
        ),
    ]
