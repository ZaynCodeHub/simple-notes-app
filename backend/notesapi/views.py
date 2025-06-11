from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import Note, User
from .serializers import NoteSerializer, UserSerializer


# 1. Create a New User (Signup)
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# 2. Login User
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if(user):
            login(request, user)
            return Response({'detail': 'LoggedIn successfully'})
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 3. Logout User    
class LogoutView(APIView):
        def post(self, request):
            logout(request)
            return Response ({'detail' : 'Logged out successfully'})
        
# 4. Show All Notes (Own + Public) & Create New Note
class NoteListCreate(generics.ListCreateAPIView):
     serializer_class = NoteSerializer
     permission_classes = [permissions.IsAuthenticated]

     def get_queryset(self):
          user = self.request.user

          return Note.objects.filter(author=user) | Note.objects.filter(is_public = True)
     
     def perform_create(self, serializer):
          serializer.save(author=self.request.user)

# 5. View, Update, or Delete a Single Note
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
     serializer_class = NoteSerializer
     permission_classes = [permissions.IsAuthenticated]

     def get_queryset(self):
          user=self.request.user

          return Note.objects.filter(author = user) | Note.objects.filter(is_public = True)
     
     def perform_update(self, serializer):
          if serializer.instance.author == self.request.User:
               serializer.save()
          else:
               return Response ({'message': 'You can only update your own messages'}, status=status.HTTP_403_FORBIDDEN)
          
     def perform_destroy(self, instance):
          if instance.author == self.request.user:
               instance.delete()
          else:
               return Response({'message': 'you can only delete your own messages'},status=status.HTTP_403_FORBIDDEN)     
     