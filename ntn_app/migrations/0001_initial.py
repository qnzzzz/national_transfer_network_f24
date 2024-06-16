# Generated by Django 5.0.1 on 2024-06-15 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_ID', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('effective_term', models.CharField(max_length=10)),
                ('credits', models.IntegerField()),
                ('equivalent_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ntn_app.course')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ntn_app.university')),
            ],
        ),
    ]