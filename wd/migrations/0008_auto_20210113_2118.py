# Generated by Django 3.0 on 2021-01-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wd', '0007_auto_20210113_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='rockets_to',
            field=models.CharField(blank=True, choices=[(1, 'Вашингтон'), (2, 'Нью Йорк'), (3, 'Чикаго'), (4, 'Лас Вегас'), (5, 'Пекин'), (6, 'Шанхай'), (7, 'Гуанчжоу'), (8, 'Гонконг'), (9, 'Москва'), (10, 'Санкт-Петербург'), (11, 'Уфа'), (12, 'Рязань'), (13, 'Тегеран'), (14, 'Шираз'), (15, 'Эсфахан'), (16, 'Тебриз'), (17, 'Пхеньян'), (18, 'Саривон'), (19, 'Синпхо'), (20, 'Синыйджу'), (21, 'Берлин'), (22, 'Гамбург'), (23, 'Мюнхен'), (24, 'Кёльн')], max_length=254, null=True, verbose_name='Города под прицелом'),
        ),
        migrations.AlterField(
            model_name='order',
            name='saction_to',
            field=models.CharField(blank=True, choices=[(1, 'США'), (2, 'Китай'), (3, 'Россия'), (4, 'Иран'), (5, 'Cев. Корея'), (6, 'Германия')], max_length=254, null=True, verbose_name='Страны для санкции'),
        ),
    ]