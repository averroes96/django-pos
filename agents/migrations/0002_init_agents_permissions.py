from django.db import migrations
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from agents.models import Agent

def up(apps, schema_editor):
    
    content_type = ContentType.objects.get_for_model(Agent)
    
    sells_permission = Permission(
        codename="sells_permissions",
        name="Can alter sells",
        content_type=content_type,
    )
    buys_permission = Permission(
        codename="buys_permissions",
        name="Can alter buys",
        content_type=content_type,
    )
    sells_debt_permission = Permission(
        codename="sells_debt_permission",
        name="Can sell with debt",
        content_type=content_type,
    )
    buys_debt_permission = Permission(
        codename='buys_debt_permission',
        name='Can buy with debt',
        content_type=content_type,
    )
    stats_permission = Permission(
        codename='stats_permission',
        name='Can view statistics',
        content_type=content_type,
    )
    
    Permission.objects.bulk_create([
        sells_permission,
        buys_permission,
        sells_debt_permission,
        buys_debt_permission,
        stats_permission,
    ])


def down(apps, schema_editor):
    Permission.objects.filter(codename__in=Agent.AGENT_CUSTOM_PERMISSIONS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=up, reverse_code=down)
    ]