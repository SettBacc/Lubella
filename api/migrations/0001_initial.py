# Generated by Django 5.1.3 on 2024-12-07 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_id', models.BigAutoField(db_column='USER_ID', primary_key=True, serialize=False)),
                ('login', models.CharField(default='login', max_length=150, unique=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'USERS',
            },
        ),
    ]
