"""
Django management command to create NWO divisions and their users
Usage: python manage.py create_division_users
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import NWO, UserProfile


class Command(BaseCommand):
    help = 'Create NWO divisions and their associated user accounts'

    def handle(self, *args, **options):
        # Division data: name, username, password
        # Keep passwords in sync with _get_division_default_password() in views.py
        DIVISIONS = [
            ('NWO CENTRAL', 'nwo_central', 'Nwo@Central@2026!'),
            ('NWO PALARIVATTOM', 'nwo_palarivattom', 'Nwo@Palarivattom@2026!'),
            ('NWO KOCHI', 'nwo_kochi', 'Nwo@Kochi2026!'),
            ('NWO TRIPUNITHARA', 'nwo_tripunithara', 'Nwo@Tripunithura@2026!'),
            ('NWO ANGAMALY', 'nwo_angamaly', 'Nwo@Angamaly@2026!'),
            ('NWO THODUPUZHA', 'nwo_thodupuzha', 'Nwo@Thodupuzha@2026!'),
            ('NWO ALUVA', 'nwo_aluva', 'Nwo@Aluva@2026!'),
            ('NWO MOOVATTUPUZHA', 'nwo_moovattupuzha', 'Nwo@Moovattupuzha@2026!'),
            ('NWO ADIMALY', 'nwo_adimaly', 'Nwo@Adimaly@2026!'),
            ('NWO KATTAPPANA', 'nwo_kattappana', 'Nwo@Kattappana@2026!'),
        ]

        created_count = 0
        updated_count = 0

        self.stdout.write(self.style.WARNING('Creating NWO Divisions and Users...'))
        self.stdout.write('=' * 70)

        for division_name, username, password in DIVISIONS:
            # Create or get the NWO division
            nwo, nwo_created = NWO.objects.get_or_create(
                name=division_name,
                defaults={'remarks': f'Auto-created division for {division_name}'}
            )

            if nwo_created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Division: {division_name}'))
                created_count += 1
            else:
                self.stdout.write(f'→ Division already exists: {division_name}')
                updated_count += 1

            # Create or update the user
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@nwo.in',
                    'first_name': division_name.split()[-1],
                    'is_staff': True,
                    'is_active': True,
                }
            )

            # Always update password
            user.set_password(password)
            user.save()

            if user_created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created User: {username}'))
            else:
                self.stdout.write(f'  → User already exists: {username}')

            # Create or update UserProfile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'per_no': f'PER-{division_name.split()[-1].upper()}',
                    'designation': 'Division Officer',
                    'division': nwo,
                }
            )

            if profile_created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created Profile: {username}'))
            else:
                self.stdout.write(f'  → Profile already exists: {username}')

        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('\n✅ All divisions and users created successfully!\n'))

        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_email = os.environ.get('ADMIN_EMAIL')

        if admin_username and admin_password and admin_email:
            self.stdout.write(self.style.WARNING('Creating default superuser account...'))
            admin_user, admin_created = User.objects.get_or_create(
                username=admin_username,
                defaults={
                    'email': admin_email,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            admin_user.email = admin_email
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.set_password(admin_password)
            admin_user.save()

            if admin_created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created superuser: {admin_username}'))
            else:
                self.stdout.write(f'  → Updated superuser: {admin_username}')
            self.stdout.write('=' * 70)
            self.stdout.write(self.style.WARNING('SUPERUSER LOGIN CREDENTIALS:'))
            self.stdout.write(f'  Username: {self.style.SUCCESS(admin_username)}')
            self.stdout.write(f'  Password: {self.style.SUCCESS(admin_password)}')
            self.stdout.write(f'  Email: {self.style.SUCCESS(admin_email)}')
            self.stdout.write('\n' + '=' * 70)

        # Display division credentials
        self.stdout.write(self.style.WARNING('DIVISION LOGIN CREDENTIALS:'))
        self.stdout.write('=' * 70)
        for division_name, username, password in DIVISIONS:
            self.stdout.write(f'\n{division_name}')
            self.stdout.write(f'  Username: {self.style.SUCCESS(username)}')
            self.stdout.write(f'  Password: {self.style.SUCCESS(password)}')
        self.stdout.write('\n' + '=' * 70)
