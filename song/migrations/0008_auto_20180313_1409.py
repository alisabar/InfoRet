# Generated by Django 2.0.2 on 2018-03-13 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0007_auto_20180228_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordsofsongs',
            name='songs',
        ),
        migrations.RemoveField(
            model_name='wordsofsongs',
            name='words',
        ),
        migrations.AddField(
            model_name='songs',
            name='word',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='song.Words'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='words',
            name='times',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='songs',
            name='song_url',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='words',
            name='num_docs',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='WordsOfSongs',
        ),
    ]