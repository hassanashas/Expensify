from django.urls import path 
from . import views
urlpatterns = [
    path('', views.index, name='exp'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('edit_expense/<int:id>', views.edit_expense, name='edit_expense')
]