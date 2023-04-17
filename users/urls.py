from django.urls import path

from .views import UsersView, LoginView, LogoutView, UserSpecificView, GetUsersEmailView

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UserSpecificView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('get_emails/', GetUsersEmailView.as_view()),
]
