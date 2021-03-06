# Generated by Django 2.0.2 on 2018-03-18 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='songofword',
            options={'ordering': ['word']},
        ),
        migrations.AlterModelOptions(
            name='words',
            options={'ordering': ['word']},
        ),
        migrations.AddField(
            model_name='songs',
            name='is_searchable',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='songs',
            name='song_name',
            field=models.CharField(db_index=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='words',
            name='word',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
