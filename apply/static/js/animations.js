/**
 * animations.js
 * 
 * This file contains all the general UI animations and interaction enhancements
 * for the Bright Skills Development Center website.
 */

// --- UI Enhancements: Theme Toggler & Animations ---
document.addEventListener('DOMContentLoaded', function () {
  const header = document.querySelector('header');
  const backToTopBtn = document.getElementById('back-to-top');

  // Theme Toggler
  const themeToggler = document.getElementById('theme-toggler');
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);

  if (themeToggler) {
    themeToggler.addEventListener('click', () => {
      let newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }

  // Header scroll effect & Back to Top button
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      if (header) header.classList.add('scrolled');
      if (backToTopBtn) backToTopBtn.classList.add('visible');
    } else {
      if (header) header.classList.remove('scrolled');
      if (backToTopBtn) backToTopBtn.classList.remove('visible');
    }
  });

  if (backToTopBtn) {
      backToTopBtn.addEventListener('click', () => {
          window.scrollTo({ top: 0, behavior: 'smooth' });
      });
  }

  // Floating form labels (if you use the .form-group-float class)
  document.querySelectorAll('.form-group-float').forEach(group => {
      const input = group.querySelector('input, textarea');
      const label = group.querySelector('label');
      if (input.value) {
          group.classList.add('active');
      }
      input.addEventListener('focus', () => group.classList.add('active'));
      input.addEventListener('blur', () => {
          if (!input.value) {
              group.classList.remove('active');
          }
      });
  });

  // Button ripple effect
  document.querySelectorAll('button, .btn').forEach(button => {
      button.addEventListener('click', function (e) {
          const rect = button.getBoundingClientRect();
          const ripple = document.createElement('span');
          ripple.className = 'ripple';
          ripple.style.left = `${e.clientX - rect.left}px`;
          ripple.style.top = `${e.clientY - rect.top}px`;
          this.appendChild(ripple);
          setTimeout(() => ripple.remove(), 600);
      });
  });

  // Fade-in animations on scroll using IntersectionObserver
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Apply fade-in to cards and other elements
  document.querySelectorAll('.course-card-wrapper, .about-card, form, .feature-card, .course-details').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });
});