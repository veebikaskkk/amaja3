import json, os, io

import pathlib
OUT = str(pathlib.Path(__file__).parent / "public")
DOM = "https://amaja.ee"

ETTEVOTE = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": DOM + "/#ettevote",
  "name": "A-MAJA OÜ",
  "description": "Arhitektuurialane ettevõte, mis projekteerib üksikelamuid, juurdeehitusi, aiamaju ja suuremaid objekte.",
  "url": DOM + "/",
  "telephone": "+37253874959",
  "email": "info@a-maja.com",
  "vatID": "EE102766103",
  "logo": DOM + "/pildid/a-maja-logo-tume.png",
  "image": DOM + "/pildid/eramu-tume-puitfassaad-01.webp",
  "address": {"@type": "PostalAddress", "streetAddress": "Sõle tn 27d-31",
              "addressLocality": "Tallinn", "addressRegion": "Harjumaa",
              "addressCountry": "EE"},
  "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
    ["Harjumaa","Hiiumaa","Ida-Virumaa","Järvamaa","Jõgevamaa","Lääne-Virumaa","Läänemaa",
     "Pärnumaa","Põlvamaa","Raplamaa","Saaremaa","Tartumaa","Valgamaa","Viljandimaa","Võrumaa"]],
  "founder": {"@type": "Person", "name": "Kaspar Lätt", "jobTitle": "Arhitekt, tase 7"},
  "employee": {"@type": "Person", "name": "Kaspar Lätt", "jobTitle": "Diplomeeritud arhitekt, tase 7",
               "hasCredential": {"@type": "EducationalOccupationalCredential",
                                 "credentialCategory": "Kutsetunnistus",
                                 "identifier": "203786",
                                 "name": "Diplomeeritud arhitekt, tase 7"}},
  "knowsAbout": ["arhitektuurne projekteerimine","ehitusprojekt","ehitusteatis","ehitusluba","eelprojekt","põhiprojekt"]
}

TEENUSED = [
  ("uksikelamu", "Üksikelamu projekt"),
  ("rekonstrueerimine", "Juurdeehituse ja rekonstrueerimise projekt"),
  ("abihoone", "Abihoone ja aiamaja projekt"),
  ("arihoone", "Ärihoone ja suurema objekti projekt"),
  ("ehitusteatis", "Eelprojekt ehitusteatise mahus"),
  ("asjaajamine", "Asjaajamine omavalitsusega"),
]

def teenus_ld():
    return {"@context":"https://schema.org","@type":"ItemList","itemListElement":[
      {"@type":"Service","position":i+1,"name":nimi,"serviceType":"Arhitektuurne projekteerimine",
       "provider":{"@id":DOM+"/#ettevote"},"areaServed":{"@type":"Country","name":"Eesti"},
       "url":DOM+"/teenused.html#"+ank,
       "offers":{"@type":"Offer","availability":"https://schema.org/InStock","priceCurrency":"EUR"}}
      for i,(ank,nimi) in enumerate(TEENUSED)]}

def puru_ld(nimi, tee):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Avaleht","item":DOM+"/"},
      {"@type":"ListItem","position":2,"name":nimi,"item":DOM+tee}]}

def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2)

MENUU = [("/tood.html","Portfoolio"),("/teenused.html","Teenused"),
         ("/meist.html","Meist"),("/tagasiside.html","Tagasiside")]

def pais(akt):
    li = []
    for tee, nimi in MENUU + [("/kontakt.html", "Kontakt")]:
        cur = ' aria-current="page"' if tee == akt else ""
        li.append(f'          <li><a href="{tee}"{cur}>{nimi}</a></li>')
    return f'''<a class="hyppa-sisule" href="#sisu">Hüppa sisu juurde</a>

<header class="pais">
  <div class="pais-sisu">
    <a class="logo" href="/" aria-label="A-MAJA OÜ avaleht">
      <img src="/pildid/a-maja-logo-hele.svg" alt="A-MAJA OÜ logo" width="2424" height="1256">
    </a>
    <button class="menuu-nupp" type="button" aria-expanded="false" aria-controls="peamenuu">
      <span class="menuu-nupp-tekst">Menüü</span>
      <span class="menuu-nupp-triibud" aria-hidden="true"><span></span><span></span></span>
    </button>
  </div>
</header>

<nav id="peamenuu" class="menuu" aria-label="Peamenüü" hidden>
  <div class="menuu-sisu">
    <div class="menuu-veerg">
      <p class="silt">Menüü</p>
      <ul>
{chr(10).join(li)}
      </ul>
    </div>
    <div class="menuu-kontakt">
      <p class="silt">Kiire hinnapäring</p>

      <form class="menuu-vorm" id="menuu-vorm" data-paring novalidate>
        <p class="vormi-teade" id="menuu-vormi-teade" role="alert" aria-live="polite" hidden></p>

        <div class="vali">
          <label for="menuu-nimi">Nimi</label>
          <input type="text" id="menuu-nimi" name="nimi" autocomplete="name" required>
        </div>
        <div class="vali">
          <label for="menuu-epost">E-post</label>
          <input type="email" id="menuu-epost" name="epost" autocomplete="email" required>
        </div>
        <div class="vali">
          <label for="menuu-sonum">Mida plaanite?</label>
          <textarea id="menuu-sonum" name="sonum" rows="3" required></textarea>
        </div>

        <div class="nousolek">
          <input type="checkbox" id="menuu-nousolek" name="nousolek" required>
          <label for="menuu-nousolek">Nõustun andmete töötlemisega. <a href="/privaatsus.html">Privaatsus</a></label>
        </div>

        <div class="meepott" aria-hidden="true">
          <label for="menuu-veebiaadress">Jätke see väli tühjaks</label>
          <input type="text" id="menuu-veebiaadress" name="veebiaadress" tabindex="-1" autocomplete="off">
        </div>

        <button type="submit" class="nupp" data-saada>Saada päring</button>
      </form>

      <p class="menuu-kontakt-rida">
        <a href="tel:+37253874959">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com">info@a-maja.com</a>
      </p>
    </div>
  </div>
</nav>'''

JALUS = '''<footer class="jalus">
  <div class="raam jalus-ruudustik">
    <div class="jalus-plokk">
      <img src="/pildid/a-maja-logo-hele.svg" alt="A-MAJA OÜ logo" width="2424" height="1256" loading="lazy">
      <p>Arhitektuurialane ettevõte. Projekteerime üksikelamuid, juurdeehitusi ja abihooneid, kuid ka suuremaid objekte.</p>
    </div>
    <div class="jalus-plokk">
      <h2 class="jalus-pealkiri">Kontakt</h2>
      <p><a href="tel:+37253874959">+372 5387 4959</a></p>
      <p><a href="mailto:info@a-maja.com">info@a-maja.com</a></p>
      <p>Kaspar Lätt, juhatuse liige</p>
    </div>
    <div class="jalus-plokk">
      <h2 class="jalus-pealkiri">Lehed</h2>
      <ul>
        <li><a href="/teenused.html">Teenused</a></li>
        <li><a href="/tood.html">Tehtud tööd</a></li>
        <li><a href="/tagasiside.html">Tagasiside</a></li>
        <li><a href="/kontakt.html">Kontakt</a></li>
        <li><a href="/privaatsus.html">Privaatsus</a></li>
      </ul>
    </div>
    <div class="jalus-plokk">
      <h2 class="jalus-pealkiri">Ettevõte</h2>
      <p>A-MAJA OÜ, osaühing</p>
      <p>Registrikood 16765213</p>
      <p>KMKR EE102766103</p>
      <address>Sõle tn 27d-31, Põhja-Tallinna linnaosa, Tallinn</address>
      <p>Tegevuspiirkond: kogu Eesti</p>
    </div>
  </div>
  <div class="raam jalus-alumine">
    <p>© <span id="aasta">2026</span> A-MAJA OÜ</p>
  </div>
</footer>'''

def leht(fail, title, desc, tee, sisu, ldid=(), akt="", noindex=False):
    ld = "\n".join(f'<script type="application/ld+json">\n{j(o)}\n</script>' for o in ldid)
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ''
    html = f'''<!DOCTYPE html>
<html lang="et">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{DOM}{tee}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="A-MAJA OÜ">
<meta property="og:locale" content="et_EE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOM}{tee}">
<meta property="og:image" content="{DOM}/jagamispilt.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A-MAJA OÜ, arhitektuurne projekteerimine üle Eesti">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#241A14">

<link rel="preload" href="/fondid/ibm-plex-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/stiil.css">
{ld}
</head>
<body>

{pais(akt)}

<main id="sisu">
{sisu}
</main>

{JALUS}

<script src="/skript.js" defer></script>
</body>
</html>
'''
    with io.open(os.path.join(OUT, fail), "w", encoding="utf-8") as f:
        f.write(html)
    return html


def puru(nimi):
    return f'''  <nav class="leivapuru" aria-label="Leivapuru">
    <div class="raam">
      <ol>
        <li><a href="/">Avaleht</a></li>
        <li>{nimi}</li>
      </ol>
    </div>
  </nav>
'''

def kohatäide(fail, alt, klass=""):
    k = (" " + klass) if klass else ""
    return (f'<div class="kohatäide{k}" role="img" aria-label="Kohatäide. {alt}">'
            f'<span>{fail}</span></div>')

# ---------------------------------------------------------------- AVALEHT

PORTFOOLIO = [
 ("/pildid/eramu-must-vertikaalne-puitlaudis-metsas.webp",1600,893,
  "Musta vertikaalse puitlaudisega üksikelamu järsu viilkatuse ja suure kaldakna all oleva elutoaga männimetsas.",
  "Metsamaja","Üksikelamu"),
 ("/pildid/eramu-tume-puitlaudis-viilkatus-mannimetsas.webp",1200,1474,
  "Tumeda vertikaalse puitlaudisega kahekorruseline elamu männimetsas, avatud terrass ja kõrged aknad viilus.",
  "Metsaelamu terrassiga","Üksikelamu"),
 ("/pildid/eramu-terrakota-plekkfassaad-viilkatus.webp",1600,893,
  "Terrakotapunase plekkfassaadi ja sama tooni katusega ühekorruseline elamu, kaks viilu ja tagasiastuv sissepääs.",
  "Terrakotamaja","Üksikelamu"),
 ("/pildid/eramu-lamekatus-kivifassaad-varjualune.webp",1600,1204,
  "Lamekatusega üksikelamu heleda kivifassaadi, tumeda karniisi ja avatud autovarjualusega tänava ääres.",
  "Kivifassaadiga elamu","Üksikelamu"),
 ("/pildid/eramu-kahekorruseline-lamekatus-krohv-puit.webp",1600,1122,
  "Kahekorruseline lamekatusega elamu heleda krohvfassaadi ja puitlaudisega aktsentribadega männimetsas.",
  "Krohvfassaadiga elamu","Üksikelamu"),
 ("/pildid/eramu-punane-laudis-valge-piirdelaud.webp",1600,893,
  "Punase püstlaudise ja valgete piirdelaudadega elamu musta valtsplekk-katuse ja telliskorstnaga maastikus.",
  "Punane talumaja","Üksikelamu"),
 ("/pildid/eramu-kelpkatus-garaaz-maakivi.webp",1600,733,
  "Ühekorruseline kelpkatusega elamu valge krohvfassaadi, maakiviga sissepääsu ja kahe auto garaažiga.",
  "Kelpkatusega elamu","Üksikelamu"),
 ("/pildid/suvekohvik-raatuse-tanav-tartu-projekt.webp",1200,655,
  "Suvekohviku hoone Raatuse tänaval Tartus, tumeda puitlaudisega paviljon ja haljastatud katuseterrass pargis.",
  "Suvekohvik Raatuse tänaval","Ärihoone"),
 ("/pildid/korterelamu-visualiseering-03.webp",1200,1275,
  "Tumeroheliseks värvitud puidust korterelamu tänavavaade, prantsuse rõdud ja puitaknad.",
  "Üksikelamu ümberehitus ja laiendus","Ümberehitus"),
 ("/pildid/eramu-juurdeehitus-puitribifassaadiga.webp",1600,1200,
  "Olemasoleva krohvitud eramu tänavavaade koos uue puitribifassaadiga juurdeehitusega.",
  "Üksikelamu juurdeehitus","Juurdeehitus"),
 ("/pildid/eramu-punane-puitfassaad-varjualusega.webp",1200,807,
  "Punase vertikaalse puitlaudisega üksikelamu järsu viilkatuse ja räästa alla viidud autovarjualusega.",
  "Elamu varjualusega","Üksikelamu"),
 ("/pildid/eramu-tume-puitfassaad-paikesepaneelidega.webp",1200,559,
  "Kahekorruseline tumeda puitlaudisega elamu kelpkatuse ja katusele paigaldatud päikesepaneelidega.",
  "Kortermaja","Kortermaja"),
 ("/pildid/eramu-puitfassaad-metsas-02.webp",1200,559,
  "Halliks patineerunud vertikaalse puitlaudisega elamu männimetsa serval, otsaseinas heledast tellisest maht.",
  "Elamu metsa serval","Üksikelamu"),
 ("/pildid/eramu-must-laudis-katusealune-terrass.webp",1536,1024,
  "Valminud musta püstlaudisega ühekorruseline elamu kahe viiluga, puitpostidel katusealune terrass, laudterrass ja kümblustünn.",
  "Valminud must elamu","Üksikelamu"),
 ("/pildid/eramu-roheline-puitfassaad-aiaga.webp",1400,631,
  "Valminud heleroheline püstlaudisega ühekorruseline elamu aias, must plekk-katus, viilu all kolmnurkne aken ning ees lillepeenrad ja kased.",
  "Valminud juurdeehitus","Juurdeehitus"),
 ("/pildid/eramu-tume-laudis-kelpkatus-talvel.webp",1800,1013,
  "Valminud ühekorruseline kelpkatusega elamu talvel, tumeda ja pruuni püstlaudise vaheldumine ning fassaadi valgustus õhtuhämaruses.",
  "Valminud elamu talvel","Üksikelamu"),
 ("/pildid/eramu-tume-puitfassaad-01.webp",1800,764,
  "Sinakashalli püstlaudise ja valtsplekk-katusega üksikelamu metsaserval, kõrge klaasitud viil ja munakivitee.",
  "Üksikelamu viilkatusega","Üksikelamu"),
]


# Projektijoonised, mis avanevad valgusti korvalpaneelis, kui tellija
# klopsab portfoolio pildil. Eraldi joonistegaleriid lehel ei ole, seega
# nahtavale jouavad ainult need joonised, millele SEOSED viitab.
# Kirje kuju: (fail, laius, korgus, pealkiri, kirjeldus, alt).
PROJEKTI_JOONISED = [
 ("juurdeehituse-puitribifassaad-lahivaade.webp",1300,1625,
  "Juurdeehitus, fassaad lähivaates",
  "Puitribid varjavad trepimahtu, aga lasevad valguse läbi.",
  "Juurdeehituse puitribifassaadi lähivaade, mille taga paistab läbi ribide kahekorruseline trepp ja soklikorruse aknad."),
 ("musta-laudisega-elamu-otsavaade.webp",1800,873,
  "Valminud must elamu, vaade otsast",
  "Kaks viilu kõrvuti, vahel hallikas laudisega osa.",
  "Valminud musta püstlaudisega elamu kahe viilkatusega mahuga, mille vahel on hallika laudisega osa, taustal kuusemets."),
 ("musta-laudisega-elamu-kulgvaade.webp",1800,912,
  "Valminud must elamu, vaade küljelt",
  "Pikk maht ja kõrgemate akendega elutoa ots.",
  "Valminud musta püstlaudisega elamu külgvaade, pikk maht väikeste akendega ja teises otsas kõrged klaasuksed, ümber veel korrastamata krunt."),
 ("musta-laudisega-elamu-korruse-plaan-joonis.webp",1400,1529,
  "Valminud must elamu, korruse plaan",
  "Elu- ja söögituba 40,33 m², kolm magamistuba, kaetud terrass 24,63 m².",
  "Ühekorruselise elamu korruse plaani joonis mõõtkavas 1:50, kus on elu- ja söögituba 40,33 m², kolm magamistuba, vannituba 10,03 m², kontor ning kaetud terrass 24,63 m²."),
 ("musta-laudisega-elamu-loige-joonis.webp",1800,629,
  "Valminud must elamu, lõige A-A",
  "Kaks viilkatusega mahtu ja nende vahel kaetud terrass.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud kaks viilkatusega mahtu, ruumide kõrgused ja nende vahele jääv kaetud terrass."),
 ("roheline-elamu-korruse-plaan-joonis.webp",1800,1107,
  "Valminud juurdeehitus, korruse plaan",
  "Elu- ja söögituba 39,86 m², köök 12,73 m², magamistuba 23,66 m².",
  "Juurdeehitusega elamu korruse plaani joonis mõõtkavas 1:50, kus lilla punktiirjoon märgib juurdeehitust ning ruumide hulgas on elu- ja söögituba 39,86 m², köök, saun ja kaks vannituba."),
 ("roheline-elamu-vaated-joonis.webp",1800,1163,
  "Valminud juurdeehitus, vaated",
  "Heleroheline laudis ja must plekk-katus, mis sobivad olemasolevaga.",
  "Elamu eest- ja külgvaate joonis mõõtkavas 1:50, kus fassaadil on heleroheline laudis, valged aknapiirded ja must plekk-katus ning lilla punktiirjoon märgib juurdeehitust."),
 ("roheline-elamu-loige-joonis.webp",1800,599,
  "Valminud juurdeehitus, lõige A-A",
  "Juurdeehituse viilkatus ja liitumine olemasoleva hoonega.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud juurdeehituse viilkatuse kalle, ruumide kõrgused ja liitumine olemasoleva hoonega."),

 ("suvekohvik-raatuse-tanav-vaade-eest-joonis.webp",897,290,"Suvekohvik, vaade eest","Raatuse tänav, Tartu. Mõõtkava 1:50.","Suvekohviku hoone eestvaate joonis mõõtkavas 1:50, tähistatud puitlaudis, roostevaba piire ja katuseterrassi haljastus."),
 ("suvekohvik-esimese-korruse-plaan-joonis.webp",898,420,"Suvekohvik, korruse plaan","Restoran 23,35 m², baar, köök ja tehnoruum.","Suvekohviku esimese korruse plaani joonis mõõtkavas 1:50, restoranisaal, baar, köök ja tehnoruum."),

 ("umberehitatud-elamu-soklikorruse-ja-esimese-korruse-plaan-joonis.webp",1800,882,
  "Ümberehitus, soklikorrus ja esimene korrus",
  "Garaaž 16 m², köök ja söögituba 24 m², elutuba 24,9 m².",
  "Ümberehitatava elamu soklikorruse ja esimese korruse plaanide joonis mõõtkavas 1:50, kus punasega on märgitud lammutatavad ja rohelisega juurde projekteeritavad osad."),
 ("umberehitatud-elamu-teise-korruse-ja-katuse-plaan-joonis.webp",1800,884,
  "Ümberehitus, teine korrus ja katus",
  "Kaks magamistuba 12 ja 11,1 m², koridor 12 m².",
  "Elamu teise korruse plaani ja katuse plaani joonis mõõtkavas 1:50 koos ruumide pindalade, katuseakende ja korstnaga."),
 ("umberehitatud-elamu-loiked-joonis.webp",1800,662,
  "Ümberehitus, lõiked A-A ja B-B",
  "Kaks lõiget koos fassaadi ja rõdu lahendusega.",
  "Elamu lõigete A-A ja B-B joonis mõõtkavas 1:50, kus on näidatud korruste kõrgused, rõdu, garaaž ja tumeroheline puitlaudisfassaad."),

 ("juurdeehitus-vundamendi-plaan-joonis.webp",1800,1659,
  "Juurdeehitus, vundamendi plaan",
  "Tööruum 33,90 m² olemasoleva maja kõrval.",
  "Juurdeehituse vundamendi plaani joonis mõõtkavas 1:50, kus punane punktiirjoon eraldab uue tööruumi 33,90 m² olemasolevast hoonest."),
 ("juurdeehitus-esimese-korruse-plaan-joonis.webp",1800,1709,
  "Juurdeehitus, esimene korrus",
  "Puhkeruum 15,93 m², köök 6,60 m², vannituba 4,58 m².",
  "Juurdeehituse esimese korruse plaani joonis mõõtkavas 1:50, kus uues osas on puhkeruum 15,93 m², köök, vannituba ja esik ning vanas osas elutuba 26,71 m²."),
 ("juurdeehitus-teise-korruse-plaan-joonis.webp",1800,1732,
  "Juurdeehitus, teine korrus",
  "Puhkeruum 19,23 m², kontor 11,55 m², saun 2,75 m².",
  "Juurdeehituse teise korruse plaani joonis mõõtkavas 1:50, kus uues osas on puhkeruum 19,23 m², köök ja vannituba ning vanas osas magamistuba, kontor ja saun."),

 ("lamekatusega-elamu-korruse-plaan-joonis.webp",1400,1918,
  "Lamekatusega elamu, korruse plaan",
  "Elutuba 30,8 m², köök ja söögituba 23,5 m², kolm magamistuba.",
  "Ühekorruselise elamu korruse plaani joonis mõõtkavas 1:50 koos elutoa, köögi, kolme magamistoa, sauna, kontori ja garaažiga."),

 ("punase-laudisega-elamu-korruse-plaan-joonis.webp",1800,1891,
  "Punane elamu, korruse plaan",
  "Elutuba ja köök 35,7 m², kolm magamistuba.",
  "Ühekorruselise elamu korruse plaani joonis mõõtkavas 1:50, kus on elutuba ja köök 35,7 m², kolm magamistuba, vannituba, tehnoruum ning garderoob."),
 ("punase-laudisega-elamu-loige-joonis.webp",1800,1186,
  "Punane elamu, lõige A-A",
  "Katusekalle 30 kraadi, varjualuse räästas.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud 30-kraadine katusekalle, ruumide kõrgused ja varjualuse räästa lahendus."),
 ("punase-laudisega-elamu-kulg-ja-tagavaade-joonis.webp",1800,500,
  "Punane elamu, külg- ja tagavaade",
  "Rootsipunane puitlaudis, valge tuulekast ja klaasitud viil.",
  "Elamu külg- ja tagavaate joonis mõõtkavas 1:50, kus on rootsipunane puitlaudis, valged tuulekastid, klaasitud viil ja autovarjualune."),

 ("tumeda-puitfassaadiga-elamu-korruste-plaanid-joonis.webp",1800,941,
  "Tume elamu, korruste plaanid",
  "Elutuba 24,1 m², söögituba 19 m², neli magamistuba.",
  "Kahekorruselise elamu esimese ja teise korruse plaanide joonis mõõtkavas 1:50, kus esimesel korrusel on elutuba, köök, saun ja tehnoruum ning teisel korrusel neli magamistuba ja vannituba."),
 ("tumeda-puitfassaadiga-elamu-neli-vaadet-joonis.webp",1800,1178,
  "Tume elamu, neli vaadet",
  "Vaated idast, läänest, põhjast ja lõunast.",
  "Elamu nelja välisvaate joonis mõõtkavas 1:50, kus fassaadil on tumepruun puitlaudis, tumehall kivikatus ja krohvitud korsten."),
 ("tumeda-puitfassaadiga-elamu-loige-joonis.webp",1400,1311,
  "Tume elamu, lõige B-B",
  "Katusekalle 35 kraadi, avatud liimpuitpalk.",
  "Elamu lõike B-B joonis mõõtkavas 1:50, kus katusekalle on 35 kraadi ning kuivades ruumides jääb välissein avatud liimpuitpalgina nähtavale."),

 ("kortermaja-esimese-korruse-plaan-joonis.webp",1800,1047,
  "Kortermaja, esimese korruse plaan",
  "Kaks korterit 80,2 m², elutuba-köök 25,9 m².",
  "Kortermaja esimese korruse plaani joonis mõõtkavas 1:50, kus on kaks 80,2 m² korterit, mõlemas elutuba-köök 25,9 m², kolm magamistuba ja vannituba."),
 ("kortermaja-teise-korruse-plaan-joonis.webp",1800,993,
  "Kortermaja, teise korruse plaan",
  "Kaks korterit 85,4 m² koos sauna ja vannitoaga.",
  "Kortermaja teise korruse plaani joonis mõõtkavas 1:50, kus on kaks 85,4 m² korterit, mõlemas saun 5,1 m², vannituba ja kolm magamistuba."),
 ("kortermaja-loiked-joonis.webp",1800,703,
  "Kortermaja, lõiked A-A ja B-B",
  "Katusekalle 15 kraadi, eraldi tulesektsiooniga pööning.",
  "Kortermaja lõigete A-A ja B-B joonis mõõtkavas 1:50, kus on näidatud korruste kõrgused, eraldi tulesektsiooniga pööning ja 15-kraadine katusekalle."),
 ("kortermaja-eest-ja-kulgvaade-joonis.webp",1800,885,
  "Kortermaja, eest- ja külgvaade",
  "Tumehall laudis ja päikesepaneelid vähemalt 9,6 kW.",
  "Kortermaja eest- ja külgvaate joonis mõõtkavas 1:50, kus fassaadil on tumehall puitlaudis, sissepääsu juures tumepruun laudis ning katusel päikesepaneelid."),

 ("kelpkatusega-elamu-korruse-plaan-joonis.webp",1800,1502,
  "Kelpkatusega elamu, korruse plaan",
  "Garaaž 42,1 m², puhkeruum 25 m², köök 12,2 m².",
  "Ühekorruselise elamu korruse plaani joonis mõõtkavas 1:50 koos kahe auto garaažiga 42,1 m², kahe puhkeruumi, vannitoa ja köögiga."),
 ("kelpkatusega-elamu-loige-joonis.webp",1800,1088,
  "Kelpkatusega elamu, lõige A-A",
  "Katusekalle 25 kraadi ja katusefermid.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud katusefermid, 25-kraadine katusekalle ja sokli veekindluse lahendus."),
 ("kelpkatusega-elamu-neli-vaadet-joonis.webp",1800,694,
  "Kelpkatusega elamu, neli vaadet",
  "Valge krohv, beež kiviplaat ja tumehall plekk-katus.",
  "Elamu nelja välisvaate joonis mõõtkavas 1:50, kus fassaadil on valge krohv, beež kivimustriga fassaadiplaat ja tumehall plekk-katus."),

 ("rekonstrueeritud-elamu-esimese-korruse-plaan-joonis.webp",1800,976,
  "Rekonstrueeritav elamu, esimene korrus",
  "Elutuba 27,5 m², söögituba 11,6 m², köök 10 m².",
  "Rekonstrueeritava elamu esimese korruse plaani joonis mõõtkavas 1:50, kus hallina on märgitud säilitatavad ja punase punktiiriga lammutatavad välisseinad."),
 ("rekonstrueeritud-elamu-teise-korruse-plaan-joonis.webp",1400,1009,
  "Rekonstrueeritav elamu, teine korrus",
  "Magamistuba 23,7 m², vannituba 9,6 m² ja garderoobid.",
  "Elamu teise korruse plaani joonis mõõtkavas 1:50 koos kolme magamistoa, kahe vannitoa ja kahe garderoobiga."),
 ("rekonstrueeritud-elamu-loige-joonis.webp",1400,1195,
  "Rekonstrueeritav elamu, lõige A-A",
  "Katusekalle 20 kraadi ja vundamendi põhimõte.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud kahe korruse kõrgused, 20-kraadine katusekalle ja vundamendi põhimõtteline lahendus."),
 ("rekonstrueeritud-elamu-eestvaade-joonis.webp",1800,795,
  "Rekonstrueeritav elamu, eestvaade",
  "Tumepruun voodrilaud 145 mm ja hele kivisein.",
  "Elamu eestvaate joonis mõõtkavas 1:50, kus fassaadil on tumepruun 145 mm voodrilaud, hele kivisein ja kõrge trepikoja aken."),

 ("krohvitud-lamekatusega-elamu-korruste-plaanid-joonis.webp",1800,1258,
  "Krohvitud elamu, korruste plaanid",
  "Elu- ja söögituba 37 m², köök 19,6 m², kontor 9,5 m².",
  "Kahekorruselise elamu esimese ja teise korruse plaanide joonis mõõtkavas 1:50, kus esimesel korrusel on elu- ja söögituba 37 m², köök, saun ning kontor ja teisel korrusel kolm magamistuba, garderoobid ja rõdu."),
 ("krohvitud-lamekatusega-elamu-loige-joonis.webp",1800,1258,
  "Krohvitud elamu, lõige A-A",
  "Lamekatuse kalle 1:40 ja puitkarkassil parapett.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud lamekatuse kalle 1:40, puitkarkassil parapett ja kahe korruse kõrgused."),
 ("krohvitud-lamekatusega-elamu-neli-vaadet-joonis.webp",1800,1258,
  "Krohvitud elamu, neli vaadet",
  "Valge krohv, puitimitatsiooniga plaat ja klaaspiirdega rõdu.",
  "Elamu nelja välisvaate joonis mõõtkavas 1:50, kus fassaadil on valge krohv, halli puitimitatsiooniga fassaadiplaat ja metallraamil klaaspiirdega rõdu."),

 ("terrakotafassaadiga-elamu-korruse-plaan-joonis.webp",1400,1615,
  "Terrakotamaja, korruse plaan",
  "Elu- ja söögituba 30,9 m², köök 16,4 m², puhkeruum 27 m².",
  "Ühekorruselise L-kujulise elamu korruse plaani joonis mõõtkavas 1:50 koos elu- ja söögitoa, köögi, kolme magamistoa, kontori ja puhkeruumiga."),
 ("terrakotafassaadiga-elamu-loige-joonis.webp",1800,741,
  "Terrakotamaja, lõige A-A",
  "Kaks viilkatusega mahtu, katusekalle 35 kraadi.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus on näidatud kaks viilkatusega mahtu, katusefermid ja 35-kraadine katusekalle."),

 ("punase-talumaja-korruste-plaanid-joonis.webp",1800,903,
  "Punane elamu, korruste plaanid",
  "Elutuba 17,5 m², köök 14,7 m², kaks magamistuba.",
  "Elamu esimese ja teise korruse plaanide joonis mõõtkavas 1:50, kus hallina on märgitud säilitatavad ja punase punktiiriga lammutatavad välisseinad."),
 ("punase-talumaja-loige-joonis.webp",1800,1856,
  "Punane elamu, lõige A-A",
  "Katusekalle muudetud 43 kraadile, põrandaküte.",
  "Elamu lõike A-A joonis mõõtkavas 1:50, kus olemasolev 48-kraadine katusekalle on asendatud 43-kraadisega ning näidatud on põrandakütte ja vahelae tarindid."),
 ("punase-talumaja-neli-vaadet-joonis.webp",1800,1466,
  "Punane elamu, neli vaadet",
  "Punane püstlaudis, valged piirdelauad ja must katus.",
  "Elamu nelja välisvaate joonis mõõtkavas 1:50, kus fassaadil on punane püstlaudis, valged piirdelauad ja must plekk-katus."),

 ("musta-laudisega-abihoone-korruse-plaan-joonis.webp",1800,1235,
  "Metsamaja, korruse plaan",
  "Panipaik 17,1 m² ning puhkeruumid 11,4 ja 9,2 m².",
  "Hoone korruse plaani joonis mõõtkavas 1:50, kus on panipaik 17,1 m² ning puhkeruumid 11,4 ja 9,2 m²."),
 ("musta-laudisega-abihoone-vaated-joonis.webp",1800,1134,
  "Metsamaja, vaated",
  "Mustpruun termopuit ja ruudujaotusega kõrge aken.",
  "Hoone eest- ja külgvaadete joonis mõõtkavas 1:50, kus fassaadil on mustpruun termopuit ning külgseinas ruudujaotusega kõrge aken."),
 ("musta-laudisega-abihoone-loige-ja-solm-joonis.webp",1800,1223,
  "Metsamaja, lõige ja räästasõlm",
  "Katusekalle 45 kraadi, räästasõlm mõõtkavas 1:10.",
  "Hoone lõike joonis mõõtkavas 1:50 koos räästasõlme joonisega mõõtkavas 1:10, kus on kirjeldatud fassaadi, katuse ja soojustuse kihid."),
]


# Milline joonis kuulub millise objekti juurde. Seos avaneb valgustis,
# kui tellija klopsab portfoolio pildil. Sidumise aluseks on projektinumber
# failinimes, mitte piltide sarnasus.
SEOSED = {
    "/pildid/suvekohvik-raatuse-tanav-tartu-projekt.webp": {
        "tekst": "Suvekohvik pargis, mis avaneb hooajal tervenisti välja. Klaasfassaad on "
                         "lükandustega avatav ja katusel on haljastatud terrass, kuhu viib eraldi väline "
                         "trepp. Sees on restoranisaal 23,35 m², baar ja köök.",
        "joonised": [
            "suvekohvik-raatuse-tanav-vaade-eest-joonis.webp",
            "suvekohvik-esimese-korruse-plaan-joonis.webp",
        ],
    },
    "/pildid/korterelamu-visualiseering-03.webp": {
        "tekst": "Olemasolev maja ehitati ümber ja sai juurde uue mahu. Soklikorrusele jäi "
                         "garaaž, esimesele korrusele avatud köök koos söögitoaga ning eraldi elutuba, "
                         "teisele korrusele kaks magamistuba. Fassaad on tumeroheline puitlaudis, aknad "
                         "ja rõdupiirded tumehallid.",
        "joonised": [
            "umberehitatud-elamu-soklikorruse-ja-esimese-korruse-plaan-joonis.webp",
            "umberehitatud-elamu-teise-korruse-ja-katuse-plaan-joonis.webp",
            "umberehitatud-elamu-loiked-joonis.webp",
        ],
    },
    "/pildid/eramu-juurdeehitus-puitribifassaadiga.webp": {
        "tekst": "Juurdeehitus olemasoleva elamu kõrvale, kolmel tasapinnal. Kõige all on "
                         "tööruum, keskel puhkeruum koos köögi ja vannitoaga, ülal saun ning kontor. "
                         "Fassaad on vertikaalsetest puitribidest, mis varjavad trepimahu, aga lasevad "
                         "valguse läbi.",
        "joonised": [
            "juurdeehituse-puitribifassaad-lahivaade.webp",
            "juurdeehitus-vundamendi-plaan-joonis.webp",
            "juurdeehitus-esimese-korruse-plaan-joonis.webp",
            "juurdeehitus-teise-korruse-plaan-joonis.webp",
        ],
    },
    "/pildid/eramu-must-laudis-katusealune-terrass.webp": {
        "tekst": "Maja on kokku pandud kahest viilkatusega mahust. Ühte jäävad elu- ja söögituba "
                 "koos köögiga, teise kolm magamistuba ja vannituba. Mahtude vahele tuli "
                 "puitpostidel katusealune terrass, mis seob need kokku ja annab varju. "
                 "Fassaad on must püstlaudis ja katus must valtsplekk.",
        "joonised": [
            "musta-laudisega-elamu-otsavaade.webp",
            "musta-laudisega-elamu-kulgvaade.webp",
            "musta-laudisega-elamu-korruse-plaan-joonis.webp",
            "musta-laudisega-elamu-loige-joonis.webp",
        ],
    },
    "/pildid/eramu-roheline-puitfassaad-aiaga.webp": {
        "tekst": "Vanale majale ehitati juurde uus maht, mis on nüüdseks valmis. Sinna tulid "
                 "elu- ja söögituba koos köögiga ning uus sissepääs, vanasse ossa jäid magamistuba, "
                 "saun ja vannituba. Aia poole avaneb kaetud terrass. Fassaadilaudis ja katusekate "
                 "valiti nii, et need sobiksid olemasoleva majaga kokku.",
        "joonised": [
            "roheline-elamu-korruse-plaan-joonis.webp",
            "roheline-elamu-vaated-joonis.webp",
            "roheline-elamu-loige-joonis.webp",
        ],
    },
    "/pildid/eramu-lamekatus-kivifassaad-varjualune.webp": {
        "tekst": "Ühekorruseline lamekatusega maja, kus elutuba ja köök on hoone avatud otsas "
                         "ning kolm magamistuba teises otsas. Sissepääsu ja autokoha ees on katusest "
                         "välja ulatuv varjualune. Fassaad on hele kivi.",
        "joonised": [
            "lamekatusega-elamu-korruse-plaan-joonis.webp",
        ],
    },
    "/pildid/eramu-punane-puitfassaad-varjualusega.webp": {
        "tekst": "Elutuba ja köök on ühes 35,7 m² ruumis, magamistoad jäävad maja mõlemasse "
                         "otsa. Viilu alla tuli kõrge klaaspind ja pikendatud räästa alla "
                         "autovarjualune. Fassaad on rootsipunane laudis valgete piirdelaudadega, "
                         "katusekalle 30 kraadi.",
        "joonised": [
            "punase-laudisega-elamu-korruse-plaan-joonis.webp",
            "punase-laudisega-elamu-loige-joonis.webp",
            "punase-laudisega-elamu-kulg-ja-tagavaade-joonis.webp",
        ],
    },
    "/pildid/eramu-tume-puitlaudis-viilkatus-mannimetsas.webp": {
        "tekst": "Kahekorruseline liimpuitpalgist maja männimetsas. Esimesel korrusel on "
                         "elutuba, söögituba, köök ja saun, teisele korrusele mahub neli magamistuba. "
                         "Fassaad on tumepruun puitlaudis ja katusekalle 35 kraadi.",
        "joonised": [
            "tumeda-puitfassaadiga-elamu-korruste-plaanid-joonis.webp",
            "tumeda-puitfassaadiga-elamu-neli-vaadet-joonis.webp",
            "tumeda-puitfassaadiga-elamu-loige-joonis.webp",
        ],
    },
    "/pildid/eramu-tume-puitfassaad-paikesepaneelidega.webp": {
        "tekst": "Neljakorteriline maja, kummalgi korrusel kaks korterit. Igas korteris on "
                         "elutuba koos köögiga ja kolm magamistuba, teise korruse korterites lisaks "
                         "saun. Katusele on ette nähtud päikesepaneelid võimsusega vähemalt 9,6 kW.",
        "joonised": [
            "kortermaja-esimese-korruse-plaan-joonis.webp",
            "kortermaja-teise-korruse-plaan-joonis.webp",
            "kortermaja-loiked-joonis.webp",
            "kortermaja-eest-ja-kulgvaade-joonis.webp",
        ],
    },
    "/pildid/eramu-kelpkatus-garaaz-maakivi.webp": {
        "tekst": "Ühekorruseline kelpkatusega maja, mille külge on ehitatud kahe auto garaaž. "
                         "Elutiivas on kaks puhkeruumi, köök ja vannituba. Fassaad on valge krohv koos "
                         "beeži kiviplaadiga, katus tumehall plekk ja kalle 25 kraadi.",
        "joonised": [
            "kelpkatusega-elamu-korruse-plaan-joonis.webp",
            "kelpkatusega-elamu-loige-joonis.webp",
            "kelpkatusega-elamu-neli-vaadet-joonis.webp",
        ],
    },
    "/pildid/eramu-puitfassaad-metsas-02.webp": {
        "tekst": "Vana maja rekonstrueeriti ja laiendati. Olemasolevast välisseinast säilis "
                         "umbes kolmandik, ülejäänu ehitati uuesti. Esimesele korrusele jäid elutuba, "
                         "söögituba ja köök, teisele kolm magamistuba. Uus fassaad on tumepruun 145 mm "
                         "voodrilaud.",
        "joonised": [
            "rekonstrueeritud-elamu-esimese-korruse-plaan-joonis.webp",
            "rekonstrueeritud-elamu-teise-korruse-plaan-joonis.webp",
            "rekonstrueeritud-elamu-loige-joonis.webp",
            "rekonstrueeritud-elamu-eestvaade-joonis.webp",
        ],
    },
    "/pildid/eramu-kahekorruseline-lamekatus-krohv-puit.webp": {
        "tekst": "Kahekorruseline lamekatusega maja, mille elutuba on avatud läbi kahe korruse. "
                         "Esimesel korrusel on lisaks köök, kontor ja saun, teisel kolm magamistuba koos "
                         "garderoobidega ning rõdu. Fassaad on valge krohv koos puiduimitatsiooniga "
                         "plaatidega ja katusele on ette nähtud päikesepaneelid kuni 15 kW.",
        "joonised": [
            "krohvitud-lamekatusega-elamu-korruste-plaanid-joonis.webp",
            "krohvitud-lamekatusega-elamu-loige-joonis.webp",
            "krohvitud-lamekatusega-elamu-neli-vaadet-joonis.webp",
        ],
    },
    "/pildid/eramu-terrakota-plekkfassaad-viilkatus.webp": {
        "tekst": "Ühekorruseline maja, mille mahud on paigutatud L-tähena. Ühes tiivas on elu- "
                         "ja söögituba koos köögiga, teises kolm magamistuba, kontor ja puhkeruum. "
                         "Fassaad ja katus on sama terrakotatooni plekk, katusekalle 35 kraadi.",
        "joonised": [
            "terrakotafassaadiga-elamu-korruse-plaan-joonis.webp",
            "terrakotafassaadiga-elamu-loige-joonis.webp",
        ],
    },
    "/pildid/eramu-punane-laudis-valge-piirdelaud.webp": {
        "tekst": "Olemasoleva maja ümberehitus. Katuseharja tõsteti ja kallet muudeti 43 "
                         "kraadile, nii et teine korrus muutus kasutatavaks. Sinna tulid kaks "
                         "magamistuba ja kontor. Fassaad on punane püstlaudis valgete piirdelaudadega.",
        "joonised": [
            "punase-talumaja-korruste-plaanid-joonis.webp",
            "punase-talumaja-loige-joonis.webp",
            "punase-talumaja-neli-vaadet-joonis.webp",
        ],
    },
    "/pildid/eramu-must-vertikaalne-puitlaudis-metsas.webp": {
        "tekst": "Väike viilkatusega abihoone, kus on panipaik ja kaks puhkeruumi. Katusekalle "
                         "on 45 kraadi ja katus on kaetud sama mustpruuni termopuiduga mis fassaad. "
                         "Külgseinas on kõrge ruudujaotusega aken.",
        "joonised": [
            "musta-laudisega-abihoone-korruse-plaan-joonis.webp",
            "musta-laudisega-abihoone-vaated-joonis.webp",
            "musta-laudisega-abihoone-loige-ja-solm-joonis.webp",
        ],
    },
}


# Portfoolio jarjekord ja see, millised tood votavad kogu laiuse.
TOOD_AVAPILT = "/pildid/eramu-terrakota-plekkfassaad-viilkatus.webp"

# Portfoolio jarjekord. Rutm hoiab ruudustiku taidetuna: kitsaid kaarte on
# iga laia kaardi vahel paarisarv, muidu jaab rea lopus auk.
TOOD_JARJEKORD = [
    "eramu-juurdeehitus-puitribifassaadiga.webp",
    "eramu-tume-laudis-kelpkatus-talvel.webp",
    "eramu-must-vertikaalne-puitlaudis-metsas.webp",
    "eramu-tume-puitlaudis-viilkatus-mannimetsas.webp",
    "eramu-lamekatus-kivifassaad-varjualune.webp",
    "eramu-punane-laudis-valge-piirdelaud.webp",
    "eramu-kahekorruseline-lamekatus-krohv-puit.webp",
    "suvekohvik-raatuse-tanav-tartu-projekt.webp",
    "eramu-roheline-puitfassaad-aiaga.webp",
    "korterelamu-visualiseering-03.webp",
    "eramu-tume-puitfassaad-paikesepaneelidega.webp",
    "eramu-puitfassaad-metsas-02.webp",
    "eramu-punane-puitfassaad-varjualusega.webp",
    "eramu-kelpkatus-garaaz-maakivi.webp",
    "eramu-must-laudis-katusealune-terrass.webp",
    "eramu-tume-puitfassaad-01.webp",
]

TOOD_LAIAD = {
    "eramu-must-vertikaalne-puitlaudis-metsas.webp",
    "eramu-punane-laudis-valge-piirdelaud.webp",
    "eramu-roheline-puitfassaad-aiaga.webp",
    "eramu-must-laudis-katusealune-terrass.webp",
    "eramu-puitfassaad-metsas-02.webp",
    "eramu-tume-puitfassaad-01.webp",
}

AVALEHE_JARJEKORD = [
    "eramu-terrakota-plekkfassaad-viilkatus.webp",
    "eramu-lamekatus-kivifassaad-varjualune.webp",
    "eramu-kahekorruseline-lamekatus-krohv-puit.webp",
    "eramu-punane-laudis-valge-piirdelaud.webp",
    "eramu-kelpkatus-garaaz-maakivi.webp",
    "suvekohvik-raatuse-tanav-tartu-projekt.webp",
    "korterelamu-visualiseering-03.webp",
    "eramu-juurdeehitus-puitribifassaadiga.webp",
]
AVALEHE_LAIAD = {
    "eramu-terrakota-plekkfassaad-viilkatus.webp",
    "eramu-punane-laudis-valge-piirdelaud.webp",
}


def leia(fail):
    for p in PORTFOOLIO:
        if p[0].endswith("/" + fail):
            return p
    raise KeyError(fail)


def avapilt_link(fail):
    """Lehe avapilt klopsitavana, samade andmetega mis tookaart."""
    src, w, h, alt, pealkiri, liik = leia(fail)
    seos = SEOSED.get(src)
    andmed = ""
    if seos:
        andmed = (' data-joonised="' + ",".join(seos["joonised"]) + '"'
                  ' data-projekt-tekst="' + seos["tekst"] + '"')
    return (f'<a class="teenus-avapilt-link" href="{src}"'
            f' aria-label="Vaata suurelt: {pealkiri}"'
            f' data-pealkiri="{pealkiri}" data-kirjeldus="{liik}"{andmed}>'
            f'<img src="{src}" width="{w}" height="{h}" fetchpriority="high" alt="{alt}">'
            f'</a>')


def kaardid(jarjekord, laiad, esimesed_kiired=2):
    read = []
    for i, fail in enumerate(jarjekord):
        read.append(pilt_kaart(leia(fail),
                               laisk=(i >= esimesed_kiired),
                               suur=(fail in laiad)))
    return chr(10).join(read)


# Lai kaart venib ule terve ekraani, seetottu on monest pildist ka suurem
# variant. Vaikimisi src jaab vaiksem, nii et mobiil ei lae arvutiversiooni.
SUURED_VARIANDID = {
    "/pildid/eramu-tume-puitfassaad-01.webp": ("/pildid/eramu-tume-puitfassaad-01-2800.webp", 2800),
}


def pilt_kaart(p, laisk=True, suur=False):
    src, w, h, alt, pealkiri, liik = p
    ll = ' loading="lazy"' if laisk else ' fetchpriority="high"'
    kl = " tookaart-suur" if suur else ""
    variant = SUURED_VARIANDID.get(src)
    if variant and suur:
        ll += (f' srcset="{variant[0]} {variant[1]}w, {src} {w}w"'
               ' sizes="100vw"')
    seos = SEOSED.get(src)
    andmed = ""
    if seos:
        andmed = (' data-joonised="' + ",".join(seos["joonised"]) + '"'
                  ' data-projekt-tekst="' + seos["tekst"] + '"')
    return f'''      <figure class="tookaart{kl}"{andmed}>
        <a href="{src}" aria-label="Vaata suurelt: {pealkiri}">
          <img src="{src}" width="{w}" height="{h}"{ll} alt="{alt}">
        </a>
        <figcaption><strong>{pealkiri}</strong><span>{liik}</span></figcaption>
      </figure>'''


avaleht = '''  <section class="avapilt" aria-labelledby="hero-pealkiri">
    <img class="avapilt-taust"
         src="/pildid/eramu-must-puitlaudis-metsamaja-hero.webp"
         srcset="/pildid/eramu-must-puitlaudis-metsamaja-hero-1400.webp 1400w, /pildid/eramu-must-puitlaudis-metsamaja-hero.webp 1800w"
         sizes="100vw" width="1800" height="1005" fetchpriority="high"
         alt="Musta vertikaalse puitlaudisega üksikelamu järsu viilkatuse ja suure kaldakna all oleva elutoaga männimetsas.">
    <div class="avapilt-sisu">
      <h1 id="hero-pealkiri" class="visuaalselt-peidus">A-MAJA OÜ, arhitektuurne projekteerimine üle Eesti</h1>
      <svg class="avapilt-logo" viewBox="0 0 1818 942" role="img"
           aria-label="A-MAJA OÜ, arhitektuuribüroo" xmlns="http://www.w3.org/2000/svg">
        <path class="logo-joon" pathLength="1000" fill="none" stroke="#EDE6DC" stroke-width="4"
              stroke-linejoin="round" stroke-linecap="round" d="M108 931C106 930 103 928 102 926C101 924 100 913 100 644L100 365L103 360C106 354 113 347 121 343C134 335 141 331 142 329C144 328 146 326 149 325C151 324 155 321 158 319C161 318 163 316 164 316C164 316 168 314 172 311C176 309 180 306 182 305C183 304 188 301 192 298C196 295 202 292 204 290C207 289 211 287 212 285C214 284 217 282 219 281C222 280 227 277 230 274C239 269 245 265 254 259C262 254 271 248 281 242C284 240 288 237 290 237C294 235 298 232 319 219C327 214 335 208 339 206C342 204 347 201 351 198C355 196 359 193 360 192C363 191 371 186 378 181C380 180 385 177 388 175C395 171 402 166 406 163C408 162 412 160 414 158C417 157 422 154 424 153C427 151 432 147 437 145C441 142 447 138 451 135C455 133 462 129 467 125C472 122 477 119 478 118C480 117 482 115 485 114C487 113 492 110 495 108C514 95 514 95 541 112C544 113 549 117 553 119C556 121 562 124 565 127C569 129 572 131 573 131C574 132 578 134 581 136C587 140 595 145 602 149C604 150 608 153 610 154C612 156 614 157 615 157C615 157 618 159 621 161C625 163 629 166 632 168C638 171 647 176 652 180C654 181 658 184 661 185C664 187 666 188 667 189C667 190 670 191 673 193C676 194 684 199 690 203C697 207 703 211 705 212C706 213 711 216 716 219C721 222 726 226 728 227C731 228 734 230 736 232C737 233 741 235 744 237C747 238 751 240 752 242C754 243 757 245 759 246C762 247 767 250 777 257C781 260 789 264 798 270C801 271 805 274 808 276C810 277 814 280 817 281C819 283 822 284 823 285C823 286 826 288 828 289C831 290 835 292 838 294C849 301 855 305 860 307C862 309 865 311 866 312C867 312 870 314 873 316C876 318 880 320 882 321C883 323 886 324 888 325C890 326 896 330 908 338C911 340 915 342 917 343C920 344 923 347 926 350L930 355L930 368C932 394 931 494 929 497C925 503 917 503 912 498L910 496L909 432C909 374 908 367 907 365C905 362 903 361 888 352C884 350 879 347 876 345C874 343 870 341 868 340C861 335 858 333 852 329C848 327 845 325 844 325C844 325 841 324 839 322C836 320 832 317 830 316C827 315 824 313 822 312C821 310 817 308 814 307C811 305 809 304 809 303C808 302 806 301 803 299C800 298 796 296 794 294C784 287 780 285 774 282C762 275 758 272 752 268C750 267 746 264 744 263C742 262 736 258 730 255C714 245 709 241 704 238C701 237 697 234 695 233C693 231 689 229 687 228C685 228 682 226 680 224C676 221 667 216 660 212C657 210 654 208 652 207C651 206 648 204 646 203C644 202 640 200 638 198C636 197 632 194 629 193C621 189 613 184 609 180C607 179 603 176 601 175C597 173 591 169 581 163C579 161 575 159 573 158C570 157 567 155 565 153C563 152 560 150 557 148C555 147 549 144 544 141C539 138 533 134 530 132C526 130 522 128 521 127C515 123 511 125 486 141C479 145 473 149 473 149C473 149 470 151 467 153C465 155 461 157 459 158C456 159 452 161 450 163C443 168 432 175 429 177C427 178 424 180 422 181C420 183 418 184 417 184C417 184 414 186 412 187C409 189 405 192 403 193C400 194 397 196 396 198C394 199 390 201 388 203C385 204 381 207 379 208C377 210 375 211 375 211C374 211 371 213 368 215C365 217 361 220 359 220C357 221 354 223 353 224C351 226 349 228 337 234C334 236 328 240 324 242C304 255 295 261 288 265C277 272 274 274 272 276C270 277 267 279 264 280C262 281 258 284 256 285C254 287 251 289 248 290C246 291 243 293 241 295C239 296 236 298 234 299C232 300 230 302 228 303C227 304 224 306 222 308C219 309 215 312 213 313C210 315 208 316 207 316C207 316 204 318 202 319C199 321 195 324 192 325C190 327 187 329 186 330C184 331 181 334 178 335C175 337 169 340 166 343C162 345 155 349 152 351C148 353 145 355 144 356C144 357 142 358 139 359C137 361 132 364 130 367L125 372L125 636C125 909 125 905 129 907C130 907 324 908 560 908C959 908 990 909 993 910C999 914 1001 924 996 929L993 932L553 933C122 933 112 933 108 931ZM1136 930C1131 929 1130 928 1129 924C1127 917 1120 901 1118 898C1116 897 1114 896 1095 896C1070 896 1070 896 1067 906C1066 910 1063 916 1062 918C1061 921 1060 923 1060 924C1060 924 1059 926 1058 927C1054 932 1045 930 1046 925C1048 917 1052 906 1054 903C1055 901 1057 896 1058 892C1059 889 1061 883 1062 881C1064 879 1066 873 1067 868C1068 864 1070 858 1072 856C1073 853 1075 849 1076 845C1077 841 1079 836 1081 832C1088 817 1087 819 1093 818C1099 818 1102 819 1103 824C1104 826 1106 829 1107 832C1109 834 1111 839 1112 843C1113 848 1115 853 1116 855C1118 857 1120 861 1120 864C1121 868 1123 872 1125 875C1126 877 1128 882 1129 886C1130 889 1132 894 1134 898C1135 901 1137 905 1138 908C1139 910 1141 914 1142 918C1146 926 1145 932 1140 931C1140 931 1138 930 1136 930ZM1349 930C1340 926 1339 923 1338 892L1338 865L1334 860C1330 854 1330 851 1334 844C1336 841 1337 838 1338 835C1339 824 1349 822 1349 833C1349 838 1351 844 1356 848C1360 852 1360 854 1355 858C1350 862 1349 865 1349 887C1349 911 1349 911 1357 919C1364 926 1364 927 1359 929C1354 931 1353 931 1349 930ZM1404 930C1399 929 1386 920 1383 917C1381 914 1379 912 1379 911C1375 908 1374 877 1377 871C1380 866 1389 855 1391 854C1405 846 1430 849 1437 859C1439 861 1440 863 1441 863C1444 863 1448 879 1446 885C1444 891 1443 891 1420 891C1395 891 1392 892 1390 897C1389 900 1394 913 1396 913C1396 913 1399 915 1401 917C1409 924 1418 922 1427 913C1440 900 1452 904 1440 917C1430 929 1416 933 1404 930ZM1518 929C1517 927 1515 925 1514 923C1508 914 1505 909 1503 907C1502 905 1500 902 1498 900C1497 897 1495 895 1493 894C1484 889 1481 894 1481 913C1481 928 1480 931 1474 930C1466 929 1467 933 1467 874C1468 816 1467 819 1475 819C1480 819 1480 820 1481 846C1481 861 1482 872 1482 873C1483 877 1486 877 1489 874C1490 873 1491 871 1492 870C1493 869 1495 867 1496 866C1509 852 1521 844 1523 849C1524 852 1520 857 1511 866C1501 876 1500 880 1505 886C1506 888 1508 891 1509 893C1510 894 1512 898 1513 900C1519 908 1523 914 1525 917C1525 919 1527 922 1528 923C1530 926 1530 926 1528 928C1525 931 1521 932 1518 929ZM1561 930C1551 926 1550 923 1550 893C1550 866 1550 865 1544 858C1541 853 1541 851 1546 844C1549 840 1550 837 1550 834C1550 830 1553 825 1556 825C1559 825 1561 829 1561 834C1561 840 1563 844 1567 848C1572 851 1572 854 1566 859L1562 863L1561 885C1561 912 1561 911 1569 919C1576 925 1577 928 1571 929C1570 930 1568 930 1567 930C1566 931 1563 930 1561 930ZM1610 930C1593 924 1590 915 1590 880C1589 853 1590 850 1596 849C1602 848 1603 852 1603 876C1603 907 1604 909 1610 915C1618 922 1624 922 1633 916C1640 910 1641 907 1642 880C1642 854 1642 853 1646 852C1655 847 1656 849 1656 891C1656 928 1656 929 1651 929C1647 929 1640 926 1639 924C1637 922 1633 923 1630 926C1626 931 1617 932 1610 930ZM1700 930C1695 929 1686 923 1684 920C1679 909 1679 908 1678 881L1678 855L1681 852C1683 850 1685 849 1687 849C1691 849 1692 852 1692 882C1693 912 1692 911 1700 916C1708 922 1714 922 1722 915C1729 909 1730 905 1731 876C1731 852 1732 851 1738 851C1744 851 1744 851 1744 891C1744 931 1744 930 1737 929C1735 928 1732 927 1730 926C1726 923 1722 923 1719 926C1715 931 1708 932 1700 930ZM1158 928C1155 924 1156 854 1158 851C1161 848 1161 848 1165 851C1168 853 1168 853 1175 852C1191 848 1197 849 1197 855C1197 859 1194 861 1187 861C1173 863 1170 870 1170 906C1170 924 1170 926 1168 928C1165 931 1160 931 1158 928ZM1214 928L1211 927L1211 876L1211 824L1213 822C1221 814 1224 818 1225 836C1226 853 1227 855 1237 852C1244 849 1251 849 1259 850C1267 853 1268 853 1273 861L1276 868L1277 897L1277 927L1275 928C1272 930 1265 929 1264 927C1263 926 1263 914 1263 900C1263 873 1262 868 1259 864C1254 858 1238 858 1232 863C1226 869 1226 871 1225 900C1224 929 1224 930 1219 930C1218 930 1215 929 1214 928ZM1303 929C1300 928 1300 927 1300 890L1300 854L1303 852C1307 848 1309 848 1311 851C1313 854 1314 926 1312 929C1311 930 1307 930 1303 929ZM1770 929C1769 928 1768 927 1767 926C1766 921 1767 855 1769 854C1771 851 1776 851 1781 852C1785 853 1786 853 1790 851C1799 847 1807 849 1807 855C1807 859 1806 860 1798 861C1782 863 1780 869 1780 910C1780 931 1779 933 1770 929ZM1109 884C1112 882 1111 872 1107 866C1106 863 1103 857 1102 854C1100 844 1099 842 1094 842C1089 842 1088 844 1085 855C1084 860 1082 865 1080 868C1078 872 1077 881 1079 883C1081 886 1107 886 1109 884ZM1431 877L1433 874L1432 871C1428 863 1425 861 1417 859C1404 857 1394 862 1391 872C1390 878 1394 880 1413 880C1428 880 1428 879 1431 877ZM620 873C617 872 614 871 613 870C610 868 602 853 600 845C599 842 597 838 596 836C594 833 593 830 592 828C591 825 589 821 588 817C586 813 584 809 583 806C582 804 580 800 579 796C577 792 575 788 575 787C574 785 572 780 569 775C567 769 565 765 565 764C565 763 563 759 562 756C560 752 557 747 556 743C556 740 553 735 552 732C550 729 548 724 547 721C545 717 543 713 543 712C542 711 540 706 539 703C538 699 536 693 534 690C532 688 530 683 529 680C529 677 527 672 525 670C523 667 522 662 521 660C520 658 519 653 517 650C516 648 513 643 513 640C512 637 509 632 507 628C506 624 504 620 503 618C502 615 500 611 498 607C497 603 495 599 494 596C493 594 492 591 491 588C489 586 487 581 486 578C485 574 483 569 482 567C479 563 473 548 469 536C467 532 465 527 464 526C463 523 455 505 451 496C450 492 448 487 446 485C445 483 443 478 442 475C441 471 439 466 438 464C436 461 434 457 434 454C433 451 431 446 429 444C428 441 426 436 425 433C424 430 422 425 420 423C419 421 417 416 416 413C414 407 408 393 403 384C401 380 398 373 396 367L393 356L395 351C402 337 416 346 424 372C425 375 427 379 428 382C430 384 432 389 433 393C434 396 436 402 438 404C439 407 441 412 442 415C443 418 445 422 446 424C448 427 450 432 451 436C452 439 454 444 456 447C457 449 459 454 460 458C462 461 464 465 464 466C465 468 467 471 468 474C469 477 471 484 474 488C476 493 478 498 478 499C478 499 479 503 481 506C483 509 485 514 486 518C487 522 489 526 490 528C492 530 493 534 494 537C496 542 498 546 507 568C510 573 512 579 513 582C514 584 516 588 517 590C519 593 521 598 521 601C522 604 524 608 525 610C527 613 529 617 530 621C531 625 534 630 535 632C537 635 538 640 539 642C540 644 542 650 544 654C553 673 556 680 556 683C557 685 559 689 560 692C562 696 565 701 566 704C566 707 569 712 570 715C571 718 573 722 574 724C575 727 577 731 579 734C580 738 582 743 583 745C584 749 588 757 596 774C598 779 600 784 601 786C601 788 603 792 605 796C606 800 609 805 610 808C611 812 613 816 614 818C615 820 617 824 618 827C620 834 627 845 630 849C632 850 634 851 765 851C838 851 899 851 902 850C910 849 909 850 910 800C910 760 911 756 912 754C918 745 931 751 932 762C933 765 933 789 933 815C932 869 933 867 924 872L920 874L772 874C657 874 623 874 620 873ZM1304 830C1298 827 1301 819 1308 819C1312 819 1313 822 1313 827C1312 832 1309 833 1304 830ZM275 744C267 739 267 735 271 725C273 722 274 716 275 714C276 712 277 707 279 704C280 702 282 697 283 694C284 691 286 687 287 684C289 682 291 677 292 674C293 670 295 665 296 663C298 660 300 655 301 652C302 648 304 643 305 642C306 641 308 636 310 631C311 626 314 621 315 619C316 617 317 613 318 611C319 609 320 605 321 602C323 600 325 594 327 589C329 584 331 578 332 576C334 573 336 569 337 566C337 563 339 559 340 557C341 556 343 551 344 547C346 544 348 538 349 535C351 533 353 528 354 524C355 521 357 516 358 513C360 511 362 506 363 503C364 500 365 495 367 492C368 489 371 484 371 481C372 478 374 473 376 470C377 468 379 463 381 459C386 442 393 436 399 442C406 449 407 458 403 466C401 469 399 474 398 477C397 480 395 485 393 489C392 493 389 498 389 502C388 505 386 509 385 510C384 512 382 516 381 520C380 523 378 527 376 529C375 531 373 536 372 540C371 545 369 551 367 553C365 556 363 561 363 564C362 567 360 571 359 574C355 580 349 598 349 601C349 605 350 605 407 606C458 606 460 607 463 609C469 613 471 623 467 628L464 630L406 630C343 630 339 630 335 634C333 637 328 645 328 647C328 648 326 652 324 656C323 660 320 666 319 670C318 674 316 679 314 682C312 684 311 688 311 690C310 691 308 695 307 699C305 703 302 709 301 713C298 720 293 733 290 738C289 741 281 746 279 746C278 746 276 745 275 744ZM841 738C835 735 836 724 842 711C844 707 847 701 847 697C848 694 850 689 852 687C853 685 855 680 856 675C857 671 859 666 860 664C862 661 864 656 865 652C866 648 868 642 870 639C871 636 873 632 873 630C874 629 876 624 878 619C880 614 882 609 882 607C883 605 884 601 886 598C888 595 890 589 891 585C892 581 894 576 896 573C897 571 899 566 900 562C904 549 909 545 921 546C930 547 933 549 935 556C937 559 938 563 940 565C941 567 943 572 944 575C945 579 947 585 949 588C951 591 952 596 953 598C954 600 955 605 957 608C959 610 961 615 962 618C962 621 965 626 966 629C968 633 970 638 971 640C972 643 973 648 975 650C977 653 979 658 979 661C980 665 982 670 984 672C986 675 988 680 988 683C989 687 991 692 993 694C995 697 997 702 997 705C998 708 1000 712 1001 713C1003 716 1008 730 1008 733C1008 736 1004 738 996 738C985 738 982 736 980 728C979 725 977 720 975 717C974 714 971 708 970 704C968 696 961 684 958 682C956 681 951 680 921 680C877 680 878 680 873 695C872 698 871 703 869 705C868 708 866 713 865 717C861 734 852 742 841 738ZM1039 738C1028 735 1019 727 1013 714C1002 692 1006 682 1023 684C1028 685 1029 687 1031 697C1033 706 1034 707 1040 712C1051 722 1066 722 1077 712C1086 704 1085 712 1086 627C1086 586 1087 552 1087 551C1089 548 1091 547 1100 546C1113 545 1112 537 1112 624C1112 707 1112 702 1104 716C1099 726 1090 734 1081 737C1076 739 1046 739 1039 738ZM1430 738C1426 737 1419 735 1415 733C1411 731 1408 729 1407 729C1407 729 1404 727 1401 725C1388 715 1380 705 1374 694C1372 691 1370 687 1369 685C1368 683 1367 681 1367 680C1367 678 1366 673 1364 667C1361 655 1361 635 1364 624C1364 620 1366 614 1367 610C1369 595 1388 568 1399 562C1400 561 1403 559 1405 558C1407 556 1412 554 1417 552C1422 551 1428 548 1430 548C1440 544 1472 545 1481 549C1483 550 1488 552 1491 553C1495 554 1499 556 1501 558C1503 559 1506 561 1508 562C1516 566 1531 584 1535 593C1535 595 1537 600 1539 603C1547 619 1547 673 1539 683C1538 685 1536 688 1535 691C1534 695 1532 698 1531 700C1529 701 1527 704 1526 707C1517 720 1492 736 1475 738C1465 739 1438 739 1430 738ZM1617 738C1601 736 1583 722 1576 707C1568 692 1569 694 1569 618L1568 551L1571 548C1576 544 1585 545 1589 551C1590 553 1591 558 1591 613L1592 674L1594 685C1598 701 1602 707 1616 714L1626 718L1642 718L1658 718L1666 715C1676 711 1682 706 1687 697C1692 687 1692 689 1693 618C1693 581 1694 551 1694 550C1696 545 1711 545 1715 549L1718 551L1718 614C1718 652 1718 679 1717 682C1710 711 1702 722 1682 732C1677 735 1671 737 1667 738C1659 739 1625 739 1617 738ZM1127 736C1125 735 1125 734 1125 732C1126 727 1130 717 1134 709C1135 705 1137 699 1138 697C1139 695 1140 690 1142 687C1144 684 1146 679 1147 675C1148 672 1150 666 1151 663C1153 660 1155 654 1156 650C1157 647 1159 642 1160 640C1161 639 1163 634 1164 630C1165 626 1167 620 1169 618C1170 615 1172 610 1173 608C1174 605 1176 600 1177 597C1179 594 1181 588 1182 584C1183 580 1185 575 1186 573C1188 570 1190 565 1191 561C1195 549 1200 545 1212 546C1221 547 1223 549 1225 554C1226 556 1228 560 1230 564C1231 567 1234 573 1235 576C1235 580 1237 585 1239 588C1241 591 1243 595 1244 598C1244 601 1246 606 1248 608C1250 611 1252 616 1252 619C1253 622 1255 627 1257 630C1258 633 1260 638 1261 640C1262 642 1263 647 1265 650C1267 652 1269 657 1270 661C1270 664 1273 669 1274 672C1276 676 1278 681 1279 684C1280 686 1281 691 1283 694C1284 696 1287 701 1287 704C1288 707 1290 712 1292 714C1301 733 1300 738 1286 738C1275 738 1273 737 1270 728C1269 725 1267 719 1265 717C1264 714 1262 709 1261 705C1259 697 1252 685 1249 683C1246 681 1245 680 1213 680C1170 680 1168 680 1164 694C1164 697 1162 701 1161 704C1159 706 1157 713 1155 719C1153 725 1151 730 1149 733L1145 738L1137 738C1131 738 1129 738 1127 736ZM778 732C770 727 771 741 770 598C770 482 769 471 768 469C765 467 762 469 760 474C759 477 757 481 755 483C754 485 752 489 751 492C750 496 748 500 747 503C745 505 743 509 742 512C742 515 739 519 737 522C736 525 733 530 732 533C732 536 730 540 728 543C727 545 725 549 724 552C723 556 721 560 720 562C718 565 716 569 715 572C714 575 712 580 710 583C709 586 707 590 706 592C705 595 703 599 701 603C700 606 698 609 698 610C698 611 696 615 694 620C692 624 689 629 688 632C688 635 686 639 684 642C683 644 681 648 680 652C679 655 677 659 675 662C674 664 672 668 671 671C670 674 666 683 662 690C659 698 655 708 653 711C645 737 628 734 619 706C618 703 616 697 613 692C606 676 600 663 600 662C600 662 596 653 591 642C586 632 582 623 582 622C582 621 580 618 579 614C572 602 566 589 564 583C563 580 562 576 560 574C559 572 557 568 556 565C555 562 553 557 551 553C546 543 539 529 539 528C539 527 531 509 525 498C524 494 522 489 521 486C520 484 518 480 517 478C515 475 513 470 512 467C511 464 509 460 507 458C506 456 505 452 504 449C503 446 500 442 499 440C495 435 495 426 498 423C505 416 516 422 521 434C522 437 524 441 525 443C528 449 536 466 539 475C540 479 543 483 544 485C545 486 546 489 547 492C548 494 550 499 552 502C554 506 556 512 557 515C558 518 560 522 562 524C563 526 565 530 566 533C566 536 569 541 570 544C572 548 574 552 575 554C576 557 578 561 580 565C581 568 583 571 583 572C583 573 591 590 597 601C598 605 600 609 600 609C600 610 602 615 604 620C607 625 609 630 610 632C611 635 613 639 614 641C616 644 618 648 618 650C620 656 631 678 634 681C639 686 642 685 644 676C645 673 647 668 649 666C651 664 652 660 653 658C654 655 656 650 658 645C660 641 664 633 666 629C668 624 670 619 671 616C672 614 674 610 676 607C677 604 679 600 680 598C681 595 683 591 684 589C686 587 688 582 688 578C689 575 691 571 693 569C694 567 696 563 697 560C698 557 700 552 702 548C704 544 706 539 707 536C708 533 710 530 711 528C712 526 714 523 715 520C716 517 718 512 720 508C721 505 723 501 724 500C724 499 726 494 729 489C731 484 733 479 733 478C733 478 735 474 736 470C738 467 741 461 742 458C743 455 745 452 745 450C746 449 748 445 749 441C753 432 757 426 761 423C766 420 782 420 786 424C793 429 792 416 792 578L792 724L790 728C786 733 782 735 778 732ZM1466 719C1488 716 1512 694 1516 672C1521 648 1519 613 1513 603C1511 601 1509 598 1508 595C1506 591 1499 584 1492 578C1474 564 1435 563 1416 577C1404 586 1395 597 1393 607C1392 610 1391 615 1390 618C1387 626 1386 648 1388 658C1394 701 1424 724 1466 719ZM947 658C951 655 951 652 948 646C946 643 945 639 944 636C943 634 941 629 940 626C938 623 936 617 935 613C934 610 932 604 930 600C929 596 927 592 926 590C925 581 922 577 919 579C916 579 911 590 909 598C908 603 906 609 904 612C902 615 901 620 900 623C899 626 897 632 895 635C888 651 888 657 895 659C901 661 945 660 947 658ZM1238 658C1242 656 1242 653 1239 648C1237 645 1235 640 1234 636C1233 631 1231 626 1230 625C1229 623 1227 618 1226 614C1225 610 1223 605 1222 603C1221 601 1219 596 1217 591C1214 581 1213 579 1209 581C1205 582 1202 587 1200 598C1199 602 1197 608 1195 611C1193 614 1191 620 1190 623C1190 626 1188 632 1186 635C1178 650 1178 658 1186 659C1197 661 1236 659 1238 658ZM1609 532C1605 529 1604 516 1606 512C1610 506 1628 507 1630 514C1630 517 1629 528 1628 530C1626 534 1612 536 1609 532ZM1660 533C1656 531 1654 513 1658 511C1665 506 1676 508 1678 514C1679 518 1677 528 1675 531C1673 534 1665 535 1660 533ZM12 339C5 332 8 320 18 315C31 308 35 306 37 303C38 302 41 300 44 299C48 297 58 291 66 285C68 284 72 281 74 280C77 278 83 275 87 272C91 269 97 266 99 265C102 263 106 260 108 259C113 256 123 249 132 243C149 233 152 231 172 219C179 214 186 209 186 208C187 206 188 184 188 119C189 23 188 31 196 26L200 24L257 23C294 23 318 23 323 24C339 26 338 25 339 71C340 111 339 110 346 111C349 111 351 110 361 104C367 100 374 95 376 94C387 87 401 79 404 76C406 75 411 72 415 70C428 62 433 59 437 56C440 54 446 50 450 48C454 45 460 42 461 40C463 39 467 37 469 36C472 34 476 31 478 30C481 28 486 24 490 22C498 18 501 15 507 11C511 8 523 9 528 13C536 18 539 21 544 24C547 25 551 28 554 30C556 32 560 34 562 35C565 36 568 38 570 40C572 41 576 44 579 45C581 47 585 49 587 50C588 51 593 54 596 56C600 59 605 62 608 64C610 65 615 68 618 70C620 71 624 73 625 75C626 76 629 78 631 79C635 80 640 83 651 91C653 92 656 94 657 95C659 96 662 98 665 100C667 101 672 104 674 105C676 106 679 108 681 109C682 110 685 112 689 114C692 115 695 118 696 118C697 119 699 121 701 122C703 123 707 126 710 127C712 129 716 132 718 132C721 134 726 137 736 144C738 146 742 148 744 149C747 150 749 152 750 153C751 153 755 156 758 158C762 160 767 162 768 163C772 167 786 175 797 182C800 183 804 186 807 188C809 189 813 192 815 193C818 194 821 196 822 198C824 199 828 201 830 203C833 204 837 206 839 208C840 209 842 210 842 210C843 210 848 213 855 218C861 222 869 227 872 229C875 230 879 233 881 234C887 237 900 246 907 250C910 252 915 255 918 257C922 259 926 262 929 264C931 265 934 267 936 268C937 269 939 271 941 272C943 272 947 275 949 277C952 278 955 280 956 281C958 281 962 284 965 286C969 289 973 291 975 292C976 293 980 296 984 298C987 300 992 303 994 305C1019 319 1024 326 1016 336C1014 338 1012 340 1011 340C1008 340 996 334 990 329C987 327 984 325 984 325C983 325 978 322 963 312C960 310 957 308 956 308C955 308 941 299 934 294C932 293 929 290 926 289C924 288 921 286 919 284C916 282 914 281 914 281C913 281 909 279 904 276C900 273 894 269 891 267C888 265 882 261 877 258C872 255 866 252 863 250C860 248 855 244 851 242C847 239 843 237 843 237C842 237 840 235 837 234C834 232 831 229 829 228C825 226 812 218 810 216C808 215 805 213 803 212C801 211 796 208 794 206C791 204 789 203 788 203C788 203 784 201 780 198C776 196 770 192 766 190C760 186 755 182 737 171C733 168 728 165 725 163C722 162 718 159 715 158C709 154 700 149 695 145C693 144 690 141 687 140C685 139 682 137 680 135C678 134 672 130 668 128C663 126 658 122 656 120C653 118 650 116 647 115C645 114 640 111 636 109C633 106 627 103 623 100C615 95 607 91 599 85C596 83 591 80 588 79C586 77 582 75 580 74C579 72 575 70 572 69C570 67 566 65 564 64C555 57 551 55 546 53C544 51 539 49 537 47C518 34 514 33 504 40C501 42 495 46 490 49C486 52 481 55 479 57C475 59 473 60 461 68C456 71 442 79 435 84C430 87 419 95 409 101C406 103 401 106 398 108C395 110 390 113 387 114C384 116 380 118 379 119C378 120 373 123 368 126C358 133 357 134 344 142C335 149 334 149 329 149C317 149 317 150 317 97C316 49 317 50 309 47C305 46 223 45 219 47C212 49 212 48 212 136C212 211 212 215 210 218C208 222 201 228 200 228C199 228 196 230 193 232C190 234 186 237 184 237C182 238 179 240 178 242C176 243 172 245 169 247C166 249 162 251 161 252C157 255 145 263 131 271C128 272 125 275 123 276C121 278 117 280 114 281C111 283 108 285 107 285C107 286 104 288 101 290C93 294 85 299 81 303C79 304 75 307 73 308C70 309 66 312 64 314C59 317 57 318 46 324C42 327 35 331 30 334C20 341 15 343 12 339Z"/>
        <path class="logo-tais" fill="#EDE6DC" fill-rule="evenodd" d="M108 931C106 930 103 928 102 926C101 924 100 913 100 644L100 365L103 360C106 354 113 347 121 343C134 335 141 331 142 329C144 328 146 326 149 325C151 324 155 321 158 319C161 318 163 316 164 316C164 316 168 314 172 311C176 309 180 306 182 305C183 304 188 301 192 298C196 295 202 292 204 290C207 289 211 287 212 285C214 284 217 282 219 281C222 280 227 277 230 274C239 269 245 265 254 259C262 254 271 248 281 242C284 240 288 237 290 237C294 235 298 232 319 219C327 214 335 208 339 206C342 204 347 201 351 198C355 196 359 193 360 192C363 191 371 186 378 181C380 180 385 177 388 175C395 171 402 166 406 163C408 162 412 160 414 158C417 157 422 154 424 153C427 151 432 147 437 145C441 142 447 138 451 135C455 133 462 129 467 125C472 122 477 119 478 118C480 117 482 115 485 114C487 113 492 110 495 108C514 95 514 95 541 112C544 113 549 117 553 119C556 121 562 124 565 127C569 129 572 131 573 131C574 132 578 134 581 136C587 140 595 145 602 149C604 150 608 153 610 154C612 156 614 157 615 157C615 157 618 159 621 161C625 163 629 166 632 168C638 171 647 176 652 180C654 181 658 184 661 185C664 187 666 188 667 189C667 190 670 191 673 193C676 194 684 199 690 203C697 207 703 211 705 212C706 213 711 216 716 219C721 222 726 226 728 227C731 228 734 230 736 232C737 233 741 235 744 237C747 238 751 240 752 242C754 243 757 245 759 246C762 247 767 250 777 257C781 260 789 264 798 270C801 271 805 274 808 276C810 277 814 280 817 281C819 283 822 284 823 285C823 286 826 288 828 289C831 290 835 292 838 294C849 301 855 305 860 307C862 309 865 311 866 312C867 312 870 314 873 316C876 318 880 320 882 321C883 323 886 324 888 325C890 326 896 330 908 338C911 340 915 342 917 343C920 344 923 347 926 350L930 355L930 368C932 394 931 494 929 497C925 503 917 503 912 498L910 496L909 432C909 374 908 367 907 365C905 362 903 361 888 352C884 350 879 347 876 345C874 343 870 341 868 340C861 335 858 333 852 329C848 327 845 325 844 325C844 325 841 324 839 322C836 320 832 317 830 316C827 315 824 313 822 312C821 310 817 308 814 307C811 305 809 304 809 303C808 302 806 301 803 299C800 298 796 296 794 294C784 287 780 285 774 282C762 275 758 272 752 268C750 267 746 264 744 263C742 262 736 258 730 255C714 245 709 241 704 238C701 237 697 234 695 233C693 231 689 229 687 228C685 228 682 226 680 224C676 221 667 216 660 212C657 210 654 208 652 207C651 206 648 204 646 203C644 202 640 200 638 198C636 197 632 194 629 193C621 189 613 184 609 180C607 179 603 176 601 175C597 173 591 169 581 163C579 161 575 159 573 158C570 157 567 155 565 153C563 152 560 150 557 148C555 147 549 144 544 141C539 138 533 134 530 132C526 130 522 128 521 127C515 123 511 125 486 141C479 145 473 149 473 149C473 149 470 151 467 153C465 155 461 157 459 158C456 159 452 161 450 163C443 168 432 175 429 177C427 178 424 180 422 181C420 183 418 184 417 184C417 184 414 186 412 187C409 189 405 192 403 193C400 194 397 196 396 198C394 199 390 201 388 203C385 204 381 207 379 208C377 210 375 211 375 211C374 211 371 213 368 215C365 217 361 220 359 220C357 221 354 223 353 224C351 226 349 228 337 234C334 236 328 240 324 242C304 255 295 261 288 265C277 272 274 274 272 276C270 277 267 279 264 280C262 281 258 284 256 285C254 287 251 289 248 290C246 291 243 293 241 295C239 296 236 298 234 299C232 300 230 302 228 303C227 304 224 306 222 308C219 309 215 312 213 313C210 315 208 316 207 316C207 316 204 318 202 319C199 321 195 324 192 325C190 327 187 329 186 330C184 331 181 334 178 335C175 337 169 340 166 343C162 345 155 349 152 351C148 353 145 355 144 356C144 357 142 358 139 359C137 361 132 364 130 367L125 372L125 636C125 909 125 905 129 907C130 907 324 908 560 908C959 908 990 909 993 910C999 914 1001 924 996 929L993 932L553 933C122 933 112 933 108 931ZM1136 930C1131 929 1130 928 1129 924C1127 917 1120 901 1118 898C1116 897 1114 896 1095 896C1070 896 1070 896 1067 906C1066 910 1063 916 1062 918C1061 921 1060 923 1060 924C1060 924 1059 926 1058 927C1054 932 1045 930 1046 925C1048 917 1052 906 1054 903C1055 901 1057 896 1058 892C1059 889 1061 883 1062 881C1064 879 1066 873 1067 868C1068 864 1070 858 1072 856C1073 853 1075 849 1076 845C1077 841 1079 836 1081 832C1088 817 1087 819 1093 818C1099 818 1102 819 1103 824C1104 826 1106 829 1107 832C1109 834 1111 839 1112 843C1113 848 1115 853 1116 855C1118 857 1120 861 1120 864C1121 868 1123 872 1125 875C1126 877 1128 882 1129 886C1130 889 1132 894 1134 898C1135 901 1137 905 1138 908C1139 910 1141 914 1142 918C1146 926 1145 932 1140 931C1140 931 1138 930 1136 930ZM1349 930C1340 926 1339 923 1338 892L1338 865L1334 860C1330 854 1330 851 1334 844C1336 841 1337 838 1338 835C1339 824 1349 822 1349 833C1349 838 1351 844 1356 848C1360 852 1360 854 1355 858C1350 862 1349 865 1349 887C1349 911 1349 911 1357 919C1364 926 1364 927 1359 929C1354 931 1353 931 1349 930ZM1404 930C1399 929 1386 920 1383 917C1381 914 1379 912 1379 911C1375 908 1374 877 1377 871C1380 866 1389 855 1391 854C1405 846 1430 849 1437 859C1439 861 1440 863 1441 863C1444 863 1448 879 1446 885C1444 891 1443 891 1420 891C1395 891 1392 892 1390 897C1389 900 1394 913 1396 913C1396 913 1399 915 1401 917C1409 924 1418 922 1427 913C1440 900 1452 904 1440 917C1430 929 1416 933 1404 930ZM1518 929C1517 927 1515 925 1514 923C1508 914 1505 909 1503 907C1502 905 1500 902 1498 900C1497 897 1495 895 1493 894C1484 889 1481 894 1481 913C1481 928 1480 931 1474 930C1466 929 1467 933 1467 874C1468 816 1467 819 1475 819C1480 819 1480 820 1481 846C1481 861 1482 872 1482 873C1483 877 1486 877 1489 874C1490 873 1491 871 1492 870C1493 869 1495 867 1496 866C1509 852 1521 844 1523 849C1524 852 1520 857 1511 866C1501 876 1500 880 1505 886C1506 888 1508 891 1509 893C1510 894 1512 898 1513 900C1519 908 1523 914 1525 917C1525 919 1527 922 1528 923C1530 926 1530 926 1528 928C1525 931 1521 932 1518 929ZM1561 930C1551 926 1550 923 1550 893C1550 866 1550 865 1544 858C1541 853 1541 851 1546 844C1549 840 1550 837 1550 834C1550 830 1553 825 1556 825C1559 825 1561 829 1561 834C1561 840 1563 844 1567 848C1572 851 1572 854 1566 859L1562 863L1561 885C1561 912 1561 911 1569 919C1576 925 1577 928 1571 929C1570 930 1568 930 1567 930C1566 931 1563 930 1561 930ZM1610 930C1593 924 1590 915 1590 880C1589 853 1590 850 1596 849C1602 848 1603 852 1603 876C1603 907 1604 909 1610 915C1618 922 1624 922 1633 916C1640 910 1641 907 1642 880C1642 854 1642 853 1646 852C1655 847 1656 849 1656 891C1656 928 1656 929 1651 929C1647 929 1640 926 1639 924C1637 922 1633 923 1630 926C1626 931 1617 932 1610 930ZM1700 930C1695 929 1686 923 1684 920C1679 909 1679 908 1678 881L1678 855L1681 852C1683 850 1685 849 1687 849C1691 849 1692 852 1692 882C1693 912 1692 911 1700 916C1708 922 1714 922 1722 915C1729 909 1730 905 1731 876C1731 852 1732 851 1738 851C1744 851 1744 851 1744 891C1744 931 1744 930 1737 929C1735 928 1732 927 1730 926C1726 923 1722 923 1719 926C1715 931 1708 932 1700 930ZM1158 928C1155 924 1156 854 1158 851C1161 848 1161 848 1165 851C1168 853 1168 853 1175 852C1191 848 1197 849 1197 855C1197 859 1194 861 1187 861C1173 863 1170 870 1170 906C1170 924 1170 926 1168 928C1165 931 1160 931 1158 928ZM1214 928L1211 927L1211 876L1211 824L1213 822C1221 814 1224 818 1225 836C1226 853 1227 855 1237 852C1244 849 1251 849 1259 850C1267 853 1268 853 1273 861L1276 868L1277 897L1277 927L1275 928C1272 930 1265 929 1264 927C1263 926 1263 914 1263 900C1263 873 1262 868 1259 864C1254 858 1238 858 1232 863C1226 869 1226 871 1225 900C1224 929 1224 930 1219 930C1218 930 1215 929 1214 928ZM1303 929C1300 928 1300 927 1300 890L1300 854L1303 852C1307 848 1309 848 1311 851C1313 854 1314 926 1312 929C1311 930 1307 930 1303 929ZM1770 929C1769 928 1768 927 1767 926C1766 921 1767 855 1769 854C1771 851 1776 851 1781 852C1785 853 1786 853 1790 851C1799 847 1807 849 1807 855C1807 859 1806 860 1798 861C1782 863 1780 869 1780 910C1780 931 1779 933 1770 929ZM1109 884C1112 882 1111 872 1107 866C1106 863 1103 857 1102 854C1100 844 1099 842 1094 842C1089 842 1088 844 1085 855C1084 860 1082 865 1080 868C1078 872 1077 881 1079 883C1081 886 1107 886 1109 884ZM1431 877L1433 874L1432 871C1428 863 1425 861 1417 859C1404 857 1394 862 1391 872C1390 878 1394 880 1413 880C1428 880 1428 879 1431 877ZM620 873C617 872 614 871 613 870C610 868 602 853 600 845C599 842 597 838 596 836C594 833 593 830 592 828C591 825 589 821 588 817C586 813 584 809 583 806C582 804 580 800 579 796C577 792 575 788 575 787C574 785 572 780 569 775C567 769 565 765 565 764C565 763 563 759 562 756C560 752 557 747 556 743C556 740 553 735 552 732C550 729 548 724 547 721C545 717 543 713 543 712C542 711 540 706 539 703C538 699 536 693 534 690C532 688 530 683 529 680C529 677 527 672 525 670C523 667 522 662 521 660C520 658 519 653 517 650C516 648 513 643 513 640C512 637 509 632 507 628C506 624 504 620 503 618C502 615 500 611 498 607C497 603 495 599 494 596C493 594 492 591 491 588C489 586 487 581 486 578C485 574 483 569 482 567C479 563 473 548 469 536C467 532 465 527 464 526C463 523 455 505 451 496C450 492 448 487 446 485C445 483 443 478 442 475C441 471 439 466 438 464C436 461 434 457 434 454C433 451 431 446 429 444C428 441 426 436 425 433C424 430 422 425 420 423C419 421 417 416 416 413C414 407 408 393 403 384C401 380 398 373 396 367L393 356L395 351C402 337 416 346 424 372C425 375 427 379 428 382C430 384 432 389 433 393C434 396 436 402 438 404C439 407 441 412 442 415C443 418 445 422 446 424C448 427 450 432 451 436C452 439 454 444 456 447C457 449 459 454 460 458C462 461 464 465 464 466C465 468 467 471 468 474C469 477 471 484 474 488C476 493 478 498 478 499C478 499 479 503 481 506C483 509 485 514 486 518C487 522 489 526 490 528C492 530 493 534 494 537C496 542 498 546 507 568C510 573 512 579 513 582C514 584 516 588 517 590C519 593 521 598 521 601C522 604 524 608 525 610C527 613 529 617 530 621C531 625 534 630 535 632C537 635 538 640 539 642C540 644 542 650 544 654C553 673 556 680 556 683C557 685 559 689 560 692C562 696 565 701 566 704C566 707 569 712 570 715C571 718 573 722 574 724C575 727 577 731 579 734C580 738 582 743 583 745C584 749 588 757 596 774C598 779 600 784 601 786C601 788 603 792 605 796C606 800 609 805 610 808C611 812 613 816 614 818C615 820 617 824 618 827C620 834 627 845 630 849C632 850 634 851 765 851C838 851 899 851 902 850C910 849 909 850 910 800C910 760 911 756 912 754C918 745 931 751 932 762C933 765 933 789 933 815C932 869 933 867 924 872L920 874L772 874C657 874 623 874 620 873ZM1304 830C1298 827 1301 819 1308 819C1312 819 1313 822 1313 827C1312 832 1309 833 1304 830ZM275 744C267 739 267 735 271 725C273 722 274 716 275 714C276 712 277 707 279 704C280 702 282 697 283 694C284 691 286 687 287 684C289 682 291 677 292 674C293 670 295 665 296 663C298 660 300 655 301 652C302 648 304 643 305 642C306 641 308 636 310 631C311 626 314 621 315 619C316 617 317 613 318 611C319 609 320 605 321 602C323 600 325 594 327 589C329 584 331 578 332 576C334 573 336 569 337 566C337 563 339 559 340 557C341 556 343 551 344 547C346 544 348 538 349 535C351 533 353 528 354 524C355 521 357 516 358 513C360 511 362 506 363 503C364 500 365 495 367 492C368 489 371 484 371 481C372 478 374 473 376 470C377 468 379 463 381 459C386 442 393 436 399 442C406 449 407 458 403 466C401 469 399 474 398 477C397 480 395 485 393 489C392 493 389 498 389 502C388 505 386 509 385 510C384 512 382 516 381 520C380 523 378 527 376 529C375 531 373 536 372 540C371 545 369 551 367 553C365 556 363 561 363 564C362 567 360 571 359 574C355 580 349 598 349 601C349 605 350 605 407 606C458 606 460 607 463 609C469 613 471 623 467 628L464 630L406 630C343 630 339 630 335 634C333 637 328 645 328 647C328 648 326 652 324 656C323 660 320 666 319 670C318 674 316 679 314 682C312 684 311 688 311 690C310 691 308 695 307 699C305 703 302 709 301 713C298 720 293 733 290 738C289 741 281 746 279 746C278 746 276 745 275 744ZM841 738C835 735 836 724 842 711C844 707 847 701 847 697C848 694 850 689 852 687C853 685 855 680 856 675C857 671 859 666 860 664C862 661 864 656 865 652C866 648 868 642 870 639C871 636 873 632 873 630C874 629 876 624 878 619C880 614 882 609 882 607C883 605 884 601 886 598C888 595 890 589 891 585C892 581 894 576 896 573C897 571 899 566 900 562C904 549 909 545 921 546C930 547 933 549 935 556C937 559 938 563 940 565C941 567 943 572 944 575C945 579 947 585 949 588C951 591 952 596 953 598C954 600 955 605 957 608C959 610 961 615 962 618C962 621 965 626 966 629C968 633 970 638 971 640C972 643 973 648 975 650C977 653 979 658 979 661C980 665 982 670 984 672C986 675 988 680 988 683C989 687 991 692 993 694C995 697 997 702 997 705C998 708 1000 712 1001 713C1003 716 1008 730 1008 733C1008 736 1004 738 996 738C985 738 982 736 980 728C979 725 977 720 975 717C974 714 971 708 970 704C968 696 961 684 958 682C956 681 951 680 921 680C877 680 878 680 873 695C872 698 871 703 869 705C868 708 866 713 865 717C861 734 852 742 841 738ZM1039 738C1028 735 1019 727 1013 714C1002 692 1006 682 1023 684C1028 685 1029 687 1031 697C1033 706 1034 707 1040 712C1051 722 1066 722 1077 712C1086 704 1085 712 1086 627C1086 586 1087 552 1087 551C1089 548 1091 547 1100 546C1113 545 1112 537 1112 624C1112 707 1112 702 1104 716C1099 726 1090 734 1081 737C1076 739 1046 739 1039 738ZM1430 738C1426 737 1419 735 1415 733C1411 731 1408 729 1407 729C1407 729 1404 727 1401 725C1388 715 1380 705 1374 694C1372 691 1370 687 1369 685C1368 683 1367 681 1367 680C1367 678 1366 673 1364 667C1361 655 1361 635 1364 624C1364 620 1366 614 1367 610C1369 595 1388 568 1399 562C1400 561 1403 559 1405 558C1407 556 1412 554 1417 552C1422 551 1428 548 1430 548C1440 544 1472 545 1481 549C1483 550 1488 552 1491 553C1495 554 1499 556 1501 558C1503 559 1506 561 1508 562C1516 566 1531 584 1535 593C1535 595 1537 600 1539 603C1547 619 1547 673 1539 683C1538 685 1536 688 1535 691C1534 695 1532 698 1531 700C1529 701 1527 704 1526 707C1517 720 1492 736 1475 738C1465 739 1438 739 1430 738ZM1617 738C1601 736 1583 722 1576 707C1568 692 1569 694 1569 618L1568 551L1571 548C1576 544 1585 545 1589 551C1590 553 1591 558 1591 613L1592 674L1594 685C1598 701 1602 707 1616 714L1626 718L1642 718L1658 718L1666 715C1676 711 1682 706 1687 697C1692 687 1692 689 1693 618C1693 581 1694 551 1694 550C1696 545 1711 545 1715 549L1718 551L1718 614C1718 652 1718 679 1717 682C1710 711 1702 722 1682 732C1677 735 1671 737 1667 738C1659 739 1625 739 1617 738ZM1127 736C1125 735 1125 734 1125 732C1126 727 1130 717 1134 709C1135 705 1137 699 1138 697C1139 695 1140 690 1142 687C1144 684 1146 679 1147 675C1148 672 1150 666 1151 663C1153 660 1155 654 1156 650C1157 647 1159 642 1160 640C1161 639 1163 634 1164 630C1165 626 1167 620 1169 618C1170 615 1172 610 1173 608C1174 605 1176 600 1177 597C1179 594 1181 588 1182 584C1183 580 1185 575 1186 573C1188 570 1190 565 1191 561C1195 549 1200 545 1212 546C1221 547 1223 549 1225 554C1226 556 1228 560 1230 564C1231 567 1234 573 1235 576C1235 580 1237 585 1239 588C1241 591 1243 595 1244 598C1244 601 1246 606 1248 608C1250 611 1252 616 1252 619C1253 622 1255 627 1257 630C1258 633 1260 638 1261 640C1262 642 1263 647 1265 650C1267 652 1269 657 1270 661C1270 664 1273 669 1274 672C1276 676 1278 681 1279 684C1280 686 1281 691 1283 694C1284 696 1287 701 1287 704C1288 707 1290 712 1292 714C1301 733 1300 738 1286 738C1275 738 1273 737 1270 728C1269 725 1267 719 1265 717C1264 714 1262 709 1261 705C1259 697 1252 685 1249 683C1246 681 1245 680 1213 680C1170 680 1168 680 1164 694C1164 697 1162 701 1161 704C1159 706 1157 713 1155 719C1153 725 1151 730 1149 733L1145 738L1137 738C1131 738 1129 738 1127 736ZM778 732C770 727 771 741 770 598C770 482 769 471 768 469C765 467 762 469 760 474C759 477 757 481 755 483C754 485 752 489 751 492C750 496 748 500 747 503C745 505 743 509 742 512C742 515 739 519 737 522C736 525 733 530 732 533C732 536 730 540 728 543C727 545 725 549 724 552C723 556 721 560 720 562C718 565 716 569 715 572C714 575 712 580 710 583C709 586 707 590 706 592C705 595 703 599 701 603C700 606 698 609 698 610C698 611 696 615 694 620C692 624 689 629 688 632C688 635 686 639 684 642C683 644 681 648 680 652C679 655 677 659 675 662C674 664 672 668 671 671C670 674 666 683 662 690C659 698 655 708 653 711C645 737 628 734 619 706C618 703 616 697 613 692C606 676 600 663 600 662C600 662 596 653 591 642C586 632 582 623 582 622C582 621 580 618 579 614C572 602 566 589 564 583C563 580 562 576 560 574C559 572 557 568 556 565C555 562 553 557 551 553C546 543 539 529 539 528C539 527 531 509 525 498C524 494 522 489 521 486C520 484 518 480 517 478C515 475 513 470 512 467C511 464 509 460 507 458C506 456 505 452 504 449C503 446 500 442 499 440C495 435 495 426 498 423C505 416 516 422 521 434C522 437 524 441 525 443C528 449 536 466 539 475C540 479 543 483 544 485C545 486 546 489 547 492C548 494 550 499 552 502C554 506 556 512 557 515C558 518 560 522 562 524C563 526 565 530 566 533C566 536 569 541 570 544C572 548 574 552 575 554C576 557 578 561 580 565C581 568 583 571 583 572C583 573 591 590 597 601C598 605 600 609 600 609C600 610 602 615 604 620C607 625 609 630 610 632C611 635 613 639 614 641C616 644 618 648 618 650C620 656 631 678 634 681C639 686 642 685 644 676C645 673 647 668 649 666C651 664 652 660 653 658C654 655 656 650 658 645C660 641 664 633 666 629C668 624 670 619 671 616C672 614 674 610 676 607C677 604 679 600 680 598C681 595 683 591 684 589C686 587 688 582 688 578C689 575 691 571 693 569C694 567 696 563 697 560C698 557 700 552 702 548C704 544 706 539 707 536C708 533 710 530 711 528C712 526 714 523 715 520C716 517 718 512 720 508C721 505 723 501 724 500C724 499 726 494 729 489C731 484 733 479 733 478C733 478 735 474 736 470C738 467 741 461 742 458C743 455 745 452 745 450C746 449 748 445 749 441C753 432 757 426 761 423C766 420 782 420 786 424C793 429 792 416 792 578L792 724L790 728C786 733 782 735 778 732ZM1466 719C1488 716 1512 694 1516 672C1521 648 1519 613 1513 603C1511 601 1509 598 1508 595C1506 591 1499 584 1492 578C1474 564 1435 563 1416 577C1404 586 1395 597 1393 607C1392 610 1391 615 1390 618C1387 626 1386 648 1388 658C1394 701 1424 724 1466 719ZM947 658C951 655 951 652 948 646C946 643 945 639 944 636C943 634 941 629 940 626C938 623 936 617 935 613C934 610 932 604 930 600C929 596 927 592 926 590C925 581 922 577 919 579C916 579 911 590 909 598C908 603 906 609 904 612C902 615 901 620 900 623C899 626 897 632 895 635C888 651 888 657 895 659C901 661 945 660 947 658ZM1238 658C1242 656 1242 653 1239 648C1237 645 1235 640 1234 636C1233 631 1231 626 1230 625C1229 623 1227 618 1226 614C1225 610 1223 605 1222 603C1221 601 1219 596 1217 591C1214 581 1213 579 1209 581C1205 582 1202 587 1200 598C1199 602 1197 608 1195 611C1193 614 1191 620 1190 623C1190 626 1188 632 1186 635C1178 650 1178 658 1186 659C1197 661 1236 659 1238 658ZM1609 532C1605 529 1604 516 1606 512C1610 506 1628 507 1630 514C1630 517 1629 528 1628 530C1626 534 1612 536 1609 532ZM1660 533C1656 531 1654 513 1658 511C1665 506 1676 508 1678 514C1679 518 1677 528 1675 531C1673 534 1665 535 1660 533ZM12 339C5 332 8 320 18 315C31 308 35 306 37 303C38 302 41 300 44 299C48 297 58 291 66 285C68 284 72 281 74 280C77 278 83 275 87 272C91 269 97 266 99 265C102 263 106 260 108 259C113 256 123 249 132 243C149 233 152 231 172 219C179 214 186 209 186 208C187 206 188 184 188 119C189 23 188 31 196 26L200 24L257 23C294 23 318 23 323 24C339 26 338 25 339 71C340 111 339 110 346 111C349 111 351 110 361 104C367 100 374 95 376 94C387 87 401 79 404 76C406 75 411 72 415 70C428 62 433 59 437 56C440 54 446 50 450 48C454 45 460 42 461 40C463 39 467 37 469 36C472 34 476 31 478 30C481 28 486 24 490 22C498 18 501 15 507 11C511 8 523 9 528 13C536 18 539 21 544 24C547 25 551 28 554 30C556 32 560 34 562 35C565 36 568 38 570 40C572 41 576 44 579 45C581 47 585 49 587 50C588 51 593 54 596 56C600 59 605 62 608 64C610 65 615 68 618 70C620 71 624 73 625 75C626 76 629 78 631 79C635 80 640 83 651 91C653 92 656 94 657 95C659 96 662 98 665 100C667 101 672 104 674 105C676 106 679 108 681 109C682 110 685 112 689 114C692 115 695 118 696 118C697 119 699 121 701 122C703 123 707 126 710 127C712 129 716 132 718 132C721 134 726 137 736 144C738 146 742 148 744 149C747 150 749 152 750 153C751 153 755 156 758 158C762 160 767 162 768 163C772 167 786 175 797 182C800 183 804 186 807 188C809 189 813 192 815 193C818 194 821 196 822 198C824 199 828 201 830 203C833 204 837 206 839 208C840 209 842 210 842 210C843 210 848 213 855 218C861 222 869 227 872 229C875 230 879 233 881 234C887 237 900 246 907 250C910 252 915 255 918 257C922 259 926 262 929 264C931 265 934 267 936 268C937 269 939 271 941 272C943 272 947 275 949 277C952 278 955 280 956 281C958 281 962 284 965 286C969 289 973 291 975 292C976 293 980 296 984 298C987 300 992 303 994 305C1019 319 1024 326 1016 336C1014 338 1012 340 1011 340C1008 340 996 334 990 329C987 327 984 325 984 325C983 325 978 322 963 312C960 310 957 308 956 308C955 308 941 299 934 294C932 293 929 290 926 289C924 288 921 286 919 284C916 282 914 281 914 281C913 281 909 279 904 276C900 273 894 269 891 267C888 265 882 261 877 258C872 255 866 252 863 250C860 248 855 244 851 242C847 239 843 237 843 237C842 237 840 235 837 234C834 232 831 229 829 228C825 226 812 218 810 216C808 215 805 213 803 212C801 211 796 208 794 206C791 204 789 203 788 203C788 203 784 201 780 198C776 196 770 192 766 190C760 186 755 182 737 171C733 168 728 165 725 163C722 162 718 159 715 158C709 154 700 149 695 145C693 144 690 141 687 140C685 139 682 137 680 135C678 134 672 130 668 128C663 126 658 122 656 120C653 118 650 116 647 115C645 114 640 111 636 109C633 106 627 103 623 100C615 95 607 91 599 85C596 83 591 80 588 79C586 77 582 75 580 74C579 72 575 70 572 69C570 67 566 65 564 64C555 57 551 55 546 53C544 51 539 49 537 47C518 34 514 33 504 40C501 42 495 46 490 49C486 52 481 55 479 57C475 59 473 60 461 68C456 71 442 79 435 84C430 87 419 95 409 101C406 103 401 106 398 108C395 110 390 113 387 114C384 116 380 118 379 119C378 120 373 123 368 126C358 133 357 134 344 142C335 149 334 149 329 149C317 149 317 150 317 97C316 49 317 50 309 47C305 46 223 45 219 47C212 49 212 48 212 136C212 211 212 215 210 218C208 222 201 228 200 228C199 228 196 230 193 232C190 234 186 237 184 237C182 238 179 240 178 242C176 243 172 245 169 247C166 249 162 251 161 252C157 255 145 263 131 271C128 272 125 275 123 276C121 278 117 280 114 281C111 283 108 285 107 285C107 286 104 288 101 290C93 294 85 299 81 303C79 304 75 307 73 308C70 309 66 312 64 314C59 317 57 318 46 324C42 327 35 331 30 334C20 341 15 343 12 339Z"/>
      </svg>
      <p class="avapilt-rida">Arhitektuurne projekteerimine üle Eesti</p>
    </div>
    <a class="avapilt-kerimine" href="#tood" aria-label="Keri tööde juurde">
      <span>Tööd</span>
      <span class="nool" aria-hidden="true">\u2193</span>
    </a>
  </section>

  <section class="tood-osa" id="tood" aria-labelledby="tood-pealkiri">
    <h2 id="tood-pealkiri" class="visuaalselt-peidus">Valik töid</h2>
    <div class="tood-ruudustik">
''' + kaardid(AVALEHE_JARJEKORD, AVALEHE_LAIAD) + '''
    </div>
    <div class="raam tood-lopp">
      <a href="/tood.html" class="nupp">Kogu portfoolio</a>
    </div>
  </section>

  <section class="triip" aria-labelledby="triip-pealkiri">
    <div class="raam triip-sisu">
      <p class="silt">A-MAJA OÜ</p>
      <h2 id="triip-pealkiri">Üksikelamud, juurdeehitused ja suuremad objektid. Eskiisist ehitusloani.</h2>
      <div class="triip-lingid">
        <a href="/teenused.html" class="link-nool">Teenused</a>
        <a href="/meist.html" class="link-nool">Meist</a>
        <a href="/kontakt.html" class="link-nool">Küsi pakkumist</a>
      </div>
    </div>
  </section>

  <section class="tsitaadiriba" aria-labelledby="tsitaat-pealkiri">
    <div class="raam">
      <p class="silt">Tagasiside</p>
      <h2 id="tsitaat-pealkiri">Kliendid räägivad</h2>
      <p class="sissejuhatus">Keskmine hinnang 4,9 tellijate antud tagasiside põhjal.</p>

      <div class="tsitaadid">
        <blockquote class="tsitaat">
          <p class="hinne"><span aria-hidden="true">★★★★★</span> <span class="visuaalselt-peidus">Hinnang 5 punkti 5-st</span></p>
          <p>Väga proaktiivne ja lahenduskeskne tegija. Leiab parima ja tõhusama lahenduse. Töö kvaliteetne ja kiire. Hindan väga, et võttis oma peale kogu suhtluse omavalitsusega ja tegi seda tulemuslikult.</p>
          <footer>Veronika T.<span>Eramaja ehitusprojekti koostamine, september 2025</span></footer>
        </blockquote>
        <blockquote class="tsitaat">
          <p class="hinne"><span aria-hidden="true">★★★★★</span> <span class="visuaalselt-peidus">Hinnang 5 punkti 5-st</span></p>
          <p>Väga asjalik projekteerija, soovitan! Koostöö sujus ja ehitusluba käes.</p>
          <footer>Ivar K.<span>Maja projekt, detsember 2023</span></footer>
        </blockquote>
      </div>

      <a href="/tagasiside.html" class="nupp nupp-tyhi">Loe kõiki hinnanguid</a>
    </div>
  </section>

  <section class="kutse" aria-labelledby="kutse-pealkiri">
    <div class="raam kutse-sisu">
      <div>
        <p class="silt">Kontakt</p>
        <h2 id="kutse-pealkiri">Räägime teie objektist</h2>
        <p class="juhtlause">Kirjeldage lühidalt, mida plaanite. Vastame, mis mahus projekti on vaja.</p>
      </div>
      <div class="kutse-kontakt">
        <a href="tel:+37253874959" class="suur-link">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com" class="suur-link">info@a-maja.com</a>
        <a href="/kontakt.html" class="nupp">Saada hinnapäring</a>
      </div>
    </div>
  </section>
'''.replace("\\u2193", "\u2193")

leht("index.html",
     "Arhitektuurne projekteerimine üle Eesti | A-MAJA OÜ",
     "Diplomeeritud arhitekt, tase 7. Eramute, juurdeehituste ja abihoonete projektid ehitusteatise või ehitusloa mahus. Töid võtame vastu üle Eesti.",
     "/", avaleht, [ETTEVOTE, teenus_ld()], akt="/")

# ---------------------------------------------------------------- TEENUSED

TEENUSEPILDID = {
 "uksikelamu": ("/pildid/eramu-must-vertikaalne-puitlaudis-metsas.webp",1600,893,
   "Musta vertikaalse puitlaudisega üksikelamu järsu viilkatuse ja suure kaldaknaga männimetsas."),
 "rekonstrueerimine": ("/pildid/eramu-juurdeehitus-puitribifassaadiga.webp",1600,1200,
   "Olemasoleva krohvitud eramu tänavavaade koos uue puitribifassaadiga juurdeehitusega."),
 "abihoone": ("/pildid/eramu-tume-puitfassaad-01.webp",1800,764,
   "Sinakashalli püstlaudise ja valtsplekk-katusega üksikelamu metsaserval, kõrge klaasitud viil ja munakivitee."),
 "arihoone": ("/pildid/suvekohvik-raatuse-tanav-tartu-projekt.webp",1200,655,
   "Suvekohviku hoone Raatuse tänaval Tartus, puitlaudisega paviljon ja haljastatud katuseterrass."),
 "ehitusteatis": ("/pildid/eramu-kelpkatus-garaaz-maakivi.webp",1600,733,
   "Ühekorruseline kelpkatusega elamu valge krohvfassaadi ja kahe auto garaažiga."),
 "asjaajamine": ("/pildid/eramu-kahekorruseline-lamekatus-krohv-puit.webp",1600,1122,
   "Kahekorruseline lamekatusega elamu heleda krohvfassaadi ja puitlaudisega aktsentribadega."),
}


def teenus_plokk_paar():
    read = []
    for ank, num, pealkiri, tekst in [
        ("ehitusteatis", "05", "Eelprojekt ehitusteatise mahus",
         "Kõik ehitised ei vaja ehitusluba. Osa juhtudest lahendab ehitusteatis, mille jaoks on vaja eelprojekti. Kontrollime enne töö alustamist ära, kumb menetlus teie ehitisele kehtib, et te ei maksaks suurema mahu eest kui vaja."),
        ("asjaajamine", "06", "Asjaajamine omavalitsusega",
         "Projekti esitamine, puuduste kõrvaldamine ja kirjavahetus ametnikega käib meie poolelt. See on osa tööst, mitte eraldi lisateenus. Te ei pea ise ehitisregistris orienteeruma ega menetlust jälgima."),
    ]:
        src, w, h, alt = TEENUSEPILDID[ank]
        read.append(f'''    <article class="paar-kaart" id="{ank}">
      <a href="{src}" aria-label="Vaata suurelt: {pealkiri}">
        <img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}">
      </a>
      <div class="paar-tekst">
        <span class="teenus-number">{num}</span>
        <h2>{pealkiri}</h2>
        <p>{tekst}</p>
      </div>
    </article>''')
    return chr(10).join(read) + chr(10)


def teenus_plokk(ank, num, pealkiri, sisu, poole="vasak"):
    src, w, h, alt = TEENUSEPILDID[ank]
    return f'''  <section class="teenus teenus-{poole}" id="{ank}">
    <div class="raam teenus-ruudustik">
      <figure class="teenus-pilt">
        <a href="{src}" aria-label="Vaata suurelt: {pealkiri}">
          <img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}">
        </a>
        <figcaption><span class="teenus-number">{num}</span></figcaption>
      </figure>
      <div class="teenus-tekst">
        <h2>{pealkiri}</h2>
{sisu}
      </div>
    </div>
  </section>
'''


teenused = puru("Teenused") + '''  <section class="teenus-avapilt">
    <img src="/pildid/eramu-punane-laudis-valge-piirdelaud.webp" width="1600" height="893"
         fetchpriority="high"
         alt="Punase püstlaudise ja valgete piirdelaudadega elamu musta valtsplekk-katuse ja telliskorstnaga maastikus.">
    <div class="teenus-avapilt-sisu">
      <div class="raam">
        <p class="silt">Teenused</p>
        <h1>Eskiisist ehitusloani</h1>
        <p class="juhtlause">Iga projekt algab sellest, et vaatame üle krundi, kehtivad piirangud ja teie soovid. Alles siis saab öelda, mis mahus projekti on tegelikult vaja.</p>
      </div>
    </div>
  </section>

''' + teenus_plokk("uksikelamu", "01", "Üksikelamu projekt", '''        <p>Uue eramu arhitektuurne projekt algab eskiisist ja lõpeb dokumentidega, millega saab ehitusloa taotleda. Vaatame läbi detailplaneeringu või projekteerimistingimused ning kontrollime, mis on krundil üldse lubatud.</p>
        <p>Lahenduse kujundame teie elukorralduse järgi. Kui plaan on kolm magamistuba, aga eelarve kannab kahte, ütleme seda kohe.</p>
        <ul>
          <li>Eskiislahendus ja mahulised variandid</li>
          <li>Eelprojekt ehitusloa taotlemiseks</li>
          <li>Põhiprojekt ehitajale ja ehituse jaoks</li>
          <li>Kooskõlastused ja suhtlus omavalitsusega</li>
        </ul>''', "vasak") \
+ teenus_plokk("rekonstrueerimine", "02", "Juurdeehitus ja rekonstrueerimine", '''        <p>Olemasoleva hoone laiendamine, ümberehitamine või kasutusotstarbe muutmine. Alustame sellest, mis on tegelikult olemas, sest vanade hoonete puhul erineb see sageli dokumentides kirjapandust.</p>
        <p>Rekonstrueerimisprojekt on tavaliselt keerukam kui uus maja, sest lahendus peab arvestama kandekonstruktsiooni, olemasolevaid kõrgusi ja seda, mida saab reaalselt lammutada.</p>
        <ul>
          <li>Olemasoleva olukorra ülevaatus</li>
          <li>Juurdeehituse mahuline lahendus</li>
          <li>Rekonstrueerimisprojekt ehitusloa mahus</li>
          <li>Kasutusotstarbe muutmise projekt</li>
        </ul>''', "parem") \
+ '''  <section class="vahepilt">
    <img src="/pildid/eramu-lamekatus-kivifassaad-varjualune.webp" width="1600" height="1204" loading="lazy"
         alt="Lamekatusega üksikelamu heleda kivifassaadi, tumeda karniisi ja avatud autovarjualusega tänava ääres.">
    <p class="vahepilt-tekst">Piirangud tulevad krundiga kaasa. Hea lahendus arvestab nendega algusest peale.</p>
  </section>

''' + teenus_plokk("abihoone", "03", "Abihoone ja aiamaja", '''        <p>Saunad, garaažid, kuurid, varjualused ja aiamajad. Väiksemate hoonete puhul piisab sageli ehitusteatisest, mis on kiirem ja odavam tee kui täismahus ehitusluba.</p>
        <p>Ütleme kohe alguses, kumb variant teie hoone puhul kehtib, sest see määrab nii projekti mahu kui ka hinna.</p>
        <ul>
          <li>Aiamaja ja saunamaja projektid</li>
          <li>Garaaži ja abihoone projektid</li>
          <li>Moodulmaja projektid</li>
        </ul>''', "vasak") \
+ teenus_plokk("arihoone", "04", "Ärihoone ja suurem objekt", '''        <p>Korterelamud, ärihooned ja muud suuremad mahud. Kaheksa aasta kogemus ei piirdu üksikelamutega, seega tasub küsida ka siis, kui objekt on tavapärasest suurem.</p>
        <p>Suuremate objektide puhul lepime eraldi kokku, milline osa projektist meie käes on ja millised osad tulevad teistelt eriosade projekteerijatelt.</p>
        <ul>
          <li>Korterelamu arhitektuurne projekt</li>
          <li>Ärihoone arhitektuurne projekt</li>
          <li>Mahulised eskiisid ja visualiseeringud</li>
        </ul>''', "parem") \
+ '''  <section class="paar">
''' + teenus_plokk_paar() + '''  </section>

  <section class="kutse">
    <div class="raam kutse-sisu">
      <div>
        <p class="silt">Järgmine samm</p>
        <h2>Ei tea, mis mahus projekti vajate?</h2>
        <p class="juhtlause">Kirjeldage objekti paari lausega. Ütleme, kas piisab ehitusteatisest või on vaja ehitusluba.</p>
      </div>
      <div class="kutse-kontakt">
        <a href="tel:+37253874959" class="suur-link">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com" class="suur-link">info@a-maja.com</a>
        <a href="/kontakt.html" class="nupp">Saada hinnapäring</a>
      </div>
    </div>
  </section>
'''

leht("teenused.html",
     "Projekteerimisteenused | A-MAJA OÜ arhitektibüroo",
     "Eramu, juurdeehituse, abihoone ja ärihoone projektid. Eelprojekt, põhiprojekt, ehitusteatis ja ehitusluba. Diplomeeritud arhitekt, tase 7.",
     "/teenused.html", teenused,
     [teenus_ld(), puru_ld("Teenused", "/teenused.html")], akt="/teenused.html")

# ---------------------------------------------------------------- TOOD


tood = puru("Portfoolio") + '''  <section class="teenus-avapilt teenus-avapilt-klopsitav">
    ''' + avapilt_link("eramu-terrakota-plekkfassaad-viilkatus.webp") + '''
    <div class="teenus-avapilt-sisu">
      <div class="raam">
        <p class="silt">Portfoolio</p>
        <h1>Tehtud tööd</h1>
        <p class="juhtlause">Üksikelamud, juurdeehitused, kortermajad ja ärihooned. Klõps avab pildi suurelt koos projekti joonistega.</p>
      </div>
    </div>
  </section>

  <section class="tood-osa">
    <div class="tood-ruudustik">
''' + kaardid(TOOD_JARJEKORD, TOOD_LAIAD) + '''
    </div>
  </section>


  <section class="kutse">
    <div class="raam kutse-sisu">
      <div>
        <p class="silt">Järgmine samm</p>
        <h2>Sarnane projekt plaanis?</h2>
        <p class="juhtlause">Vaadake üle <a href="/teenused.html">teenuste leht</a> või kirjutage kohe, mis objektiga tegu on.</p>
      </div>
      <div class="kutse-kontakt">
        <a href="tel:+37253874959" class="suur-link">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com" class="suur-link">info@a-maja.com</a>
        <a href="/kontakt.html" class="nupp">Saada hinnapäring</a>
      </div>
    </div>
  </section>
'''

leht("tood.html",
     "Portfoolio, tehtud tööd | A-MAJA OÜ arhitektibüroo",
     "Eramud, korterelamud, juurdeehitused ja ärihooned koos projektijoonistega. Vaadake A-MAJA OÜ tehtud töid ja visualiseeringuid.",
     "/tood.html", tood,
     [puru_ld("Portfoolio", "/tood.html")], akt="/tood.html")

# ---------------------------------------------------------------- TAGASISIDE

HINNANGUD = [
 ("Eramaja ehitusprojekti koostamine","5,0","01.09.2025",5,5,5,
  "Väga proaktiivne ja lahenduskeskne tegija. Leiab parima ja tõhusama lahenduse. Töö kvaliteetne ja kiire. Hindan väga, et võttis oma peale kogu suhtluse omavalitsusega ja tegi seda tulemuslikult.",
  "Veronika T."),
 ("Projekt eramu rekonstrueerimiseks","4,7","06.07.2025",5,5,4,
  "Projekteerija mõtleb sinuga kaasa ja pakub ise lahendusi.","Siim V."),
 ("Eelprojekti koostamine ehitusteatise mahus","4,7","10.04.2025",5,5,4,
  None,None),
 ("30 m² moodulmaja ehitusprojekt","5,0","22.07.2024",5,5,5,
  "Töö suurepärane ja professionaalne. Kommunikatsioon teostajaga sujus, vastas vajadusel lisaküsimustele. Soovitan!","Rainer S."),
 ("Eelprojekti koostamine ja ehitusteatise esitamine","5,0","19.07.2024",5,5,5,
  "Asjalik ja tellijaga kaasamõtlev projekteerija.","Kuldar K."),
 ("Maja projekt","5,0","06.12.2023",5,5,5,
  "Väga asjalik projekteerija, soovitan! Koostöö sujus ja ehitusluba käes.","Ivar K."),
 ("Projekteerimine","5,0","08.09.2023",5,5,5,
  "Teab ja tunneb oma tööd väga hästi. Töö kiire ja korralik.","Ravo T."),
]

def hinnang_kirje(h):
    pealkiri, punkt, kuup, kiirus, kvaliteet, hind, tekst, autor = h
    tekst_html = f"        <p>{tekst}</p>\n" if tekst else ""
    autor_html = f'        <p class="hinnang-autor">{autor}</p>\n' if autor else ""
    return f'''      <article class="hinnang">
        <div class="hinnang-pais">
          <h3>{pealkiri}</h3>
          <span class="hinnang-punkt">{punkt}</span>
        </div>
        <p class="hinnang-kuup">{kuup}</p>
        <p class="mootrida">
          <span>Töökiirus <b>{kiirus}/5</b></span>
          <span>Kvaliteet <b>{kvaliteet}/5</b></span>
          <span>Hind <b>{hind}/5</b></span>
        </p>
{tekst_html}{autor_html}      </article>'''

tagasiside = puru("Tagasiside") + f'''  <section class="lehe-pais">
    <div class="raam">
      <p class="silt">Tagasiside</p>
      <h1>Kliendid räägivad</h1>
      <p class="juhtlause">Kõik hinnangud on tellijate antud pärast töö valmimist. Ühtegi arvustust ei ole siia juurde kirjutatud.</p>

      <div class="hinne-kokku">
        <span class="arv">4,9</span>
        <div>
          <p>Keskmine hinnang kõigi seni antud tagasisidede põhjal.</p>
          <p>Hinnatakse töökiirust, kvaliteeti ja hinda.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="lohik">
    <div class="raam">
      <p class="silt">01 / Hinnangud</p>
      <h2>Kõik hinnangud</h2>
      <div class="hinnangud">
{chr(10).join(hinnang_kirje(h) for h in HINNANGUD)}
      </div>
    </div>
  </section>

  <section class="vahepilt">
    <img src="/pildid/eramu-tume-puitfassaad-01.webp" width="1800" height="764" loading="lazy"
         alt="Sinakashalli püstlaudise ja valtsplekk-katusega üksikelamu metsaserval, kõrge klaasitud viil ja munakivitee.">
    <p class="vahepilt-tekst">Iga hinnangu taga on valmis projekt.</p>
  </section>

  <section class="kutse">
    <div class="raam kutse-sisu">
      <div>
        <p class="silt">Järgmine samm</p>
        <h2>Alustame teie projektiga</h2>
        <p class="juhtlause">Vaadake <a href="/tood.html">portfooliot</a> või kirjutage kohe, mis objekti plaanite.</p>
      </div>
      <div class="kutse-kontakt">
        <a href="tel:+37253874959" class="suur-link">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com" class="suur-link">info@a-maja.com</a>
        <a href="/kontakt.html" class="nupp">Saada hinnapäring</a>
      </div>
    </div>
  </section>
'''

leht("tagasiside.html",
     "Klientide tagasiside | A-MAJA OÜ arhitektibüroo",
     "Keskmine hinnang 4,9. Lugege, mida tellijad A-MAJA OÜ arhitektuurse projekteerimise töö kohta ütlevad.",
     "/tagasiside.html", tagasiside,
     [puru_ld("Tagasiside", "/tagasiside.html")], akt="/tagasiside.html")

# ---------------------------------------------------------------- MEIST

meist = puru("Meist") + '''  <section class="lehe-pais">
    <div class="raam">
      <p class="silt">Meist</p>
      <h1>Üks arhitekt, kes viib projekti lõpuni</h1>
    </div>
  </section>

  <section class="meist-tutvustus">
    <div class="raam meist-ruudustik">
      <figure class="meist-pilt">
        <img src="/pildid/eramu-tume-puitlaudis-viilkatus-mannimetsas.webp" width="1200" height="1474"
             alt="Tumeda vertikaalse puitlaudisega kahekorruseline elamu männimetsas, avatud terrass ja kõrged aknad viilus.">
      </figure>
      <div class="meist-tekst">
        <p class="juhtlause">A-MAJA OÜ on arhitektuurialane ettevõte. Projekteerime nii väiksemaid hooneid, üksikelamuid, juurdeehitusi ja aiamaju, kui ka suuremaid objekte.</p>
        <p>Ettevõtte taga seisab diplomeeritud arhitekt, tase 7, kutsetunnistus 203786. Kaheksa aastat projekteerimiskogemust. Töid võtame vastu üle Eesti ning pöörduda võivad nii eraisikud kui ka ettevõtted.</p>
        <div class="meist-arvud">
          <div><span class="arv">8</span><span class="arv-silt">aastat kogemust</span></div>
          <div><span class="arv">7</span><span class="arv-silt">kutsetase</span></div>
          <div><span class="arv">4,9</span><span class="arv-silt">keskmine hinnang</span></div>
          <div><span class="arv">15</span><span class="arv-silt">maakonda</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="lohik">
    <div class="raam kaks-veergu">
      <div>
        <p class="silt">Miks meid</p>
        <h2>Neli asja, mis vahet teevad</h2>
      </div>
      <div class="loend">
        <div class="loend-rida">
          <h3>Kutsetunnistusega arhitekt</h3>
          <p>Ettevõtte taga seisab diplomeeritud arhitekt, tase 7, kutsetunnistus 203786. Kaheksa aastat projekteerimiskogemust.</p>
        </div>
        <div class="loend-rida">
          <h3>Suhtlus omavalitsusega meie poolelt</h3>
          <p>Võtame kooskõlastuste ajamise enda peale, et teie ei peaks ametiasutustega ise kirjavahetust pidama.</p>
        </div>
        <div class="loend-rida">
          <h3>Otsekontakt, mitte projektijuht vahel</h3>
          <p>Räägite kogu projekti vältel sama inimesega, kes joonised teeb. Küsimused ei jää kellegi vahele kinni.</p>
        </div>
        <div class="loend-rida">
          <h3>Terve Eesti</h3>
          <p>Tegevuspiirkond katab kõik viisteist maakonda. Objekti asukoht ei ole takistus.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="vahepilt">
    <img src="/pildid/eramu-must-vertikaalne-puitlaudis-metsas.webp" width="1600" height="893" loading="lazy"
         alt="Musta vertikaalse puitlaudisega üksikelamu järsu viilkatuse ja suure kaldakna all oleva elutoaga männimetsas.">
    <p class="vahepilt-tekst">Projekteerime üle Eesti, eraisikutele ja ettevõtetele.</p>
  </section>

  <section class="kutse">
    <div class="raam kutse-sisu">
      <div>
        <p class="silt">Kontakt</p>
        <h2>Alustame teie projektiga</h2>
        <p class="juhtlause">Vaadake <a href="/tood.html">portfooliot</a> või kirjutage kohe, mis objekti plaanite.</p>
      </div>
      <div class="kutse-kontakt">
        <a href="tel:+37253874959" class="suur-link">+372 5387 4959</a>
        <a href="mailto:info@a-maja.com" class="suur-link">info@a-maja.com</a>
        <a href="/kontakt.html" class="nupp">Saada hinnapäring</a>
      </div>
    </div>
  </section>
'''

leht("meist.html",
     "Meist, arhitekt Kaspar Lätt | A-MAJA OÜ",
     "Diplomeeritud arhitekt, tase 7, kutsetunnistus 203786. Kaheksa aastat projekteerimiskogemust. Võtame suhtluse omavalitsusega enda peale.",
     "/meist.html", meist,
     [ETTEVOTE, puru_ld("Meist", "/meist.html")], akt="/meist.html")

# ---------------------------------------------------------------- KONTAKT

kontakt = puru("Kontakt") + '''  <section class="lehe-pais">
    <div class="raam">
      <p class="silt">Kontakt</p>
      <h1>Küsi hinnapakkumist</h1>
      <p class="juhtlause">Kirjeldage objekti paari lausega. Vastame tavaliselt tööpäeva jooksul ja ütleme, mis mahus projekti on vaja.</p>
    </div>
  </section>

  <section class="lohik">
    <div class="raam kontakt-ruudustik">
      <div>
        <p class="silt">01 / Hinnapäring</p>
        <h2>Saada päring</h2>

        <form class="vorm" id="paringu-vorm" data-paring novalidate>
          <p class="vormi-teade" id="vormi-teade" role="alert" aria-live="polite" hidden></p>

          <div class="vali">
            <label for="nimi">Nimi <span aria-hidden="true">*</span></label>
            <input type="text" id="nimi" name="nimi" autocomplete="name" required>
          </div>

          <div class="vali">
            <label for="ettevote">Ettevõte</label>
            <input type="text" id="ettevote" name="ettevote" autocomplete="organization">
          </div>

          <div class="vali">
            <label for="epost">E-post <span aria-hidden="true">*</span></label>
            <input type="email" id="epost" name="epost" autocomplete="email" required>
          </div>

          <div class="vali">
            <label for="telefon">Telefon</label>
            <input type="tel" id="telefon" name="telefon" autocomplete="tel">
          </div>

          <fieldset class="vorm-raam">
            <legend>Mis laadi töö?</legend>
            <div class="raadiorida">
              <label class="raadio"><input type="radio" name="liik" value="uus" checked> Uus hoone</label>
              <label class="raadio"><input type="radio" name="liik" value="uuendus"> Olemasoleva uuendus</label>
              <label class="raadio"><input type="radio" name="liik" value="muu"> Muu</label>
            </div>
          </fieldset>

          <div class="vali" id="olemasolev-plokk" hidden>
            <label for="olemasolev">Olemasoleva hoone aadress</label>
            <input type="text" id="olemasolev" name="olemasolev">
            <span class="abitekst">Aadress aitab meil ehitisregistrist olemasolevad andmed üle vaadata.</span>
          </div>

          <div class="vali">
            <label for="sonum">Kirjeldus <span aria-hidden="true">*</span></label>
            <textarea id="sonum" name="sonum" required></textarea>
            <span class="abitekst">Kasulik on teada: objekti asukoht, ligikaudne suurus ruutmeetrites, ehituse plaanitav aeg ja see, kas krundil on detailplaneering või projekteerimistingimused. Kui te neid ei tea, kirjutage lihtsalt, mida soovite.</span>
          </div>

          <div class="nousolek">
            <input type="checkbox" id="nousolek" name="nousolek" required>
            <label for="nousolek">Nõustun, et A-MAJA OÜ töötleb minu andmeid päringule vastamiseks. Loe <a href="/privaatsus.html">privaatsustingimusi</a>.</label>
          </div>

          <div class="meepott" aria-hidden="true">
            <label for="veebiaadress">Jätke see väli tühjaks</label>
            <input type="text" id="veebiaadress" name="veebiaadress" tabindex="-1" autocomplete="off">
          </div>

          <div>
            <button type="submit" class="nupp" data-saada>Saada päring</button>
          </div>
        </form>
      </div>

      <div>
        <p class="silt">02 / Otsekontakt</p>
        <h2>Kirjuta või helista</h2>

        <div class="kontakt-plokk">
          <h3>Telefon</h3>
          <p><a href="tel:+37253874959">+372 5387 4959</a></p>
        </div>
        <div class="kontakt-plokk">
          <h3>E-post</h3>
          <p><a href="mailto:info@a-maja.com">info@a-maja.com</a></p>
        </div>
        <div class="kontakt-plokk">
          <h3>Kontaktisik</h3>
          <p>Kaspar Lätt, juhatuse liige</p>
        </div>
        <div class="kontakt-plokk">
          <h3>Aadress</h3>
          <p>Sõle tn 27d-31<br>Põhja-Tallinna linnaosa<br>Tallinn</p>
        </div>
        <div class="kontakt-plokk">
          <h3>Tegevuspiirkond</h3>
          <p>Kogu Eesti, kõik viisteist maakonda.</p>
        </div>
        <div class="kontakt-plokk">
          <h3>Ettevõte</h3>
          <p>A-MAJA OÜ<br>Registrikood 16765213<br>KMKR EE102766103</p>
        </div>
      </div>
    </div>
  </section>

  <section class="vahepilt vahepilt-tyhi">
    <img src="/pildid/eramu-kelpkatus-garaaz-maakivi.webp" width="1600" height="733" loading="lazy"
         alt="Ühekorruseline kelpkatusega elamu valge krohvfassaadi, maakiviga sissepääsu ja kahe auto garaažiga.">
  </section>

'''

kontakt_ld = dict(ETTEVOTE)
leht("kontakt.html",
     "Kontakt ja hinnapäring | A-MAJA OÜ arhitektibüroo",
     "Küsi arhitektuurse projekteerimise hinnapakkumist. Telefon +372 5387 4959, e-post info@a-maja.com. Töid võtame vastu üle Eesti.",
     "/kontakt.html", kontakt,
     [kontakt_ld, puru_ld("Kontakt", "/kontakt.html")], akt="/kontakt.html")

# ---------------------------------------------------------------- AITAH

aitah = '''  <section class="vealeht">
    <div class="raam">
      <p class="silt">Päring saadetud</p>
      <h1>Aitäh, päring on kohal</h1>
      <p class="juhtlause">Vastame tavaliselt ühe tööpäeva jooksul. Kui asi on kiire, helistage julgelt numbril <a href="tel:+37253874959">+372 5387 4959</a>.</p>
      <div class="nupurida">
        <a href="/" class="nupp">Tagasi avalehele</a>
        <a href="/tood.html" class="nupp nupp-tyhi">Vaata tehtud töid</a>
      </div>
    </div>
  </section>
'''
leht("aitah.html", "Aitäh, päring on saadetud | A-MAJA OÜ",
     "Teie hinnapäring on kohale jõudnud. Vastame tavaliselt ühe tööpäeva jooksul.",
     "/aitah.html", aitah, [], noindex=True)

# ---------------------------------------------------------------- 404

nelisada = '''  <section class="vealeht">
    <div class="raam">
      <p class="number">404</p>
      <h1>Sellist lehte ei ole</h1>
      <p class="juhtlause">Aadress on vale või leht on kolinud. Alustage avalehelt või vaadake tehtud töid.</p>
      <div class="nupurida">
        <a href="/" class="nupp">Avalehele</a>
        <a href="/tood.html" class="nupp nupp-tyhi">Tehtud tööd</a>
      </div>
    </div>
  </section>
'''
leht("404.html", "Lehte ei leitud | A-MAJA OÜ", "Otsitud lehte ei ole olemas. Liikuge tagasi avalehele.",
     "/404.html", nelisada, [], noindex=True)

# ---------------------------------------------------------------- PRIVAATSUS

privaatsus = puru("Privaatsus") + '''  <section class="lehe-pais">
    <div class="raam">
      <p class="silt">Privaatsus</p>
      <h1>Privaatsustingimused</h1>
      <p class="juhtlause">Kuidas A-MAJA OÜ teie andmeid töötleb, kui saadate hinnapäringu.</p>
    </div>
  </section>

  <section class="lohik">
    <div class="raam sisuleht">
      <h2>Vastutav töötleja</h2>
      <p>A-MAJA OÜ, registrikood 16765213, KMKR EE102766103, aadress Sõle tn 27d-31, Põhja-Tallinna linnaosa, Tallinn. E-post info@a-maja.com, telefon +372 5387 4959.</p>

      <h2>Milliseid andmeid kogume</h2>
      <p>Hinnapäringu vormi kaudu kogume ainult neid andmeid, mille te ise sisestate:</p>
      <ul>
        <li>nimi</li>
        <li>e-posti aadress</li>
        <li>telefoninumber, kui selle lisate</li>
        <li>ettevõtte nimi, kui selle lisate</li>
        <li>objekti aadress ja päringu kirjeldus</li>
      </ul>
      <p>Me ei kogu külastajate kohta muid isikuandmeid ega kasuta jälgimisküpsiseid.</p>

      <h2>Mis eesmärgil</h2>
      <p>Andmeid kasutame ainult selleks, et teie päringule vastata ja vajadusel pakkumine koostada. Me ei kasuta neid turunduseks ega saada uudiskirju.</p>

      <h2>Õiguslik alus</h2>
      <p>Andmete töötlemise alus on teie nõusolek, mille annate vormi saatmisel, ning lepingueelsed läbirääkimised.</p>

      <h2>Kui kaua säilitame</h2>
      <p>Päringuid säilitame kuni kaks aastat. Kui päringust kasvab välja leping, säilitame projektiga seotud andmeid nii kaua, kui seadus raamatupidamis- ja projektidokumentide osas nõuab.</p>

      <h2>Kellega jagame</h2>
      <p>Andmeid ei müü ega jaga kolmandatele isikutele turunduseks.</p>
      <p>Kui projekt jõuab ehitusloa menetlusse, esitame vajalikud andmed kohalikule omavalitsusele, sest ilma selleta menetlust läbi viia ei saa.</p>

      <h2>Statistika</h2>
      <p>Kasutame külastusstatistika kogumiseks küpsisevaba lahendust, mis ei tuvasta üksikkülastajat ega loo profiili. Seetõttu ei ole lehel küpsiste nõusolekuriba.</p>

      <h2>Teie õigused</h2>
      <p>Teil on õigus küsida, milliseid andmeid teie kohta on, nõuda nende parandamist või kustutamist ning võtta nõusolek tagasi. Selleks kirjutage aadressil <a href="mailto:info@a-maja.com">info@a-maja.com</a>. Vastame ühe kuu jooksul.</p>
      <p>Kui te ei ole vastusega rahul, saate pöörduda Andmekaitse Inspektsiooni poole.</p>

      <h2>Muudatused</h2>
      <p>Kui tingimused muutuvad, avaldame uue versiooni siin lehel.</p>
    </div>
  </section>
'''
leht("privaatsus.html", "Privaatsustingimused | A-MAJA OÜ",
     "Kuidas A-MAJA OÜ hinnapäringu andmeid töötleb, kui kaua neid säilitatakse ja millised on teie õigused.",
     "/privaatsus.html", privaatsus, [puru_ld("Privaatsus", "/privaatsus.html")])

print("HTML valmis")
