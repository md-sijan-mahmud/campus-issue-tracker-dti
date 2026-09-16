from django.db import models

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="সমস্যার শিরোনাম (যেমন: পিসি নষ্ট)")
    description = models.TextField(verbose_name="বিস্তারিত বিবরণ")
    image = models.ImageField(upload_to='complaints/', blank=True, null=True, verbose_name="সমস্যার ছবি")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title