from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from api.models import Ingredient

TABLES = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        n = 0
        for models, file_name in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/data/{file_name}',
                'r',
                encoding='utf-8'
            ) as file:
                reader = DictReader(file)
                data = []
                for line in reader:
                    data.append(models(**line))
                models.objects.bulk_create(data)
            self.stdout.write(self.style.WARNING(
                f'Импорт данных из {file_name}...')
            )
            n += 1
        if n == len(TABLES):
            self.stdout.write(self.style.SUCCESS(
                'Импорт из CSV файлов успешно завершён.')
            )
