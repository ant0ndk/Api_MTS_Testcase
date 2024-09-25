from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Employee, Position
from .serializers import (DepartmentSerializer, EmployeeCreateSerializer,
                          EmployeeSerializer, PositionSerializer)


class EmployeeListView(generics.ListAPIView):
    """
    View для получения списка всех сотрудников
    API возвращает список всех сотрудников
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PositionListView(generics.ListAPIView):
    """
    View для получения списка всех должностей
    API возвращает список всех должностей
    """

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentListView(generics.ListAPIView):
    """
    View для получения списка всех департаментов
    API возвращает список всех департаментов
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    """
    View для получения информации о конкретном сотруднике
    API возвращает информацию о сотруднике,
    включая его id, имя, фамилию, должность и департамент.
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        position = get_object_or_404(Position, employee_id=employee.pk)
        department = get_object_or_404(Department, position=position.title,
                                       last_name=employee.last_name)
        return Response({
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': position.title,
            'department': department.title,
        })


class EmployeeWithDetailsListView(generics.ListAPIView):
    """
    View для получения списка сотрудников с детализацией
    API возвращает список всех сотрудников с детализацией.
    Каждый сотрудник будет представлен в виде
    json-объекта со следующими полями:
        - id: int, id сотрудника
        - first_name: string, имя сотрудника
        - last_name: string, фамилия сотрудника
        - position: string, должность
        - department: string, название отдела
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def get(self, request):
        employees = self.get_queryset().values('pk', 'first_name', 'last_name')
        result = []
        positions = Position.objects.all().values('pk', 'title', 'employee_id')
        departments = Department.objects.all().values('pk', 'title',
                                                      'position', 'last_name')
        for employee in employees:
            position = (
                [id for id in positions
                 if id.get('employee_id') == employee.get('pk')]
                [0]
            )
            department = (
                [id for id in departments
                 if id.get('position') == position.get('title')
                 and id.get('last_name') == employee.get('last_name')]
                [0]
            )
            result.append({
                'id': employee.get('pk'),
                'first_name': employee.get('first_name'),
                'last_name': employee.get('last_name'),
                'position': position.get('title'),
                'department': department.get('title'),
            })
        return Response(result)


class EmployeeCreateView(APIView):
    """
    View для создания сотрудника
    API позволяет создавать новых сотрудников.
    В теле запроса необходимо передать поля:
        - first_name: string, имя сотрудника
        - last_name: string, фамилия сотрудника
        - position_title: string, должность (например, 'DevOps', 'BackendDev')
        - department_name: string, название отдела (например, 'Developers')
    В ответе будет возвращен json-объект со следующими полями:
        - id: int, id созданного сотрудника
        - first_name: string, имя сотрудника
        - last_name: string, фамилия сотрудника
        - position: string, должность
        - department: string, название отдела
    """

    @swagger_auto_schema(
        request_body=EmployeeCreateSerializer,  # Описание полей в теле запроса
        responses={201: 'Сотрудник успешно создан', 400: 'Ошибка валидации'}
    )
    def post(self, request):
        employee = EmployeeSerializer(data={
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
        })
        department = DepartmentSerializer(data={
            'title': request.data['department_name'],
            'position': request.data['position_title'],
            'last_name': request.data['last_name'],
        })
        try:
            with transaction.atomic():
                if Department.objects.filter(
                    position=request.data['position_title'],
                        last_name=request.data['last_name']).exists():
                    return Response(
                        data={'error': 'Department with the given position \
                            and last name already exists'},
                        status=status.HTTP_400_BAD_REQUEST)

                if not Department.objects.filter(
                        title=request.data['department_name']).exists():
                    return Response(
                        data={'error': 'Department title not found'},
                        status=status.HTTP_400_BAD_REQUEST)

                if not Position.objects.filter(
                        title=request.data['position_title']).exists():
                    return Response(
                        data={'error': 'Position title not found'},
                        status=status.HTTP_400_BAD_REQUEST)

                if employee.is_valid() and department.is_valid():
                    emp = employee.save()
                    department.save()
                    Position.objects.create(
                        title=request.data['position_title'],
                        employee_id=emp.id)

            return Response(employee.data | department.data,
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response(data={'error': 'Error'},
                        status=status.HTTP_400_BAD_REQUEST)
