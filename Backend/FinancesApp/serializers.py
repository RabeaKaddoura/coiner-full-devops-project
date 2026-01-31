from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer): #for user registeration
    class Meta:
        model = User #the model is predefined using an imported library above. So no need to create one in models.py for users
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password":{"write_only": True}} 
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer): #customizing token-fetching to include username
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data
    
    
    
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "user", "name", "balance"]
        extra_kwargs = {"user":{"read_only": True}} #make sure user can't be modified.
        

class TransSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "user", "wallet", "trans_type", "amount", "trans_date", "category", "desc", "created_on"]
        extra_kwargs = {"user":{"read_only": True}} #make sure user can't be modified.


class BudgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "user", "category", "amount", "budg_date", "desc"]
        extra_kwargs = {"user":{"read_only": True}} #make sure user can't be modified.


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "user", "target_amount", "current_amount", "category", "start_date", "target_date", "desc"]
        extra_kwargs = {"user":{"read_only": True}} #make sure user can't be modified.

