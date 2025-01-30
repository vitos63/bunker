from bunker_app.forms import FormMember, RequiredFormSet
from django.forms import formset_factory
from bunker_app.services.session_service import MemberSessionSevice


class FormProcessing:

    def __init__(self,session_key, post_data = None):

        self.session_key = session_key
        self.post_data = post_data
        self.formset_factory = formset_factory(FormMember, formset=RequiredFormSet, extra=self.get_extra_context())

    def get_extra_context(self):
        return self.post_data.get('members_count',0) if self.post_data else 0
    
    def is_valid(self):
        self.formset = self.formset_factory(self.post_data)
        return self.formset.is_valid()
    
    def save(self):
        for form in self.formset:
            MemberSessionSevice(self.session_key).save_member_session_key(form)
    
    def render_form(self):
        return self.formset_factory

             