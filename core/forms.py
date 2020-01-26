from django import forms

class imgForm(forms.Form):
    imageUrl = forms.URLField(label='Загрузите изображение',
                              widget=forms.URLInput(attrs={'class': 'form-control',
                              'placeholder': 'Вставьте ссылку на изображение'}),required=False)
    imageFile = forms.ImageField(label='Или выберите картинку',required=False)
