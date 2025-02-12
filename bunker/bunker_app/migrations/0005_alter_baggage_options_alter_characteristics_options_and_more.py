# Generated by Django 5.0 on 2024-12-03 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunker_app', '0004_rename_information1_information'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baggage',
            options={'verbose_name': 'Багаж персонажа', 'verbose_name_plural': 'Багаж персонажей'},
        ),
        migrations.AlterModelOptions(
            name='characteristics',
            options={'verbose_name': 'Описание характеристик', 'verbose_name_plural': 'Описание характеристик'},
        ),
        migrations.AlterModelOptions(
            name='disasters',
            options={'verbose_name': 'Катастрофа', 'verbose_name_plural': 'Катастрофы'},
        ),
        migrations.AlterModelOptions(
            name='fact',
            options={'verbose_name': 'Факты о персонаже', 'verbose_name_plural': 'Факты о персонажах'},
        ),
        migrations.AlterModelOptions(
            name='health',
            options={'verbose_name': 'Здоровье персонажа', 'verbose_name_plural': 'Здоровье персонажей'},
        ),
        migrations.AlterModelOptions(
            name='hobbii',
            options={'verbose_name': 'Хобби персонажа', 'verbose_name_plural': 'Хобби персонажей'},
        ),
        migrations.AlterModelOptions(
            name='phobia',
            options={'verbose_name': 'Фобия персонажа', 'verbose_name_plural': 'Фобии персонажей'},
        ),
        migrations.AlterModelOptions(
            name='profession',
            options={'verbose_name': 'Профессия персонажа', 'verbose_name_plural': 'Профессии персонажей'},
        ),
        migrations.RemoveField(
            model_name='disasters',
            name='slug',
        ),
    ]
