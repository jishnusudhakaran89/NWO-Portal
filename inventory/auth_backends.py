from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CaseInsensitiveModelBackend(ModelBackend):
    """Authenticate with a case-insensitive username or email."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            email_field = getattr(UserModel, 'EMAIL_FIELD', 'email')
            if email_field and email_field != UserModel.USERNAME_FIELD:
                try:
                    user = UserModel.objects.get(**{f'{email_field}__iexact': username})
                except UserModel.DoesNotExist:
                    return None
            else:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
