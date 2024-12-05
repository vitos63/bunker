from random import randint
from .models import Health, Logs
from django.db.models import Q, Min, Sum
from django.db.models.query import QuerySet
import redis

redis_client = redis.StrictRedis(host ='localhost', port=6379, db=0)

class Calculation():
    def __init__(self, members:QuerySet, disaster:str, session_key:str):
        self.session_key = session_key
        self.members = members
        self.disaster = disaster
        self.members_professions = members.values_list('profession__profession_ru', flat=True)
        self.members_facts = list(members.values_list('fact_1__fact_ru', flat=True)) + list(members.values_list('fact_2__fact_ru', flat=True))
        self.members_hobbii = members.values_list('hobbii__hobbii_ru', flat=True)
        self.perfect_health = Health.objects.get(health_ru='Идеальное здоровье')



    def remark(self):
        if 'Уролог' in self.members_professions:
            self.members.filter(sex='Man barren').update(sex='Man')
            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'urologist').consequences)
    
        if 'Онколог' in self.members_professions:
            self.members.filter(health__health_ru='Рак').update(health=self.perfect_health)
            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'oncologist').consequences)
    
        if 'Гинеколог' in self.members_professions:
            self.members.filter(sex='Woman barren').update(sex='Woman')
            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'gynecologist').consequences)
    
        if 'Психолог' in self.members_hobbii:
            self.members.filter(health__health_ru='Суицидальные наклонности').update(health=self.perfect_health)
            self.members.update(phobia=None)
            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'psychologist').consequences)
    
        if 'Проходил курсы урологии' in self.members_facts:
            min_age = self.members.filter(sex='Man barren').aggregate(Min('age'))['age__min']
            young_man = self.members.filter(sex='Man barren', age=min_age)
            if young_man:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'urolog_course').consequences.format(name=young_man[0].name))
                young_man.update(sex='Man')

        if 'Проходил курсы гинекологии' in self.members_facts:
            min_age = self.members.filter(sex='Woman barren').aggregate(Min('age'))['age__min']
            young_woman = self.members.filter(sex='Woman barren', age=min_age)
            if young_woman:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'gynecolog_course').consequences.format(name=young_woman[0].name))               
                young_woman.update(sex='Woman')
        
        if 'Пчеловод' in self.members_professions:
            apiphobia = self.members.filter(phobia__phobia_ru='Апифобия')
            for i in apiphobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'bee_keeper').consequences.format(name=i.name))
            apiphobia.update(alive=False)
        
        if 'Клоун' in self.members_professions:
            clown =self.members.filter(phobia__phobia_ru='Клоунофобия')
            for i in clown:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'clown').consequences.format(name=i.name))
            clown.update(alive=False)
        
        if 'Переводчик' in self.members_professions or 'Знает 5 языков' in self.members_facts:
            self.members.filter(fact_1__fact_ru = 'Не говорит по-русски').update(fact_1=None)
            self.members.filter(fact_2__fact_ru = 'Не говорит по-русски').update(fact_2=None)
        
        if self.disaster=='Ядерная зима':
            criophobia = self.members.filter(phobia__phobia_ru='Криофобия')
            for i in criophobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'nuclear_winter_kill').consequences.format(name=i.name, disaster = self.disaster))
            criophobia.update(alive=False)
            self.members.filter(phobia__phobia_ru='Гелиофобия').update(phobia=None)
            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'nuclear_winter_heal').consequences.format(disaster = self.disaster))
        
        elif self.disaster=='Наводнение':
            aquaphobia = self.members.filter(phobia__phobia_ru='Аквафобия')
            for i in aquaphobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'flood').consequences.format(name = i.name,disaster = self.disaster))
            aquaphobia.update(alive=False)
        
        elif self.disaster=='Пришествие дьявола':
            devilphobia = self.members.filter(phobia__phobia_ru='Демонофобия')
            for i in devilphobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'the_coming_of_the_devil').consequences.format(name = i.name,disaster = self.disaster))
            devilphobia.update(alive=False)
        
        elif self.disaster=='Засуха':
            termo_aridito_phobia =self.members.filter(Q(phobia__phobia_ru='Термофобия') | Q(phobia__phobia_ru='Аридитафобия'))
            for i in termo_aridito_phobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'the_coming_of_the_devil').consequences.format(name = i.name, phobia=i.phobia.phobia_ru, disaster = self.disaster))
            termo_aridito_phobia.update(alive=False)
        
        elif self.disaster=='Инопланетяне':
            ufophobia = self.members.filter(phobia__phobia_ru='Уфофобия')
            for i in ufophobia:
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'aliens').consequences.format(name = i.name, disaster = self.disaster))
            ufophobia.update(alive=False)

    
    def contamination(self):
        for i in self.members.filter(alive=True):
            current = i.health
            
            if current.fatal or (i.phobia and i.phobia.fatal):
                self.members.filter(pk=i.pk).update(alive=False)
                if current.fatal:
                    redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'fatal_illness').consequences.format(name = i.name, health = i.health.health_ru))
                else:
                    redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'fatal_phobia').consequences.format(name = i.name, phobia = i.phobia.phobia_ru))
            
            elif current.health_ru=='Шизофрения':
                    for j in self.members.filter(alive=True):
                        if j.pk!=i.pk:
                            j.alive = False if randint(1,100)<i.stage else True
                            if not j.alive:
                                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'schizophrenia').consequences.format(name = i.name))
                            j.save()

            elif current.with_stage and randint(1,100)<i.stage:
                self.members.filter(pk=i.pk).update(alive=False)
                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'fatal_illness').consequences.format(name = i.name, health = i.health.health_ru))
                
            elif current.infected:
                if current.health_ru!='СПИД открытый':
                    for j in self. members.filter(alive=True):
                        if j.health.health_ru != current.health_ru and randint(0,1):
                            redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'infected_illness').consequences.format(name = i.name, health = i.health.health_ru))
                            j.infection = j.infection + f', {current}' if j.infection else f'{current.health_ru}'
                            j.alive = False if randint(1,100)<70 else True
                            if not j.alive:
                                redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'fatal_illness').consequences.format(name = i.name, health = i.health.health_ru))
                            j.save()
                alive = False if randint(1,100)<70 else True
                if not alive:
                    redis_client.rpush(self.session_key, Logs.objects.get(occassion = 'fatal_illness').consequences.format(name = i.name, health = i.health.health_ru))
                self.members.filter(pk=i.pk).update(alive=alive)
    
    def breeding_score(self):
        breeding_points=0
        breeding_points+=self.members.aggregate(Sum('baggage__breeding_points'))['baggage__breeding_points__sum']
        members_alive=self.members.filter(alive=True)
        breeding_points+=15*members_alive.filter(Q(age__range=(18,34),sex='Woman')).count()
        breeding_points+=10*members_alive.filter(Q(age__range=(18,35), sex='Man') | Q(age__range=(35,50), sex='Woman')).count()
        breeding_points+=5*members_alive.filter(Q(sex='Man',age__gt=35) | Q(age__gt=50, sex='Woman')).count()
        breeding_points+=self.members.aggregate(Sum('profession__breeding_points'))['profession__breeding_points__sum']
        breeding_points+=self.members.aggregate(Sum('health__breeding_points'))['health__breeding_points__sum']
        breeding_points+=self.members.aggregate(Sum('fact_1__breeding_points'))['fact_1__breeding_points__sum'] + self.members.aggregate(Sum('fact_2__breeding_points'))['fact_2__breeding_points__sum'] 
        
        return breeding_points
    

    def survival_score(self):
        survival_points = 0
        survival_points += self.members.aggregate(Sum('baggage__survival_points'))['baggage__survival_points__sum']
        members_alive = self.members.filter(alive=True)
        survival_points += 10*members_alive.filter(Q(sex='Man', age__range=(18,35)) | Q(sex = 'Man', age__gte=50) | Q(sex = 'Woman', age__range=(35,50)) | Q(sex = 'Woman barren', age__range=(35,50)) | Q(sex='Man barren', age__range=(18,35)) | Q(sex = 'Man barren', age__gte=50)).count()
        survival_points += 20*members_alive.filter(Q(sex='Man', age__range=(36,49)) | Q(sex='Man barren', age__range=(36,49))).count()
        survival_points += 5*members_alive.filter(Q(sex='Woman', age__range=(18,35)) | Q(sex='Woman barren', age__gte=50)).count()
        survival_points += self.members.aggregate(Sum('profession__survival_points'))['profession__survival_points__sum']
        survival_points += self.members.aggregate(Sum('hobbii__survival_points'))['hobbii__survival_points__sum']
        survival_points += self.members.aggregate(Sum('fact_1__survival_points'))['fact_1__survival_points__sum'] + self.members.aggregate(Sum('fact_2__survival_points'))['fact_2__survival_points__sum']

        return survival_points
    


def total_score(members,disaster, session_key):
    calculated_characteristics = Calculation(members, disaster, session_key)
    calculated_characteristics.remark()
    calculated_characteristics.contamination()
    breeding_points = calculated_characteristics.breeding_score() // members.all().count()
    survival_points = calculated_characteristics.survival_score() // members.all().count()
    logs = [i.decode('utf-8') for i in redis_client.lrange(session_key, 0, -1)]
    redis_client.expire(session_key, 1800)

    return breeding_points, survival_points, logs


def reproduction(members, breeding_points, bunker_alive):
    chance_breed = Logs.objects.get(occassion='breed_per_cent_0').consequences
    bunker_breed = Logs.objects.get(occassion='bunker_not_breed').consequences
    members_count = members.filter(alive=True).count() 
    if bunker_alive==Logs.objects.get(occassion='bunker_alive').consequences and members_count>1 and members.filter(sex='Man').exists() and members.filter(sex='Woman').exists():
        if members_count%2==0:
            perfect_breed = (25*members_count//2)
            breed_per_cent = round(breeding_points/(perfect_breed/100),1)
            chance_breed = Logs.objects.get(occassion='breed_per_cent').consequences.format(breed_per_cent=min(breed_per_cent,100))
        else:
            perfect_breed = 10*members_count//2 + 15*(members_count//2 + 1)
            breed_per_cent = round(breeding_points/(perfect_breed/100),1)
            chance_breed = Logs.objects.get(occassion='breed_per_cent').consequences.format(breed_per_cent=min(breed_per_cent,100))
        if randint(1,perfect_breed)<breeding_points:
            bunker_breed =Logs.objects.get(occassion='bunker_breed').consequences
    return chance_breed, bunker_breed


def survival(members, survival_points):
    bunker_alive = Logs.objects.get(occassion='bunker_dead').consequences
    chance_survive = Logs.objects.get(occassion='survive_per_cent_0').consequences
    if members.filter(alive=True).exists():
        survive_per_cent = round(survival_points/(55/100),1)
        chance_survive = Logs.objects.get(occassion='survive_per_cent').consequences.format(survive_per_cent=min(survive_per_cent,100))
        if randint(1,55)<survival_points:
            bunker_alive = Logs.objects.get(occassion='bunker_alive').consequences
    return chance_survive, bunker_alive


def context(members,survival_points,breeding_points, logs):
    chance_survive, bunker_alive = survival(members=members, survival_points=survival_points)
    chance_breed, bunker_breed = reproduction(members=members, breeding_points=breeding_points, bunker_alive=bunker_alive)

    return {
    'breeding_points' : breeding_points, 
    'survival_points': survival_points, 
    'members_alive': members.filter(alive=True), 
    'members_dead': members.filter(alive=False),
    'logs': logs,
    'chance_survive': chance_survive,
    'bunker_alive': bunker_alive,
    'chance_breed': chance_breed,
    'bunker_breed': bunker_breed,
    }