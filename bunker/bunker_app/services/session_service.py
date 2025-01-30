from bunker_app.models import MemberCharact

class SessionService:
    
    def __init__(self, session):
        self.session = session

    def set_user_session_key(self, user_key):
        self.session['user'] = user_key
    
    def get_user_session_key(self):
        return self.session.session_key
    
    def get_any_session_key(self, key):
        return self.session[key]
    
    def set_any_session_key(self, key, value):
        self.session[key] = value
    
    def del_any_session_key(self, key):
        del self.session[key]

    def has_redirect(self):
        return self.session.get('came_from_redirect', False)


class MemberSessionSevice:

    def __init__(self, session_key):
        self.session_key = session_key
    
    def delete_member_session_key(self):
        MemberCharact.objects.filter(session_key = self.session_key).delete()
    
    def save_member_session_key(self, form):
        member = form.save(commit=False)
        member.session_key = self.session_key
        member.save()

