from django.contrib import admin
from employees.models import Employee, Position, Department


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name')
    search_fields = ['first_name', 'last_name']


class PositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'employee_id')
    search_fields = ['title']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'position', 'last_name')
    search_fields = ['title', 'position', 'last_name']


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Department, DepartmentAdmin)
