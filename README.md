# Portfolio de Kaire Mame Faty

Site portfolio en HTML, CSS et JavaScript pur, sans framework ni outil de build.

## Structure

```
portfolio/
├── index.html            Accueil
├── apropos.html          À propos
├── competences.html      Compétences
├── projets.html          Projets (filtres)
├── projet-*.html         Une page de détail par projet
├── parcours.html         Parcours
├── contact.html          Contact
├── css/style.css         Tous les styles
├── js/main.js            Menu, thème clair/sombre, filtres, contact
└── assets/
    ├── photo.jpg         Ta photo
    └── cv.pdf            Ton CV
```

## Lancer le site

Double-clique sur `index.html`, ou ouvre le dossier avec l'extension Live Server de VS Code.

## Mettre en ligne (gratuit)

- **GitHub Pages** : envoie le dossier dans un dépôt GitHub, puis Settings, Pages, branche `main`.
- **Netlify** : glisse-dépose le dossier sur app.netlify.com/drop.

## Modifier le contenu

- Textes : directement dans les fichiers `.html`.
- Couleurs : variables CSS en haut de `css/style.css` (`--blue`, `--navy`, `--bg`).
- Photo ou CV : remplace `assets/photo.jpg` ou `assets/cv.pdf` en gardant le même nom.

## Formulaire de contact

Le formulaire prépare le message à copier. Pour un envoi automatique, branche-le sur un service comme Formspree ou EmailJS dans `js/main.js`.
