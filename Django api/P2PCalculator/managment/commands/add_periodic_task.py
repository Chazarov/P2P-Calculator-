from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import Celery

class Command(BaseCommand):
    help = 'Создает периодические задачи'

    def handle(self, *args, **kwargs):
        # Создаем интервал для задачи (например, каждую минуту)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )

        # Создаем периодическую задачу
        PeriodicTask.objects.get_or_create(
            interval=schedule,                  # используем интервал
            name='Pars Bybit',             # уникальное имя задачи
            task='STPars.tasks.sync_refresh_data_BYBIT',  # путь к задаче
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,                  # используем интервал
            name='Pars Bitget',             # уникальное имя задачи
            task='STPars.tasks.sync_refresh_data_BITGET',  # путь к задаче
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,                  # используем интервал
            name='Pars HTX',             # уникальное имя задачи
            task='STPars.tasks.sync_refresh_data_HTX',  # путь к задаче
        )

        self.stdout.write(self.style.SUCCESS('Периодические задачи созданы успешно!'))