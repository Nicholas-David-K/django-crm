from django.urls import  path
from . import views

urlpatterns = [
    # leads
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('leads/', views.LeadListView.as_view(), name='lead_list'),
    path('leads/<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('leads/create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead_update'),
    path('leads/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead_delete'),
    path('leads/<int:pk>/assign-agent/', views.AssignAgentView.as_view(), name='assign_agent'),

    # categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),


    path('accounts/register/', views.SignUpView.as_view(), name='register'),


]


# continue 6:56