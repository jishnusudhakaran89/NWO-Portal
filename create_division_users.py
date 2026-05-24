#!/usr/bin/env python
"""
Script to create NWO divisions and their associated user accounts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nwo_portal.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import NWO, UserProfile
from inventory.defaults import DIVISION_CREDENTIALS

# Division data: name, username, password
DIVISIONS = DIVISION_CREDENTIALS

def create_divisions_and_users():
    print("Creating NWO Divisions and Users...")
    
    for division_name, username, password in DIVISIONS:
        # Create or get the NWO division
        nwo, created = NWO.objects.get_or_create(
            name=division_name,
            defaults={'remarks': f'Auto-created division for {division_name}'}
        )
        
        if created:
            print(f"✓ Created Division: {division_name}")
        else:
            print(f"→ Division already exists: {division_name}")
        
        # Create or update the user
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@nwo.in',
                'first_name': division_name.split()[-1],  # Use last word as first name
                'is_staff': True,
                'is_active': True,
            }
        )
        
        # Set password
        user.set_password(password)
        user.save()
        
        if user_created:
            print(f"  ✓ Created User: {username}")
        else:
            print(f"  → User already exists: {username}")
        
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
            print(f"  ✓ Created Profile: {username}")
        else:
            print(f"  → Profile already exists: {username}")
    
    print("\n" + "="*60)
    print("DIVISION LOGIN CREDENTIALS:")
    print("="*60)
    for division_name, username, password in DIVISIONS:
        print(f"{division_name}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print()

if __name__ == '__main__':
    create_divisions_and_users()
    print("\nAll divisions and users created successfully!")
