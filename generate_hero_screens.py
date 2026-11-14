"""
Generate attractive landing/home page screenshots for each project.
These will be used as Slide 1 (the most representative hero image) in each slider.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 960, 570
OUT = r"c:\Users\USER\Desktop\mes projet\portefeulio_MameFatyKaire\assets"

def get_font(size, bold=False, mono=False):
    names = []
    if mono:
        names = ["Consolas", "Courier New", "monospace"]
    elif bold:
        names = ["Segoe UI Bold", "Arial Bold", "DejaVuSans-Bold.ttf", "Arial"]
    else:
        names = ["Segoe UI", "Arial", "DejaVuSans.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except:
            pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1,y1,x2,y2 = xy
    # Clamp radius so it never exceeds half the shortest dimension
    half_w = max(1, (x2 - x1) // 2)
    half_h = max(1, (y2 - y1) // 2)
    radius = min(radius, half_w, half_h)
    if fill:
        if x1+radius <= x2-radius:
            draw.rectangle([x1+radius,y1,x2-radius,y2], fill=fill)
        if y1+radius <= y2-radius:
            draw.rectangle([x1,y1+radius,x2,y2-radius], fill=fill)
        draw.ellipse([x1,y1,x1+2*radius,y1+2*radius], fill=fill)
        draw.ellipse([x2-2*radius,y1,x2,y1+2*radius], fill=fill)
        draw.ellipse([x1,y2-2*radius,x1+2*radius,y2], fill=fill)
        draw.ellipse([x2-2*radius,y2-2*radius,x2,y2], fill=fill)
    if outline:
        for d in range(width):
            draw.arc([x1+d,y1+d,x1+2*radius+d,y1+2*radius+d], 180, 270, fill=outline)
            draw.arc([x2-2*radius-d,y1+d,x2-d,y1+2*radius+d], 270, 360, fill=outline)
            draw.arc([x1+d,y2-2*radius-d,x1+2*radius+d,y2-d], 90, 180, fill=outline)
            draw.arc([x2-2*radius-d,y2-2*radius-d,x2-d,y2-d], 0, 90, fill=outline)
            draw.line([x1+radius,y1+d,x2-radius,y1+d], fill=outline, width=1)
            draw.line([x1+radius,y2-d,x2-radius,y2-d], fill=outline, width=1)
            draw.line([x1+d,y1+radius,x1+d,y2-radius], fill=outline, width=1)
            draw.line([x2-d,y1+radius,x2-d,y2-radius], fill=outline, width=1)

def centered_text(draw, x, y, text, font, fill):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    draw.text((x - tw//2, y), text, font=font, fill=fill)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1: Locaux — Login page (dark navy left + white right, role selection)
# ─────────────────────────────────────────────────────────────────────────────
def gen_locaux_login():
    img = Image.new("RGB", (W, H), "#F0F4FF")
    d = ImageDraw.Draw(img)

    # LEFT panel dark navy
    d.rectangle([0, 0, 400, H], fill="#0B1733")

    # Gradient overlay subtle - draw a few bands
    for i in range(80):
        alpha_color = tuple(int(c * (1 - i/120)) for c in (0x14, 0x2A, 0x5E))
        d.rectangle([0, H - i*7, 400, H - i*7 + 7], fill=alpha_color)

    # Logo circle on left panel
    d.ellipse([155, 48, 245, 118], fill="#1D68FF")
    # University cap icon simplified
    # Cap top
    d.polygon([(200,65),(160,82),(200,99),(240,82)], fill="white")
    d.rectangle([224,82,232,100], fill="white")
    d.ellipse([225,98,231,104], fill="white")

    # Brand name
    f_brand = get_font(15, bold=True)
    f_title = get_font(22, bold=True)
    f_sub = get_font(13)
    f_feat = get_font(12)

    d.text((200-45, 128), "CROUS-T / UCAD", font=f_brand, fill="#6BA3FF")
    centered_text(d, 200, 155, "Gestion des Locaux", f_title, "white")
    centered_text(d, 200, 185, "Universitaires", f_title, "white")

    # Tagline
    f_tag = get_font(11)
    centered_text(d, 200, 220, "Plateforme centralisée de gestion", f_tag, "#A8C4FF")
    centered_text(d, 200, 236, "des espaces académiques", f_tag, "#A8C4FF")

    # Features list
    features = ["✓  Gestion des demandes", "✓  Validation multi-niveaux", "✓  Suivi comptable", "✓  Rapports et statistiques"]
    fy = 268
    for feat in features:
        d.text((60, fy), feat, font=f_feat, fill="#7EC8A0")
        fy += 24

    # Footer left panel
    centered_text(d, 200, H-32, "© 2024 CROUS-T — Tous droits réservés", get_font(10), "#4A6FA5")

    # RIGHT panel (white card)
    # Card shadow effect
    d.rectangle([430, 60, 910, H-50], fill="#E8EEF8")
    d.rectangle([420, 50, 900, H-60], fill="white")

    # Title right panel
    f_wlc = get_font(18, bold=True)
    f_sel = get_font(13)
    d.text((660-80, 72), "Bienvenue 👋", font=f_wlc, fill="#0B1733")
    d.text((660-100, 100), "Sélectionnez votre profil pour continuer", font=f_sel, fill="#6B7280")

    # Role buttons
    roles = [
        ("🏛️", "Demandeur", "Soumettre une demande de local", "#0062FF", "#EEF3FF"),
        ("🏢", "DCUVE", "Direction de la construction", "#059669", "#ECFDF5"),
        ("👥", "Commission", "Comité de validation", "#7C3AED", "#F5F3FF"),
        ("📊", "Directeur", "Supervision générale", "#DC2626", "#FEF2F2"),
        ("💰", "Comptable", "Gestion financière", "#D97706", "#FFFBEB"),
    ]
    ry = 135
    for icon, name, desc, color, bg in roles:
        draw_rounded_rect(d, [430, ry, 890, ry+55], 10, fill=bg)
        draw_rounded_rect(d, [430, ry, 890, ry+55], 10, outline=color, width=1)
        # Icon circle
        d.ellipse([445, ry+10, 475, ry+40], fill=color)
        d.text((452, ry+14), icon, font=get_font(14), fill="white")
        # Name
        d.text((488, ry+9), name, font=get_font(13, bold=True), fill=color)
        d.text((488, ry+27), desc, font=get_font(10), fill="#6B7280")
        # Arrow
        d.text((864, ry+18), "›", font=get_font(20, bold=True), fill=color)
        ry += 65

    # Save
    img.save(os.path.join(OUT, "locaux-screen-1.png"), quality=95)
    print("✓ locaux-screen-1.png")


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2: Locaux — DCUVE Dashboard (KPI cards + table)
# ─────────────────────────────────────────────────────────────────────────────
def gen_locaux_dashboard():
    img = Image.new("RGB", (W, H), "#F0F4FF")
    d = ImageDraw.Draw(img)

    # Sidebar
    d.rectangle([0, 0, 200, H], fill="#0B1733")
    # Logo sidebar
    d.ellipse([78, 15, 118, 55], fill="#1D68FF")
    d.text((86, 24), "🏛", font=get_font(20), fill="white")
    centered_text(d, 100, 62, "CROUS-T", get_font(11, bold=True), "#6BA3FF")

    menu = [("🏠","Accueil",True),("📋","Demandes",False),("🏢","Locaux",False),("📊","Rapports",False),("⚙️","Paramètres",False)]
    my = 90
    for icon, label, active in menu:
        if active:
            d.rectangle([0, my-4, 200, my+34], fill="#1D68FF")
        d.text((16, my), icon, font=get_font(16), fill="white")
        d.text((42, my+3), label, font=get_font(12, bold=active), fill="white" if active else "#A8C4FF")
        my += 50

    # Main area
    # Header
    d.rectangle([200, 0, W, 55], fill="white")
    d.text((220, 16), "Tableau de bord — DCUVE", font=get_font(16, bold=True), fill="#0B1733")
    d.text((220, 36), "Gestion des locaux universitaires", font=get_font(10), fill="#6B7280")
    # Avatar
    d.ellipse([900, 10, 940, 50], fill="#1D68FF")
    d.text((912, 18), "MF", font=get_font(13, bold=True), fill="white")

    # KPI Cards
    kpis = [
        ("42", "Locaux disponibles", "#0062FF", "#EEF3FF", "🏢"),
        ("18", "En cours validation", "#D97706", "#FFFBEB", "⏳"),
        ("127", "Demandes traitées", "#059669", "#ECFDF5", "✅"),
        ("3", "Urgences actives", "#DC2626", "#FEF2F2", "🚨"),
    ]
    cx = 215
    for val, label, color, bg, icon in kpis:
        draw_rounded_rect(d, [cx, 68, cx+170, 155], 10, fill=bg)
        d.text((cx+12, 80), icon, font=get_font(22), fill=color)
        d.text((cx+12, 108), val, font=get_font(26, bold=True), fill=color)
        d.text((cx+12, 138), label, font=get_font(9), fill="#6B7280")
        cx += 182

    # Table header
    d.rectangle([215, 168, 940, 196], fill="#0B1733")
    cols = ["N°","Type de Local","Bâtiment","Capacité","Statut","Actions"]
    cw = [40, 180, 140, 90, 100, 110]
    tx = 225
    for col, w in zip(cols, cw):
        d.text((tx, 176), col, font=get_font(10, bold=True), fill="white")
        tx += w

    # Table rows
    rows = [
        ("01","Salle de cours","Bât. A","45 places","Disponible","#059669"),
        ("02","Amphithéâtre","Bât. B","250 places","Réservé","#D97706"),
        ("03","Salle TD","Bât. C","30 places","En maintenance","#DC2626"),
        ("04","Laboratoire","Bât. D","20 places","Disponible","#059669"),
        ("05","Salle TD","Bât. A","30 places","Disponible","#059669"),
        ("06","Bureau dir.","Bât. Admin","8 places","Réservé","#D97706"),
    ]
    ry = 196
    for i, (n, typ, bat, cap, stat, sc) in enumerate(rows):
        bg_row = "white" if i % 2 == 0 else "#F8FAFF"
        d.rectangle([215, ry, 940, ry+32], fill=bg_row)
        vals = [n, typ, bat, cap]
        tx = 225
        cw2 = [40, 180, 140, 90]
        for v, w in zip(vals, cw2):
            d.text((tx, ry+9), v, font=get_font(10), fill="#374151")
            tx += w
        # Status badge
        draw_rounded_rect(d, [tx, ry+7, tx+88, ry+25], 8, fill=sc+"22")
        d.text((tx+6, ry+10), stat, font=get_font(9, bold=True), fill=sc)
        # Action button
        draw_rounded_rect(d, [tx+100, ry+7, tx+198, ry+25], 8, fill="#EEF3FF")
        d.text((tx+112, ry+10), "Voir détails", font=get_font(9), fill="#0062FF")
        ry += 32

    img.save(os.path.join(OUT, "locaux-screen-2.png"), quality=95)
    print("✓ locaux-screen-2.png")


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 3: Locaux — Formulaire de demande
# ─────────────────────────────────────────────────────────────────────────────
def gen_locaux_form():
    img = Image.new("RGB", (W, H), "#F0F4FF")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 200, H], fill="#0B1733")
    # sidebar minimal
    centered_text(d, 100, 30, "CROUS-T", get_font(13, bold=True), "#6BA3FF")
    menu = [("🏠","Accueil",False),("📋","Demandes",True),("🏢","Locaux",False),("📊","Rapports",False)]
    my = 70
    for icon, label, active in menu:
        if active:
            d.rectangle([0, my-4, 200, my+34], fill="#1D68FF")
        d.text((16, my), icon, font=get_font(16), fill="white")
        d.text((42, my+3), label, font=get_font(12, bold=active), fill="white")
        my += 50

    # Main
    d.rectangle([200, 0, W, 55], fill="white")
    d.text((220, 16), "Nouvelle demande de local", font=get_font(16, bold=True), fill="#0B1733")

    # Form card
    draw_rounded_rect(d, [215, 65, 940, H-20], 14, fill="white")

    # Steps bar
    steps = ["1. Infos personnelles", "2. Type de local", "3. Période", "4. Validation"]
    sx = 240
    for i, step in enumerate(steps):
        col = "#1D68FF" if i == 1 else ("#D1D5DB" if i > 1 else "#059669")
        draw_rounded_rect(d, [sx, 80, sx+155, 100], 10, fill=col)
        d.text((sx+6, 83), step, font=get_font(9, bold=(i==1)), fill="white")
        sx += 165

    # Form fields
    d.text((240, 115), "Type de local souhaité *", font=get_font(12, bold=True), fill="#374151")
    # Dropdown
    draw_rounded_rect(d, [240, 132, 580, 162], 8, fill="#F9FAFB", outline="#D1D5DB", width=1)
    d.text((254, 141), "Salle de cours TD (30-45 places)", font=get_font(11), fill="#374151")
    d.text((555, 143), "▼", font=get_font(10), fill="#6B7280")

    d.text((240, 175), "Bâtiment préféré", font=get_font(12, bold=True), fill="#374151")
    draw_rounded_rect(d, [240, 192, 580, 222], 8, fill="#F9FAFB", outline="#D1D5DB", width=1)
    d.text((254, 201), "Bâtiment A — UFR Sciences", font=get_font(11), fill="#374151")

    # Date pickers in a row
    d.text((240, 235), "Date de début *", font=get_font(12, bold=True), fill="#374151")
    d.text((510, 235), "Date de fin *", font=get_font(12, bold=True), fill="#374151")
    draw_rounded_rect(d, [240, 252, 490, 282], 8, fill="#F9FAFB", outline="#1D68FF", width=2)
    d.text((254, 261), "📅  15 / 03 / 2024", font=get_font(11), fill="#374151")
    draw_rounded_rect(d, [510, 252, 760, 282], 8, fill="#F9FAFB", outline="#D1D5DB", width=1)
    d.text((524, 261), "📅  22 / 03 / 2024", font=get_font(11), fill="#374151")

    d.text((240, 295), "Motif de la demande *", font=get_font(12, bold=True), fill="#374151")
    draw_rounded_rect(d, [240, 312, 760, 400], 8, fill="#F9FAFB", outline="#D1D5DB", width=1)
    d.text((254, 322), "Cours de Structures de données — L3 Informatique", font=get_font(11), fill="#374151")
    d.text((254, 342), "Nombre d'étudiants : 38 — Durée : 2h", font=get_font(10), fill="#6B7280")

    # Capacité
    d.text((240, 415), "Capacité requise", font=get_font(12, bold=True), fill="#374151")
    for cap, x in [("< 30 places", 240), ("30 – 50 places", 360), ("50 – 100 places", 490), ("> 100 places", 630)]:
        active = cap == "30 – 50 places"
        brd = "#1D68FF" if active else "#D1D5DB"
        bg2 = "#EEF3FF" if active else "#F9FAFB"
        draw_rounded_rect(d, [x, 432, x+108, 458], 8, fill=bg2, outline=brd, width=2 if active else 1)
        d.text((x+8, 440), cap, font=get_font(9, bold=active), fill="#1D68FF" if active else "#374151")

    # Buttons
    draw_rounded_rect(d, [240, 490, 390, 528], 10, fill="#F3F4F6")
    d.text((284, 502), "← Retour", font=get_font(12), fill="#374151")
    draw_rounded_rect(d, [610, 490, 760, 528], 10, fill="#0062FF")
    d.text((648, 502), "Continuer →", font=get_font(12, bold=True), fill="white")

    img.save(os.path.join(OUT, "locaux-screen-3.png"), quality=95)
    print("✓ locaux-screen-3.png")


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 4: Locaux — Commission validation view
# ─────────────────────────────────────────────────────────────────────────────
def gen_locaux_commission():
    img = Image.new("RGB", (W, H), "#F0F4FF")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 200, H], fill="#0B1733")
    centered_text(d, 100, 30, "CROUS-T", get_font(13, bold=True), "#6BA3FF")

    # Main area
    d.rectangle([200, 0, W, 55], fill="white")
    d.text((220, 16), "Commission de validation", font=get_font(16, bold=True), fill="#0B1733")
    d.text((220, 36), "12 demandes en attente d'examen", font=get_font(10), fill="#D97706")

    # Kanban columns
    cols_data = [
        ("En attente", "#D97706", "#FFFBEB", 5),
        ("En examen", "#1D68FF", "#EEF3FF", 3),
        ("Approuvées", "#059669", "#ECFDF5", 4),
    ]
    cx = 210
    for title, color, bg, count in cols_data:
        draw_rounded_rect(d, [cx, 65, cx+230, H-20], 12, fill=bg)
        d.rectangle([cx, 65, cx+230, 100], fill=color)
        d.text((cx+12, 72), title, font=get_font(13, bold=True), fill="white")
        d.text((cx+180, 73), str(count), font=get_font(13, bold=True), fill="white")

        # Cards in column
        cy = 108
        items = [
            ("Salle TD 304","M. Diallo — L3 Info","15/03","30 places"),
            ("Amphi 200","Pr. Ndiaye — Master","18/03","200 places"),
            ("Labo Info","Mme Sarr — L2","20/03","25 places"),
        ][:count if count <= 3 else 3]
        for name, req, date, cap in items:
            draw_rounded_rect(d, [cx+8, cy, cx+222, cy+72], 8, fill="white")
            d.text((cx+16, cy+8), name, font=get_font(11, bold=True), fill="#0B1733")
            d.text((cx+16, cy+26), req, font=get_font(9), fill="#6B7280")
            d.text((cx+16, cy+42), f"📅 {date}  👥 {cap}", font=get_font(9), fill="#6B7280")
            # Action buttons
            draw_rounded_rect(d, [cx+16, cy+55, cx+78, cy+70], 6, fill=color+"22")
            d.text((cx+22, cy+58), "Voir" if title!="Approuvées" else "Détails", font=get_font(8, bold=True), fill=color)
            cy += 82
        cx += 242

    img.save(os.path.join(OUT, "locaux-screen-4.png"), quality=95)
    print("✓ locaux-screen-4.png")


# ─────────────────────────────────────────────────────────────────────────────
# TOUBA SERVICE — Screen 1: Landing page hero
# ─────────────────────────────────────────────────────────────────────────────
def gen_touba_landing():
    img = Image.new("RGB", (W, H), "#F9FAFB")
    d = ImageDraw.Draw(img)

    # Navbar
    d.rectangle([0, 0, W, 56], fill="white")
    d.rectangle([0, 55, W, 57], fill="#E5E7EB")
    d.text((30, 14), "🕌", font=get_font(22), fill="#059669")
    d.text((62, 18), "Touba Service", font=get_font(16, bold=True), fill="#059669")
    # Nav links
    for txt, x in [("Accueil",320),("Services",420),("Artisans",520),("Urgence",620),("À propos",720)]:
        d.text((x, 20), txt, font=get_font(12), fill="#374151")
    draw_rounded_rect(d, [820, 12, 940, 44], 20, fill="#059669")
    d.text((838, 20), "Se connecter", font=get_font(11, bold=True), fill="white")

    # Hero section green gradient
    # Draw green gradient background
    for i in range(300):
        ratio = i / 300
        r = int(5 + (16-5)*ratio)
        g = int(150 + (120-150)*ratio)
        b = int(105 + (80-105)*ratio)
        d.rectangle([0, 57+i, W, 58+i], fill=(r,g,b))

    # Hero text
    d.text((60, 90), "Trouvez un artisan de", font=get_font(34, bold=True), fill="white")
    d.text((60, 134), "confiance à Touba", font=get_font(34, bold=True), fill="white")
    d.text((60, 184), "Des professionnels vérifiés à portée de main —", font=get_font(14), fill="#D1FAE5")
    d.text((60, 203), "Plombiers, électriciens, menuisiers et plus encore.", font=get_font(14), fill="#D1FAE5")

    # Trust badges
    badges = ["✅ 500+ artisans vérifiés", "⭐ Note moyenne 4.8/5", "📍 Localisation en temps réel"]
    bx = 60
    for b_txt in badges:
        d.text((bx, 230), b_txt, font=get_font(11), fill="#A7F3D0")
        bx += 220

    # Search bar
    draw_rounded_rect(d, [55, 258, 865, 310], 30, fill="white")
    d.text((80, 274), "🔍", font=get_font(16), fill="#6B7280")
    d.text((110, 277), "Type de service...", font=get_font(13), fill="#9CA3AF")
    d.rectangle([330, 270, 332, 300], fill="#E5E7EB")
    d.text((345, 274), "📍", font=get_font(16), fill="#6B7280")
    d.text((375, 277), "Quartier à Touba...", font=get_font(13), fill="#9CA3AF")
    draw_rounded_rect(d, [725, 262, 858, 306], 24, fill="#059669")
    d.text((748, 274), "🔍 Rechercher", font=get_font(12, bold=True), fill="white")

    # Categories section
    d.rectangle([0, 357, W, H], fill="white")
    centered_text(d, W//2, 365, "Nos catégories de services", get_font(18, bold=True), "#0B1733")
    centered_text(d, W//2, 390, "Trouvez le bon professionnel pour chaque besoin", get_font(12), "#6B7280")

    cats = [
        ("🔧","Plomberie","#0062FF","#EEF3FF"),
        ("⚡","Électricité","#D97706","#FFFBEB"),
        ("🪵","Menuiserie","#92400E","#FEF3C7"),
        ("❄️","Climatisation","#0891B2","#E0F2FE"),
        ("🔩","Mécanique","#4B5563","#F3F4F6"),
        ("🧱","Maçonnerie","#B45309","#FEF9C3"),
    ]
    cx = 60
    for icon, name, color, bg in cats:
        draw_rounded_rect(d, [cx, 420, cx+128, 540], 14, fill=bg)
        d.ellipse([cx+39, 428, cx+89, 478], fill=color)
        d.text((cx+50, 437), icon, font=get_font(22), fill="white")
        centered_text(d, cx+64, 485, name, get_font(11, bold=True), "#374151")
        draw_rounded_rect(d, [cx+24, 508, cx+104, 530], 10, fill=color)
        centered_text(d, cx+64, 513, "Explorer →", get_font(9, bold=True), "white")
        cx += 148

    img.save(os.path.join(OUT, "touba-screen-1.png"), quality=95)
    print("✓ touba-screen-1.png")


# ─────────────────────────────────────────────────────────────────────────────
# TOUBA SERVICE — Screen 2: Artisan profile card / search results
# ─────────────────────────────────────────────────────────────────────────────
def gen_touba_artisan():
    img = Image.new("RGB", (W, H), "#F9FAFB")
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 56], fill="white")
    d.text((30, 14), "🕌 Touba Service", font=get_font(14, bold=True), fill="#059669")
    d.text((300, 20), "← Retour aux résultats", font=get_font(11), fill="#6B7280")

    # Profile hero
    for i in range(140):
        ratio = i/140
        r = int(5 + 10*ratio)
        g = int(150 - 30*ratio)
        b = int(105 - 25*ratio)
        d.rectangle([0, 56+i, W, 57+i], fill=(r,g,b))

    # Avatar
    d.ellipse([55, 80, 155, 180], fill="white")
    d.ellipse([65, 90, 145, 170], fill="#059669")
    d.text((87, 108), "👷", font=get_font(36), fill="white")

    # Name + rating
    d.text((175, 85), "Modou Diallo", font=get_font(22, bold=True), fill="white")
    d.text((175, 115), "Plombier certifié — Touba Mosquée", font=get_font(13), fill="#D1FAE5")
    # Stars
    d.text((175, 142), "⭐⭐⭐⭐⭐", font=get_font(14), fill="#FCD34D")
    d.text((320, 147), "4.9 (87 avis)", font=get_font(11), fill="#D1FAE5")

    # Badges
    badges_hero = [("✅ Vérifié","#059669"),("🏆 Top artisan","#D97706"),("📍 Disponible","#0062FF")]
    bx = 175
    for b_t, b_c in badges_hero:
        draw_rounded_rect(d, [bx, 165, bx+len(b_t)*7+16, 185], 10, fill=b_c)
        d.text((bx+6, 168), b_t, font=get_font(9, bold=True), fill="white")
        bx += len(b_t)*7+24

    # Main content below hero
    # Left card — info
    draw_rounded_rect(d, [30, 210, 450, H-20], 14, fill="white")
    d.text((50, 225), "Informations", font=get_font(14, bold=True), fill="#0B1733")
    infos = [("📞","77 123 45 67"),("📧","modou@touba.sn"),("📍","Quartier Darou Khoudoss"),("🕐","Disponible 7j/7 · 7h-20h"),("🛠","12 ans d'expérience")]
    iy = 252
    for icon, val in infos:
        d.text((50, iy), icon, font=get_font(14), fill="#059669")
        d.text((80, iy+2), val, font=get_font(11), fill="#374151")
        iy += 32

    # Specialties
    d.text((50, 420), "Spécialités", font=get_font(13, bold=True), fill="#0B1733")
    specs = ["Canalisations","Chauffe-eau","Sanitaires","Forage","Irrigation"]
    sx = 50
    sy = 445
    for s in specs:
        sw = len(s)*7+16
        draw_rounded_rect(d, [sx, sy, sx+sw, sy+24], 10, fill="#ECFDF5", outline="#059669", width=1)
        d.text((sx+6, sy+5), s, font=get_font(9), fill="#059669")
        sx += sw + 8
        if sx > 400:
            sx = 50
            sy += 32

    # Right side — reviews + action
    draw_rounded_rect(d, [470, 210, 930, 390], 14, fill="white")
    d.text((490, 225), "Avis clients récents", font=get_font(13, bold=True), fill="#0B1733")
    reviews = [
        ("Amadou S.", "Excellent travail, très professionnel !", "5.0"),
        ("Fatou D.", "Réparation rapide et soignée, je recommande", "4.8"),
        ("Ibrahima N.", "Prix raisonnable et ponctuel", "5.0"),
    ]
    ry = 252
    for name, text, stars in reviews:
        d.ellipse([490, ry, 514, ry+24], fill="#059669")
        d.text((496, ry+4), name[0], font=get_font(10, bold=True), fill="white")
        d.text((522, ry+2), name, font=get_font(10, bold=True), fill="#374151")
        d.text((522, ry+16), text[:45], font=get_font(9), fill="#6B7280")
        d.text((850, ry+6), f"⭐{stars}", font=get_font(9), fill="#D97706")
        ry += 44

    # Action buttons
    draw_rounded_rect(d, [470, 408, 695, 460], 12, fill="#059669")
    d.text((520, 424), "📱 Contacter sur WhatsApp", font=get_font(12, bold=True), fill="white")
    draw_rounded_rect(d, [705, 408, 930, 460], 12, fill="#0062FF")
    d.text((740, 424), "📅 Prendre rendez-vous", font=get_font(12, bold=True), fill="white")

    # Map snippet
    draw_rounded_rect(d, [470, 475, 930, H-20], 12, fill="#E8F5E9")
    # Fake mini map
    d.rectangle([470, 475, 930, H-20], fill="#C8E6C9")
    d.rectangle([550, 490, 850, H-35], fill="#A5D6A7")
    d.text((550, 490), "📍 Position sur la carte — Darou Khoudoss", font=get_font(10), fill="#1B5E20")
    # road lines
    d.line([550,520,850,520], fill="#81C784", width=2)
    d.line([700,490,700,H-35], fill="#81C784", width=2)
    d.ellipse([685,505,715,535], fill="#059669")
    d.text((690,512), "📍", font=get_font(14), fill="white")

    img.save(os.path.join(OUT, "touba-screen-2.png"), quality=95)
    print("✓ touba-screen-2.png")


# ─────────────────────────────────────────────────────────────────────────────
# TOUBA SERVICE — Screen 3: Carte interactive / Map view
# ─────────────────────────────────────────────────────────────────────────────
def gen_touba_map():
    img = Image.new("RGB", (W, H), "#F9FAFB")
    d = ImageDraw.Draw(img)

    # Navbar
    d.rectangle([0, 0, W, 56], fill="white")
    d.text((30, 14), "🕌 Touba Service", font=get_font(14, bold=True), fill="#059669")
    d.text((700, 20), "🔔", font=get_font(16), fill="#374151")
    d.ellipse([760, 10, 800, 50], fill="#059669")
    d.text((772, 20), "MF", font=get_font(12, bold=True), fill="white")

    # Left sidebar
    draw_rounded_rect(d, [10, 65, 290, H-10], 12, fill="white")
    d.text((25, 75), "🔍 Rechercher un artisan", font=get_font(12, bold=True), fill="#374151")
    draw_rounded_rect(d, [18, 97, 282, 127], 8, fill="#F9FAFB", outline="#D1D5DB", width=1)
    d.text((32, 106), "Plombier, électricien...", font=get_font(11), fill="#9CA3AF")

    # Filters
    d.text((25, 138), "Filtrer par service", font=get_font(10, bold=True), fill="#374151")
    filters = [("🔧 Plomberie", True),("⚡ Électricité", False),("🪵 Menuiserie", False),("❄️ Clim", False)]
    fy = 155
    for ftxt, active in filters:
        bg_f = "#ECFDF5" if active else "#F9FAFB"
        brd_f = "#059669" if active else "#E5E7EB"
        draw_rounded_rect(d, [18, fy, 282, fy+30], 8, fill=bg_f, outline=brd_f, width=1)
        d.text((30, fy+8), ftxt, font=get_font(10, bold=active), fill="#059669" if active else "#6B7280")
        fy += 38

    # Result list
    d.text((25, 320), "12 artisans trouvés", font=get_font(10, bold=True), fill="#374151")
    artisans = [
        ("Modou D.","Plombier","⭐4.9","Dispo","#059669"),
        ("Cheikh F.","Électricien","⭐4.7","Dispo","#059669"),
        ("Ibou N.","Menuisier","⭐4.5","Occupé","#D97706"),
    ]
    ay = 338
    for name, job, rating, status, sc in artisans:
        draw_rounded_rect(d, [18, ay, 282, ay+65], 8, fill="#F9FAFB")
        d.ellipse([28, ay+10, 56, ay+38], fill=sc)
        d.text((34, ay+16), name[0], font=get_font(11, bold=True), fill="white")
        d.text((64, ay+10), name, font=get_font(11, bold=True), fill="#374151")
        d.text((64, ay+26), job, font=get_font(9), fill="#6B7280")
        d.text((64, ay+40), rating, font=get_font(9), fill="#D97706")
        draw_rounded_rect(d, [190, ay+22, 272, ay+42], 8, fill=sc+"22")
        d.text((198, ay+26), status, font=get_font(9, bold=True), fill=sc)
        ay += 73

    # Map main area
    # Green map background
    d.rectangle([300, 65, W-10, H-10], fill="#E8F5E9")
    # Streets
    d.line([300,250,950,250], fill="#C8E6C9", width=4)
    d.line([300,380,950,380], fill="#C8E6C9", width=4)
    d.line([450,65,450,560], fill="#C8E6C9", width=4)
    d.line([650,65,650,560], fill="#C8E6C9", width=4)
    d.line([800,65,800,560], fill="#C8E6C9", width=4)
    # Mosque landmark
    draw_rounded_rect(d, [590,180,720,320], 8, fill="#A5D6A7")
    centered_text(d, 655, 230, "🕌", get_font(32), "#1B5E20")
    centered_text(d, 655, 268, "Grande Mosquée", get_font(9, bold=True), "#1B5E20")
    centered_text(d, 655, 282, "de Touba", get_font(9), "#1B5E20")

    # Artisan markers
    markers = [(390,170,"M","#059669"),(500,310,"C","#0062FF"),(730,200,"I","#D97706"),(820,400,"S","#059669"),(680,440,"O","#059669")]
    for mx, my, lbl, mc in markers:
        d.ellipse([mx-18,my-18,mx+18,my+18], fill=mc)
        d.text((mx-5, my-8), lbl, font=get_font(13, bold=True), fill="white")

    # Popup card on selected marker
    draw_rounded_rect(d, [340, 70, 530, 165], 10, fill="white")
    d.text((356, 80), "Modou Diallo", font=get_font(12, bold=True), fill="#374151")
    d.text((356, 98), "Plombier · ⭐ 4.9", font=get_font(10), fill="#6B7280")
    d.text((356, 114), "📍 300m de vous", font=get_font(10), fill="#059669")
    draw_rounded_rect(d, [356, 132, 510, 155], 8, fill="#059669")
    d.text((388, 138), "Contacter →", font=get_font(10, bold=True), fill="white")

    img.save(os.path.join(OUT, "touba-screen-3.png"), quality=95)
    print("✓ touba-screen-3.png")


# ─────────────────────────────────────────────────────────────────────────────
# TOUBA SERVICE — Screen 4: Urgence page
# ─────────────────────────────────────────────────────────────────────────────
def gen_touba_urgence():
    img = Image.new("RGB", (W, H), "#FEF2F2")
    d = ImageDraw.Draw(img)

    # Header red band
    d.rectangle([0, 0, W, 70], fill="#DC2626")
    d.text((30, 14), "🕌 Touba Service", font=get_font(14, bold=True), fill="white")
    d.text((30, 36), "⚠️ Mode Urgence — Service d'intervention rapide", font=get_font(12), fill="#FCA5A5")

    # Main urgence card
    draw_rounded_rect(d, [80, 90, W-80, H-20], 18, fill="white")
    # Red icon
    d.ellipse([W//2-45, 110, W//2+45, 200], fill="#FEE2E2")
    d.text((W//2-28, 122), "🚨", font=get_font(44), fill="#DC2626")
    centered_text(d, W//2, 213, "Besoin d'une intervention urgente ?", get_font(18, bold=True), "#0B1733")
    centered_text(d, W//2, 243, "Trouvez un artisan disponible en moins de 15 minutes", get_font(12), "#6B7280")

    # Type urgence buttons
    urgences = [("💧","Fuite d'eau","Plomberie d'urgence"),("⚡","Panne électrique","Court-circuit"),("🔒","Serrurerie","Porte bloquée"),("❄️","Clim en panne","Réparation rapide")]
    ux = 100
    for icon, title, sub in urgences:
        draw_rounded_rect(d, [ux, 280, ux+180, 380], 14, fill="#FEF2F2", outline="#DC2626", width=2)
        centered_text(d, ux+90, 300, icon, get_font(28), "#DC2626")
        centered_text(d, ux+90, 335, title, get_font(11, bold=True), "#DC2626")
        centered_text(d, ux+90, 355, sub, get_font(9), "#6B7280")
        ux += 198

    # Location
    draw_rounded_rect(d, [100, 395, W-100, 445], 10, fill="#FEF9C3", outline="#D97706", width=1)
    d.text((120, 408), "📍 Votre position actuelle : Darou Khoudoss, Touba", font=get_font(12), fill="#92400E")
    d.text((120, 426), "✅ Partage de localisation activé", font=get_font(10), fill="#059669")

    # CTA
    draw_rounded_rect(d, [200, 460, W-200, 528], 24, fill="#DC2626")
    centered_text(d, W//2, 476, "🚨  Lancer une alerte urgence maintenant", get_font(14, bold=True), "white")
    centered_text(d, W//2, 500, "Des artisans vérifiés seront notifiés immédiatement", get_font(10), "#FCA5A5")

    img.save(os.path.join(OUT, "touba-screen-4.png"), quality=95)
    print("✓ touba-screen-4.png")


# ─────────────────────────────────────────────────────────────────────────────
# UNIV SCHEDULER — Screen 1: Login dark JavaFX style
# ─────────────────────────────────────────────────────────────────────────────
def gen_scheduler_login():
    img = Image.new("RGB", (W, H), "#0F172A")
    d = ImageDraw.Draw(img)

    # Gradient background
    for i in range(H):
        ratio = i / H
        r = int(15 + 10*ratio)
        g = int(23 + 15*ratio)
        b = int(42 + 30*ratio)
        d.rectangle([0, i, W, i+1], fill=(r, g, b))

    # Decorative circles
    d.ellipse([-80, -80, 220, 220], outline="#1D68FF22", width=3)
    d.ellipse([-40, -40, 180, 180], outline="#1D68FF33", width=2)
    d.ellipse([740, 350, 1060, 670], outline="#1D68FF22", width=3)

    # Left brand panel
    # Animated gradient left side
    for i in range(460):
        ratio = i/460
        r = int(13 + 5*ratio)
        g = int(20 + 8*ratio)
        b = int(40 + 20*ratio)
        d.rectangle([0, 0+i, 420, 1+i], fill=(r,g,b))

    # University logo
    d.ellipse([170, 60, 250, 140], fill="#1D68FF")
    d.ellipse([180, 70, 240, 130], fill="#0B1733")
    d.text((192, 82), "🎓", font=get_font(30), fill="#1D68FF")
    centered_text(d, 210, 150, "UCAD", get_font(18, bold=True), "white")
    centered_text(d, 210, 174, "Université Cheikh Anta Diop", get_font(10), "#64748B")

    # App name
    centered_text(d, 210, 215, "UNIV SCHEDULER", get_font(20, bold=True), "#1D68FF")
    centered_text(d, 210, 244, "Planification intelligente", get_font(13), "#94A3B8")
    centered_text(d, 210, 262, "des emplois du temps", get_font(13), "#94A3B8")

    # Features
    feats = ["🗓️  Gestion des créneaux horaires", "🏛️  Affectation des salles", "👨‍🏫  Suivi enseignants", "⚠️  Détection des conflits", "📄  Export PDF / Excel"]
    fy = 300
    for feat in feats:
        d.text((60, fy), feat, font=get_font(11), fill="#94A3B8")
        fy += 30

    # Login card
    draw_rounded_rect(d, [460, 50, 920, H-50], 16, fill="#1E293B")
    draw_rounded_rect(d, [460, 50, 920, H-50], 16, outline="#334155", width=1)

    d.text((506, 80), "Connexion au système", font=get_font(18, bold=True), fill="white")
    d.text((506, 108), "Entrez vos identifiants pour continuer", font=get_font(11), fill="#64748B")

    # Role selector
    d.text((506, 145), "Votre rôle", font=get_font(11, bold=True), fill="#94A3B8")
    roles2 = [("🛡️","Administrateur",True),("👨‍🏫","Enseignant",False),("👨‍🎓","Étudiant",False),("📋","Gestionnaire",False)]
    rx = 506
    for icon, role, active in roles2:
        rw = 85
        draw_rounded_rect(d, [rx, 164, rx+rw, 196], 8, fill="#1D68FF" if active else "#0F172A")
        draw_rounded_rect(d, [rx, 164, rx+rw, 196], 8, outline="#1D68FF" if active else "#334155", width=1)
        d.text((rx+6, 171), f"{icon} {role[:5]}", font=get_font(9, bold=active), fill="white" if active else "#64748B")
        rx += 93

    # Input fields
    d.text((506, 212), "Identifiant", font=get_font(11, bold=True), fill="#94A3B8")
    draw_rounded_rect(d, [506, 230, 894, 268], 8, fill="#0F172A", outline="#334155", width=1)
    d.text((522, 242), "👤  admin@ucad.sn", font=get_font(12), fill="#E2E8F0")

    d.text((506, 282), "Mot de passe", font=get_font(11, bold=True), fill="#94A3B8")
    draw_rounded_rect(d, [506, 300, 894, 338], 8, fill="#0F172A", outline="#1D68FF", width=1)
    d.text((522, 312), "🔒  ••••••••••••", font=get_font(12), fill="#E2E8F0")
    d.text((858, 316), "👁", font=get_font(14), fill="#64748B")

    # Forgot password
    d.text((700, 350), "Mot de passe oublié ?", font=get_font(10), fill="#1D68FF")

    # Login button
    for i in range(50):
        ratio = i/50
        r = int(29 + (13-29)*ratio)
        g = int(104 + (104-104)*ratio)
        b = int(255 + (200-255)*ratio)
        d.rectangle([506, 375+i, 894, 376+i], fill=(r,g,b))
    draw_rounded_rect(d, [506, 375, 894, 425], 10, outline="#1D68FF", width=0)
    # Redo as solid
    draw_rounded_rect(d, [506, 375, 894, 425], 10, fill="#1D68FF")
    centered_text(d, 700, 390, "Se connecter →", get_font(14, bold=True), "white")

    # Version info
    centered_text(d, 700, 445, "UNIV-SCHEDULER v2.4.1  |  Java 17 + JavaFX", get_font(9), "#334155")
    centered_text(d, 700, 462, "© 2024 MameFaty Kaire — UFR Sciences et Technologies", get_font(9), "#334155")

    img.save(os.path.join(OUT, "scheduler-screen-1.png"), quality=95)
    print("✓ scheduler-screen-1.png")


# ─────────────────────────────────────────────────────────────────────────────
# UNIV SCHEDULER — Screen 2: Main timetable grid
# ─────────────────────────────────────────────────────────────────────────────
def gen_scheduler_grid():
    img = Image.new("RGB", (W, H), "#0F172A")
    d = ImageDraw.Draw(img)

    # Sidebar
    d.rectangle([0, 0, 190, H], fill="#1E293B")
    d.rectangle([189, 0, 191, H], fill="#334155")
    d.text((16, 16), "🎓 UNIV SCHED", font=get_font(13, bold=True), fill="#1D68FF")
    menu2 = [("📅","Emploi du temps",True),("🏛️","Salles",False),("⚠️","Conflits",False),("👨‍🏫","Enseignants",False),("📄","Export",False),("⚙️","Paramètres",False)]
    my = 55
    for icon2, label2, active2 in menu2:
        if active2:
            d.rectangle([0, my-4, 190, my+32], fill="#1D68FF")
        d.text((12, my), icon2, font=get_font(14), fill="white")
        d.text((38, my+2), label2, font=get_font(10, bold=active2), fill="white" if active2 else "#64748B")
        my += 44

    # Main area
    d.rectangle([191, 0, W, 50], fill="#1E293B")
    d.text((208, 12), "Emploi du temps — Semaine 11", font=get_font(14, bold=True), fill="white")
    d.text((208, 32), "L3 Informatique — UFR Sciences et Technologies", font=get_font(10), fill="#64748B")
    # Week nav
    draw_rounded_rect(d, [740, 10, 790, 40], 8, fill="#334155")
    d.text((754, 18), "‹ Préc", font=get_font(10), fill="#94A3B8")
    draw_rounded_rect(d, [795, 10, 850, 40], 8, fill="#1D68FF")
    d.text((808, 18), "Suiv ›", font=get_font(10, bold=True), fill="white")

    # Day headers
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    dx = 258
    for day in days:
        d.rectangle([dx, 50, dx+118, 78], fill="#0F172A")
        centered_text(d, dx+59, 57, day, get_font(10, bold=True), "#94A3B8")
        dx += 120

    # Time slots (left column)
    times = ["08h00","09h30","11h00","12h30","14h00","15h30","17h00","18h30"]
    ty = 78
    slot_h = 58
    for t in times:
        d.rectangle([191, ty, 258, ty+slot_h], fill="#1E293B")
        d.text((201, ty+20), t, font=get_font(9), fill="#64748B")
        d.line([191, ty+slot_h, W, ty+slot_h], fill="#334155", width=1)
        ty += slot_h

    # Course blocks
    # Format: (day_idx, slot_idx, duration_slots, name, teacher, room, color, text_color)
    courses = [
        (0, 0, 2, "Algo & Structures", "Pr. Diallo", "A204", "#1D68FF", "#DBEAFE"),
        (0, 3, 1, "Mathématiques", "Pr. Ndiaye", "B102", "#7C3AED", "#EDE9FE"),
        (0, 5, 2, "Bases de données", "Mme Sarr", "Labo", "#059669", "#D1FAE5"),
        (1, 0, 1, "Systèmes", "M. Fall", "A106", "#1D68FF", "#DBEAFE"),
        (1, 2, 2, "Réseaux", "Pr. Mbaye", "B304", "#0891B2", "#E0F2FE"),
        (1, 5, 1, "Anglais", "Mme Diop", "C201", "#D97706", "#FEF3C7"),
        (2, 1, 2, "POO Java", "Pr. Diallo", "Labo", "#059669", "#D1FAE5"),
        (2, 4, 1, "Complexité", "M. Sow", "A204", "#7C3AED", "#EDE9FE"),
        (3, 0, 3, "Projet Informatique", "Encadrants", "P102", "#DC2626", "#FEE2E2"),
        (3, 5, 2, "Compilation", "Pr. Toure", "A106", "#1D68FF", "#DBEAFE"),
        (4, 1, 1, "Probabilités", "Mme Faye", "B102", "#D97706", "#FEF3C7"),
        (4, 3, 2, "IA & ML", "Pr. Kane", "Labo", "#059669", "#D1FAE5"),
        (5, 0, 2, "TD Algo", "M. Diallo", "A204", "#0891B2", "#E0F2FE"),
    ]
    for day_i, slot_i, dur, name, teacher, room, color, text_col in courses:
        cx2 = 258 + day_i*120
        cy2 = 78 + slot_i*slot_h
        ch = dur*slot_h - 4
        draw_rounded_rect(d, [cx2+2, cy2+2, cx2+117, cy2+ch], 6, fill=color)
        # Course name
        d.text((cx2+6, cy2+6), name[:16], font=get_font(8, bold=True), fill=text_col)
        if dur > 1:
            d.text((cx2+6, cy2+20), teacher, font=get_font(7), fill=text_col+"CC")
            d.text((cx2+6, cy2+32), f"🏛 {room}", font=get_font(7), fill=text_col+"AA")

    img.save(os.path.join(OUT, "scheduler-screen-2.png"), quality=95)
    print("✓ scheduler-screen-2.png")


# ─────────────────────────────────────────────────────────────────────────────
# UNIV SCHEDULER — Screen 3: Dashboard admin
# ─────────────────────────────────────────────────────────────────────────────
def gen_scheduler_dashboard():
    img = Image.new("RGB", (W, H), "#0F172A")
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 190, H], fill="#1E293B")
    d.text((16, 16), "🎓 UNIV SCHED", font=get_font(13, bold=True), fill="#1D68FF")
    menu3 = [("📅","Emploi du temps",False),("🏠","Dashboard",True),("⚠️","Conflits",False),("👨‍🏫","Enseignants",False),("📄","Export",False)]
    my = 55
    for icon3, lbl3, active3 in menu3:
        if active3:
            d.rectangle([0, my-4, 190, my+32], fill="#1D68FF")
        d.text((12, my), icon3, font=get_font(14), fill="white")
        d.text((38, my+2), lbl3, font=get_font(10, bold=active3), fill="white" if active3 else "#64748B")
        my += 44

    d.rectangle([191, 0, W, 50], fill="#1E293B")
    d.text((208, 12), "Tableau de bord Administrateur", font=get_font(14, bold=True), fill="white")
    d.text((208, 32), "Vue d'ensemble — Semestre 2 · 2023-2024", font=get_font(10), fill="#64748B")

    # KPI cards
    kpis2 = [("94","Cours planifiés","📅","#1D68FF"),("28","Salles gérées","🏛️","#059669"),("67","Enseignants","👨‍🏫","#7C3AED"),("5","Conflits","⚠️","#DC2626")]
    kx = 205
    for val2, lbl4, icon4, col2 in kpis2:
        draw_rounded_rect(d, [kx, 60, kx+172, 140], 10, fill="#1E293B")
        draw_rounded_rect(d, [kx, 60, kx+172, 140], 10, outline=col2, width=1)
        d.text((kx+12, 72), icon4, font=get_font(22), fill=col2)
        d.text((kx+12, 100), val2, font=get_font(26, bold=True), fill=col2)
        d.text((kx+12, 128), lbl4, font=get_font(9), fill="#64748B")
        kx += 184

    # Room occupation bars
    d.text((208, 155), "Occupation des salles", font=get_font(12, bold=True), fill="#94A3B8")
    rooms_occ = [("Amphi 500",82,"#1D68FF"),("Labo Info",95,"#DC2626"),("Salle A204",65,"#059669"),("Salle B102",48,"#D97706"),("Salle C301",71,"#7C3AED"),("Amphi 200",88,"#1D68FF")]
    ry3 = 178
    for rm, pct, col3 in rooms_occ:
        d.text((208, ry3), rm, font=get_font(9), fill="#94A3B8")
        d.text((340, ry3), f"{pct}%", font=get_font(9, bold=True), fill=col3)
        # Bar bg
        d.rectangle([380, ry3+2, 740, ry3+14], fill="#334155")
        # Bar fill
        bar_w = int(360 * pct / 100)
        d.rectangle([380, ry3+2, 380+bar_w, ry3+14], fill=col3)
        ry3 += 28

    # Conflicts panel
    draw_rounded_rect(d, [755, 148, 940, H-20], 10, fill="#1E293B")
    draw_rounded_rect(d, [755, 148, 940, H-20], 10, outline="#DC2626", width=1)
    d.text((768, 158), "⚠️ Conflits détectés", font=get_font(10, bold=True), fill="#DC2626")
    conflicts = [("Mardi 11h","Salle A204 — double réservation"),("Jeudi 14h","Pr. Diallo — 2 cours simultanés"),("Vendredi","Labo complet — surbooking")]
    cy3 = 178
    for ctime, cdesc in conflicts:
        draw_rounded_rect(d, [762, cy3, 932, cy3+52], 6, fill="#FEE2E2"+"22")
        d.text((770, cy3+5), ctime, font=get_font(8, bold=True), fill="#DC2626")
        d.text((770, cy3+20), cdesc[:30], font=get_font(8), fill="#94A3B8")
        draw_rounded_rect(d, [770, cy3+36, 870, cy3+50], 6, fill="#DC262633")
        d.text((780, cy3+39), "Résoudre →", font=get_font(8), fill="#DC2626")
        cy3 += 60

    # Recent activity
    d.text((208, 365), "Activité récente", font=get_font(12, bold=True), fill="#94A3B8")
    activities = [("✅","Cours 'BDD L3' planifié — Salle A204","il y a 5 min"),("📝","Emploi du temps M2 mis à jour","il y a 22 min"),("⚠️","Conflit détecté — Mardi 11h","il y a 1h"),("📄","Export PDF généré — L2 Info","il y a 2h")]
    ay3 = 388
    for icon5, act, when in activities:
        d.text((208, ay3), icon5, font=get_font(14), fill="#94A3B8")
        d.text((232, ay3+1), act, font=get_font(9), fill="#E2E8F0")
        d.text((232, ay3+16), when, font=get_font(8), fill="#64748B")
        ay3 += 38

    img.save(os.path.join(OUT, "scheduler-screen-3.png"), quality=95)
    print("✓ scheduler-screen-3.png")


# ─────────────────────────────────────────────────────────────────────────────
# UNIV SCHEDULER — Screen 4: Conflict resolution
# ─────────────────────────────────────────────────────────────────────────────
def gen_scheduler_conflicts():
    img = Image.new("RGB", (W, H), "#0F172A")
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 190, H], fill="#1E293B")
    d.text((16, 16), "🎓 UNIV SCHED", font=get_font(13, bold=True), fill="#1D68FF")
    menu4 = [("📅","Emploi du temps",False),("🏠","Dashboard",False),("⚠️","Conflits",True),("👨‍🏫","Enseignants",False),("📄","Export",False)]
    my = 55
    for icon6, lbl5, active4 in menu4:
        if active4:
            d.rectangle([0, my-4, 190, my+32], fill="#DC2626")
        d.text((12, my), icon6, font=get_font(14), fill="white")
        d.text((38, my+2), lbl5, font=get_font(10, bold=active4), fill="white" if active4 else "#64748B")
        my += 44

    d.rectangle([191, 0, W, 50], fill="#1E293B")
    d.text((208, 12), "⚠️ Détection & Résolution des conflits", font=get_font(14, bold=True), fill="#DC2626")
    d.text((208, 32), "5 conflits détectés — 2 résolus · 3 en attente", font=get_font(10), fill="#64748B")

    conflicts2 = [
        ("🔴","Critique","Mardi 11h00","Salle A204","BDD L3 (Mme Sarr) & Réseaux M2 (Pr. Mbaye)","Double réservation de salle","#DC2626","#FEE2E2"),
        ("🟠","Modéré","Jeudi 14h00","Pr. Diallo","Algo L3 & Systèmes L2","Enseignant affecté à 2 cours simultanés","#D97706","#FEF3C7"),
        ("🟡","Faible","Vendredi 08h","Labo Info","TD BDD + TP Systèmes","Capacité dépassée (35 > 30 places)","#EAB308","#FEF9C3"),
    ]
    cy4 = 60
    for emoji, severity, timing, resource, desc, reason, col4, bg4 in conflicts2:
        draw_rounded_rect(d, [205, cy4, 940, cy4+118], 10, fill="#1E293B")
        draw_rounded_rect(d, [205, cy4, 940, cy4+118], 10, outline=col4, width=1)
        # Left severity bar
        d.rectangle([205, cy4, 212, cy4+118], fill=col4)
        # Header
        d.text((222, cy4+10), emoji, font=get_font(16), fill=col4)
        d.text((248, cy4+12), f"Conflit {severity}", font=get_font(12, bold=True), fill=col4)
        d.text((680, cy4+12), timing, font=get_font(11, bold=True), fill="#94A3B8")
        # Resource
        d.text((222, cy4+36), f"📍 {resource}", font=get_font(10), fill="#E2E8F0")
        d.text((222, cy4+54), desc, font=get_font(10), fill="#94A3B8")
        d.text((222, cy4+72), f"Cause : {reason}", font=get_font(9), fill="#64748B")
        # Action buttons
        draw_rounded_rect(d, [222, cy4+90, 390, cy4+112], 6, fill=col4)
        d.text((240, cy4+96), "Résoudre automatiquement", font=get_font(9, bold=True), fill="white")
        draw_rounded_rect(d, [400, cy4+90, 540, cy4+112], 6, fill="#334155")
        d.text((415, cy4+96), "Résoudre manuellement", font=get_font(9), fill="#94A3B8")
        draw_rounded_rect(d, [550, cy4+90, 660, cy4+112], 6, fill="#334155")
        d.text((565, cy4+96), "Ignorer", font=get_font(9), fill="#94A3B8")
        cy4 += 128

    # Resolved conflicts
    d.text((208, cy4+5), "✅ Conflits résolus", font=get_font(10, bold=True), fill="#059669")
    for txt in ["Lundi 09h30 — Salle B102 réaffectée automatiquement", "Mercredi 11h — Créneau décalé de 30 minutes"]:
        draw_rounded_rect(d, [205, cy4+25, 940, cy4+50], 6, fill="#ECFDF5"+"11")
        d.text((220, cy4+31), f"✅  {txt}", font=get_font(9), fill="#059669")
        cy4 += 30

    img.save(os.path.join(OUT, "scheduler-screen-4.png"), quality=95)
    print("✓ scheduler-screen-4.png")


if __name__ == "__main__":
    print("Generating attractive landing/home screens...")
    gen_locaux_login()
    gen_locaux_dashboard()
    gen_locaux_form()
    gen_locaux_commission()
    gen_touba_landing()
    gen_touba_artisan()
    gen_touba_map()
    gen_touba_urgence()
    gen_scheduler_login()
    gen_scheduler_grid()
    gen_scheduler_dashboard()
    gen_scheduler_conflicts()
    print("\nAll screens generated successfully!")
