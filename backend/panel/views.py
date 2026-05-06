"""
Panel App — Views
Superuser-only admin panel for managing VASTIK products.
"""
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q

from store.models import Product, ProductImage
from .forms import ProductForm


# ── Decorator ─────────────────────────────────────────────────────────────────

def superuser_required(view_func):
    """Redirect to panel login if user is not an authenticated superuser."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('panel-login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Auth Views ────────────────────────────────────────────────────────────────

def panel_login(request):
    """Login page for superusers."""
    # Already logged in superuser → go to dashboard
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('panel-dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            next_url = request.GET.get('next', 'panel-dashboard')
            return redirect(next_url)
        else:
            error = 'Invalid credentials or insufficient privileges.'

    return render(request, 'panel/login.html', {'error': error})


def panel_logout(request):
    """Log out and redirect to login page."""
    logout(request)
    return redirect('panel-login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@superuser_required
def panel_dashboard(request):
    """Admin dashboard with overview stats."""
    total = Product.objects.count()
    featured = Product.objects.filter(is_featured=True).count()
    categories = Product.objects.values('category').annotate(
        count=Count('id')
    ).order_by('category')

    # Build a dict for easy template access
    cat_counts = {c['category']: c['count'] for c in categories}

    context = {
        'total_products': total,
        'featured_count': featured,
        'mesh_count': cat_counts.get('Mesh', 0),
        'script_count': cat_counts.get('Script', 0),
        'texture_count': cat_counts.get('Texture', 0),
    }
    return render(request, 'panel/dashboard.html', context)


# ── Product List ──────────────────────────────────────────────────────────────

@superuser_required
def panel_products(request):
    """List all products with search and category filter."""
    queryset = Product.objects.prefetch_related('images').all()

    search = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(serial_number__icontains=search) |
            Q(description__icontains=search)
        )
    if category:
        queryset = queryset.filter(category__iexact=category)

    context = {
        'products': queryset,
        'search': search,
        'category': category,
    }
    return render(request, 'panel/products.html', context)


# ── Product Add ───────────────────────────────────────────────────────────────

@superuser_required
def panel_product_add(request):
    """Create a new product with image URLs."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            _save_image_urls(request, product)
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('panel-products')
    else:
        form = ProductForm()

    return render(request, 'panel/product_form.html', {
        'form': form,
        'editing': False,
        'page_title': 'Add Product',
    })


# ── Product Edit ──────────────────────────────────────────────────────────────

@superuser_required
def panel_product_edit(request, pk):
    """Edit an existing product and its image URLs."""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Remove old images and re-create from submitted URLs
            product.images.all().delete()
            _save_image_urls(request, product)
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('panel-products')
    else:
        form = ProductForm(instance=product)

    existing_images = list(product.images.values('image_url', 'order'))

    return render(request, 'panel/product_form.html', {
        'form': form,
        'editing': True,
        'product': product,
        'existing_images': existing_images,
        'page_title': f'Edit — {product.name}',
    })


# ── Product Delete ────────────────────────────────────────────────────────────

@superuser_required
def panel_product_delete(request, pk):
    """Confirm and delete a product."""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('panel-products')

    return render(request, 'panel/product_delete.html', {'product': product})


# ── Helpers ───────────────────────────────────────────────────────────────────

def _save_image_urls(request, product):
    """Parse dynamic image URL fields from POST data and create ProductImage records."""
    urls = request.POST.getlist('image_urls')
    orders = request.POST.getlist('image_orders')

    for i, url in enumerate(urls):
        url = url.strip()
        if not url:
            continue
        order = 0
        if i < len(orders):
            try:
                order = int(orders[i])
            except (ValueError, TypeError):
                order = i
        ProductImage.objects.create(
            product=product,
            image_url=url,
            order=order,
        )
