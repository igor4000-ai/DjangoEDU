from django.db import models


class Phone(models.Model):
    name = models.CharField('Название', max_length=100)
    image = models.URLField('Изображение')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=0)
    release_date = models.DateField('Дата выпуска')
    lte_exists = models.BooleanField('LTE есть', default=False)
    slug = models.SlugField('Slug', unique=True)

    def __str__(self):
        return self.name
