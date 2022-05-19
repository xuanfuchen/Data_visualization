# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CompanyInfo(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    stock_symbol = models.CharField(max_length=255)
    country = models.CharField(max_length=255, blank=True, null=True)
    exchange = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    employees = models.CharField(max_length=255, blank=True, null=True)
    sales = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info'


class PriceHistory(models.Model):
    company_name = models.CharField(max_length=255)
    stock_symbol = models.CharField(primary_key=True, max_length=255)
    price_date = models.DateField()
    open = models.CharField(max_length=255, blank=True, null=True)
    high = models.CharField(max_length=255, blank=True, null=True)
    low = models.CharField(max_length=255, blank=True, null=True)
    close = models.CharField(max_length=255, blank=True, null=True)
    volume = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'price_history'
        unique_together = (('stock_symbol', 'price_date'),)
