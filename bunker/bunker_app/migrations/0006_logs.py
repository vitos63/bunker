# Generated by Django 5.0 on 2024-12-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker_app', '0005_alter_baggage_options_alter_characteristics_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occassion', models.CharField(max_length=150, null=True)),
                ('consequences', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
    ]