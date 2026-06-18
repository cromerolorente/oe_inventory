from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oe_inventory_py_web', '0012_customuser_nebula'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='omada',
            new_name='net_overview',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='net_overview',
            field=models.IntegerField(default=0, verbose_name='net_overview'),
        ),
    ]
