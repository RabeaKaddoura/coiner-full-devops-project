from django.urls import path
from FinancesApp.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
  path("register/", CreateUserView.as_view(), name="Register"),
  path("token/", MyTokenObtainPairView.as_view(), name="Token"), #this is basically a log-in url
  path("refresh_token/", TokenRefreshView.as_view(), name="Refresh"), 
  
  path("wallet/", WalletList.as_view(), name="Wallets"), 
  path("wallet/<int:id>/", WalletDetail.as_view(), name="Wallet-Details"),  
  
  path("trans/", TransactionList.as_view(), name="Transactions"), 
  path("trans/<int:id>/", TransDetail.as_view(), name="Trans-Details"), 
  
  path("budget/", BudgetList.as_view(), name="Budgets"), 
  path("budget/<int:id>/", BudgetDetail.as_view(), name="Budget-Details"), 
  
  path("goal/", GoalList.as_view(), name="Goals"), 
  path("goal/<int:id>/", GoalDetail.as_view(), name="Goal-Details"),
  
]