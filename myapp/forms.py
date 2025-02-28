from django import forms
from .models import *
from .models import ImageUpload


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['heading', 'image','descrption','product1','product2','product3','product4','product5','product6','product7','product8','product9','product10']

class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ['productName', 'image', 'productPrice', 'quantity', 'Discount', 'Category']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'image']