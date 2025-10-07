from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('todo_list', 'Category')
    for name in ['Work', 'Personal', 'Shopping']:
        Category.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]