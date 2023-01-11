from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path('',
         RedirectView.as_view(pattern_name='expenses:expense-list'),
         name='dashboard'),
    path('expenses/',
         include(('expenses.urls', 'expenses'), namespace='expenses')),
    path('admin/', admin.site.urls),
]
