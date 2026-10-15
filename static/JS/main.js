document.addEventListener('DOMContentLoaded', () => {
            
    // --- GESTIÓN DE TEMA OSCURO ---
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.documentElement;
    
    if (localStorage.getItem('theme') === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeToggle.textContent = '☀️';
    }
    
    themeToggle.addEventListener('click', () => {
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            themeToggle.textContent = '🌙';
        } else {
            body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeToggle.textContent = '☀️';
        }
    });

    // --- ANIMACIÓN DE CONTADORES ---
    const counters = document.querySelectorAll('.counter');
    const statsSection = document.getElementById('stats-section');
    let hasAnimated = false;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const animateCounters = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            
            if (prefersReducedMotion) {
                counter.innerText = target.toLocaleString();
                return; 
            }

            const duration = 2000; 
            const increment = target / (duration / 16); 
            
            let current = 0;
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = Math.ceil(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target.toLocaleString();
                }
            };
            updateCounter();
        });
    };

    const observer = new IntersectionObserver((entries) => {
        if(entries[0].isIntersecting && !hasAnimated) {
            animateCounters();
            hasAnimated = true; 
        }
    }, { threshold: 0.5 });
    
    if (statsSection) observer.observe(statsSection);


    // --- ACORDEÓN FAQ ---
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const btn = item.querySelector('.faq-btn');
        btn.addEventListener('click', () => {
            const isCurrentlyExpanded = btn.getAttribute('aria-expanded') === 'true';

            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-btn').setAttribute('aria-expanded', 'false');
                }
            });

            if (isCurrentlyExpanded) {
                item.classList.remove('active');
                btn.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                btn.setAttribute('aria-expanded', 'true');
            }
        });
    });


    // --- CARRUSEL DE IMÁGENES ---
    const items = document.querySelectorAll('.carousel-item');
    const dots = document.querySelectorAll('.dot');
    let index = 0;
    
    function showSlide(n) {
        if(items.length === 0) return;
        
        items[index].classList.remove('active');
        dots[index].classList.remove('active');
        dots[index].setAttribute('aria-current', 'false'); 
        
        index = (n + items.length) % items.length;
        
        items[index].classList.add('active');
        dots[index].classList.add('active');
        dots[index].setAttribute('aria-current', 'true'); 
    }
    
    const nextBtn = document.querySelector('.carousel-next');
    const prevBtn = document.querySelector('.carousel-prev');
    
    if (nextBtn) nextBtn.addEventListener('click', () => showSlide(index + 1));
    if (prevBtn) prevBtn.addEventListener('click', () => showSlide(index - 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => showSlide(i)));
    
    let carouselInterval;
    const startCarousel = () => {
        if (items.length > 0) {
            carouselInterval = setInterval(() => showSlide(index + 1), 5000);
        }
    };
    const stopCarousel = () => {
        clearInterval(carouselInterval);
    };

    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', stopCarousel);
        carouselContainer.addEventListener('mouseleave', startCarousel);
        carouselContainer.addEventListener('focusin', stopCarousel);
        carouselContainer.addEventListener('focusout', startCarousel);
    }
    startCarousel();


    // --- SISTEMA DE SONIDOS ---
    document.addEventListener('click', (event) => {
        if (event.target.closest('.btn-primary') || event.target.closest('.carousel-prev') || 
            event.target.closest('.carousel-next') || event.target.closest('.dot') || event.target.closest('.faq-btn')) {
            const audio = document.getElementById('click-sound');
            if (audio) {
                audio.currentTime = 0;
                audio.play().catch(() => {});
            }
        }
    });


    // --- EASTER EGGS ---
    const ojosSecretos = document.getElementById('ojos-secretos');
    const oofSound = document.getElementById('oof-sound'); 

    // 1. Botón secreto del footer
    if (ojosSecretos) {
        ojosSecretos.addEventListener('click', () => {
            if (oofSound) {
                oofSound.currentTime = 0;
                oofSound.play().catch(() => {});
            }

            if (!prefersReducedMotion) {
                document.body.classList.add('efecto-teletransporte');
            }

            setTimeout(() => {
                window.open('https://youtu.be/bi6Q_lzaIow?si=ZsdpVNqZ3gk0J8bK', '_blank');
                document.body.classList.remove('efecto-teletransporte');
            }, prefersReducedMotion ? 100 : 1500); 
        });
    }

    // 2. Evento Teclado: Código "FAH"
    let typedKeys = '';
    const secretWord = 'fah';

    document.addEventListener('keydown', (e) => {
        typedKeys += e.key.toLowerCase();
        
        if (typedKeys.length > secretWord.length) {
            typedKeys = typedKeys.slice(-secretWord.length);
        }
        
        if (typedKeys === secretWord) {
            if (oofSound) {
                oofSound.currentTime = 0;
                oofSound.play().catch(()=>{});
            }
            
            if (!prefersReducedMotion) {
                document.body.classList.add('shaking');
                setTimeout(() => {
                    document.body.classList.remove('shaking');
                }, 500);
            }
        }
    });
});


// --- EASTER EGG GLOBAL: Modo Todd Howard ---
let typedKeys = '';
const secretWord = 'fah';
const toddWord = 'todd';

document.addEventListener('keydown', (e) => {
    typedKeys += e.key.toLowerCase();
    
    if (typedKeys.length > 10) typedKeys = typedKeys.slice(-10);
    
    if (typedKeys.endsWith(secretWord)) {
        if (oofSound) {
            oofSound.currentTime = 0;
            oofSound.play().catch(()=>{});
        }
        document.body.classList.add('shaking');
        setTimeout(() => document.body.classList.remove('shaking'), 500);
    }

    if (typedKeys.endsWith(toddWord)) {
        alert("It just works. Por favor, compra Skyrim otra vez.");
        document.documentElement.style.filter = "invert(1)"; 
        setTimeout(() => document.documentElement.style.filter = "none", 1000);
    }
});