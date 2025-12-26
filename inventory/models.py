from django.db import models
from django.db import models, transaction

class Location(models.Model):
    LOCATION_TYPES = (
        ("WAREHOUSE", "Anbar"),
        ("STORE", "Mağaza"),
        ("SERVICE", "Servis"),
    )

    name = models.CharField(max_length=150)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"


class Fridge(models.Model):
    STATUS_CHOICES = (
        ("WORKING", "İşləyir"),
        ("BROKEN", "Xarab"),
        ("REPAIR", "Təmirdə"),
        ("SCRAPPED", "Utilizasiya"),
    )

    barcode = models.CharField(max_length=100, unique=True)
    akt_no = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="WORKING")
    current_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.barcode


class Transfer(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    from_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="from_transfers"
    )
    to_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="to_transfers"
    )
    transfer_date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # əgər from_location boşdursa, soyuducunun cari yerini götür
            if not self.from_location and self.fridge_id:
                self.from_location = self.fridge.current_location

            super().save(*args, **kwargs)

            # Transfer saxlanandan sonra soyuducunun cari yerini yenilə
            if self.to_location and self.fridge_id:
                Fridge.objects.filter(id=self.fridge_id).update(current_location=self.to_location)

    def __str__(self):
        return f"{self.fridge.barcode} → {self.to_location}"