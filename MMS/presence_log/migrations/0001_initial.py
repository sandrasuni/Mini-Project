# Generated by Django 3.2.25 on 2024-09-23 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PresenceLog',
            fields=[
                ('presencelog_id', models.AutoField(primary_key=True, serialize=False)),
                ('mess_id', models.IntegerField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'presence_log',
                'managed': False,
            },
        ),
    ]
