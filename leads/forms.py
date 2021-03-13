from django import forms
from .models import Lead

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Agent



User = get_user_model()

class LeadModelForm(forms.ModelForm):
    
    class Meta:
        model = Lead
        fields = ('first_name', 'last_name', 'email', 'age', 'description', 'phone_number', 'category',)



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)




class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents