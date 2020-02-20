from django.contrib import admin
from orders import models

admin.site.register(models.Particular)
admin.site.register(models.ParticularSpecificationTypePricing)
admin.site.register(models.Specification)
admin.site.register(models.SpecificationType)
admin.site.register(models.Order)
admin.site.register(models.OrderMaterial)
admin.site.register(models.OrderSpecification)
admin.site.register(models.OrderPayment)
