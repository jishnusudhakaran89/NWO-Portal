# Fixing Login Issues After Deployment

## Problem
After successful deployment, users cannot login with their credentials. The error message is:
> "Please enter a correct username and password. Note that both fields may be case-sensitive."

## Root Cause
There was a password mismatch in the codebase:
- The `create_division_users.py` management command created users with password `Nwo@Kochi@2026!` (with @ symbol)
- But the `views.py` file defines the default password as `Nwo@Kochi2026!` (without @)
- During deployment, the management command ran with the incorrect password

## Solution

### Option 1: Fix via Django Management Command (Recommended for Deployed App)

If you have access to the Render dashboard or deployed instance:

```bash
# SSH into your Render service or use the web terminal
python manage.py fix_user_passwords
```

This command will:
1. Check all division users
2. Update passwords to match the correct defaults from views.py
3. Display a summary of what was updated

### Option 2: Manual Fix via Django Shell

```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User
from inventory.models import NWO

# Update each division user
divisions_passwords = {
    'NWO CENTRAL': 'Nwo@Central@2026!',
    'NWO PALARIVATTOM': 'Nwo@Palarivattom@2026!',
    'NWO KOCHI': 'Nwo@Kochi2026!',  # Note: no @ between Kochi and 2026
    'NWO TRIPUNITHARA': 'Nwo@Tripunithura@2026!',
    'NWO ANGAMALY': 'Nwo@Angamaly@2026!',
    'NWO THODUPUZHA': 'Nwo@Thodupuzha@2026!',
    'NWO ALUVA': 'Nwo@Aluva@2026!',
    'NWO MOOVATTUPUZHA': 'Nwo@Moovattupuzha@2026!',
    'NWO ADIMALY': 'Nwo@Adimaly@2026!',
    'NWO KATTAPPANA': 'Nwo@Kattappana@2026!',
}

for division_name, password in divisions_passwords.items():
    division = NWO.objects.get(name=division_name)
    users = User.objects.filter(profile__division=division)
    for user in users:
        user.set_password(password)
        user.save()
        print(f"Updated {user.username}")

exit()
```

### Option 3: Update via Render Dashboard Terminal

1. Go to your Render service (nwo-portal)
2. Click the "Shell" tab
3. Run: `python manage.py fix_user_passwords`
4. Verify all passwords were updated

## Verification

After running the fix, try logging in with:

| Division | Username | Password |
|----------|----------|----------|
| NWO CENTRAL | nwo_central | Nwo@Central@2026! |
| NWO PALARIVATTOM | nwo_palarivattom | Nwo@Palarivattom@2026! |
| NWO KOCHI | nwo_kochi | Nwo@Kochi2026! |
| NWO TRIPUNITHARA | nwo_tripunithara | Nwo@Tripunithura@2026! |
| NWO ANGAMALY | nwo_angamaly | Nwo@Angamaly@2026! |
| NWO THODUPUZHA | nwo_thodupuzha | Nwo@Thodupuzha@2026! |
| NWO ALUVA | nwo_aluva | Nwo@Aluva@2026! |
| NWO MOOVATTUPUZHA | nwo_moovattupuzha | Nwo@Moovattupuzha@2026! |
| NWO ADIMALY | nwo_adimaly | Nwo@Adimaly@2026! |
| NWO KATTAPPANA | nwo_kattappana | Nwo@Kattappana@2026! |

## Code Changes Made

1. **Fixed password in `inventory/management/commands/create_division_users.py`**
   - Changed NWO KOCHI password from `Nwo@Kochi@2026!` to `Nwo@Kochi2026!`
   - Now matches the default password defined in `views.py`

2. **Created new management command: `inventory/management/commands/fix_user_passwords.py`**
   - Allows fixing existing user passwords after deployment
   - Can be run on deployed instance without code changes

3. **Updated `RENDER_CHECKLIST.md`**
   - Added quick fix for invalid credentials issue
   - References the new management command

## Prevention for Future Deployments

The passwords are now synchronized across:
- `inventory/management/commands/create_division_users.py` - Creates new users during deployment
- `inventory/views.py` - Defines default passwords for password reset
- `inventory/management/commands/fix_user_passwords.py` - Fixes passwords if they get out of sync

All new deployments will now use the correct passwords automatically.
