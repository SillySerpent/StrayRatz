// StrayRatz JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Adjust for navbar height
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add active class to nav items
    const currentPage = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Interest level radio buttons visual enhancement
    const interestLevels = document.querySelectorAll('input[name="interest_level"]');
    if (interestLevels.length > 0) {
        interestLevels.forEach(radio => {
            radio.addEventListener('change', function() {
                // Remove active class from all labels
                document.querySelectorAll('.form-check-inline').forEach(el => {
                    el.classList.remove('active');
                });
                
                // Add active class to selected label
                if (this.checked) {
                    this.parentElement.classList.add('active');
                }
            });
        });
    }
    
    // Newsletter form AJAX submission (backup for when jQuery might not be loaded)
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            // If jQuery is handling this, let it continue
            if (window.jQuery) return;
            
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('newsletter-result');
            
            fetch(this.getAttribute('action'), {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
                    newsletterForm.reset();
                } else {
                    resultDiv.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = '<div class="alert alert-danger">An error occurred. Please try again.</div>';
            });
        });
    }
    
    // Animated elements on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const position = element.getBoundingClientRect();
            
            // If element is in viewport
            if (position.top < window.innerHeight && position.bottom >= 0) {
                element.classList.add('animated');
            }
        });
    };
    
    // Add animation class to elements
    document.querySelectorAll('.feature-card, .testimonial-card').forEach(el => {
        el.classList.add('animate-on-scroll');
    });
    
    // Initial check and add scroll event
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    // Flavor selector in product section
    const flavorButtons = document.querySelectorAll('.flavor-btn');
    
    if (flavorButtons.length > 0) {
        flavorButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                flavorButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
            });
        });
    }
}); 