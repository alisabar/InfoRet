# Generated by Django 2.0.2 on 2018-02-28 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0005_auto_20180227_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_name', models.CharField(max_length=300)),
                ('author_name', models.CharField(max_length=300)),
                ('song_url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('num_docs', models.IntegerField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WordsOfSongs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Songs')),
                ('words', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Words')),
            ],
        ),
        migrations.RemoveField(
            model_name='songwords',
            name='song',
        ),
        migrations.RemoveField(
            model_name='word',
            name='song',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
        migrations.DeleteModel(
            name='Songwords',
        ),
        migrations.DeleteModel(
            name='Word',
        ),
    ]