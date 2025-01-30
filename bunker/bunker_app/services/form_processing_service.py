from bunker_app.forms import FormMember, RequiredFormSet
from django.forms import formset_factory
from bunker_app.services.session_service import MemberSessionSevice, SessionService


class FormProcessing:

    def init(self,session_key, members_count, post_data = None):

        self.session_key = session_key
        self.post_data = post_data
        self.formset_factory = formset_factory(FormMember, formset=RequiredFormSet, extra=members_count)

    def is_valid(self):
        self.formset = self.formset_factory(self.post_data)
        return self.formset.is_valid()
    
    def save(self):
        for form in self.formset:
            MemberSessionSevice(self.session_key).save_member_session_key(form)
    
    def render_form(self):
        return self.formset_factory