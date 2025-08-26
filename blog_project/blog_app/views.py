from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from .models import Blog, Category, Comment, Notice, ContactMessage

def home(request):
    main_post = Blog.objects.filter(Main_post=True).order_by('-id')[:1]


    notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:5]

    categories = Category.objects.all()


    # Recent
    recent = Blog.objects.filter(section='Recent').order_by('-id')[:5]
    recent_first = recent.first()
    recent_rest = recent[1:]

    # Popular
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:5]

    # Trending
    trending = Blog.objects.filter(section='Trending').order_by('-id')[:5]
    trending_first = trending.first()
    trending_rest = trending[1:]

    categories = Category.objects.all()

    context = {
        'main_post': main_post,

        'categories': categories,

        'notices': notices,

        # Recent split
        'recent_first': recent_first,
        'recent_rest': recent_rest,

        # Popular (not split yet)
        'popular': popular,

        # Trending split
        'trending_first': trending_first,
        'trending_rest': trending_rest,

        'categories': categories,
    }
    return render(request, "home.html", context)


def blog_detail(request, pk):
    categories = Category.objects.all()
    post = get_object_or_404(Blog, pk=pk)
    post.views += 1
    post.save()
    comments = Comment.objects.filter(blog_id=post.id).order_by('-date')
    return render(request, "blog_detail.html", {'post': post, 'categories': categories, 'comments': comments})

def category(request, pk):
    current_category = get_object_or_404(Category, pk=pk)
    blog_cat = Blog.objects.filter(category=current_category)
    categories = Category.objects.all()
    return render(request, 'category.html', {
        'current_category': current_category,
        'blog_cat': blog_cat,
        'categories': categories,
    })


def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Blog, pk=pk)
        parent_id = request.POST.get('parent_id')
        parent_comment = get_object_or_404(Comment, id=parent_id) if parent_id else None
        Comment.objects.create(
            post=post,
            name=request.POST.get('InputName'),
            email=request.POST.get('InputEmail'),
            website=request.POST.get('InputWeb'),
            comment=request.POST.get('InputComment'),
            parent=parent_comment
        )
    return redirect("blog_detail", pk=pk)


def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})




def contact(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if not message_text:
            messages.error(request, "Please enter a message!")
        else:
            # Save to database
            ContactMessage.objects.create(name=name, email=email, message=message_text)

            # Optional: send email
            send_mail(
                subject=f"New message from {name}",
                message=f"Sender: {email}\n\nMessage:\n{message_text}",
                from_email='koni98882@gmail.com',
                recipient_list=['koni98882@gmail.com'],
            )

            messages.success(request, "Your message has been sent!")

    return render(request, "contact.html", {'categories': categories})


def search(request):
    query = request.GET.get('q')
    results = Blog.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='1'
    ) if query else Blog.objects.none()
    categories = Category.objects.all()
    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'categories': categories,
    })
