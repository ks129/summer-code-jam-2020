# Generated by Django 3.1 on 2020-08-08 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retro_news', '0002_blogarticle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogarticle',
            name='date_created',
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
