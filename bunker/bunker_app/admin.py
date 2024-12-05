from django.contrib import admin
from .models import *


@admin.register(Information, Rules)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('id','title','name', 'info')
    list_display_links = ('id', 'name')
    ordering = ('id',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_name')


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('profession_ru', 'profession_en', 'survival_points', 'breeding_points')


@admin.register(Characteristics)
class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = ('characteristic', 'description', 'image')


@admin.register(Health)
class HealthAdmin(admin.ModelAdmin):
    list_display = ('health_ru', 'health_en', 'infected', 'with_stage', 'fatal', 'breeding_points')


@admin.register(Hobbii)
class HobbiiAdmin(admin.ModelAdmin):
    list_display = ('hobbii_ru', 'hobbii_en', 'survival_points')


@admin.register(Phobia)
class PhobiaAdmin(admin.ModelAdmin):
    list_display = ('phobia_ru', 'phobia_en', 'fatal')


@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
    list_display = ('baggage_ru', 'baggage_en', 'survival_points', 'breeding_points')


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('fact_ru', 'fact_en', 'survival_points', 'breeding_points')


@admin.register(Disasters)
class DisastersAdmin(admin.ModelAdmin):
    list_display = ('disaster_ru', 'disaster_en')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('occassion', 'consequences')






