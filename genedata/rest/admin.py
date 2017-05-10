#!/usr/bin/env python
#-*-coding:utf-8-*-

from django.contrib import admin

# Register your models here.
from .models import Genome, Track, Genecode, Contact

admin.site.register(Genome)
admin.site.register(Track)
admin.site.register(Genecode)
admin.site.register(Contact)
