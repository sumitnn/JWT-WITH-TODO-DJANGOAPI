from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.
class Same(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created']
        abstract=True

# custumManager
class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
            
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        password=set_password(password)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email_activated', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('email_activated') is not True:
            raise ValueError('Email Activation must have email_activated=True.')

        return self._create_user(username, email, password, **extra_fields)



# CustumUSer
class User(AbstractBaseUser, Same,PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),}
    )
    email = models.EmailField(_('Enter Your Email'),unique=True)
    email_activated=models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    emailtoken= models.UUIDField(unique=True,null=True,blank=True)

    first_name=None 
    last_name=None
    objects = MyUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def Token(self):
        import jwt
        from django.conf import settings
        import datetime
        token = jwt.encode({
                'username':self.username,
                'email': self.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }, settings.SECRET_KEY, algorithms="HS256")
        return token






