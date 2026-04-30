/* ============================================================
   VASTIK — Main JavaScript  (rewritten)
   Dark + Gold Indian cultural theme
   Multi-page: Home, Store, Gallery, Product Detail
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initScrollAnimations();
    initHeroParticles();
    initPageHeaderParticles();
    initStatsCounter();
    updateWishlistBadge();

    // Page-specific inits
    if (document.getElementById('productsGrid')) { initStorePage(); }
    if (document.getElementById('galleryGrid')) { initGalleryPage(); }
    if (document.getElementById('featuredCarousel')) { loadFeaturedProducts(); }
    if (document.getElementById('testimonialsCarousel')) { loadTestimonials(); }
    if (document.getElementById('slName')) { initContactForm(); }
    if (window.PRODUCT_ID) { loadProductDetail(); }

    initCategoryFromURL();
});

/* ============================================================
   API HELPER
   ============================================================ */
const API_BASE = '/api/v1';

async function apiFetch(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json', ...options.headers },
            ...options,
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        return { success: false, error: 'Network error. Please try again.' };
    }
}

/* ============================================================
   1. TOAST NOTIFICATION SYSTEM
   ============================================================ */
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = { success: 'check-circle', error: 'exclamation-circle', info: 'info-circle' };
    const icon = icons[type] || 'info-circle';

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${icon}"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(toast);

    // Trigger slide-in
    requestAnimationFrame(() => {
        requestAnimationFrame(() => toast.classList.add('visible'));
    });

    // Auto-remove
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 350);
    }, duration);
}

/* ============================================================
   2. NAVBAR
   ============================================================ */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const navOverlay = document.getElementById('navOverlay');
    const backToTop = document.getElementById('backToTop');

    if (!navbar || !hamburger || !navLinks || !navOverlay) return;

    const closeMenu = () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
        navOverlay.classList.remove('active');
        document.body.style.overflow = '';
    };

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
        if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 400);
    });

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('open');
        navOverlay.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });

    navOverlay.addEventListener('click', closeMenu);

    // Back-to-top
    if (backToTop) {
        backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // Smooth-scroll hash links
    document.querySelectorAll('.nav-links a[href*="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            const hash = href.substring(href.indexOf('#') + 1);
            const target = document.getElementById(hash);
            if (target) {
                e.preventDefault();
                closeMenu();
                const y = target.getBoundingClientRect().top + window.scrollY - 80;
                window.scrollTo({ top: y, behavior: 'smooth' });
            }
        });
    });

    document.querySelectorAll('.nav-links a:not([href*="#"])').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Active section tracking (home page only)
    if (window.location.pathname === '/') {
        const sections = document.querySelectorAll('section[id]');
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(sec => {
                if (window.scrollY >= sec.offsetTop - 100) current = sec.getAttribute('id');
            });
            document.querySelectorAll('.nav-links a').forEach(link => {
                const href = link.getAttribute('href');
                if (href.includes('#')) {
                    link.classList.toggle('active', href.endsWith(`#${current}`));
                }
            });
        });
    }
}

/* ============================================================
   3. SCROLL ANIMATIONS
   ============================================================ */
function initScrollAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => entry.target.classList.add('visible'), index * 100);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );
    document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => observer.observe(el));
}

/* ============================================================
   4. PARTICLES
   ============================================================ */
function createParticles(container, count) {
    for (let i = 0; i < count; i++) {
        const p = document.createElement('div');
        p.classList.add('particle');
        p.style.left = `${Math.random() * 100}%`;
        p.style.animationDelay = `${Math.random() * 6}s`;
        p.style.animationDuration = `${4 + Math.random() * 4}s`;
        const size = `${2 + Math.random() * 4}px`;
        p.style.width = size;
        p.style.height = size;
        container.appendChild(p);
    }
}

function initHeroParticles() {
    const c = document.getElementById('heroParticles');
    if (c) createParticles(c, 30);
}

function initPageHeaderParticles() {
    const c = document.getElementById('pageHeaderParticles');
    if (c) createParticles(c, 15);
}

/* ============================================================
   5. ANIMATED STATS COUNTER
   ============================================================ */
function initStatsCounter() {
    const statsGrid = document.querySelector('.stats-grid');
    if (!statsGrid) return;

    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    obs.unobserve(entry.target);
                    entry.target.querySelectorAll('.stat-number[data-target]').forEach(el => {
                        animateCount(el);
                    });
                }
            });
        },
        { threshold: 0.3 }
    );
    observer.observe(statsGrid);
}

function animateCount(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const duration = 2000;
    const start = performance.now();

    function step(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const value = Math.round(eased * target);
        el.textContent = value.toLocaleString() + (target > 10 ? '+' : '');
        if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

/* ============================================================
   6. WISHLIST (localStorage)
   ============================================================ */
const WISHLIST_KEY = 'vastik_wishlist';

function getWishlist() {
    try { return JSON.parse(localStorage.getItem(WISHLIST_KEY)) || []; }
    catch { return []; }
}

function saveWishlist(list) {
    localStorage.setItem(WISHLIST_KEY, JSON.stringify(list));
}

function updateWishlistBadge() {
    const list = getWishlist();
    const badge = document.getElementById('wishlistBadge');
    const navWL = document.getElementById('navWishlist');

    if (badge) badge.textContent = list.length;
    if (navWL) navWL.style.display = list.length > 0 ? '' : 'none';
}

function toggleWishlist(productId, event) {
    if (event) event.stopPropagation();
    const id = String(productId);
    let list = getWishlist();
    const idx = list.indexOf(id);
    const btn = document.querySelector(`.wishlist-btn[data-product-id="${id}"]`);

    if (idx === -1) {
        list.push(id);
        showToast('Added to wishlist ♥', 'success');
        if (btn) { btn.classList.add('active'); btn.querySelector('i').className = 'fas fa-heart'; }
    } else {
        list.splice(idx, 1);
        showToast('Removed from wishlist', 'info');
        if (btn) { btn.classList.remove('active'); btn.querySelector('i').className = 'far fa-heart'; }
    }

    saveWishlist(list);
    updateWishlistBadge();
}

function toggleWishlistDetail() {
    const btn = document.getElementById('wishlistDetailBtn');
    if (!btn) return;
    const id = String(window.PRODUCT_ID);
    let list = getWishlist();
    const idx = list.indexOf(id);

    if (idx === -1) {
        list.push(id);
        btn.classList.add('active');
        btn.querySelector('i').className = 'fas fa-heart';
        showToast('Added to wishlist ♥', 'success');
    } else {
        list.splice(idx, 1);
        btn.classList.remove('active');
        btn.querySelector('i').className = 'far fa-heart';
        showToast('Removed from wishlist', 'info');
    }
    saveWishlist(list);
    updateWishlistBadge();
}

/* ============================================================
   7. PRODUCT CARD BUILDER (shared)
   ============================================================ */
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in';

    const images = product.images || [];
    const slideshowHTML = images.length > 0
        ? images.map((img, i) => `<img src="${img.image}" alt="${product.name}" class="${i === 0 ? 'active' : ''}" loading="lazy" />`).join('')
        : `<img src="/static/images/mandala.svg" alt="No image" class="active" style="padding:40px;object-fit:contain;background:var(--bg-tertiary);" />`;

    const dotsHTML = images.length > 1
        ? `<div class="slideshow-dots">${images.map((_, i) => `<div class="slideshow-dot ${i === 0 ? 'active' : ''}" data-index="${i}"></div>`).join('')}</div>`
        : '';

    // Badges
    const wishlist = getWishlist();
    const isInWL = wishlist.includes(String(product.id));
    const isNew = product.created_at && (Date.now() - new Date(product.created_at).getTime()) < 7 * 24 * 3600 * 1000;

    const featuredBadge = product.is_featured
        ? `<span class="product-badge badge-featured">★ Featured</span>` : '';
    const newBadge = isNew
        ? `<span class="product-badge badge-new">New</span>` : '';

    const marketplaceBtn = product.marketplace_url
        ? `<a href="${product.marketplace_url}" target="_blank" rel="noopener" class="btn btn-primary">Marketplace</a>` : '';
    const inworldBtn = product.inworld_slurl
        ? `<a href="${product.inworld_slurl}" target="_blank" rel="noopener" class="btn btn-outline">Visit Inworld</a>` : '';

    card.innerHTML = `
        <div class="product-slideshow" data-slideshow>
            ${slideshowHTML}
            ${dotsHTML}
            <div class="product-badges">${featuredBadge}${newBadge}</div>
            <button class="wishlist-btn ${isInWL ? 'active' : ''}"
                    data-product-id="${product.id}"
                    onclick="toggleWishlist('${product.id}', event)"
                    aria-label="Toggle wishlist">
                <i class="${isInWL ? 'fas' : 'far'} fa-heart"></i>
            </button>
        </div>
        <div class="product-info">
            <div class="product-header">
                <span class="product-serial">${product.serial_number || ''}</span>
                <span class="product-category-tag">${product.category || ''}</span>
            </div>
            <a href="/store/product/${product.id}/" class="product-name-link">
                <h3 class="product-name">${product.name}</h3>
            </a>
            <p class="product-description" onclick="this.classList.toggle('expanded')">${product.description || ''}</p>
            <div class="product-price">L$${Number(product.price).toLocaleString()} <span>Linden Dollars</span></div>
            <div class="product-actions">${marketplaceBtn}${inworldBtn}</div>
        </div>
    `;

    requestAnimationFrame(() => requestAnimationFrame(() => card.classList.add('visible')));
    return card;
}

/* ============================================================
   8. SLIDESHOW LOGIC
   ============================================================ */
function initSlideshows() {
    document.querySelectorAll('[data-slideshow]').forEach(slideshow => {
        const images = slideshow.querySelectorAll('img');
        const dots = slideshow.querySelectorAll('.slideshow-dot');
        if (images.length <= 1) return;

        let current = 0;
        let interval;

        function goTo(index) {
            images[current].classList.remove('active');
            dots[current]?.classList.remove('active');
            current = index;
            images[current].classList.add('active');
            dots[current]?.classList.add('active');
        }

        function startAutoplay() { interval = setInterval(() => goTo((current + 1) % images.length), 4000); }
        function stopAutoplay() { clearInterval(interval); }

        startAutoplay();
        slideshow.addEventListener('mouseenter', stopAutoplay);
        slideshow.addEventListener('mouseleave', startAutoplay);
        dots.forEach(dot => dot.addEventListener('click', () => {
            stopAutoplay(); goTo(parseInt(dot.dataset.index)); startAutoplay();
        }));
    });
}

/* ============================================================
   9. STORE PAGE
   ============================================================ */
let currentCategory = '';
let currentSearch = '';
let currentSort = '';
let searchDebounce = null;

function initStorePage() {
    const searchInput = document.getElementById('storeSearchInput');
    const sortSelect = document.getElementById('storeSortSelect');

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(() => {
                currentSearch = searchInput.value.trim();
                loadProducts();
            }, 400);
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', () => handleSort(sortSelect.value));
    }

    loadProducts();
}

async function loadProducts() {
    const grid = document.getElementById('productsGrid');
    const loading = document.getElementById('productsLoading');
    const countEl = document.getElementById('storeProductCount');
    if (!grid) return;

    grid.innerHTML = '';
    if (loading) loading.style.display = 'grid';

    const params = new URLSearchParams();
    if (currentCategory) params.set('category', currentCategory);
    if (currentSearch) params.set('search', currentSearch);
    if (currentSort) params.set('ordering', currentSort);

    const qs = params.toString();
    const result = await apiFetch(`/products/${qs ? '?' + qs : ''}`);

    if (loading) loading.style.display = 'none';

    if (result.success && result.data) {
        const products = result.data.results || result.data;

        // Update count
        if (countEl) {
            const label = currentCategory ? ` ${currentCategory}` : '';
            countEl.textContent = `Showing ${products.length}${label} product${products.length !== 1 ? 's' : ''}`;
        }

        if (products.length === 0) {
            grid.innerHTML = '<div class="no-products">No products found.</div>';
            return;
        }

        products.forEach(p => grid.appendChild(createProductCard(p)));
        initSlideshows();
        initScrollAnimations();
    } else {
        grid.innerHTML = '<div class="no-products">Failed to load products. Please try again.</div>';
        showToast('Could not load products.', 'error');
    }
}

function filterCategory(category, btn) {
    currentCategory = category;
    document.querySelectorAll('.category-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    loadProducts();
}

function handleSort(value) {
    currentSort = value;
    loadProducts();
}

function initCategoryFromURL() {
    if (!document.getElementById('productsGrid')) return;
    const params = new URLSearchParams(window.location.search);
    const category = params.get('category');
    if (category) {
        currentCategory = category;
        document.querySelectorAll('.category-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.category === category);
        });
        loadProducts();
    }
}

/* ============================================================
   10. FEATURED PRODUCTS CAROUSEL (home page)
   ============================================================ */
async function loadFeaturedProducts() {
    const carousel = document.getElementById('featuredCarousel');
    if (!carousel) return;

    const result = await apiFetch('/products/featured/');
    if (!result.success || !result.data) return;

    const products = result.data.results || result.data;
    carousel.innerHTML = '';

    products.forEach(p => {
        const img = (p.images && p.images[0]) ? p.images[0].image : '/static/images/mandala.svg';
        const card = document.createElement('div');
        card.className = 'featured-card';
        card.innerHTML = `
            <a href="/store/product/${p.id}/" class="featured-card-link">
                <div class="featured-card-img">
                    <img src="${img}" alt="${p.name}" loading="lazy" />
                </div>
                <div class="featured-card-info">
                    <h4>${p.name}</h4>
                    <span class="featured-price">L$${Number(p.price).toLocaleString()}</span>
                    <span class="featured-view">View →</span>
                </div>
            </a>
        `;
        carousel.appendChild(card);
    });
}

function scrollFeaturedCarousel(direction) {
    const carousel = document.getElementById('featuredCarousel');
    if (!carousel) return;
    const card = carousel.querySelector('.featured-card');
    const width = card ? card.offsetWidth + 16 : 260;
    carousel.scrollBy({ left: direction * width, behavior: 'smooth' });
}

/* ============================================================
   11. TESTIMONIALS CAROUSEL (home page)
   ============================================================ */
let testimonialAutoScroll = null;

async function loadTestimonials() {
    const carousel = document.getElementById('testimonialsCarousel');
    if (!carousel) return;

    const result = await apiFetch('/testimonials/');
    if (!result.success || !result.data) return;

    const testimonials = result.data.results || result.data;
    carousel.innerHTML = '';

    testimonials.forEach(t => {
        const stars = buildStars(t.rating || 5);
        const card = document.createElement('div');
        card.className = 'testimonial-card';
        card.innerHTML = `
            <div class="testimonial-quote">
                <i class="fas fa-quote-left"></i>
                <p>${t.message || t.quote || ''}</p>
            </div>
            <div class="testimonial-rating">${stars}</div>
            <div class="testimonial-author">— ${t.sl_name || t.author || 'Anonymous'}</div>
        `;
        carousel.appendChild(card);
    });

    // Auto-scroll every 5s
    clearInterval(testimonialAutoScroll);
    testimonialAutoScroll = setInterval(() => scrollTestimonialCarousel(1), 5000);
}

function buildStars(rating) {
    let html = '';
    for (let i = 1; i <= 5; i++) html += i <= rating ? '★' : '☆';
    return html;
}

function scrollTestimonialCarousel(direction) {
    const carousel = document.getElementById('testimonialsCarousel');
    if (!carousel) return;
    const card = carousel.querySelector('.testimonial-card');
    const width = card ? card.offsetWidth + 20 : 300;
    carousel.scrollBy({ left: direction * width, behavior: 'smooth' });
}

/* ============================================================
   12. GALLERY
   ============================================================ */
let galleryImages = [];
let lightboxIndex = 0;
let currentGalleryCategory = '';

function initGalleryPage() {
    loadGallery();
}

function filterGalleryCategory(category, btn) {
    currentGalleryCategory = category;
    document.querySelectorAll('#galleryCategoryTabs .category-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    loadGallery(category);
}

async function loadGallery(category = currentGalleryCategory) {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return;

    grid.innerHTML = '';

    const qs = category ? `?category=${encodeURIComponent(category)}` : '';
    const result = await apiFetch(`/gallery/${qs}`);

    if (result.success && result.data) {
        const images = result.data.results || result.data;
        galleryImages = images;

        if (images.length === 0) {
            grid.innerHTML = '<p style="grid-column:1/-1;text-align:center;padding:40px;">No gallery images yet.</p>';
            return;
        }

        images.forEach((img, index) => {
            const item = document.createElement('div');
            item.className = 'gallery-item fade-in';
            item.innerHTML = `
                <img src="${img.image}" alt="${img.title}" loading="lazy" />
                <div class="gallery-item-overlay"><h4>${img.title}</h4></div>
            `;
            item.addEventListener('click', () => openLightbox(index));
            grid.appendChild(item);
        });

        initScrollAnimations();
    }
}

/* ============================================================
   13. LIGHTBOX
   ============================================================ */
let touchStartX = 0;

function openLightbox(index) {
    lightboxIndex = index;
    updateLightbox();
    const lb = document.getElementById('lightbox');
    if (lb) { lb.classList.add('active'); document.body.style.overflow = 'hidden'; }

    // Touch/swipe support
    if (lb && !lb._swipeInit) {
        lb._swipeInit = true;
        lb.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
        lb.addEventListener('touchend', e => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) navigateLightbox(diff > 0 ? 1 : -1);
        });
    }
}

function updateLightbox() {
    const img = document.getElementById('lightboxImage');
    const title = document.getElementById('lightboxTitle');
    const desc = document.getElementById('lightboxDescription');
    const counter = document.getElementById('lightboxCounter');
    const current = galleryImages[lightboxIndex];
    if (!current) return;

    if (img) img.src = current.image;
    if (title) title.textContent = current.title || '';
    if (desc) { desc.textContent = current.description || ''; desc.style.display = current.description ? '' : 'none'; }
    if (counter) counter.textContent = `Image ${lightboxIndex + 1} of ${galleryImages.length}`;
}

function closeLightbox() {
    const lb = document.getElementById('lightbox');
    if (lb) { lb.classList.remove('active'); document.body.style.overflow = ''; }
}

function navigateLightbox(direction) {
    lightboxIndex = (lightboxIndex + direction + galleryImages.length) % galleryImages.length;
    updateLightbox();
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    const lb = document.getElementById('lightbox');
    if (!lb || !lb.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
});

/* ============================================================
   14. PRODUCT DETAIL PAGE
   ============================================================ */
async function loadProductDetail() {
    const id = window.PRODUCT_ID;
    if (!id) return;

    const loadingEl = document.getElementById('productDetailLoading');
    const layoutEl = document.getElementById('productDetailLayout');
    if (loadingEl) loadingEl.style.display = 'block';
    if (layoutEl) layoutEl.style.display = 'none';

    const result = await apiFetch(`/products/${id}/`);
    if (loadingEl) loadingEl.style.display = 'none';

    if (!result.success || !result.data) {
        showToast('Failed to load product details.', 'error');
        return;
    }

    const p = result.data;

    // Breadcrumb
    const breadcrumb = document.getElementById('breadcrumbProductName');
    if (breadcrumb) breadcrumb.textContent = p.name;

    // Name / price / description
    setText('productName', p.name);
    setText('productPrice', `L$${Number(p.price).toLocaleString()}`);
    setText('productDescription', p.description);
    setText('productSerial', p.serial_number || '');
    setText('productCategory', p.category || '');

    // Badges
    const badgesEl = document.getElementById('productBadges');
    if (badgesEl) {
        const isNew = p.created_at && (Date.now() - new Date(p.created_at).getTime()) < 7 * 24 * 3600 * 1000;
        badgesEl.innerHTML =
            (p.is_featured ? `<span class="product-badge badge-featured">★ Featured</span>` : '') +
            (isNew ? `<span class="product-badge badge-new">New</span>` : '');
    }

    // Main image + thumbnails
    const mainImg = document.getElementById('mainProductImg');
    const thumbsEl = document.getElementById('productThumbnails');
    const images = p.images || [];

    if (mainImg && images.length > 0) {
        mainImg.src = images[0].image;
        mainImg.alt = p.name;
    }

    if (thumbsEl && images.length > 1) {
        thumbsEl.innerHTML = '';
        images.forEach((img, i) => {
            const t = document.createElement('div');
            t.className = `product-thumb ${i === 0 ? 'active' : ''}`;
            t.innerHTML = `<img src="${img.image}" alt="${p.name}" loading="lazy" />`;
            t.addEventListener('click', () => {
                if (mainImg) mainImg.src = img.image;
                thumbsEl.querySelectorAll('.product-thumb').forEach(el => el.classList.remove('active'));
                t.classList.add('active');
            });
            thumbsEl.appendChild(t);
        });
    }

    // Marketplace / inworld buttons
    const actionsEl = document.getElementById('productActions');
    if (actionsEl) {
        actionsEl.innerHTML =
            (p.marketplace_url ? `<a href="${p.marketplace_url}" target="_blank" rel="noopener" class="btn btn-primary"><i class="fas fa-shopping-cart"></i> Buy on Marketplace</a>` : '') +
            (p.inworld_slurl ? `<a href="${p.inworld_slurl}" target="_blank" rel="noopener" class="btn btn-outline"><i class="fas fa-map-marker-alt"></i> Visit Inworld</a>` : '') +
            `<button class="btn btn-ghost" onclick="copyProductLink()"><i class="fas fa-link"></i> Copy Link</button>`;
    }

    // Wishlist button
    const wlBtn = document.getElementById('wishlistDetailBtn');
    if (wlBtn) {
        const inList = getWishlist().includes(String(id));
        wlBtn.classList.toggle('active', inList);
        const icon = wlBtn.querySelector('i');
        if (icon) icon.className = inList ? 'fas fa-heart' : 'far fa-heart';
    }

    if (layoutEl) layoutEl.style.display = '';

    // Related products
    if (p.category) loadRelatedProducts(p.category, id);
}

async function loadRelatedProducts(category, excludeId) {
    const section = document.getElementById('relatedProducts');
    const grid = document.getElementById('relatedProductsGrid');
    if (!section || !grid) return;

    const result = await apiFetch(`/products/?category=${encodeURIComponent(category)}`);
    if (!result.success || !result.data) return;

    const all = result.data.results || result.data;
    const related = all.filter(p => String(p.id) !== String(excludeId)).slice(0, 3);

    if (related.length === 0) return;

    section.style.display = '';
    grid.innerHTML = '';
    related.forEach(p => grid.appendChild(createProductCard(p)));
    initSlideshows();
}

function copyProductLink() {
    navigator.clipboard.writeText(window.location.href)
        .then(() => showToast('Link copied to clipboard!', 'success'))
        .catch(() => showToast('Could not copy link.', 'error'));
}

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

/* ============================================================
   15. CONTACT FORM (multi-step OTP)
   ============================================================ */
let contactToken = '';
let currentStep = 1;
let resendCountdown = null;

function initContactForm() {
    const otpInputs = document.querySelectorAll('.otp-input-group input');
    if (otpInputs.length === 0) return;

    otpInputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '').slice(0, 1);
            if (e.target.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
}

function goToStep(step) {
    currentStep = step;
    document.querySelectorAll('.step').forEach((s, idx) => {
        s.classList.remove('active', 'completed');
        if (idx + 1 < step) s.classList.add('completed');
        if (idx + 1 === step) s.classList.add('active');
    });
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    const activeStep = document.getElementById(`step${step}`);
    if (activeStep) activeStep.classList.add('active');
}

async function sendOTP() {
    const slName = document.getElementById('slName')?.value.trim();
    const errorEl = document.getElementById('step1Error');
    const btn = document.getElementById('sendOtpBtn');

    if (!slName) { showFormError(errorEl, 'Please enter your Second Life name.'); return; }

    setButtonLoading(btn, true, 'Sending OTP…');
    const result = await apiFetch('/contact/send-otp/', { method: 'POST', body: JSON.stringify({ sl_name: slName }) });
    setButtonLoading(btn, false, '<i class="fas fa-paper-plane"></i> Send OTP');

    if (result.success) {
        hideFormError(errorEl);
        showToast('OTP sent to your Second Life account!', 'success');
        goToStep(2);
        startResendCountdown();
        setTimeout(() => document.querySelector('.otp-input-group input')?.focus(), 300);
    } else {
        const msg = result.error?.sl_name?.[0] || (typeof result.error === 'string' ? result.error : 'Failed to send OTP.');
        showFormError(errorEl, msg);
        showToast(msg, 'error');
    }
}

async function verifyOTP() {
    const slName = document.getElementById('slName')?.value.trim();
    const inputs = document.querySelectorAll('.otp-input-group input');
    const otpCode = Array.from(inputs).map(i => i.value).join('');
    const errorEl = document.getElementById('step2Error');
    const btn = document.getElementById('verifyOtpBtn');

    if (otpCode.length !== 6) { showFormError(errorEl, 'Please enter the complete 6-digit OTP.'); return; }

    setButtonLoading(btn, true, 'Verifying…');
    const result = await apiFetch('/contact/verify-otp/', { method: 'POST', body: JSON.stringify({ sl_name: slName, otp_code: otpCode }) });
    setButtonLoading(btn, false, '<i class="fas fa-check-circle"></i> Verify OTP');

    if (result.success) {
        contactToken = result.data.token;
        hideFormError(errorEl);
        showToast('OTP verified successfully!', 'success');
        goToStep(3);
    } else {
        const msg = typeof result.error === 'string' ? result.error : 'Invalid OTP. Please try again.';
        showFormError(errorEl, msg);
        showToast(msg, 'error');
    }
}

async function submitContact() {
    const topic = document.getElementById('contactTopic')?.value;
    const message = document.getElementById('contactMessage')?.value.trim();
    const errorEl = document.getElementById('step3Error');
    const btn = document.getElementById('submitContactBtn');

    if (!topic) { showFormError(errorEl, 'Please select a topic.'); return; }
    if (message.length < 10) { showFormError(errorEl, 'Message must be at least 10 characters.'); return; }

    setButtonLoading(btn, true, 'Submitting…');
    const result = await apiFetch('/contact/submit/', { method: 'POST', body: JSON.stringify({ token: contactToken, topic, message }) });
    setButtonLoading(btn, false, '<i class="fas fa-envelope"></i> Submit Message');

    if (result.success) {
        hideFormError(errorEl);
        showToast('Your message has been sent!', 'success');
        document.getElementById('contactFormSteps').style.display = 'none';
        document.getElementById('contactSuccess').style.display = 'block';
    } else {
        const msg = typeof result.error === 'string' ? result.error : 'Failed to submit. Please try again.';
        showFormError(errorEl, msg);
        showToast(msg, 'error');
    }
}

async function resendOTP() {
    const slName = document.getElementById('slName')?.value.trim();
    const errorEl = document.getElementById('step2Error');

    if (!slName) { showFormError(errorEl, 'SL name not found. Please go back to step 1.'); return; }

    const result = await apiFetch('/contact/send-otp/', { method: 'POST', body: JSON.stringify({ sl_name: slName }) });

    if (result.success) {
        showToast('OTP resent!', 'success');
        startResendCountdown();
        // Clear OTP inputs
        document.querySelectorAll('.otp-input-group input').forEach(i => i.value = '');
        document.querySelector('.otp-input-group input')?.focus();
    } else {
        showToast('Failed to resend OTP. Please try again.', 'error');
    }
}

function startResendCountdown() {
    const btn = document.getElementById('resendOtpBtn');
    const timer = document.getElementById('resendTimer');
    if (!btn) return;

    let seconds = 60;
    btn.disabled = true;
    clearInterval(resendCountdown);

    function tick() {
        if (timer) timer.textContent = `(${seconds}s)`;
        if (seconds <= 0) {
            btn.disabled = false;
            if (timer) timer.textContent = '';
            clearInterval(resendCountdown);
        } else {
            seconds--;
        }
    }
    tick();
    resendCountdown = setInterval(tick, 1000);
}

// Form helper utilities
function showFormError(el, msg) { if (el) { el.textContent = msg; el.classList.add('show'); } }
function hideFormError(el) { if (el) { el.textContent = ''; el.classList.remove('show'); } }
function setButtonLoading(btn, loading, html) {
    if (!btn) return;
    btn.disabled = loading;
    btn.innerHTML = loading ? `<i class="fas fa-spinner fa-spin"></i> ${html}` : html;
}

/* ============================================================
   GLOBAL SCOPE EXPOSURE
   ============================================================ */
window.filterCategory = filterCategory;
window.handleSort = handleSort;
window.filterGalleryCategory = filterGalleryCategory;
window.closeLightbox = closeLightbox;
window.navigateLightbox = navigateLightbox;
window.sendOTP = sendOTP;
window.verifyOTP = verifyOTP;
window.submitContact = submitContact;
window.goToStep = goToStep;
window.resendOTP = resendOTP;
window.scrollFeaturedCarousel = scrollFeaturedCarousel;
window.scrollTestimonialCarousel = scrollTestimonialCarousel;
window.toggleWishlist = toggleWishlist;
window.toggleWishlistDetail = toggleWishlistDetail;
window.copyProductLink = copyProductLink;