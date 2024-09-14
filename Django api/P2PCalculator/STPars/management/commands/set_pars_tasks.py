from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = "Set Stock Exchange Pars tasks"

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )



        try:
            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Pars Bitget',
                task='STPars.tasks.sync_refresh_data_BITGET',
            )
        except ValidationError as e:
            print("Periodic task with Name 'Pars Bitget' already exists.\n" + str(e))



        try:
            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Pars Bybit',
                task='STPars.tasks.sync_refresh_data_BYBIT',
            )
        except ValidationError as e:
            print("Periodic task with Name 'Pars Bybit' already exists.\n" + str(e))
        


        try:
            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Pars HTX',
                task='STPars.tasks.sync_refresh_data_HTX',
            )
        except ValidationError as e:
            print("Periodic task with Name 'Pars HTX' already exists.\n" + str(e))

        self.stdout.write(self.style.SUCCESS('Периодические задачи созданы успешно!'))