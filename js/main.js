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

    // 1. Bascule du mode Sombre / Clair (Dark Mode Toggle)
    var themeToggle = document.getElementById('theme-toggle');
    function getPreferredTheme() {
      var saved = localStorage.getItem('kmf_theme');
      if (saved) return saved;
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      if (themeToggle) {
        var isDark = theme === 'dark';
        themeToggle.setAttribute('aria-label', isDark ? 'Passer au mode clair' : 'Passer au mode sombre');
        themeToggle.setAttribute('title', isDark ? 'Mode clair' : 'Mode sombre');
      }
    }

    if (themeToggle) {
      themeToggle.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
        var next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        localStorage.setItem('kmf_theme', next);
        showToast(next === 'dark' ? '🌙 Mode sombre activé' : '☀️ Mode clair activé', 1800);
      });
    }

    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
        if (!localStorage.getItem('kmf_theme')) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }

    // 2. Animation des compteurs de statistiques clés (+3, 5+, 100%)
    var counters = document.querySelectorAll('.counter[data-target]');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
      var counterObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            var target = parseInt(el.getAttribute('data-target'), 10) || 0;
            var prefix = el.getAttribute('data-prefix') || '';
            var suffix = el.getAttribute('data-suffix') || '';
            var duration = 1500;
            var startTime = null;

            function step(timestamp) {
              if (!startTime) startTime = timestamp;
              var progress = Math.min((timestamp - startTime) / duration, 1);
              // Easing easeOutExpo
              var ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
              var current = Math.floor(ease * target);
              el.textContent = prefix + current + suffix;
              if (progress < 1) {
                requestAnimationFrame(step);
              } else {
                el.textContent = prefix + target + suffix;
              }
            }
            requestAnimationFrame(step);
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.2 });

      counters.forEach(function (c) {
        counterObserver.observe(c);
      });
    }

    // 3. Menu mobile (burger toggle)
    var menuBtn = document.getElementById('menu-btn') || document.getElementById('menu-toggle');
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

        var heroSec = document.getElementById('accueil');
        var isDarkTheme = document.documentElement.getAttribute('data-theme') === 'dark';
        if (heroSec && !isDarkTheme) {
          var heroBottom = heroSec.offsetTop + heroSec.offsetHeight - 90;
          if (y < heroBottom) {
            siteHead.classList.add('nav-hero-dark');
          } else {
            siteHead.classList.remove('nav-hero-dark');
          }
        } else {
          siteHead.classList.remove('nav-hero-dark');
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

        var nameEl = document.getElementById('contact-name') || document.getElementById('nom') || document.getElementById('f-name');
        var emailEl = document.getElementById('contact-email') || document.getElementById('email') || document.getElementById('f-mail');
        var subjectEl = document.getElementById('contact-subject') || document.getElementById('sujet') || document.getElementById('f-subject');
        var msgEl = document.getElementById('contact-message') || document.getElementById('message') || document.getElementById('f-msg');

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
        var fullBody = 'Bonjour Mame Faty Kaire,\n\n' + message + '\n\nDe : ' + name + '\nEmail : ' + email;

        showToast('Merci ' + name + ' ! Message envoyé avec succès 🚀');

        try {
          var mailtoLink = 'mailto:mfaty.kaire@univ-thies.sn?subject=' + encodeURIComponent(subjectText) + '&body=' + encodeURIComponent(fullBody);
          window.location.href = mailtoLink;
        } catch (err) {
          console.error(err);
        }

        contactForm.reset();
      });
    }

    // 5. Formulaire Newsletter
    var newsForms = document.querySelectorAll('.newsletter-form-v9, .footer-news-form');
    newsForms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var emailInput = form.querySelector('input[type="email"]');
        if (emailInput && emailInput.value.trim()) {
          showToast('📬 Merci pour votre inscription à la newsletter !', 3000);
          form.reset();
        }
      });
    });

    // 6. Animation des jauges circulaires de compétences au scroll
    var gauges = document.querySelectorAll('.skill-gauge-radial');
    if (gauges.length > 0 && 'IntersectionObserver' in window) {
      var gaugeObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var circle = entry.target.querySelector('path.circle');
            var span = entry.target.querySelector('span');
            if (circle && span) {
              var targetPct = parseInt(span.textContent, 10) || 85;
              circle.style.strokeDasharray = '0, 100';
              setTimeout(function () {
                circle.style.transition = 'stroke-dasharray 1.4s ease-out';
                circle.style.strokeDasharray = targetPct + ', 100';
              }, 120);
            }
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.3 });

      gauges.forEach(function (g) {
        gaugeObserver.observe(g);
      });
    }

    // 7. Défilement fluide compensé pour les ancres avec le header fixe
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        var targetId = this.getAttribute('href');
        if (targetId === '#') return;
        var targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          var headerOffset = 64;
          var elementPosition = targetEl.getBoundingClientRect().top;
          var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  });
})();
