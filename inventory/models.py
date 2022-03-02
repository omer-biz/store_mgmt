from django.db import models
from django.utils import timezone

CHOICES = (
    ("fungable", "Fungable"),
    ("non-fungable", "Non-Fungable"),
)

class InstoreItem(models.Model):
    name = models.CharField("Product Name", max_length=255, blank=False)
    model = models.CharField("Model", max_length=255)
    serie = models.CharField("Serie", max_length=255)
    quantity = models.PositiveIntegerField("Quantity")
    type = models.CharField("Type", max_length=255, choices=CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instore Item"
        verbose_name_plural = "Instore Items"

class IncomingItem(models.Model):
    name = models.CharField("Product Name", max_length=255, blank=False)
    model = models.CharField("Model", max_length=255)
    serie = models.CharField("Serie", max_length=255)
    quantity = models.PositiveIntegerField("Quantity")
    unit_price = models.FloatField("Unit Price")
    total_price = models.FloatField("Total Price", blank=True, null=True)
    registered_date = models.DateField("Registered Date", default=timezone.now)
    type = models.CharField("Type", max_length=255, choices=CHOICES)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        InstoreItem.objects.create(
            name=self.name,
            model=self.model,
            serie=self.serie,
            quantity=self.quantity,
            type=self.type,
        ).save()
        super(IncomingItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Incomming Item"
        verbose_name_plural = "Incomming Items"

class Employee(models.Model):
    name = models.CharField("Employee Name", max_length=255, blank=False)
    employee_id = models.CharField("Employee ID", max_length=100, blank=False)
    secret_key = models.CharField("Secret Key", max_length=100, blank=False)

    def __str__(self):
        return self.name

class OrderByEmployee(models.Model):
    name = models.CharField("Order Name", max_length=100)
    description = models.TextField("Description")
    approved_by_store_mgmt = models.BooleanField("Approved by store manager", default=False)
    ordered_by = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OnHandItem(models.Model):
    name = models.CharField("Product Name", max_length=255, blank=False)
    model = models.CharField("Model", max_length=255)
    serie = models.CharField("Serie", max_length=255)
    quantity = models.PositiveIntegerField("Quantity")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField("Type", max_length=255, choices=CHOICES)
    date = models.DateField("Date", default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "On Hand Item"
        verbose_name_plural = "On Hand Itmes"
