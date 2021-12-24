from datetime import datetime, timedelta
from typing import Reversible

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractBaseUser, Group, Permission,
                                        PermissionsMixin)
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import jwt


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not password:
            raise ValueError(_('The Password must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True, max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Activo'), default=False)
    date_joined = models.DateTimeField(
        _('Fecha de Registro'), default=timezone.now)

    @property
    def token(self):
        token = jwt.encode(
            {
                'email': self.email,
                'exp': datetime.utcnow()+timedelta(hours=24)
            },
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def post_save(sender, instance, **kwargs):
    if instance.is_staff:
        group, _ = Group.objects.get_or_create(name='AdminUser')
        for p in Permission.objects.all():
            group.permissions.add(p)

    else:
        group, _ = Group.objects.get_or_create(name='User')
        for p in Permission.objects.all():
            #print(p.content_type.__str__())
            if 'accounts' in p.content_type.__str__() or 'grades' in p.content_type.__str__():
                group.permissions.add(p)
        #print(group.permissions.all())
    instance.groups.add(group)
