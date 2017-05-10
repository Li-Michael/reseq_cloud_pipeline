#!/urs/bin/env python
#-*-coding:utf-8-*-

from django import forms

class GeneForm(forms.Form):
    gene = forms.CharField(label="Gene", max_length=18)

