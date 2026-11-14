// =========================================================
// CV — Kaire Mame Faty — interactions front-end
// =========================================================

document.addEventListener('DOMContentLoaded', () => {

  // --- Bascule thème clair / sombre avec icône SVG vectorielle nette ---
  const toggleBtn = document.getElementById('theme-toggle');

  const eyeSvg = `<svg class="eye-icon" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>`;
  const moonSvg = `<svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><path d="M12.3 2a10 10 0 00-1.9 19.8 10 10 0 0011.6-11.6A10 10 0 0112.3 2z"/></svg>`;

  const applyTheme = (theme) => {
    const isDark = theme === 'dark';
    document.body.classList.toggle('dark', isDark);
    if (toggleBtn) {
      toggleBtn.innerHTML = isDark ? moonSvg : eyeSvg;
      toggleBtn.title = isDark ? 'Passer en thème clair' : 'Passer en thème sombre';
    }
  };

  const savedTheme = localStorage.getItem('cv-theme') || 'light';
  applyTheme(savedTheme);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const next = document.body.classList.contains('dark') ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('cv-theme', next);
    });
  }

  // --- Bouton impression / export PDF ---
  const printBtn = document.getElementById('print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', () => window.print());
  }

  // --- Réinitialiser les animations avant impression ---
  window.addEventListener('beforeprint', () => {
    document.querySelectorAll('.block, .hero').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  });

  // --- Apparition progressive au scroll (IntersectionObserver) ---
  const blocks = document.querySelectorAll('.block, .hero');
  blocks.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(12px)';
    el.style.transition = 'opacity .4s ease, transform .4s ease';
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  blocks.forEach(el => observer.observe(el));
});
