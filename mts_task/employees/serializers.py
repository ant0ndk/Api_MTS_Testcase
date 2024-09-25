from rest_framework import serializers

from .models import Department, Employee, Position


class EmployeeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name']
        extra_kwargs = {
            'id': {'required': False},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['title', 'employee_id']


class DepartmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Department
        fields = ['id', 'title', 'position', 'last_name']


class EmployeeCreateSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(write_only=True)
    department_name = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name',
                  'position_title', 'department_name']

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        position_title = validated_data['position_title']
        department_name = validated_data['department_name']

        # Проверяем, существует ли указанная должность
        if not Position.objects.filter(title=position_title).exists():
            raise serializers.ValidationError('Position does not exist')

        # Проверяем, существует ли указанный отдел
        if not Department.objects.filter(title=department_name,
                                         position=position_title,
                                         last_name=last_name).exists():
            raise serializers.ValidationError(
                'Department with the given \
                    position and last name does not exist')

        # Добавляем сотрудника
        employee = Employee.objects.create(first_name=first_name,
                                           last_name=last_name)

        # Создаем запись о его должности
        Position.objects.create(title=position_title, employee_id=employee.id)

        return employee
