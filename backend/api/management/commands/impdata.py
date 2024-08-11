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
        for model, file_name in TABLES.items():
            add = 0
            sum = 0
            self.stdout.write(self.style.WARNING(
                f'Импорт данных из {file_name}')
            )
            with open(
                f'{settings.BASE_DIR}/data/{file_name}',
                'r',
                encoding='utf-8'
            ) as file:
                reader = DictReader(file)
                for line in reader:
                    sum += 1
                    try:
                        model.objects.create(**line)
                        add += 1
                    except Exception:
                        continue
            self.stdout.write(self.style.SUCCESS(
                f'Импорт из {file_name} закончен. Добавлено {add} из {sum}')
            )
            n += 1
        if n == len(TABLES):
            self.stdout.write(self.style.SUCCESS(
                'Импорт из CSV файлов успешно завершён.')
            )
