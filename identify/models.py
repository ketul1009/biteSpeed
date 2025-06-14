from django.db import models

class Contact(models.Model):
    LINK_PRECEDENCE_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
    ]

    phoneNumber = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_contacts')
    linkPrecedence = models.CharField(max_length=10, choices=LINK_PRECEDENCE_CHOICES, default='primary')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'contact'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phoneNumber']),
            models.Index(fields=['linkedId']),
        ]

    def __str__(self):
        return f"Contact {self.id} - {self.email or self.phoneNumber}"


