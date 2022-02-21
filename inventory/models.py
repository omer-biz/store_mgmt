from django.db import models

class ItemInStore(models.Model):
    name = models.CharField("Product Name", max_length=255, blank=False)
    model = models.CharField("Model", max_length=255)
    serie = models.CharField("Serie", max_length=255)
    quantity = models.IntegerField("Quantity")
    unit_price = models.FloatField("Unit Price")
    total_price = models.FloatField("Total Price", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super(ItemInStore, self).save(*args, **kwargs)

    # @property
    # def total_price(self):
    #     return self.unit_price * self.quantity

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

class Employee(models.Model):
    name = models.CharField("Employee Name", max_length=255, blank=False)

    def __str__(self):
        return self.name

class ItemOnEmpl(ItemInStore):
    onhand_quantity = models.IntegerField("Onhand Quantity", default=0, blank=True, null=True)
    employee = models.ManyToManyField(Employee)

    class Meta:
        verbose_name = "Item with employee"
        verbose_name_plural = "Items with employee"
