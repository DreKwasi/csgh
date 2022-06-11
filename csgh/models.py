from django.db import models

# model to hold info about endpoint, tokens and auths
class ApiDetail(models.Model):
    name = models.CharField(max_length=225, default="oryxapi")
    json_auth = models.CharField(max_length=10000)
    dn_auth = models.CharField(max_length=10000)
    json_url = models.CharField(max_length=100, default="https://mpharmatestapp.oryxhr.com/api/Delivery/")
    dn_url = models.CharField(max_length=100, default="https://mpharmatestapp.oryxhr.com/api/Delivery/Report/")

    def __str__(self):
        return self.name


# model to house information on Delivery Notes
class DocumentLogs(models.Model):
    deliveryId = models.CharField(max_length=10, unique=True)
    startDate = models.DateField('date processed')
    shipFromName = models.CharField(max_length=100)
    shipToName = models.CharField(max_length=100)

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.deliveryId

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'DocumentLogs'
        ordering = ['-startDate']

class SupplyData(models.Model):
    deliveryId = models.CharField(max_length=20)
    shipToName = models.CharField(max_length=100)
    product = models.CharField(max_length=225)
    qty = models.IntegerField()
    created_date = models.DateField('date processed')

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.deliveryId

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'Supply Data'
        ordering = ['-created_date']


class SalesQuoteLogs(models.Model):
    deliveryId = models.CharField(max_length=10, unique=True)
    created_date = models.DateField('date processed')
    shipFromName = models.CharField(max_length=100)
    shipToName = models.CharField(max_length=100)
    salesquote = models.FileField()

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.deliveryId

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'Sales Quotes'
        ordering = ['-created_date']

class RetailPrice(models.Model):
    product_id = models.CharField(max_length=10, unique=True)
    product = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.product

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'Retail Prices'
        ordering = ['-price']

class WHPrice(models.Model):
    product_id = models.CharField(max_length=10, unique=True)
    product = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.product

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'WH Prices'
        ordering = ['-price']

class FacilityList(models.Model):
    facility_name = models.CharField(max_length=225)
    bu = models.CharField(max_length=225)

    # representing the str attr of the object as the DN ID
    def __str__(self):
        return self.facility_name

    # declaring the plural form of the model/table & ordering rows in descending fashion
    class Meta:
        verbose_name_plural = 'Facilities'
        ordering = ['-facility_name']

