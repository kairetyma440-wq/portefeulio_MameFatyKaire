/**
 * Kaire Mame Faty — Portfolio
 * Interactions: Thème Sombre/Clair, Navigation fluide, ScrollSpy & Contact
 */

(function () {
  'use strict';

  var root = document.documentElement;

  // 1. Initialiser le thème par défaut sur SOMBRE fidèle à la maquette
  var savedTheme = 'dark';
  try {
    var stored = localStorage.getItem('kmf-theme');
    if (stored) {
      savedTheme = stored;
    }
    root.setAttribute('data-theme', savedTheme);
  } catch (e) {}

  document.addEventListener('DOMContentLoaded', function () {
    var toast = document.getElementById('toast');

    function showToast(msg, duration) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('on');
      setTimeout(function () {
        toast.classList.remove('on');
      }, duration || 2400);
    }

    // 2. Gestionnaire du bouton de thème
    var themeBtn = document.getElementById('theme-btn');
    function updateThemeBtnIcon(theme) {
      if (!themeBtn) return;
      var isDark = theme === 'dark';
      themeBtn.setAttribute('aria-label', isDark ? 'Passer au mode clair' : 'Passer au mode sombre');
      themeBtn.innerHTML = isDark
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }

    var currentTheme = root.getAttribute('data-theme') || 'dark';
    updateThemeBtnIcon(currentTheme);

    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        var active = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', active);
        updateThemeBtnIcon(active);
        try {
          localStorage.setItem('kmf-theme', active);
        } catch (e) {}
        showToast(active === 'dark' ? 'Mode sombre activé' : 'Mode clair activé', 1600);
      });
    }

    // 3. Menu mobile & fermeture automatique au clic
    var menuBtn = document.getElementById('menu-btn');
    var nav = document.getElementById('nav');

    if (menuBtn && nav) {
      menuBtn.addEventListener('click', function () {
        var isOpen = nav.classList.toggle('open');
        menuBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });

      nav.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          nav.classList.remove('open');
          menuBtn.setAttribute('aria-expanded', 'false');
        });
      });
    }

    // 4. Défilement avec état du Header (scrolled) & bouton Retour en haut
    var siteHead = document.querySelector('.site-head');
    var backToTop = document.getElementById('back-to-top');

    function onScroll() {
      var y = window.scrollY || document.documentElement.scrollTop;
      if (siteHead) {
        if (y > 20) {
          siteHead.classList.add('scrolled');
        } else {
          siteHead.classList.remove('scrolled');
        }
      }
      if (backToTop) {
        if (y > 380) {
          backToTop.classList.add('visible');
        } else {
          backToTop.classList.remove('visible');
        }
      }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    if (backToTop) {
      backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // 5. ScrollSpy automatique pour les ancres de la barre de navigation
    var sections = document.querySelectorAll('main > section[id]');
    var navLinks = document.querySelectorAll('#nav a[href^="#"]');

    if (sections.length > 0 && navLinks.length > 0) {
      var observerOptions = {
        root: null,
        rootMargin: '-20% 0px -55% 0px',
        threshold: 0
      };

      var sectionObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.getAttribute('id');
            navLinks.forEach(function (link) {
              var href = link.getAttribute('href');
              if (href === '#' + id) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
              } else {
                link.classList.remove('active');
                link.removeAttribute('aria-current');
              }
            });
          }
        });
      }, observerOptions);

      sections.forEach(function (sec) {
        sectionObserver.observe(sec);
      });
    }

    // 6. Formulaire de contact interactif
    var contactForm = document.getElementById('contact-form');
    if (contactForm) {
      contactForm.addEventListener('submit', function (e) {
        e.preventDefault();

        var nameEl = document.getElementById('f-name');
        var emailEl = document.getElementById('f-mail');
        var msgEl = document.getElementById('f-msg');

        var name = nameEl ? nameEl.value.trim() : '';
        var email = emailEl ? emailEl.value.trim() : '';
        var message = msgEl ? msgEl.value.trim() : '';

        if (!name || !email || !message) {
          showToast('Veuillez remplir tous les champs obligatoires');
          if (!name && nameEl) nameEl.focus();
          else if (!email && emailEl) emailEl.focus();
          else if (!message && msgEl) msgEl.focus();
          return;
        }

        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
          showToast('Veuillez saisir une adresse email valide');
          if (emailEl) emailEl.focus();
          return;
        }

        var fullMessage = 'Bonjour Kaire Mame Faty,\n\n' + message + '\n\nDe : ' + name + ' (' + email + ')';
        showToast('Message prêt ! Redirection vers votre client email...');

        try {
          var subject = encodeURIComponent('Contact depuis votre portfolio — ' + name);
          var body = encodeURIComponent(fullMessage);
          window.location.href = 'mailto:mfaty.kaire@univ-thies.sn?subject=' + subject + '&body=' + body;
        } catch (err) {}
      });
    }
  });
})();
