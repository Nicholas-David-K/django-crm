from django.shortcuts import render
from django.views import generic
from leads.models import Agent
from django.shortcuts import reverse
from .forms import AgentCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganizerAndLoginRequiredMixin
from django.contrib.auth.models import send_mail
import random

# Create your views here.

class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)



class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    form_class = AgentCreateForm
    template_name = 'agents/agent_create.html'


    def get_success_url(self):
        return reverse("agent_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 10000000)}")
        user.save()
        agent = Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile
        )
        agent.save()
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM, please login to start working", 
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'


    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)



class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    form_class = AgentCreateForm
    template_name = 'agents/agent_update.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('agent_detail', kwargs={'pk': pk})


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_confirm_delete.html'

    def get_success_url(self):
        return reverse('agent_list')
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


