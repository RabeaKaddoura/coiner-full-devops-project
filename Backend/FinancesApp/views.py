from rest_framework import generics, mixins
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .models import *
from rest_framework.response import Response
from .serializers import  *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserView(generics.CreateAPIView): #user registeration
      queryset = User.objects.all()
      serializer_class = UserSerializer
      permission_classes=[AllowAny]  
      
class MyTokenObtainPairView(TokenObtainPairView): #overriding TokenObtainPairView
    serializer_class = MyTokenObtainPairSerializer
      

class WalletList(generics.ListCreateAPIView): #list of all wallets for a certain user. GET is built-in, so no need to define it unless to override
                  
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): #overridden
        # Filter wallets by the currently authenticated user
        return Wallet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    


class WalletDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin): #this is needed to retrieve a single wallet
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    lookup_field ='id'

    def get_queryset(self):
        
        return Wallet.objects.filter(user=self.request.user)
    
    def get(self, request, id):
        return self.retrieve(request, id=id)
    
    def put(self, request, id):
        return self.update(request, id=id)
    
    def delete(self, request, id):
        return self.destroy(request, id=id)
    
        

class TransactionList(ListCreateAPIView): #used to create a post request for a single transaction record (not all records)
    serializer_class = TransSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): #overridden
        # Filter transactions by the currently authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class TransDetail(generics.GenericAPIView, mixins.DestroyModelMixin): #this is needed to delete a single transaction
    serializer_class = TransSerializer
    permission_classes = [IsAuthenticated]

    lookup_field ='id'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    
    def delete(self, request, id):
        return self.destroy(request, id=id)
    
    

class BudgetList(ListCreateAPIView): #used to create a post request for a single budget record (not all records)
    serializer_class = BudgSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): #overridden
        # Filter budgets by the currently authenticated user
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class BudgetDetail(generics.GenericAPIView, mixins.DestroyModelMixin): #this is needed to delete a single budget
    serializer_class = BudgSerializer
    permission_classes = [IsAuthenticated]

    lookup_field ='id'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    
    def delete(self, request, id):
        return self.destroy(request, id=id)
    
    

class GoalList(ListCreateAPIView): #used to create a post request for a single goal record (not all records)
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self): #overridden
        # Filter goals by the currently authenticated user
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class GoalDetail(generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin): #this is needed to delete a single goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    lookup_field ='id'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def put(self, request, id):
        return self.update(request, id=id, partial =True)
    
    def delete(self, request, id):
        return self.destroy(request, id=id)
    