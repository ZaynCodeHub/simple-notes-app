from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import Note, User
from .serializers import NoteSerializer, UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'Logged in successfully'})
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'})

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return user's private notes and all public notes
        return Note.objects.filter(author=self.request.user) | Note.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NoteRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own notes or public notes
        return Note.objects.filter(author=self.request.user) | Note.objects.filter(is_public=True)
    
    def perform_update(self, serializer):
        # Only the author can update
        if serializer.instance.author == self.request.user:
            serializer.save()
        else:
            raise serializers.ValidationError("You can only update your own notes.")
    
    def perform_destroy(self, instance):
        # Only the author can delete
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("You can only delete your own notes.")