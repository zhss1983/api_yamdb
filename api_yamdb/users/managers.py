from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,
                    **extra_fields):
        """
        Проверяет наличие email при создании пользователя
        и сохраняет пароль в шифрованном виде.
        """
        if not email:
            raise ValueError('Пользователи должны иметь e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,
                         **extra_fields):
        """Создаёт и сохраняет суперпользователя."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields)
        user.role = 'admin'
        user.save(using=self._db)

        return user
