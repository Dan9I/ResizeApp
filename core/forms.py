from django import forms

class imgForm(forms.Form):
    imageUrl = forms.URLField(label='Вставьте url', required=False)
    imageFile = forms.ImageField(label='Или выберите картинку',
                               required=False)

    def clean(self):
        imageUrl = self.cleaned_data.get('imageUrl')
        imageFile = self.cleaned_data.get('imageFile')

        if imageUrl and imageFile:
            raise forms.ValidationError('Заполненным может быть только 1 поле')

        if imageUrl == '' and imageFile is None:
            raise forms.ValidationError('Нужно ввести данные хотя бы в 1 поле')
