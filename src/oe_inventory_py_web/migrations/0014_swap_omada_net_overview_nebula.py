from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oe_inventory_py_web', '0013_rename_omada_customuser_net_overview'),
    ]

    operations = [
        # The screen formerly called "Net Overview" (Omada) goes back to "Omada",
        # and the Nebula screen becomes the new "Net Overview".
        migrations.RenameField(model_name='customuser', old_name='net_overview', new_name='omada'),
        migrations.RenameField(model_name='customuser', old_name='nebula', new_name='net_overview'),
        migrations.AlterField(model_name='customuser', name='omada',
                              field=models.IntegerField(default=0, verbose_name='omada')),
        migrations.AlterField(model_name='customuser', name='net_overview',
                              field=models.IntegerField(default=0, verbose_name='net_overview')),
    ]
