import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .defaults import DIVISION_CREDENTIALS
from .models import NWO, UserProfile

logger = logging.getLogger(__name__)


@receiver(post_migrate, dispatch_uid='inventory_create_division_users')
def create_division_users(sender, **kwargs):
    if sender.name != 'inventory':
        return

    logger.warning('inventory.signals.create_division_users: post_migrate for inventory started')
    print('inventory.signals.create_division_users: post_migrate for inventory started')

    for division_name, username, password in DIVISION_CREDENTIALS:
        nwo, nwo_created = NWO.objects.get_or_create(
            name=division_name,
            defaults={'remarks': f'Auto-created division for {division_name}'}
        )
        if nwo_created:
            logger.warning('Created NWO division: %s', division_name)
            print(f'Created NWO division: {division_name}')

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@nwo.in',
                'first_name': division_name.split()[-1],
                'is_staff': True,
                'is_active': True,
            }
        )

        if created:
            logger.warning('Created user: %s', username)
            print(f'Created user: {username}')

        if created or not user.check_password(password):
            user.set_password(password)
            user.save()
            logger.warning('Set password for user: %s', username)
            print(f'Set password for user: {username}')

        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'per_no': f'PER-{division_name.split()[-1].upper()}',
                'designation': 'Division Officer',
                'division': nwo,
            }
        )

        if profile_created:
            logger.warning('Created profile for user: %s', username)
            print(f'Created profile for user: {username}')

        if not profile_created and (profile.division_id != nwo.id or profile.designation != 'Division Officer'):
            profile.division = nwo
            profile.designation = 'Division Officer'
            profile.save(update_fields=['division', 'designation'])
            logger.warning('Updated profile for user: %s', username)
            print(f'Updated profile for user: {username}')

    logger.warning('inventory.signals.create_division_users: completed')
    print('inventory.signals.create_division_users: completed')
