from django.urls import path
from .views import (
    UserCreate, LoginView, LogoutView,
    NoteListCreate, NoteRetrieveUpdateDestroy
)

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('notes/', NoteListCreate.as_view(), name='note-list'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroy.as_view(), name='note-detail')
]