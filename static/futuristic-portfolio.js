// ============================================
// FUTURISTIC 3D PORTFOLIO ENGINE
// Premium 3D Effects, Animations & Interactions
// ============================================

class FuturisticPortfolio {
    constructor() {
        this.time = 0;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.particles = [];
        
        this.init();
        this.setupAnimations();
        this.setupScrollEffects();
        this.animate();
    }
    
    init() {
        this.setupCardAnimations();
        this.setupScrollReveal();
        this.setupNavbarEffect();
        this.setup3DText();
        this.setupButtonGlows();
    }
    

    
    // ============================================
    // 3D TEXT EFFECT - Headers become 3D
    // ============================================
    setup3DText() {
        const headings = document.querySelectorAll('h1, h2, h3');
        
        headings.forEach(heading => {
            heading.style.perspective = '1000px';
            heading.style.transformStyle = 'preserve-3d';
            
            // Add 3D depth effect on hover
            heading.addEventListener('mouseenter', () => {
                heading.style.transform = 'perspective(1000px) rotateX(10deg) rotateY(-5deg) translateZ(20px)';
                heading.style.transition = 'transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
                heading.style.filter = 'drop-shadow(0 20px 30px rgba(209, 60, 226, 0.3))';
            });
            
            heading.addEventListener('mouseleave', () => {
                heading.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
                heading.style.filter = 'drop-shadow(0 10px 20px rgba(209, 60, 226, 0.1))';
            });
        });
    }

    // ============================================
    // ADVANCED CARD ANIMATIONS
    // ============================================
    setupCardAnimations() {
        // Project cards with tilt effect
        const projectCards = document.querySelectorAll('[data-project-card]');
        projectCards.forEach(card => this.setupTiltCard(card));
        
        // Experience cards
        const experienceCards = document.querySelectorAll('[data-experience-card]');
        experienceCards.forEach(card => this.setupTiltCard(card));
        
        // Certification cards
        const certificationCards = document.querySelectorAll('[data-certification-card]');
        certificationCards.forEach(card => this.setupTiltCard(card));
        
        // Skill cards
        const skillCards = document.querySelectorAll('[data-skill-card]');
        skillCards.forEach(card => this.setupTiltCard(card));
        
        // Skill tags
        const skillTags = document.querySelectorAll('.skill-tag');
        skillTags.forEach(tag => this.setupTiltCard(tag));
    }
    
    setupTiltCard(card) {
        card.style.perspective = '1200px';
        card.style.transformStyle = 'preserve-3d';
        
        const rect = card.getBoundingClientRect();
        let isHovering = false;
        
        card.addEventListener('mouseenter', () => {
            isHovering = true;
            card.style.transition = 'none';
        });
        
        card.addEventListener('mousemove', (e) => {
            if (!isHovering) return;
            
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const rotateX = ((y / rect.height) - 0.5) * 20;
            const rotateY = ((x / rect.width) - 0.5) * -20;
            
            card.style.transform = `perspective(1200px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05) translateZ(30px)`;
            card.style.filter = `drop-shadow(0 20px 40px rgba(209, 60, 226, 0.4))`;
        });
        
        card.addEventListener('mouseleave', () => {
            isHovering = false;
            card.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg) scale(1) translateZ(0px)';
            card.style.filter = 'drop-shadow(0 10px 20px rgba(209, 60, 226, 0.1))';
        });
    }
    
    // ============================================
    // SCROLL REVEAL ANIMATIONS
    // ============================================
    setupScrollReveal() {
        if (!('IntersectionObserver' in window)) return;
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0) scale(1)';
                    entry.target.style.filter = 'blur(0px)';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe all cards and sections
        document.querySelectorAll(
            '[data-project-card], [data-experience-card], .skill-tag, section > div'
        ).forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px) scale(0.95)';
            el.style.filter = 'blur(5px)';
            el.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            observer.observe(el);
        });
    }
    
    // ============================================
    // NAVBAR GLASS EFFECT
    // ============================================
    setupNavbarEffect() {
        const navbar = document.querySelector('nav');
        if (!navbar) return;
        
        window.addEventListener('scroll', () => {
            const scrollProgress = window.scrollY / 100;
            const opacity = Math.min(0.95, 0.8 + scrollProgress * 0.15);
            const blur = Math.min(20, 12 + scrollProgress);
            
            navbar.style.backdropFilter = `blur(${blur}px)`;
            navbar.style.background = `rgba(15, 22, 35, ${opacity})`;
            navbar.style.boxShadow = `0 4px 30px rgba(209, 60, 226, ${Math.min(0.2, scrollProgress * 0.1)})`;
        });
    }
    
    // ============================================
    // BUTTON GLOW EFFECTS
    // ============================================
    setupButtonGlows() {
        const buttons = document.querySelectorAll('button, a[class*="px-8"]');
        
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.filter = 'drop-shadow(0 0 20px rgba(209, 60, 226, 0.8))';
                btn.style.transform = 'scale(1.08) translateY(-2px)';
                btn.style.transition = 'all 0.3s ease';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.filter = 'drop-shadow(0 0 10px rgba(209, 60, 226, 0.4))';
                btn.style.transform = 'scale(1) translateY(0)';
            });
        });
    }
    
    // ============================================
    // SCROLL-BASED EFFECTS
    // ============================================
    setupScrollEffects() {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            
            // Parallax effect on hero
            const hero = document.querySelector('section:first-of-type');
            if (hero) {
                hero.style.backgroundPosition = `0 ${scrollY * 0.5}px`;
            }
            
            // Glow intensity increases on scroll
            document.querySelectorAll('[data-project-card], [data-experience-card]').forEach(card => {
                const rect = card.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isVisible) {
                    const glowIntensity = (1 - Math.abs(rect.top) / window.innerHeight) * 0.5;
                    card.style.boxShadow = `0 0 ${20 + glowIntensity * 30}px rgba(209, 60, 226, ${0.2 + glowIntensity})`;
                }
            });
        });
    }
    
    // ============================================
    // FLOATING ANIMATION
    // ============================================
    setupAnimations() {
        // Floating text elements
        document.querySelectorAll('.inline-flex, h1, h2').forEach((el, index) => {
            el.style.animation = `float ${3 + index * 0.5}s ease-in-out infinite`;
        });
    }
    
    // ============================================
    // ANIMATION LOOP
    // ============================================
    animate = () => {
        requestAnimationFrame(this.animate);
        this.time += 0.016;
    }
}

// ============================================
// MOUSE INTERACTION EFFECTS
// ============================================
class MouseTracker {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.setup();
    }
    
    setup() {
        document.addEventListener('mousemove', (e) => {
            this.x = e.clientX;
            this.y = e.clientY;
            
            // Create cursor trail effect
            this.createTrail();
        });
    }
    
    createTrail() {
        const trail = document.createElement('div');
        trail.style.cssText = `
            position: fixed;
            pointer-events: none;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(209, 60, 226, 0.8), rgba(209, 60, 226, 0));
            left: ${this.x}px;
            top: ${this.y}px;
            transform: translate(-50%, -50%);
            z-index: 999;
            box-shadow: 0 0 10px rgba(209, 60, 226, 0.6);
        `;
        
        document.body.appendChild(trail);
        
        setTimeout(() => {
            trail.style.opacity = '0';
            trail.style.transition = 'opacity 0.6s ease';
            setTimeout(() => trail.remove(), 600);
        }, 50);
    }
}

// ============================================
// SMOOTH SCROLL ENHANCEMENT
// ============================================
class SmoothScroll {
    constructor() {
        this.setupSmoothScroll();
    }
    
    setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// ============================================
// MOBILE MENU ANIMATION
// ============================================
class MobileMenu {
    constructor() {
        this.setupMobileMenu();
    }
    
    setupMobileMenu() {
        const menuBtn = document.querySelector('[class*="md:hidden"] span');
        if (!menuBtn) return;
        
        menuBtn.addEventListener('click', () => {
            menuBtn.style.transform = 'rotate(90deg)';
            menuBtn.style.transition = 'transform 0.3s ease';
        });
    }
}

// ============================================
// COUNTER ANIMATION
// ============================================
class CounterAnimation {
    constructor() {
        this.setupCounters();
    }
    
    setupCounters() {
        if (!('IntersectionObserver' in window)) return;
        
        const counters = document.querySelectorAll('[data-counter]');
        if (counters.length === 0) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = entry.target;
                    const finalValue = parseInt(target.dataset.counter);
                    this.animateCounter(target, finalValue);
                    observer.unobserve(target);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => observer.observe(counter));
    }
    
    animateCounter(element, finalValue) {
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 60);
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = finalValue;
                clearInterval(timer);
            } else {
                element.textContent = currentValue;
            }
        }, 30);
    }
}

// ============================================
// INITIALIZATION
// ============================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    const portfolio = new FuturisticPortfolio();
    new MouseTracker();
    new SmoothScroll();
    new MobileMenu();
    new CounterAnimation();
    
    console.log('✨ Futuristic 3D Portfolio Activated!');
    console.log('🎨 Premium effects loaded');
    console.log('🚀 Ready to impress!');
}

// Add CSS Animations
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes glowPulse {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(209, 60, 226, 0.5)); }
        50% { filter: drop-shadow(0 0 30px rgba(209, 60, 226, 0.8)); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    @keyframes liquidBorder {
        0%, 100% { box-shadow: inset 0 0 20px rgba(209, 60, 226, 0.1), 0 0 20px rgba(209, 60, 226, 0.3); }
        50% { box-shadow: inset 0 0 30px rgba(209, 60, 226, 0.2), 0 0 40px rgba(209, 60, 226, 0.6); }
    }
    
    @keyframes neonFlicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            text-shadow: 0 0 10px #d13ce2, 0 0 20px #d13ce2, 0 0 30px #d13ce2;
        }
        20%, 24%, 55% {
            text-shadow: 0 0 5px #d13ce2;
        }
    }
    
    .neon-flicker {
        animation: neonFlicker 0.15s infinite;
    }
    
    .glow-pulse {
        animation: glowPulse 2s ease-in-out infinite;
    }
    
    .liquid-border {
        animation: liquidBorder 3s ease-in-out infinite;
    }
`;
document.head.appendChild(styleSheet);
