/* ============================================================
   VASTIK — Main JavaScript
   Handles API calls, slideshows, OTP flow, lightbox, animations
   Multi-page aware (Home, Store, Gallery)
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initScrollAnimations();
    initHeroParticles();
    initPageHeaderParticles();
    loadProducts();
    loadGallery();
    initContactForm();
    initCategoryFromURL();
});

/* ============================================================
   API Helper
   ============================================================ */
const API_BASE = '/api/v1';

async function apiFetch(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
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
   1. NAVBAR (multi-page aware)
   ============================================================ */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const navOverlay = document.getElementById('navOverlay');

    // Sticky navbar on scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Hamburger toggle
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('open');
        navOverlay.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });

    // Close on overlay click
    navOverlay.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
        navOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });

    // Smart nav link handling — smooth scroll on same page, navigate on different pages
    document.querySelectorAll('.nav-links a[href*="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;

            const hash = href.substring(hashIndex + 1);
            const target = document.getElementById(hash);

            if (target) {
                // Target exists on this page — smooth scroll
                e.preventDefault();

                // Close mobile menu
                hamburger.classList.remove('active');
                navLinks.classList.remove('open');
                navOverlay.classList.remove('active');
                document.body.style.overflow = '';

                // Scroll to target
                const offset = 80;
                const y = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: y, behavior: 'smooth' });
            }
            // If target doesn't exist on this page, let browser navigate normally
        });
    });

    // Close mobile menu on non-hash link clicks
    document.querySelectorAll('.nav-links a:not([href*="#"])').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('open');
            navOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Active link tracking via scroll (only on home page)
    const isHomePage = window.location.pathname === '/';
    if (isHomePage) {
        const sections = document.querySelectorAll('section[id]');
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop - 100;
                if (window.scrollY >= sectionTop) {
                    current = section.getAttribute('id');
                }
            });

            document.querySelectorAll('.nav-links a').forEach(link => {
                const href = link.getAttribute('href');
                // Only update hash-based links on home page
                if (href.includes('#')) {
                    link.classList.remove('active');
                    if (href.endsWith(`#${current}`) || (current === 'home' && href === '/')) {
                        link.classList.add('active');
                    }
                }
            });
        });
    }
}

/* ============================================================
   2. SCROLL ANIMATIONS
   ============================================================ */
function initScrollAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    // Stagger the animation
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, index * 100);
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => {
        observer.observe(el);
    });
}

/* ============================================================
   3. HERO PARTICLES
   ============================================================ */
function initHeroParticles() {
    const container = document.getElementById('heroParticles');
    if (!container) return;
    createParticles(container, 30);
}

function initPageHeaderParticles() {
    const container = document.getElementById('pageHeaderParticles');
    if (!container) return;
    createParticles(container, 15);
}

function createParticles(container, count) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 6}s`;
        particle.style.animationDuration = `${4 + Math.random() * 4}s`;
        particle.style.width = `${2 + Math.random() * 4}px`;
        particle.style.height = particle.style.width;
        container.appendChild(particle);
    }
}

/* ============================================================
   4. PRODUCTS / STORE
   ============================================================ */
let allProducts = [];

async function loadProducts(category = '') {
    const grid = document.getElementById('productsGrid');
    const loading = document.getElementById('productsLoading');
    if (!grid) return; // Not on store page

    // Show loading
    grid.innerHTML = '';
    if (loading) loading.style.display = 'block';

    const endpoint = category ? `/products/?category=${category}` : '/products/';
    const result = await apiFetch(endpoint);

    if (loading) loading.style.display = 'none';

    if (result.success && result.data) {
        // Handle paginated and non-paginated responses
        const products = result.data.results || result.data;
        allProducts = products;

        if (products.length === 0) {
            grid.innerHTML = '<div class="no-products">No products found in this category.</div>';
            return;
        }

        products.forEach(product => {
            grid.appendChild(createProductCard(product));
        });

        // Initialize slideshows
        initSlideshows();
    } else {
        grid.innerHTML = '<div class="no-products">Failed to load products. Please try again.</div>';
    }
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in';

    const images = product.images || [];
    const slideshowHTML = images.length > 0
        ? images.map((img, i) => `<img src="${img.image}" alt="${product.name}" class="${i === 0 ? 'active' : ''}" />`).join('')
        : '<img src="/static/images/mandala.svg" alt="No image" class="active" style="padding: 40px; object-fit: contain; background: var(--bg-tertiary);" />';

    const dotsHTML = images.length > 1
        ? `<div class="slideshow-dots">${images.map((_, i) => `<div class="slideshow-dot ${i === 0 ? 'active' : ''}" data-index="${i}"></div>`).join('')}</div>`
        : '';

    const marketplaceBtn = product.marketplace_url
        ? `<a href="${product.marketplace_url}" target="_blank" rel="noopener" class="btn btn-primary">Marketplace</a>`
        : '';

    const inworldBtn = product.inworld_slurl
        ? `<a href="${product.inworld_slurl}" target="_blank" rel="noopener" class="btn btn-outline">Visit Inworld</a>`
        : '';

    card.innerHTML = `
        <div class="product-slideshow" data-slideshow>
            ${slideshowHTML}
            ${dotsHTML}
        </div>
        <div class="product-info">
            <div class="product-header">
                <span class="product-serial">${product.serial_number}</span>
                <span class="product-category-tag">${product.category}</span>
            </div>
            <h3 class="product-name">${product.name}</h3>
            <p class="product-description" onclick="this.classList.toggle('expanded')">${product.description}</p>
            <div class="product-price">L$${Number(product.price).toLocaleString()} <span>Linden Dollars</span></div>
            <div class="product-actions">
                ${marketplaceBtn}
                ${inworldBtn}
            </div>
        </div>
    `;

    // Trigger animation after a tick
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            card.classList.add('visible');
        });
    });

    return card;
}

/* Slideshow Logic */
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

        function next() {
            goTo((current + 1) % images.length);
        }

        // Auto-advance every 4 seconds
        function startAutoplay() {
            interval = setInterval(next, 4000);
        }

        function stopAutoplay() {
            clearInterval(interval);
        }

        startAutoplay();

        // Pause on hover
        slideshow.addEventListener('mouseenter', stopAutoplay);
        slideshow.addEventListener('mouseleave', startAutoplay);

        // Dot clicks
        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                stopAutoplay();
                goTo(parseInt(dot.dataset.index));
                startAutoplay();
            });
        });
    });
}

/* Category Filter */
function filterCategory(category, btn) {
    // Update active tab
    document.querySelectorAll('.category-tab').forEach(tab => tab.classList.remove('active'));
    if (btn) btn.classList.add('active');

    // Reload products
    loadProducts(category);
}

/* Auto-apply category filter from URL query parameter */
function initCategoryFromURL() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return; // Not on store page

    const params = new URLSearchParams(window.location.search);
    const category = params.get('category');

    if (category) {
        // Find and activate the matching tab
        const tabs = document.querySelectorAll('.category-tab');
        tabs.forEach(tab => {
            tab.classList.remove('active');
            if (tab.dataset.category === category) {
                tab.classList.add('active');
            }
        });
        // Load filtered products
        loadProducts(category);
    }
}

// Expose to global scope for onclick handlers
window.filterCategory = filterCategory;

/* ============================================================
   5. GALLERY
   ============================================================ */
let galleryImages = [];
let lightboxIndex = 0;

async function loadGallery() {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return; // Not on gallery page

    const result = await apiFetch('/gallery/');

    if (result.success && result.data) {
        const images = result.data.results || result.data;
        galleryImages = images;

        if (images.length === 0) {
            grid.innerHTML = '<p class="text-center text-muted" style="grid-column: 1/-1; padding: 40px;">No gallery images yet.</p>';
            return;
        }

        images.forEach((img, index) => {
            const item = document.createElement('div');
            item.className = 'gallery-item fade-in';
            item.innerHTML = `
                <img src="${img.image}" alt="${img.title}" loading="lazy" />
                <div class="gallery-item-overlay">
                    <h4>${img.title}</h4>
                </div>
            `;
            item.addEventListener('click', () => openLightbox(index));

            grid.appendChild(item);
        });

        // Re-observe for scroll animations
        initScrollAnimations();
    }
}

/* Lightbox */
function openLightbox(index) {
    lightboxIndex = index;
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightboxImage');
    const title = document.getElementById('lightboxTitle');

    if (!galleryImages[index]) return;

    img.src = galleryImages[index].image;
    title.textContent = galleryImages[index].title;
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function navigateLightbox(direction) {
    lightboxIndex = (lightboxIndex + direction + galleryImages.length) % galleryImages.length;
    const img = document.getElementById('lightboxImage');
    const title = document.getElementById('lightboxTitle');
    img.src = galleryImages[lightboxIndex].image;
    title.textContent = galleryImages[lightboxIndex].title;
}

// Keyboard navigation for lightbox
document.addEventListener('keydown', (e) => {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox || !lightbox.classList.contains('active')) return;

    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
});

// Expose to global scope
window.closeLightbox = closeLightbox;
window.navigateLightbox = navigateLightbox;

/* ============================================================
   6. CONTACT FORM (Multi-step OTP)
   ============================================================ */
let contactToken = '';
let currentStep = 1;

function initContactForm() {
    // OTP input auto-advance
    const otpInputs = document.querySelectorAll('.otp-input-group input');
    if (otpInputs.length === 0) return; // Not on contact page

    otpInputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            if (value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });

        // Only allow digits
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    });
}

function goToStep(step) {
    currentStep = step;

    // Update step indicators
    document.querySelectorAll('.step').forEach((s, idx) => {
        s.classList.remove('active', 'completed');
        if (idx + 1 < step) s.classList.add('completed');
        if (idx + 1 === step) s.classList.add('active');
    });

    // Update form steps
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
    const activeStep = document.getElementById(`step${step}`);
    if (activeStep) activeStep.classList.add('active');
}

async function sendOTP() {
    const slName = document.getElementById('slName').value.trim();
    const errorEl = document.getElementById('step1Error');
    const btn = document.getElementById('sendOtpBtn');

    // Validate
    if (!slName) {
        showError(errorEl, 'Please enter your Second Life name.');
        return;
    }

    // Loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending OTP...';

    const result = await apiFetch('/contact/send-otp/', {
        method: 'POST',
        body: JSON.stringify({ sl_name: slName }),
    });

    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send OTP';

    if (result.success) {
        hideError(errorEl);
        goToStep(2);
        // Focus first OTP input
        setTimeout(() => {
            const firstInput = document.querySelector('.otp-input-group input');
            if (firstInput) firstInput.focus();
        }, 300);
    } else {
        showError(errorEl, result.error?.sl_name?.[0] || result.error || 'Failed to send OTP.');
    }
}

async function verifyOTP() {
    const slName = document.getElementById('slName').value.trim();
    const otpInputs = document.querySelectorAll('.otp-input-group input');
    const otpCode = Array.from(otpInputs).map(i => i.value).join('');
    const errorEl = document.getElementById('step2Error');
    const btn = document.getElementById('verifyOtpBtn');

    // Validate
    if (otpCode.length !== 6) {
        showError(errorEl, 'Please enter the complete 6-digit OTP.');
        return;
    }

    // Loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';

    const result = await apiFetch('/contact/verify-otp/', {
        method: 'POST',
        body: JSON.stringify({ sl_name: slName, otp_code: otpCode }),
    });

    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-check-circle"></i> Verify OTP';

    if (result.success) {
        contactToken = result.data.token;
        hideError(errorEl);
        goToStep(3);
    } else {
        showError(errorEl, typeof result.error === 'string' ? result.error : 'Invalid OTP. Please try again.');
    }
}

async function submitContact() {
    const topic = document.getElementById('contactTopic').value;
    const message = document.getElementById('contactMessage').value.trim();
    const errorEl = document.getElementById('step3Error');
    const btn = document.getElementById('submitContactBtn');

    // Validate
    if (!topic) {
        showError(errorEl, 'Please select a topic.');
        return;
    }
    if (message.length < 10) {
        showError(errorEl, 'Message must be at least 10 characters.');
        return;
    }

    // Loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

    const result = await apiFetch('/contact/submit/', {
        method: 'POST',
        body: JSON.stringify({ token: contactToken, topic, message }),
    });

    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-envelope"></i> Submit Message';

    if (result.success) {
        hideError(errorEl);
        // Show success
        document.getElementById('contactFormSteps').style.display = 'none';
        document.getElementById('contactSuccess').style.display = 'block';
    } else {
        showError(errorEl, typeof result.error === 'string' ? result.error : 'Failed to submit. Please try again.');
    }
}

function showError(el, msg) {
    if (el) {
        el.textContent = msg;
        el.classList.add('show');
    }
}

function hideError(el) {
    if (el) {
        el.textContent = '';
        el.classList.remove('show');
    }
}

// Expose to global scope
window.sendOTP = sendOTP;
window.verifyOTP = verifyOTP;
window.submitContact = submitContact;
window.goToStep = goToStep;
