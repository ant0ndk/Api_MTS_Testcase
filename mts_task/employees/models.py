'''
В соответвстии с заданием таблицы НЕ ИМЕЮТ связи друг с другом.
'''

from django.db import models


class Employee(models.Model):
    """
    Модель для хранения информации о работнике (имя, фамилия).
    """
    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Position(models.Model):
    """
    Модель для хранения информации о должности работника
    (название должности, id работника).
    """
    title = models.CharField(max_length=100,
                             verbose_name='Должность')
    employee_id = models.BigIntegerField(verbose_name='id в модели Employee')

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    Модель для хранения информации о департаменте
    (название, должность, фамилия).
    Связка должность-фамилия уникальна.
    """
    title = models.CharField(max_length=100, verbose_name='Отдел')
    position = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['position', 'last_name'],
                                    name='unique_position_last_name')
        ]
