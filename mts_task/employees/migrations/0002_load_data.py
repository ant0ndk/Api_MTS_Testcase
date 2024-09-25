from django.db import migrations
from employees.models import Employee, Position, Department


def _load_data(apps, schema_editor):
    """
    Загрузка данных в таблицы Employee, Position, Department.
    Команды:
        python manage.py makemigrations
        python manage.py migrate
    """
    Employee.objects.bulk_create(
        [
            Employee(pk=1, first_name="Василий", last_name="Васильев"),
            Employee(pk=2, first_name="Иван", last_name="Иванов"),
            Employee(pk=3, first_name="Петр", last_name="Петров"),
            Employee(pk=4, first_name="Сидор", last_name="Сидоров"),
        ]
    )
    Position.objects.bulk_create(
        [
            Position(title="DevOps", employee_id=1),
            Position(title="BackendDev", employee_id=2),
            Position(title="FrontendDev", employee_id=3),
            Position(title="FrontendDev", employee_id=4),
        ]
    )
    Department.objects.bulk_create(
        [
            Department(title="Developers", position="DevOps", last_name="Васильев"),
            Department(title="Developers", position="BackendDev", last_name="Иванов"),
            Department(title="Developers", position="FrontendDev", last_name="Петров"),
            Department(title="Developers", position="FrontendDev", last_name="Сидоров"),
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_load_data)
    ]