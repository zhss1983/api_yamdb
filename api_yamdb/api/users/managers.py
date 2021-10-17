from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy


class CustomUserManager(BaseUserManager):
    """
    В методе create_superuser() присваиваем
    дефолное значение поля 'role' = 'admin'.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(ugettext_lazy('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)
