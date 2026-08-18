// ===== MENU BURGER MOBILE =====
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');

if (burger && navLinks) {
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
}

// ===== BARRE DE PROGRESSION ET NAVIGATION ACTIVE =====
const readingProgress = document.getElementById('readingProgress');
const sections = document.querySelectorAll('main section[id]');
const navItems = document.querySelectorAll('.nav-links a');
const backToTop = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

    if (readingProgress) {
        readingProgress.style.width = `${progress}%`;
    }

    let current = '';
    sections.forEach(section => {
        if (scrollTop >= section.offsetTop - 140) {
            current = section.id;
        }
    });

    navItems.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
    });

    if (backToTop) {
        backToTop.classList.toggle('visible', scrollTop > 500);
    }
});

// ===== COMPTEURS ANIMÉS =====
function animateCounter(element, target, suffix = '') {
    if (!element) return;
    let current = 0;
    const duration = 1800;
    const step = Math.max(1, Math.ceil(target / (duration / 16)));
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = `${current}${suffix}`;
    }, 16);
}

// ===== ANIMATIONS AU DÉFILEMENT =====
const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        currentObserver.unobserve(entry.target);
    });
}, { threshold: 0.15 });

document.querySelectorAll('.fade-in-section, .langue-card, .competences-col').forEach(element => {
    observer.observe(element);
});

const statsObserver = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const item = entry.target;
        const target = Number.parseInt(item.dataset.target, 10);
        const numberElement = item.querySelector('.stat-number-big');
        const suffix = target >= 60 ? '+' : '';
        animateCounter(numberElement, target, suffix);
        currentObserver.unobserve(item);
    });
}, { threshold: 0.3 });

document.querySelectorAll('.stat-item[data-target]').forEach(item => {
    statsObserver.observe(item);
});

// ===== FORMULAIRE DE CONTACT =====
const contactForm = document.getElementById('contactForm');
const submitButton = document.getElementById('submitBtn');
const formSuccess = document.getElementById('formSuccess');

if (contactForm && submitButton) {
    contactForm.addEventListener('submit', async event => {
        event.preventDefault();
        submitButton.disabled = true;
        submitButton.textContent = 'Envoi...';

        try {
            const response = await fetch(contactForm.action, {
                method: 'POST',
                body: new FormData(contactForm),
                headers: { Accept: 'application/json' }
            });

            if (!response.ok) throw new Error('Échec de l’envoi');

            contactForm.reset();
            if (formSuccess) formSuccess.style.display = 'flex';
            submitButton.textContent = 'Envoyé !';
        } catch (error) {
            submitButton.disabled = false;
            submitButton.textContent = 'Réessayer';
            window.alert('Erreur lors de l’envoi. Contactez-moi directement par email.');
        }
    });
}
