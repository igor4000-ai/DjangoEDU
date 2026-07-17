import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_path = options.get('path') or 'phones.csv'
        
        if not os.path.exists(csv_path):
            self.stderr.write(f"File not found: {csv_path}")
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            phone_obj = Phone(
                id=phone['id'],
                name=phone['name'],
                price=phone['price'],
                image=phone['image'],
                release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d').date(),
                lte_exists=phone['lte_exists'].lower() == 'true',
                slug=slugify(phone['name'])
            )
            phone_obj.save()
        
        self.stdout.write(f"Successfully imported {len(phones)} phones")
