# Generated by Django 3.1.2 on 2020-10-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('is_free', models.BooleanField(default=True)),
            ],
        ),
    ]
