from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, reverse
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm
from .models import Lead, Category
from django.views.generic import View

from django.views import generic
from django.core.mail import send_mail


# auth
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganizerAndLoginRequiredMixin

# sms
from twilio.rest import Client



# Create your views here.

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')


class LandingPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'leads/landing_page.html'



class LeadListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'leads'
    template_name = 'leads/lead_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull = False
            ).order_by('-created_at')
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization,
                agent__isnull=False
            ).order_by('-created_at')
            queryset.filter(agent__user=self.request.user)
        return queryset


    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super(LeadListView, self).get_context_data(**kwargs)

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile,
                agent__isnull=True
            ).order_by('-created_at')
            context.update({
                "unassigned_leads": queryset
            })
        return context;



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = 'lead'
    template_name = 'leads/lead_detail.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset.filter(agent__user=self.request.user)
        return queryset



class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'

    def get_success_url(self):
        return reverse('lead_list')


    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # TODO send email
        send_mail(
            subject="A lead has been created", 
            message="go to site to see the new lead", 
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )

        # #TODO send sms
        # account_sid = "account_sid" #TODO remove this info
        # auth_token = "auth_token" #TODO remove this info
        # client = Client(account_sid, auth_token)

        # message = client.messages \
        #                 .create(
        #                     body="My mom's phone number is 0723802284",
        #                     from_=' +12199796691',
        #                     to='+254723802284'
        #                 )

        # print(message.sid) #TODO remove print statement


        # #Todo send WhatsApp Message
        # account_sid = 'AC40206a8779db114972f1dd2f6c075e5b' 
        # auth_token = 'auth_token' 
        # client = Client(account_sid, auth_token) 
        
        # message = client.messages.create( 
        #                             from_='whatsapp:+14155238886',  
        #                             body='This is a WhatsApp Test Message',      
        #                             to='whatsapp:+254733939369' 
        #                         ) 
 
        # print(message.sid) #TODO remove print statement
        return super(LeadCreateView, self).form_valid(form)



class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    form_class = LeadModelForm
    template_name = 'leads/lead_update.html'

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('lead_detail', kwargs={'pk': pk})



class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_confirm_delete.html'


    def get_success_url(self):
        return reverse('lead_list')

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)




class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    form_class = AssignAgentForm
    template_name = 'leads/assign_agent.html'

    
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs


    def form_valid(self, form):
        agent = form.cleaned_data.get('agent')
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


    def get_success_url(self):
        return reverse('lead_list')



class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'


    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization,
            )

        context.update({
            'unassigned_leads': queryset.filter(category__isnull=True).count()
        })
        return context


    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile, 
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization,
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/category_detail_view.html'
    context_object_name = 'category'

    def get_queryset(self):
        user = self.request.user

        if user.is_organizer:
            queryset = Category.objects.filter(
                organization=user.userprofile, 
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization,
            )
        return queryset


        # 7:13:29