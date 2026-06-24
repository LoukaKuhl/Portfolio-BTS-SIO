// ===== MENU BURGER (mobile) =====
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');

burger.addEventListener('click', () => {
    burger.classList.toggle('active');
    navLinks.classList.toggle('active');
    const expanded = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', String(!expanded));
});

navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        burger.classList.remove('active');
        navLinks.classList.remove('active');
        burger.setAttribute('aria-expanded', 'false');
    });
});

// ===== DARK MODE =====
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const body = document.body;

const savedTheme = localStorage.getItem('theme') || 'light';
body.className = savedTheme;
themeIcon.className = savedTheme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';

themeToggle.addEventListener('click', () => {
    const isDark = body.classList.contains('dark');
    body.className = isDark ? 'light' : 'dark';
    themeIcon.className = isDark ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
});

// ===== BARRE DE PROGRESSION DE LECTURE =====
const readingProgress = document.getElementById('readingProgress');

// ===== LIEN ACTIF AU SCROLL =====
const sections = document.querySelectorAll('main section[id]');
const navItems = document.querySelectorAll('.nav-links a');
const backToTop = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    // Progression de lecture
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    readingProgress.style.width = progress + '%';

    // Lien actif
    let current = '';
    sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - 140) {
            current = section.getAttribute('id');
        }
    });
    navItems.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });

    // Bouton retour en haut
    if (backToTop) {
        backToTop.classList.toggle('visible', window.scrollY > 500);
    }
});

// ===== COMPTEURS ANIMÉS =====
const statItems = document.querySelectorAll('.stat-item[data-target]');

function animateCounter(el, target, suffix = '') {
    let start = 0;
    const duration = 1800;
    const step = Math.ceil(target / (duration / 16));
    const timer = setInterval(() => {
        start += step;
        if (start >= target) {
            start = target;
            clearInterval(timer);
        }
        el.textContent = start + suffix;
    }, 16);
}

// ===== INTERSECTION OBSERVER (fade-in + compteurs + barres langue) =====
const observerOptions = { threshold: 0.15 };

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Fade-in sections
document.querySelectorAll('.fade-in-section').forEach(section => {
    observer.observe(section);
});

// Compteurs stats — chaque stat s'anime indépendamment
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const item = entry.target;
            const target = parseInt(item.dataset.target);
            const numEl = item.querySelector('.stat-number-big');
            const suffix = target >= 60 ? '+' : '';
            animateCounter(numEl, target, suffix);
            statsObserver.unobserve(item);
        }
    });
}, { threshold: 0.3 });

statItems.forEach(item => statsObserver.observe(item));

// Barres de langue
document.querySelectorAll('.langue-card').forEach(card => {
    observer.observe(card);
});

// Barres de compétences (progress bars) — déclenchées au scroll
document.querySelectorAll('.competences-col').forEach(col => {
    observer.observe(col);
});

// ===== FORMULAIRE CONTACT (Formspree) =====
const contactForm = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const formSuccess = document.getElementById('formSuccess');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Envoi...';

        try {
            const response = await fetch(contactForm.action, {
                method: 'POST',
                body: new FormData(contactForm),
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                contactForm.reset();
                formSuccess.style.display = 'flex';
                submitBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Envoyé !';
                submitBtn.style.backgroundColor = '#10b981';
            } else {
                throw new Error();
            }
        } catch {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Réessayer';
            alert('Erreur lors de l\'envoi. Contactez-moi directement par email.');
        }
    });
}
