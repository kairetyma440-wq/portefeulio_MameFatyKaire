/**
 * Kaire Mame Faty — Portfolio
 * Interactions: Menu mobile, Validation contact, Toasts, Filtres & Back to top
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var toast = document.getElementById('toast');

    function showToast(msg, duration) {
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('on');
      setTimeout(function () {
        toast.classList.remove('on');
      }, duration || 2600);
    }

    // 1. Menu mobile (burger toggle)
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

    // 2. Défilement avec état du Header (scrolled) & bouton Retour en haut
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
        if (y > 350) {
          backToTop.style.display = 'flex';
          backToTop.classList.add('visible');
        } else {
          backToTop.classList.remove('visible');
          backToTop.style.display = 'none';
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

    // 3. ScrollSpy automatique pour les ancres sur index.html
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

    // 4. Formulaire de contact interactif
    var contactForm = document.getElementById('contact-form');
    if (contactForm) {
      contactForm.addEventListener('submit', function (e) {
        e.preventDefault();

        var nameEl = document.getElementById('contact-name') || document.getElementById('f-name');
        var emailEl = document.getElementById('contact-email') || document.getElementById('f-mail');
        var subjectEl = document.getElementById('contact-subject') || document.getElementById('f-subject');
        var msgEl = document.getElementById('contact-message') || document.getElementById('f-msg');

        var name = nameEl ? nameEl.value.trim() : '';
        var email = emailEl ? emailEl.value.trim() : '';
        var subject = subjectEl ? subjectEl.value.trim() : '';
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

        var subjectText = subject ? 'Contact Portfolio — ' + subject + ' (' + name + ')' : 'Contact Portfolio — ' + name;
        var fullBody = 'Bonjour Kaire Mame Faty,\n\n' + message + '\n\nDe : ' + name + '\nEmail : ' + email;

        showToast('Merci ' + name + ' ! Redirection vers votre messagerie...');

        try {
          var mailtoLink = 'mailto:mfaty.kaire@univ-thies.sn?subject=' + encodeURIComponent(subjectText) + '&body=' + encodeURIComponent(fullBody);
          window.location.href = mailtoLink;
        } catch (err) {
          console.error(err);
        }

        contactForm.reset();
      });
    }
  });
})();
