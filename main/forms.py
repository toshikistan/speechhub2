from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BlogComment, BlogPost, ForumPost, ForumTopic, Order, Product


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('category', 'title', 'slug', 'excerpt', 'content', 'status')


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('body',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'slug', 'description', 'price', 'preview', 'file')


class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payer_name', 'payer_note', 'proof')


class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ('category', 'title', 'body')


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('body',)
