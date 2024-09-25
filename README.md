# Api_MTS_Testcase
Задание:

Сервис содержит 3 таблицы в БД

 

Таблицы не содержат связи друг с другом:

1) id сотрудника, Имя, Фамилия

2) Должность, id сотрудника

3) Отдел, Должность, Фамилия (связка должность-фамилия уникальна)

 

API должен реализовывать 6 методов

Get - Получить список всех сотрудников из 1й таблицы

Get - Получить список всех должностей из 2й таблицы

Get - Получить список всех отделов из 3й таблицы

 

Get - Получить данные одного сотрудника по id (Имя, Фамилия, Должность, Отдел)

Get - Получить список всех сотрудников (id, Имя, Фамилия, Должность, Отдел)

 

Post - Добавить сотрудника на существующую должность в существующий отдел



## Запуск:

Создайте файл `.env` в корневом каталоге с настройками бд:
```
DB_NAME - имя бд
DB_USER - логин для бд
DB_PASSWORD - пароль для бд
DB_HOST - хост для бд
DB_PORT - порт для бд
SECRET_KEY - секретный ключ для django
```


## Запуск локально:

1. Клонируйте репозиторий
2. Установите виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте бд `python manage.py migrate`
5. Запустите сервер `python manage.py runserver`

## Запуск в докере:

1. Создайте файл `docker-compose.yml` с настройками для запуска
2. Запустите контейнер `docker-compose up -d`
3. Выполните команду `docker compose exec web python mts_task/manage.py migrate` для применения миграций.

## Структура

* `employees` - приложение с моделями, сериализаторами, вьюхами
* `employees/migrations` - миграции для создания и заполнения таблиц в бд
* `employees/serializers.py` - сериализаторы
* `employees/views.py` - вьюхи
* `mts_task/settings.py` - настройки проекта
* `mts_task/urls.py` - urls проекта

# Предложения по улучшению стркутуры БД
В данный момент, согласно ТЗ, связей между таблицами нет и все значения являются атомарными.
Это соответсует первой нормальной форме нормализации таблиц в БД. 

Ввиду того, что в соответствии со штатным распианием сотрудник принимается на должность, которая находится в составе отдела, в перспективе он может совмещать должности.

Для расширения функционала прдлагается следующая структура:

1) Таблица Отделов с полем "наименование отдела"

2) Таблица Должностей с полем "Наименование должности" и полем связи с соответсвующей записью в таблице отделов, к которой относится данная должность.

3) Таблица Сотрудников с полями Имя, фамилия и связью с таблицей должностей

ТК сотрудник может совмещать разные должности, реализуем свзь many-to-many через отдельную таблицу EmployeePosition, где создается составной уникальный ключ из 2х полей - employee и position

Вот пример реализации моделей БД:
```
class Department(models.Model):
    name = models.CharField(max_length=100,
        verbose_name='Название департамента')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['pk']


class Position(models.Model):
    name = models.CharField(max_length=100,
        verbose_name='Название должности')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['pk']


class Employee(models.Model):
    first_name = models.CharField(max_length=100,
        verbose_name='Имя сотрудника')
    last_name = models.CharField(max_length=100,
        verbose_name='Фамилия сотрудника')
    positions = models.ManyToManyField(
        Position, through='EmployeePosition', through_fields=('employee', 'position'),
        verbose_name='Должности, на которых находится сотрижник',
        related_name='employee_position')


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['pk']


class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'position'],
                                    name='unique_employee_position')
        ]
```
