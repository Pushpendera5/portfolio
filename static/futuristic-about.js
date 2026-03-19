// ============================================
// ENHANCED FUTURISTIC ABOUT SECTION
// ============================================

console.log("✓ Enhanced About Script Loaded");

function initAbout() {
    const aboutSection = document.getElementById('about');
    if (!aboutSection) return;
    
    const cards = aboutSection.querySelectorAll('.futuristic-about-card');
    
    const colors = [
        { hex: '#ff3366', rgb: '255, 51, 102' },  // Pink
        { hex: '#2df0ac', rgb: '45, 240, 172' },  // Cyan
        { hex: '#d13ce2', rgb: '209, 60, 226' },  // Purple
        { hex: '#4faece', rgb: '79, 172, 254' }   // Blue
    ];
    
    cards.forEach((card, idx) => {
        const color = colors[idx];
        const cardInner = card.querySelector('.card-inner');
        const cardIcon = card.querySelector('.card-icon');
        const cardContent = card.querySelector('.card-content');
        const cardAccent = card.querySelector('.card-accent');
        
        if (!cardInner) return;
        
        // Animated border style with gradient
        cardInner.style.position = 'relative';
        cardInner.style.background = `linear-gradient(135deg, rgba(10, 15, 30, 0.95) 0%, rgba(20, 30, 50, 0.6) 100%)`;
        cardInner.style.border = `2px solid ${color.hex}`;
        cardInner.style.borderRadius = '1.5rem';
        cardInner.style.padding = '2rem';
        cardInner.style.transition = 'all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
        cardInner.style.cursor = 'pointer';
        cardInner.style.overflow = 'hidden';
        
        // Create animated glow border effect
        const glowBorder = document.createElement('div');
        glowBorder.style.position = 'absolute';
        glowBorder.style.inset = '0';
        glowBorder.style.borderRadius = '1.5rem';
        glowBorder.style.padding = '2px';
        glowBorder.style.background = `linear-gradient(45deg, ${color.hex}, transparent, ${color.hex})`;
        glowBorder.style.opacity = '0';
        glowBorder.style.transition = 'opacity 0.4s ease';
        glowBorder.style.pointerEvents = 'none';
        glowBorder.style.zIndex = '-1';
        cardInner.appendChild(glowBorder);
        
        // Icon styles
        if (cardIcon) {
            cardIcon.style.width = '90px';
            cardIcon.style.height = '90px';
            cardIcon.style.marginBottom = '1.2rem';
            cardIcon.style.display = 'flex';
            cardIcon.style.alignItems = 'center';
            cardIcon.style.justifyContent = 'center';
            cardIcon.style.background = `linear-gradient(135deg, rgba(${color.rgb}, 0.25) 0%, rgba(${color.rgb}, 0.08) 100%)`;
            cardIcon.style.border = `2px solid ${color.hex}`;
            cardIcon.style.borderRadius = '1.2rem';
            cardIcon.style.transition = 'all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
            cardIcon.style.boxShadow = `inset 0 0 20px rgba(${color.rgb}, 0.1)`;
            
            const iconSpan = cardIcon.querySelector('span');
            if (iconSpan) {
                iconSpan.style.fontSize = '2.8rem';
                iconSpan.style.color = color.hex;
                iconSpan.style.transition = 'all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
                iconSpan.style.filter = `drop-shadow(0 0 15px rgba(${color.rgb}, 0.5))`;
            }
        }
        
        // Content styles
        if (cardContent) {
            const h3 = cardContent.querySelector('h3');
            const p = cardContent.querySelector('p');
            
            if (h3) {
                h3.style.color = '#fff';
                h3.style.fontSize = '1.3rem';
                h3.style.fontWeight = '700';
                h3.style.marginBottom = '0.75rem';
                h3.style.transition = 'all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
                h3.style.letterSpacing = '0.02em';
            }
            
            if (p) {
                p.style.color = 'rgba(226, 232, 240, 0.8)';
                p.style.fontSize = '0.95rem';
                p.style.transition = 'all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)';
                p.style.lineHeight = '1.6';
            }
        }
        
        // Enhanced accent glow
        if (cardAccent) {
            cardAccent.style.position = 'absolute';
            cardAccent.style.top = '-30px';
            cardAccent.style.right = '-30px';
            cardAccent.style.width = '150px';
            cardAccent.style.height = '150px';
            cardAccent.style.background = color.hex;
            cardAccent.style.opacity = '0.1';
            cardAccent.style.borderRadius = '50%';
            cardAccent.style.filter = 'blur(50px)';
            cardAccent.style.pointerEvents = 'none';
            cardAccent.style.animation = 'pulseGlow 4s ease-in-out infinite';
        }
        
        // Enhanced hover effects
        card.addEventListener('mouseenter', () => {
            cardInner.style.transform = 'translateY(-12px) scale(1.02)';
            cardInner.style.boxShadow = `0 25px 50px rgba(${color.rgb}, 0.35), inset 0 0 30px rgba(${color.rgb}, 0.08)`;
            cardInner.style.borderColor = color.hex;
            glowBorder.style.opacity = '0.6';
            
            if (cardIcon) {
                cardIcon.style.transform = 'scale(1.2) rotateZ(5deg)';
                cardIcon.style.boxShadow = `0 0 35px ${color.hex}, inset 0 0 25px rgba(${color.rgb}, 0.15)`;
                cardIcon.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                const iconSpan = cardIcon.querySelector('span');
                if (iconSpan) {
                    iconSpan.style.transform = 'scale(1.25) rotateZ(-5deg)';
                    iconSpan.style.filter = `drop-shadow(0 0 25px ${color.hex})`;
                }
            }
            
            const h3 = cardContent?.querySelector('h3');
            const p = cardContent?.querySelector('p');
            if (h3) {
                h3.style.color = color.hex;
                h3.style.textShadow = `0 0 20px rgba(${color.rgb}, 0.5)`;
            }
            if (p) {
                p.style.color = 'rgba(226, 232, 240, 1)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            cardInner.style.transform = 'translateY(0) scale(1)';
            cardInner.style.boxShadow = 'none';
            cardInner.style.borderColor = color.hex;
            glowBorder.style.opacity = '0';
            
            if (cardIcon) {
                cardIcon.style.transform = 'scale(1) rotateZ(0deg)';
                cardIcon.style.boxShadow = `inset 0 0 20px rgba(${color.rgb}, 0.1)`;
                cardIcon.style.borderColor = color.hex;
                const iconSpan = cardIcon.querySelector('span');
                if (iconSpan) {
                    iconSpan.style.transform = 'scale(1) rotateZ(0deg)';
                    iconSpan.style.filter = `drop-shadow(0 0 15px rgba(${color.rgb}, 0.5))`;
                }
            }
            
            const h3 = cardContent?.querySelector('h3');
            const p = cardContent?.querySelector('p');
            if (h3) {
                h3.style.color = '#fff';
                h3.style.textShadow = 'none';
            }
            if (p) {
                p.style.color = 'rgba(226, 232, 240, 0.8)';
            }
        });
        
        // Mouse move parallax effect
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left - rect.width / 2) / 20;
            const y = (e.clientY - rect.top - rect.height / 2) / 20;
            
            if (cardIcon) {
                cardIcon.style.transform = `scale(1.2) rotateZ(5deg) translateX(${x}px) translateY(${y}px)`;
            }
        });
    });
    
    // Animate heading
    const heading = aboutSection.querySelector('h2');
    if (heading) {
        heading.style.animation = 'none';
        setTimeout(() => {
            heading.style.fontSize = '2rem';
            heading.style.fontWeight = '800';
            heading.style.transition = 'all 0.6s ease';
        }, 100);
    }
    
    // Animate paragraphs
    const textParagraphs = aboutSection.querySelector('.lg\\:col-span-5')?.querySelectorAll('p');
    if (textParagraphs) {
        textParagraphs.forEach((p, i) => {
            p.style.opacity = '1';
            p.style.animation = `fadeInUp 0.8s ease-out ${0.2 + i * 0.2}s`;
        });
    }
}

// Add pulse glow animation
if (!document.querySelector('style[data-pulseGlow]')) {
    const style = document.createElement('style');
    style.setAttribute('data-pulseGlow', 'true');
    style.textContent = `
        @keyframes pulseGlow {
            0%, 100% { transform: scale(1); opacity: 0.1; }
            50% { transform: scale(1.1); opacity: 0.15; }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
}

// Run on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAbout);
} else {
    initAbout();
}
setTimeout(initAbout, 200);
