// Search Tab Functionality
const searchTabs = document.querySelectorAll('.search-tab');

searchTabs.forEach(tab => {
  tab.addEventListener('click', function() {
    // Remove active class from all tabs
    searchTabs.forEach(t => t.classList.remove('active'));
    // Add active class to clicked tab
    this.classList.add('active');
  });
});

// Search Form Submission
const searchForm = document.querySelector('.search-form');
if (searchForm) {
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const searchQuery = this.querySelector('input[type="text"]').value;
    const location = this.querySelector('select:nth-of-type(1)').value;
    const mode = this.querySelector('select:nth-of-type(2)').value;
    
    console.log('Search Query:', searchQuery);
    console.log('Location:', location);
    console.log('Mode:', mode);
    
    // Here you would typically send this data to your backend
    alert(`Searching for: ${searchQuery}\nLocation: ${location}\nMode: ${mode}`);
  });
}

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Category Card Click Handler
const categoryCards = document.querySelectorAll('.category-card');
categoryCards.forEach(card => {
  card.addEventListener('click', function() {
    const categoryTitle = this.querySelector('.category-title').textContent;
    console.log('Category clicked:', categoryTitle);
    // Here you would typically navigate to a category page or filter results
    alert(`Showing institutes for: ${categoryTitle}`);
  });
});

// Institute "View Details" Button Handler
const viewDetailsButtons = document.querySelectorAll('.btn-view-details');
viewDetailsButtons.forEach(button => {
  button.addEventListener('click', function() {
    const instituteName = this.closest('.institute-card').querySelector('.institute-name').textContent;
    console.log('View details for:', instituteName);
    // Here you would typically navigate to the institute details page
    alert(`Loading details for: ${instituteName}`);
  });
});

// Navbar Background Change on Scroll
window.addEventListener('scroll', function() {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.style.background = 'rgba(30, 41, 59, 1)';
    navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.2)';
  } else {
    navbar.style.background = 'rgba(30, 41, 59, 0.95)';
    navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
  }
});

// Animate Stats on Scroll
const statNumbers = document.querySelectorAll('.stat-number');
let statsAnimated = false;

function animateStats() {
  if (statsAnimated) return;
  
  statNumbers.forEach(stat => {
    const finalNumber = stat.textContent;
    const numericValue = parseInt(finalNumber.replace(/\D/g, ''));
    const suffix = finalNumber.replace(/[0-9]/g, '');
    let current = 0;
    const increment = numericValue / 50;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= numericValue) {
        stat.textContent = numericValue + suffix;
        clearInterval(timer);
      } else {
        stat.textContent = Math.floor(current) + suffix;
      }
    }, 30);
  });
  
  statsAnimated = true;
}

// Intersection Observer for Stats Animation
const statsSection = document.querySelector('.stats-section');
if (statsSection) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateStats();
      }
    });
  }, { threshold: 0.5 });
  
  observer.observe(statsSection);
}

// Form Validation
function validateSearchForm() {
  const searchInput = document.querySelector('.search-form input[type="text"]');
  
  if (searchInput) {
    searchInput.addEventListener('blur', function() {
      if (this.value.trim() === '') {
        this.style.borderColor = '#ef4444';
      } else {
        this.style.borderColor = '#e2e8f0';
      }
    });
    
    searchInput.addEventListener('input', function() {
      this.style.borderColor = '#e2e8f0';
    });
  }
}

validateSearchForm();

// Loading Animation for Institute Cards
function addLoadingAnimation() {
  const instituteCards = document.querySelectorAll('.institute-card');
  
  instituteCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    
    setTimeout(() => {
      card.style.transition = 'all 0.6s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 150);
  });
}

// Call loading animation when page loads
window.addEventListener('load', addLoadingAnimation);

// Mobile Menu Toggle Enhancement
const navbarToggler = document.querySelector('.navbar-toggler');
const navbarCollapse = document.querySelector('.navbar-collapse');

if (navbarToggler) {
  navbarToggler.addEventListener('click', function() {
    console.log('Mobile menu toggled');
  });
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(event) {
  const isClickInsideNav = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
  
  if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
      toggle: false
    });
    bsCollapse.hide();
  }
});

console.log('Institute Finder Website Loaded Successfully!');