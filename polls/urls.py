from django.urls import path
from . import views

urlpatterns = [
    # The homepage for this application -> Displays a list of all the polls available
    path('', views.home_page_view, name='home'),
    # A detailed view for a single poll -> Displays all the answers and offers the possibility to vote
    path('polls/<int:poll_id>/', views.single_poll_view, name='polls'),
    # The login page, where user can log into an existing account
    path('login/', views.log_in_view, name='login'),
    # The signup page, where a new user can be created
    path('signup/', views.sign_up_view, name='signup'),
    # The creation page for a new poll
    path('create-poll/', views.create_poll_view, name='create-poll'),
    # The deletion confirmation page for a poll
    path('polls/<int:pk>/delete', views.PollDeleteView.as_view(), name='delete-poll'),
]
