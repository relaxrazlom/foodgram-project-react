import csv

from django.core.management import BaseCommand

from recipe.models import Ingredient



def import_csv_db():
    model = Ingredient
    file = 'data/ingredients.csv'
    for row in csv.DictReader(open(file, encoding='utf-8')):
        p = model(name=row['name'],
                  measurement_unit=row['measurement_unit']
        )
        p.save()
    print(f"Загрузка данных из таблицы {file} завершена успешно.")


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Начало загрузки данных в базу данных')
        try:
            import_csv_db()

        except Exception as error:
            print(f"Сбой в работе импорта: {error}.")

        finally:
            print('Загрузка всех данных произведена успешно')
