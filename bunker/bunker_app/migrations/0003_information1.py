# Generated by Django 5.0 on 2024-09-18 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bunker_app', '0002_delete_information1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Заголовок')),
                ('info', models.TextField(null=True, verbose_name='Информация')),
            ],
        ),
    ]