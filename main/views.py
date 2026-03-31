from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    BlogCommentForm,
    BlogPostForm,
    ForumPostForm,
    ForumTopicForm,
    OrderPaymentForm,
    ProductForm,
    RegisterForm,
)
from .models import BlogPost, ForumCategory, ForumTopic, Order, Product, Profile

PAYMENT_STUB = {
    'recipient': 'ООО «SpeechHub»',
    'bank': 'Тест Банк',
    'account': '40702810000000000000',
    'card': '2200 0000 0000 0000',
    'phone': '+7 900 000-00-00',
}


def home(request):
    context = {
        'posts': BlogPost.objects.filter(status='published')[:5],
        'products': Product.objects.filter(status='approved')[:6],
        'topics': ForumTopic.objects.select_related('category')[:5],
    }
    return render(request, 'main/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, display_name=user.username)
            login(request, user)
            messages.success(request, 'Регистрация выполнена.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def blog_list(request):
    posts = BlogPost.objects.filter(status='published')
    return render(request, 'main/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    if request.method == 'POST' and request.user.is_authenticated:
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = BlogCommentForm()
    return render(request, 'main/blog_detail.html', {'post': post, 'form': form})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == 'published':
                post.published_at = timezone.now()
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = BlogPostForm()
    return render(request, 'main/form_page.html', {'form': form, 'title': 'Новая статья'})


def product_list(request):
    products = Product.objects.filter(status='approved')
    return render(request, 'main/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    return render(request, 'main/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.status = 'pending'
            product.save()
            messages.info(request, 'Товар отправлен на модерацию.')
            return redirect('my_dashboard')
    else:
        form = ProductForm()
    return render(request, 'main/form_page.html', {'form': form, 'title': 'Добавить материал'})


@login_required
def create_order(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    order = Order.objects.create(user=request.user, product=product, total_amount=product.price)
    return redirect('order_pay', order_id=order.id)


@login_required
def order_pay(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = OrderPaymentForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.status = 'waiting_confirmation'
            payment.save()
            messages.success(request, 'Чек отправлен. Ожидайте подтверждения администратора.')
            return redirect('my_dashboard')
    else:
        form = OrderPaymentForm(instance=order)
    return render(request, 'main/order_pay.html', {'order': order, 'form': form, 'stub': PAYMENT_STUB})


def forum_list(request):
    categories = ForumCategory.objects.prefetch_related('topics')
    return render(request, 'main/forum_list.html', {'categories': categories})


def forum_topic_detail(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ForumPostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect(topic.get_absolute_url())
    else:
        form = ForumPostForm()
    return render(request, 'main/forum_topic_detail.html', {'topic': topic, 'form': form})


@login_required
def forum_topic_create(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect(topic.get_absolute_url())
    else:
        form = ForumTopicForm()
    return render(request, 'main/form_page.html', {'form': form, 'title': 'Создать тему'})


@login_required
def my_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html', {'products': products, 'orders': orders})


def bootstrap_demo(request):
    if not request.user.is_superuser:
        return redirect('home')
    category, _ = ForumCategory.objects.get_or_create(name='Общие вопросы', description='Разговоры о логопедии')
    User.objects.filter(username='demo_author').exists() or User.objects.create_user('demo_author', password='demo12345')
    messages.success(request, f'Форум-категория готова: {category.name}')
    return redirect('home')
