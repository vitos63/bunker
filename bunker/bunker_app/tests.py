from django.test import TestCase
from http import HTTPStatus
from random import randint, choice
from django.urls import reverse
from bunker_app.models import Profession, Health, Hobbii, Phobia, Baggage, Fact, Disasters
from bunker_app.forms import FormMember, RequiredFormSet
from django.forms import formset_factory

class GetPagesTestCase(TestCase):
    fixtures = ['bunker_disasters.json','bunker_member_charact.json',
                'bunker_profession.json', 'bunker_health.json',
                'bunker_hobbii.json', 'bunker_phobia.json',
                'bunker_baggage.json', 'bunker_fact.json',
                'bunker_logs.json', 'bunker_information.json',
                ]
    def setUp(self):
        return super().setUp()
    
    def test_home(self): 
        response = self.client.get(reverse ('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('bunker_app/index.html')
    
    def test_count(self): 
        response = self.client.get(reverse ('count'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('bunker_app/count_disaster.html')
    
    def test_rules(self):
        response = self.client.get(reverse ('rules'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('bunker_app/rules.html')
    
    def test_feedback(self):
        response = self.client.get(reverse ('feedback'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('bunker_app/feedback.html')
    

    def test_characteristics(self):
        response = self.client.get(reverse ('characteristics'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('bunker_app/characteristics.html')
    
    def test_calculate(self):
        for i in Disasters.objects.all():
            data = {'members_count': randint(1,10),
                'disaster':Disasters.objects.get(pk=i.pk).id}
            response = self.client.post(reverse('count'), data, follow = True)
            self.assertRedirects(response, reverse('members_forms'))
    
    def test_member_characts(self):
        for i in range(1,11):
            session = self.client.session
            session['members_count'] = i
            session['disaster'] = Disasters.objects.get(pk=randint(1,7)).disaster_ru
            session.save()
            data = {
            'form-TOTAL_FORMS': f'{i}',
            'form-INITIAL_FORMS': f'{i}',
            'form-MIN_NUM_FORMS': f'{i}',
            'form-MAX_NUM_FORMS': '10',
                }
            for j in range(i):
                data[f'form-{j}-name'] = 'Some_name'
                data[f'form-{j}-sex'] =  choice(['Man', 'Woman', 'Man barren', 'Woman barren'])
                data[f'form-{j}-age'] = randint(18,100)
                data[f'form-{j}-profession'] = Profession.objects.get(pk=randint(1,20)).pk
                data[f'form-{j}-health']= Health.objects.get(pk=randint(1,26)).pk
                data[f'form-{j}-stage'] = choice([f for f in range(0,101,10)])
                data[f'form-{j}-hobbii'] = Hobbii.objects.get(pk=randint(1,20)).pk
                data[f'form-{j}-phobia'] = Phobia.objects.get(pk = randint(1,20)).pk
                data[f'form-{j}-baggage'] = Baggage.objects.get(pk=randint(1,20)).pk
                data[f'form-{j}-fact_1'] = Fact.objects.get(pk=randint(1,40)).pk
                data[f'form-{j}-fact_2'] = Fact.objects.get(pk=randint(1,40)).pk
            FormMemberFactory = formset_factory(FormMember, formset = RequiredFormSet, extra = session['members_count'])
            formset = FormMemberFactory(data)
            self.assertTrue(formset.is_valid())
            response = self.client.post(reverse('members_forms'),data, follow=True)
            self.assertRedirects(response, reverse('calculat'))
   
    def tearDown(self):
        return super().tearDown()