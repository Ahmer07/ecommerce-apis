from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_customer(self, email, password,**kwargs):
        kwargs.setdefault('role', 'customer')
        return self.create_user(email, password **kwargs)

    def create_superadmin(self, email, password, **kwargs):
        kwargs.setdefault('role', 'super_admin')
        return self.create_user(email, password, **kwargs)
