# Generated by Django 5.0 on 2024-12-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker_app', '0007_alter_information_options_alter_menu_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='title',
            field=models.CharField(max_length=150, null=True),
        ),
    ]