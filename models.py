# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class GogleMapPoint(models.Model):
    
    longitude = models.DecimalField(max_digits=8, decimal_places=4,
                                    verbose_name=u'Долгота', default=0)
    
    latitude  = models.DecimalField(max_digits=8, decimal_places=4,
                                    verbose_name=u'Широта', default=0)      
        
    