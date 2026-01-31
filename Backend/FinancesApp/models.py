from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallets")
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    trans_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2) 
    trans_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    budg_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(blank=True)
    

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50)
    start_date = models.DateField()
    target_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    desc = models.TextField(blank=True)