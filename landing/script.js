/* Dealix Landing — interactions */
(function () {
  'use strict';

  // ---- Theme toggle ----
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  let theme = prefersDark ? 'dark' : 'light';
  root.setAttribute('data-theme', theme);

  const sunSvg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  const moonSvg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  function renderToggle() {
    if (!toggle) return;
    toggle.innerHTML = theme === 'dark' ? sunSvg : moonSvg;
    toggle.setAttribute('aria-label', theme === 'dark' ? 'التبديل إلى الوضع الفاتح' : 'التبديل إلى الوضع الداكن');
  }
  renderToggle();

  if (toggle) {
    toggle.addEventListener('click', function () {
      theme = theme === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', theme);
      renderToggle();
    });
  }

  // ---- Mobile menu ----
  const burger = document.querySelector('[data-menu-toggle]');
  const links = document.querySelector('.nav__links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      const open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ---- Smooth scroll (in case scroll-behavior unsupported) ----
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const id = a.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---- Reveal on scroll ----
  if ('IntersectionObserver' in window) {
    const elements = document.querySelectorAll('.card, .agent, .step, .quote, .badge, .faq__item');
    elements.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity 600ms ease, transform 600ms cubic-bezier(0.16, 1, 0.3, 1)';
    });
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    elements.forEach(function (el) { io.observe(el); });
  }
})();

// ---- CTA form handler ----
function handleCtaSubmit(e) {
  e.preventDefault();
  const form = e.target;
  const input = form.querySelector('input[type="email"]');
  const note = document.getElementById('cta-response');
  if (!input || !input.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
    if (note) note.textContent = 'الرجاء إدخال بريد إلكتروني صالح.';
    input && input.focus();
    return false;
  }
  if (note) note.textContent = 'شكراً! سنتواصل معك خلال يوم عمل على: ' + input.value;
  form.reset();
  return false;
}
