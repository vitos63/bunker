from django.shortcuts import render, redirect
from django.views.generic import ListView
from bunker_app.forms import FormMember, MembersCount, RequiredFormSet
from django.urls import reverse_lazy,reverse
from bunker_app.models import MemberCharact, Disasters, Characteristics, Rules, Information
from bunker_app.services.calculation import total_score, context, redis_client
from bunker_app.services.session_service import SessionService, MemberSessionSevice
from bunker_app.services.form_processing_service import FormProcessing
from django.forms import formset_factory
from django.views.generic import FormView



class Index(ListView):
    queryset = Information.objects.filter(title = 'main_page')
    context_object_name = 'object_list'
    template_name = 'bunker_app/index.html'
    extra_context ={'title':'Бункер'}


class Rules(ListView):
    model = Rules
    context_object_name = 'rules'
    template_name = 'bunker_app/rules.html'
    extra_context = {'title':'Правила игры'}


class DescriptionCharacteristics(ListView):
    model = Characteristics
    context_object_name = 'characteristics'
    template_name = 'bunker_app/characteristics.html'
    extra_context ={'title':'Описание характеристик'}

class Feedback(ListView):
    queryset = Information.objects.filter(title = 'feedback')
    context_object_name = 'feedback'
    template_name = 'bunker_app/feedback.html'
    extra_context ={'title':'Обратная связь'}


class Count(FormView):
    form_class = MembersCount
    template_name = 'bunker_app/count_disaster.html'
    extra_context ={'title':'Количество игроков'}
    success_url = reverse_lazy('members_forms') 
    def form_valid(self, form):
        self.request.session['came_from_redirect'] = True
        self.request.session['disaster'] = Disasters.objects.get(disaster_ru=form.cleaned_data['disaster']).disaster_ru
        self.request.session['members_count'] = form.cleaned_data['members_count']
        return super().form_valid(form)


def members_forms(request):
    session_service = SessionService(request.session)
    session_service.set_user_session_key('user_key')

    member_session = MemberSessionSevice(session_service.get_user_session_key())
    member_session.delete_member_session_key()

    form_processing_service = FormProcessing(session_service.get_user_session_key(), request.POST)
    
    if request.method == 'POST':
        session_service.set_any_session_key('came_from_redirect', True)

        if form_processing_service.is_valid():
            form_processing_service.save()

        return redirect(reverse('calculat'))
    
    else:
        if not session_service.has_redirect():
            return redirect(reverse('count'))
        
        session_service.set_any_session_key('came_from_redirect', False)
    return render(request, 'bunker_app/members_forms.html', {'title': 'Характеристики игроков','formset':form_processing_service.render_form()})


def calculation(request):
    session_service = SessionService(request.session)

    if not session_service.has_redirect():
        return redirect(reverse('count'))
    
    session_service.del_any_session_key('came_from_redirect')
    redis_client.delete(request.session.session_key)
    
    disaster = session_service.get_any_session_key('disaster')
    members = MemberCharact.objects.filter(session_key = session_service.get_user_session_key())
    breeding_points, survival_points, logs = total_score(members=members, disaster=disaster, session_key=session_service.get_user_session_key())
    data = context(members=members, survival_points=survival_points, breeding_points=breeding_points, logs=logs)
    data['title'] = 'Итоги игры'

    return render(request, 'bunker_app/calculation.html',context=data)


