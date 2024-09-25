from re import DEBUG

from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from . import views

urlpatterns = [
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('positions/', views.PositionListView.as_view(), name='position-list'),
    path('departments/',
         views.DepartmentListView.as_view(),
         name='department-list'),
    path('employee/<int:pk>/',
         views.EmployeeDetailView.as_view(),
         name='employee-detail'),
    path('employees/details/', views.EmployeeWithDetailsListView.as_view(),
         name='employee-details'),
    path('employee/add/',
         views.EmployeeCreateView.as_view(),
         name='add-employee'),
]

if DEBUG:
    urlpatterns += debug_toolbar_urls()
