"""
Django management command to fix user passwords after deployment
Usage: python manage.py fix_user_passwords
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import NWO


class Command(BaseCommand):
    help = 'Fix user passwords to match deployment defaults'

    def handle(self, *args, **options):
        # Passwords that match the ones in _get_division_default_password() in views.py
        CORRECT_PASSWORDS = {
            'NWO CENTRAL': 'Nwo@Central@2026!',
            'NWO PALARIVATTOM': 'Nwo@Palarivattom@2026!',
            'NWO KOCHI': 'Nwo@Kochi2026!',
            'NWO TRIPUNITHARA': 'Nwo@Tripunithura@2026!',
            'NWO ANGAMALY': 'Nwo@Angamaly@2026!',
            'NWO THODUPUZHA': 'Nwo@Thodupuzha@2026!',
            'NWO ALUVA': 'Nwo@Aluva@2026!',
            'NWO MOOVATTUPUZHA': 'Nwo@Moovattupuzha@2026!',
            'NWO ADIMALY': 'Nwo@Adimaly@2026!',
            'NWO KATTAPPANA': 'Nwo@Kattappana@2026!',
        }

        self.stdout.write(self.style.WARNING('\n' + '='*70))
        self.stdout.write(self.style.WARNING('FIXING USER PASSWORDS - DEPLOYMENT ISSUE'))
        self.stdout.write(self.style.WARNING('='*70 + '\n'))

        updated_count = 0

        for division_name, correct_password in CORRECT_PASSWORDS.items():
            try:
                division = NWO.objects.get(name=division_name)
                # Get the user associated with this division
                users_with_profile = User.objects.filter(profile__division=division)

                for user in users_with_profile:
                    # Check if password needs updating
                    if not user.check_password(correct_password):
                        user.set_password(correct_password)
                        user.save()
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Updated password for: {user.username} ({division_name})')
                        )
                        updated_count += 1
                    else:
                        self.stdout.write(
                            f'→ Password already correct for: {user.username} ({division_name})'
                        )
            except NWO.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠ Division not found: {division_name}'))

        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✅ Password update complete! {updated_count} user(s) updated.'))
        self.stdout.write('='*70)
        self.stdout.write(self.style.WARNING('\nDIVISION LOGIN CREDENTIALS (CORRECT PASSWORDS):'))
        self.stdout.write('='*70)
        
        division_data = [
            ('NWO CENTRAL', 'nwo_central'),
            ('NWO PALARIVATTOM', 'nwo_palarivattom'),
            ('NWO KOCHI', 'nwo_kochi'),
            ('NWO TRIPUNITHARA', 'nwo_tripunithara'),
            ('NWO ANGAMALY', 'nwo_angamaly'),
            ('NWO THODUPUZHA', 'nwo_thodupuzha'),
            ('NWO ALUVA', 'nwo_aluva'),
            ('NWO MOOVATTUPUZHA', 'nwo_moovattupuzha'),
            ('NWO ADIMALY', 'nwo_adimaly'),
            ('NWO KATTAPPANA', 'nwo_kattappana'),
        ]

        for division_name, username in division_data:
            password = CORRECT_PASSWORDS.get(division_name, 'N/A')
            self.stdout.write(f'\n{division_name}')
            self.stdout.write(f'  Username: {self.style.SUCCESS(username)}')
            self.stdout.write(f'  Password: {self.style.SUCCESS(password)}')

        self.stdout.write('\n' + '='*70 + '\n')
