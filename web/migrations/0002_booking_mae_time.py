# Generated by Django 4.1 on 2023-09-14 02:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="mae_time",
            field=models.IntegerField(
                choices=[(1, "上午"), (2, "下午"), (3, "晚上")],
                default=1,
                verbose_name="上下晚时间段",
            ),
            preserve_default=False,
        ),
    ]
