from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='id')
    user_name = models.CharField(db_column='username')
    user_surname = models.CharField(db_column='user_surname')
    user_hobby = models.CharField(db_column='hobby')
    class Meta:
        db_table = 'Test_Users'
        managed = True