# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LittlelemonapiCart(models.Model):
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    menuitem = models.ForeignKey('LittlelemonapiMenuitem', models.DO_NOTHING)
    user = models.ForeignKey('LittlelemonapiCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_cart'
        unique_together = (('user', 'menuitem'),)


class LittlelemonapiCategory(models.Model):
    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=225)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_category'


class LittlelemonapiCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    contact = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_customuser'


class LittlelemonapiCustomuserGroups(models.Model):
    customuser = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_customuser_groups'
        unique_together = (('customuser', 'group'),)


class LittlelemonapiCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class LittlelemonapiMenuitem(models.Model):
    title = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    featured = models.BooleanField()
    category = models.ForeignKey(LittlelemonapiCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_menuitem'


class LittlelemonapiOrder(models.Model):
    status = models.BooleanField()
    total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    date = models.DateField()
    delivery_crew = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING, related_name='littlelemonapiorder_user_set')

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_order'


class LittlelemonapiOrderitem(models.Model):
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    menuitem = models.ForeignKey(LittlelemonapiMenuitem, models.DO_NOTHING)
    user = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'LittleLemonAPI_orderitem'
        unique_together = (('user', 'menuitem'),)


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


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(LittlelemonapiCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(LittlelemonapiCustomuser, models.DO_NOTHING)
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
