# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

#--------------------------------------------------------------------------------------------------------#

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    descripcion = models.CharField(max_length=500)
    def __str__(self):
     return f"{self.nombre} - {self.saldo}"

class RegistroGasto(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=False)
    motivo = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=100, decimal_places=0)
    def save(self, *args, **kwargs):
        if self.pk is None:  # Si es un nuevo registro de gasto
            if self.cuenta.saldo < self.monto:
                raise ValidationError("Saldo insuficiente en la cuenta.")
            self.cuenta.saldo -= self.monto
            self.cuenta.save()
        super(RegistroGasto, self).save(*args, **kwargs)

class RegistroCambios(models.Model):
    gasto = models.ForeignKey(RegistroGasto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    justificacion = models.CharField(max_length=500)
    monto_anterior = models.DecimalField(max_digits=100, decimal_places=0)
    monto_nuevo = models.DecimalField(max_digits=100, decimal_places=0)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Actualizar el saldo de la cuenta
        self.cuenta.saldo += self.monto_anterior  # Agrega el monto anterior
        self.cuenta.saldo -= self.monto_nuevo  # Descuenta el nuevo monto
        self.cuenta.save()
        super(RegistroCambios, self).save(*args, **kwargs)

