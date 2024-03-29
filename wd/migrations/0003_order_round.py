# Generated by Django 3.0 on 2021-01-12 12:14

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wd', '0002_game_creator_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameround', to='wd.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_for_city_1', models.BooleanField(default=False, verbose_name='статус на город1')),
                ('status_for_city_2', models.BooleanField(default=False, verbose_name='статус на город2')),
                ('status_for_city_3', models.BooleanField(default=False, verbose_name='статус на город3')),
                ('status_for_city_4', models.BooleanField(default=False, verbose_name='статус на город4')),
                ('shield_for_city_1', models.BooleanField(default=False, verbose_name='щит на город1')),
                ('shield_for_city_2', models.BooleanField(default=False, verbose_name='щит на город2')),
                ('shield_for_city_3', models.BooleanField(default=False, verbose_name='щит на город3')),
                ('shield_for_city_4', models.BooleanField(default=False, verbose_name='щит на город4')),
                ('build_tech', models.BooleanField(default=False, verbose_name='кач ядерки')),
                ('buy_rockets', models.IntegerField(default=0, max_length=1, verbose_name='покупка ракетт')),
                ('eco_up', models.BooleanField(default=False, verbose_name='Улучшение экологии')),
                ('rockets_to', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Вашингтон'), (2, 'Нью Йорк'), (3, 'Чикаго'), (4, 'Лас Вегас'), (5, 'Пекин'), (6, 'Шанхай'), (7, 'Гуанчжоу'), (8, 'Гонконг')], max_length=15, verbose_name='Города под прицелом')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_for', to='wd.Country')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Round', to='wd.Round')),
            ],
        ),
    ]
