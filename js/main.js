/**
 * Kaire Mame Faty — Portfolio
 * Interactions: Thème Sombre/Clair, Navigation fluide, ScrollSpy, Filtres & Contact
 */

(function () {
  'use strict';

  var root = document.documentElement;

  // 1. Initialiser le thème le plus tôt possible
  var savedTheme = 'light';
  try {
    savedTheme = localStorage.getItem('kmf-theme');
    if (!savedTheme) {
      savedTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
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
        ? '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }

    var currentTheme = root.getAttribute('data-theme') || 'light';
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

    // 5. ScrollSpy automatique pour les ancres sur la page d'accueil
    var sections = document.querySelectorAll('main > section[id]');
    var navLinks = document.querySelectorAll('#nav a[href^="#"]');

    if (sections.length > 0 && navLinks.length > 0) {
      var observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
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

    // 6. Filtrage dynamique des projets
    var filterBtns = document.querySelectorAll('.filter');
    var projectCards = document.querySelectorAll('[data-cats]');

    filterBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filterBtns.forEach(function (b) {
          b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
        });
        var category = btn.getAttribute('data-filter');

        projectCards.forEach(function (card) {
          if (category === 'all') {
            card.hidden = false;
          } else {
            var cats = ' ' + (card.getAttribute('data-cats') || '') + ' ';
            card.hidden = cats.indexOf(' ' + category + ' ') === -1;
          }
        });
      });
    });

    // 7. Boutons de copie rapide dans le presse-papier
    document.querySelectorAll('[data-copy]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var text = btn.getAttribute('data-copy');
        if (!text) return;

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            showToast('Copié : ' + text);
          }).catch(function () {
            fallbackCopy(text);
          });
        } else {
          fallbackCopy(text);
        }
      });
    });

    function fallbackCopy(text) {
      var temp = document.createElement('textarea');
      temp.value = text;
      temp.style.position = 'fixed';
      temp.style.opacity = '0';
      document.body.appendChild(temp);
      temp.select();
      try {
        document.execCommand('copy');
        showToast('Copié : ' + text);
      } catch (e) {
        showToast('Sélectionné : ' + text);
      }
      document.body.removeChild(temp);
    }

    // 8. Formulaire de contact interactif
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
          showToast('Veuillez remplir tous les champs obligatoires (*)');
          if (!name && nameEl) nameEl.focus();
          else if (!email && emailEl) emailEl.focus();
          else if (!message && msgEl) msgEl.focus();
          return;
        }

        // Vérification email sommaire
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
          showToast('Veuillez saisir une adresse email valide');
          if (emailEl) emailEl.focus();
          return;
        }

        var fullMessage = 'Bonjour Kaire Mame Faty,\n\n' + message + '\n\nDe : ' + name + ' (' + email + ')';
        var out = document.getElementById('out');
        var outText = document.getElementById('out-text');

        if (out && outText) {
          outText.value = fullMessage;
          out.hidden = false;
        }

        showToast('Message préparé ! Ouverture de votre messagerie...');

        try {
          var subject = encodeURIComponent('Contact depuis votre portfolio — ' + name);
          var body = encodeURIComponent(fullMessage);
          window.location.href = 'mailto:mfaty.kaire@univ-thies.sn?subject=' + subject + '&body=' + body;
        } catch (err) {}
      });
    }

    var copyOutBtn = document.getElementById('out-copy');
    if (copyOutBtn) {
      copyOutBtn.addEventListener('click', function () {
        var outText = document.getElementById('out-text');
        if (outText && outText.value) {
          fallbackCopy(outText.value);
        }
      });
    }

    // 9. Animation fluide des barres de progression des compétences
    var skillFills = document.querySelectorAll('.skill-bar-colored-fill[data-width]');
    if (skillFills.length > 0 && 'IntersectionObserver' in window) {
      skillFills.forEach(function (bar) {
        bar.style.width = '0%';
      });

      var skillsObserver = new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var bar = entry.target;
            var targetWidth = bar.getAttribute('data-width');
            if (targetWidth) {
              bar.style.width = targetWidth;
            }
            observer.unobserve(bar);
          }
        });
      }, { threshold: 0.15 });

      skillFills.forEach(function (bar) {
        skillsObserver.observe(bar);
      });
    }
  });
})();
