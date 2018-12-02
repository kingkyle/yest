import random
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

def random_id():
    randID = random.randint(1000000000, 9999999999)
    return randID

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """ Creates and Saves a User with the entered Email, First Name, Last Name and Password """
        if not email:
            raise ValueError("Please Provide a Valid Email")

        if not first_name:
            raise ValueError("Please Provide a Legal First Name")

        if not last_name:
            raise ValueError("Please Provide a Legal Last Name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, email, password=None):
        if not email:
            raise ValueError("Email is Required")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Creates and Saves a Superuser with the entered Email and Password """

        user = self.create_admin(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email Address', max_length=225)
    first_name = models.CharField(max_length=200, verbose_name='First Name')
    last_name = models.CharField(max_length=200, verbose_name='Last Name')

    is_active = models.BooleanField(default=True, verbose_name='active',
                                    help_text=_('Designates whether this user should be treated as active.'
                                                'Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(default=False, verbose_name='staff',
                                   help_text=_('Designates whether the user can log into this admin site.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    user_no = models.IntegerField(unique=True, verbose_name='User_ID', default=random_id, editable=False)
    country = models.CharField(max_length=200, verbose_name='Country', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)
    phone = models.IntegerField(verbose_name='Phone Number', null=True, blank=True)
    state = models.CharField(max_length=200, verbose_name='State/Region', null=True, blank=True)
    postal_code = models.CharField(max_length=100, verbose_name='Postal Code', null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} Profile'


class Address(models.Model):
    useraddress = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=200, verbose_name='Country')
    address = models.CharField(max_length=200, verbose_name='Address')
    state = models.CharField(max_length=200, verbose_name='State/Region')
    postal_code = models.CharField(max_length=100, verbose_name='Postal Code')

    def __str__(self):
        return f'{self.address}'