from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'id': 'article-title',
                   'class': 'form-control',
                   'placeholder': 'category1/category2/.../タイトル #tag1, tag2'}
        )
    )

    body = forms.CharField(
        label='article-body',
        widget=forms.Textarea(
            attrs={'id': 'article-code', }
        )
    )

    templates = forms.ChoiceField(
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', }
        )
    )

    class Meta:
        model = Article
        fields = ['body', ]


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'コメント'}
        )
    )

    class Meta:
        model = Comment
        fields = ['body', ]
