from django import forms
from datetime import date


class NewsForm(forms.Form):
    """Форма для добавления новости"""
    title = forms.CharField(
        max_length=100,
        label="Заголовок",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок новости'
        })
    )
    summary = forms.CharField(
        max_length=200,
        label="Краткое описание",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Краткое описание новости'
        })
    )
    content = forms.CharField(
        label="Текст новости",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Полный текст новости'
        })
    )
    pub_date = forms.DateField(
        label="Дата публикации",
        initial=date.today,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise forms.ValidationError('Заголовок должен содержать минимум 3 символа')
        return title.strip()

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary.strip()) < 10:
            raise forms.ValidationError('Краткое описание должно содержать минимум 10 символов')
        return summary.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 20:
            raise forms.ValidationError('Текст новости должен содержать минимум 20 символов')
        return content.strip()