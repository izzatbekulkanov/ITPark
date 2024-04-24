from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=100, help_text=_("Xizmat nomi"))
    icon = models.ForeignKey('Icons', on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Icon"))
    code = models.CharField(max_length=100, help_text=_("Xizmat kodi"))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("O'zgartirilgan vaqti"))

    def __str__(self):
        return self.name if self.name else ""

class Icons(models.Model):
    name = models.CharField(max_length=100, help_text=_("Icon nomi"))
    icon = models.CharField(max_length=100, help_text=_("Icon"))  # Yangi ustun: ikon

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("O'zgartirilgan vaqti"))

    def __str__(self):
        return self.name if self.name else ""

class Queue(models.Model):
    DONE_CHOICES = [
        ('accept', _('Bajarildi')),
        ('reject', _('Bajarilmadi')),
        ('delay', _('Kechiktirildi')),
        ('waiting', _('Kutilmoqda')),
    ]
    first_name = models.CharField(max_length=100, help_text=_("Ism"))
    last_name = models.CharField(max_length=100, help_text=_("Familiya"))
    services = models.ForeignKey(Services, on_delete=models.SET_NULL, verbose_name=_("Xizmat turi"), null=True, blank=True, help_text=_("Xizmat turi"))
    order_number = models.PositiveIntegerField(help_text=_("Buyurtma raqami"), editable=False)
    done = models.CharField(max_length=20, choices=DONE_CHOICES, help_text=_("Bajarilganlik holati"))
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text=_("Foydalanuvchi"))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("O'zgartirilgan vaqti"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Mijozlar uchun ishlatilgan tartib raqamlarini topish
            latest_order_number = Queue.objects.filter(services=self.services).order_by('-order_number').first()
            if latest_order_number:
                self.order_number = latest_order_number.order_number + 1
            else:
                # Agar uchun mijozlar uchun ishlatilgan tartib raqamlar mavjud emas bo'lsa, boshlang'ich tartib raqamini 1 ga o'rnating
                self.order_number = 1
        super().save(*args, **kwargs)
