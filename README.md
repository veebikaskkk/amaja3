# A-MAJA OÜ koduleht

Puhas HTML, CSS ja JavaScript. Raamistikku ega ehitusprotsessi ei ole.
Majutus Cloudflare Workeri peal, hinnapäringu vormi taust Resend.

---

## 1. Mida tuleb koodis asendada

Praegu on kõik viited domeenile `https://amaja.ee`. Kui domeen on teine,
asenda see nendes failides:

- `sitemap.xml`
- `robots.txt`
- kõigi HTML-failide `<link rel="canonical">` ja `og:url`
- `worker.js` sisus on domeen ainult kirja pealkirjas, mujal seda ei ole

Kiire viis: otsi kõigist failidest `amaja.ee` ja asenda.

Postiindeksit JSON-LD plokis ei ole, sest Sõle tn 27d täpset indeksit ma
ei tea. Kui see on käepärast, saab selle lisada `postalCode` väljana
`index.html`, `meist.html` ja `kontakt.html` struktuurandmetesse.

---

## 2. Pildid

Kõik pildid on lehel olemas. Kohatäiteid ei ole enam üheski kohas.

**Fotod ja visualiseeringud, 16 tükki** portfoolio ruudustikus ja üks
portfoolio avapildina. Neist kolm on valminud hoonete fotod, ülejäänud
3D visuaalid. Ruudustik käib rütmis lai, kaks kitsast, lai, nii et ükski
rida ei jää pooleks ega satu kaks laia kaarti kõrvuti. Avalehe avapildiks on musta puitlaudisega metsamaja, mis on
eraldi optimeeritud kahes suuruses, et mobiil ei laeks arvutiversiooni.

Portfoolio avapilt on samuti klõpsatav ja avab sama projekti info mis
avalehel oleval kaardil. Juurdeehituse fassaadi lähivaade ei ole enam
eraldi töö, vaid avaneb selle projekti pildi alt.

Portfoolio on nüüd ühtlane ruudustik, kus osa töid võtab kogu laiuse.
Pildid on kärbitud ühtsesse kuvasuhtesse, sest portfooliona mõjub see
palju rahulikumalt kui erikõrgused. Terve, kärpimata pilt on alati ühe
klõpsu kaugusel: klõps avab foto valgustis samal lehel.

**Projektijoonised, 43 tükki.** Eraldi joonistegaleriid lehel ei ole,
sest üksik joonis ilma projektita ei ütle tellijale midagi. Joonised on
seotud portfoolio piltidega projektinumbri kaudu ja avanevad valgusti
kõrvalpaneelis, kui tellija klõpsab foto peal. Iga projekti kohta on kuni
neli joonist: korruste plaanid, välisvaated ja lõige. Detailsõlmed,
tuleohutuse skeemid ja tekstitabelid on välja jäetud.

Kõrvalpaneelis joonisel klõpsates vahetavad joonis ja projekti pilt kohad,
nii et pilt jääb alles ja sinna saab ühe klõpsuga tagasi. Kui projektil
jooniseid ei ole, siis kõrvalpaneeli ei kuvata ja pilt võtab kogu laiuse.

Joonised on nimekirjas `PROJEKTI_JOONISED` ja seosed nimekirjas `SEOSED`,
mõlemad failis `ehita.py`. Joonis, millele `SEOSED` ei viita, ei jõua
kuhugi, seetõttu ei ole kaustas `pildid/` ka ühtegi kasutuseta joonist.

Laiast kaardist, mis venib üle terve ekraani, on ka 2800 px variant.
Vaikimisi `src` jääb väiksem ja `srcset` annab selle ainult suurele
ekraanile, nii et mobiil ei lae arvutiversiooni. Vastavus on failis
`ehita.py` nimekirjas `SUURED_VARIANDID`.

Kõik on WebP, EXIF ja GPS-koordinaadid eemaldatud, failinimed
kirjeldavad, alt-tekstid täislausetena. Joonised on kvaliteediga 94 ja
ilma suurendamiseta. Vanemad joonised olid lähtefailis ligikaudu 900 px
laiad, uued projektijoonised tulid A1 lehtedena ja on 1800 px laiad,
üksikud 1400 px, et iga fail jääks alla 400 KB.

### Logo

Logo on vektor, SVG. Ta on trassitud puhasteks kõverateks, seega on igal
suurusel terav ja fail on väike. Kaustas on kolm varianti:

- `pildid/a-maja-logo-hele.svg` tumedale taustale
- `pildid/a-maja-logo-tume.svg` heledale taustale
- `pildid/a-maja-logo.svg` võtab värvi ümbritsevast tekstist

PNG-versioonid on samuti olemas, nende jaoks, kus vektorit kasutada ei
saa. Faviconid ja jagamispilt on kõik samast vektorist tehtud.

Avalehe suur logo on HTML-i sisse kirjutatud SVG-na, mitte pildina.
Seda on vaja selleks, et logo saaks end lehe avanemisel joonistada:
esmalt tõmmatakse kontuur joonena, siis täidetakse kuju ja joon kaob.
Animatsioon kestab umbes kolm sekundit. Kui külastajal on
operatsioonisüsteemis liikumise vähendamine sisse lülitatud, kuvatakse
logo kohe lõppolekus.

See lisab avalehele umbes 22 KB, pakituna umbes 6 KB. Header ja jalus
kasutavad tavalist pildiviidet, sest seal animatsiooni vaja ei ole.

**Hero pildi kvaliteet.** Suvekohviku render on 1800 px lai, mis on
korras. Kui mõnest joonisest on originaal olemas suuremana, saada, siis
teen selle uuesti suurema lahutusega, sest praeguse pealt suurendades
jõuab piir kätte.

**Mida pildilt näha ei ole.** Objektide asukohti ja aastaid ma ei tea,
välja arvatud suvekohvik, mille sildil on Raatuse tänav 2 peal.
Kohanimi failinimes ja alt-tekstis on kohaliku pildiotsingu jaoks
kõige mõjusam üksik täiendus, mida siin veel teha saab. Vaata punkt 11.

---

## 3. Cloudflare Worker, avaldamine

Cloudflare ei loo enam Pages projekte, vaid Workereid, seetõttu on leht
Workeri kujul. Staatilised failid on kaustas `public/` ja Cloudflare
serveerib neid ise. Ainus dünaamiline osa on hinnapäringu vorm aadressil
`/api/kontakt`, mis elab failis `worker.js`.

Seadistus on failis `wrangler.jsonc`:

- `main` osutab failile `worker.js`
- `assets.directory` on `./public`
- `assets.run_worker_first` on `["/api/*"]`, seega vormi päring jõuab
  Workerini enne, kui otsitakse staatilist faili
- `not_found_handling` on `404-page`, seega tundmatu aadress saab
  `public/404.html`

Kausta `public/` sisu serveeritakse juurtasandilt. Seetõttu on HTML-is
viited endiselt kujul `/pildid/fail.webp`, mitte `/public/pildid/...`.

Juurtasandile jäävad failid, mida brauser ei näe: `worker.js`,
`wrangler.jsonc`, `ehita.py`, `README.md` ja `.gitignore`. Kuna Worker
serveerib ainult kausta `public/`, siis need välja ei paista.

### Avaldamine

1. Lae failid GitHubi hoidlasse.
2. Cloudflare paneelis: **Compute, Workers & Pages, Create, Import a
   repository**.
3. Build command jääb tühjaks. Deploy command jääb vaikeväärtusele
   `npx wrangler deploy`.
4. Pärast esimest õnnestunud deployd ilmub projektile lahter
   **Variables and secrets**, kuhu käivad `RESEND_API_KEY`, `SAATJA` ja
   `SAAJA`. Ilma nendeta vastab vorm veaga 500.

Käsurealt saab sama teha nii:

```
python3 ehita.py
npx wrangler deploy
```

### Kohapeal proovimine

```
npx wrangler dev
```

See jooksutab sama asja, mis Cloudflare: staatilised failid kaustast
`public/`, `_headers` päised ja `/api/kontakt`. Muutujad loeb kohapeal
failist `.dev.vars`, mille näidis on `.dev.vars.naidis`. Fail `.dev.vars`
on `.gitignore`-s.

Kontrollimiseks:

```
curl -i http://127.0.0.1:8788/api/kontakt
```

405 tähendab, et Worker vastab. 404 tähendab, et päring läks staatiliste
failide kätte ja `run_worker_first` on katki.

### Miks Cloudflare, mitte Vercel

Verceli tasuta plaan lubab ainult mittekaubanduslikku isiklikku kasutust.
Kliendi äritegevust tutvustav leht ei mahu selle alla, seega seal oleks
vaja Pro plaani. Cloudflare tasuta plaan lubab ärilist kasutust,
staatiliste failide serveerimist ei arvestata päringute hulka ja piiriks
on 100 000 Workeri päringut päevas. Selles projektis on umbes 60 faili.

### Domeen ja DNS

`.ee` domeeni Cloudflare ise ei müü, seega domeen jääb sinna, kus ta on,
näiteks Zone või Veebimajutus.

1. Lisa domeen Cloudflare kontosse: **Add a site**, vali **Free**.
2. Cloudflare annab kaks nimeserverit. Mine domeeni registripidaja
   juurde ja asenda seal senised nimeserverid nendega.
3. Oota levimist, tavaliselt tunnist mõne tunnini.
4. Workeri projekti all: **Settings, Domains and routes, Add custom
   domain**, sisesta `amaja.ee`, seejärel sama `www.amaja.ee` jaoks.

SSL tuleb automaatselt ja tasuta.

### Eelvaate aadress ei tohi Google'isse jõuda

`public/_headers` failis on reegel, mis lisab `workers.dev` aadressile
`X-Robots-Tag: noindex`. Ilma selleta indekseeriks Google sama lehe
kaks korda ja jagaks otsingutulemused kahe aadressi vahel laiali.
Vana `pages.dev` reegel on alles, see ei sega.

---

## 4. Hinnapäringu vorm, Resend

Vorm asub failis `worker.js`, funktsioonis `kontakt`. Tasuta plaanil on
100 000 päringut päevas.

1. Loo konto resend.com ja lisa domeen `amaja.ee`.
2. Kinnita domeen DNS-kirjetega, mille Resend annab. Kuna DNS on nüüd
   Cloudflare'is, lisa need kirjed sinna.
3. Loo API võti.
4. Cloudflare: **Workeri projekt, Settings, Variables and secrets**.
   Lahter ilmub alles pärast esimest õnnestunud deployd. Lisa kolm
   muutujat:

| Nimi | Väärtus | Tüüp |
|---|---|---|
| `RESEND_API_KEY` | Resendi API võti | Secret |
| `SAATJA` | `Koduleht <info@amaja.ee>` | Text |
| `SAAJA` | `info@a-maja.com` | Text |

**Muutujad jõustuvad alles uue deploy järel.** Pärast lisamist tee
Deployments alt **Retry deployment**. See on kõige sagedasem põhjus,
miks vorm ei tööta.

**Kinnitamata domeeniga Resend saadab ainult konto omaniku aadressile.**
Kui `SAAJA` on mõni muu aadress, tuleb vastuseks 403.

---

## 5. Statistika

Cloudflare Web Analytics on küpsisevaba ja seda ei pea koodi lisama.
Paneelis: **Web Analytics, Add a site**, vali domeen ja lülita sisse
automaatne paigaldus. Nõusolekuriba ei ole vaja, seetõttu seda lehel ka
ei ole.

---

## 5b. Kui klient tahab hiljem Google Ads-i

Praegu Ads-i ei ole ja jälgimiskoodi lehel ei ole. Lisamine on tehtav,
aga sellel on tagajärjed, mis tasub kliendile enne selgeks teha.

Vaja on kolme muudatust:

1. **Konversioonimõõtmine.** Google'i jälgimiskood tuleb lisada kõigi
   lehtede `<head>` ossa ja konversioon seotakse lehega `aitah.html`,
   kuhu külastaja jõuab pärast vormi saatmist. See leht on juba olemas
   just sel eesmärgil.
2. **Turvapoliitika.** Failis `_headers` tuleb `Content-Security-Policy`
   real laiendada `script-src` ja `connect-src` väärtusi Google'i
   domeenidega. Ilma selleta brauser blokeerib jälgimiskoodi.
3. **Küpsised.** Google'i kood kasutab küpsiseid. See tähendab, et lehele
   tuleb küpsiste nõusolekuriba ja `privaatsus.html` vajab eraldi
   küpsiste peatükki. Praegu on leht küpsisevaba ja riba puudub.

Ehk tehniliselt on kõik ette valmistatud, aga Ads toob kaasa
nõusolekuriba, mis muudab lehe külastaja jaoks pisut tüütumaks. See on
teadlik vahetus, mitte tehniline takistus.

---

## 6. Juhend kliendile: Google'i ettevõtteprofiil

Tasuta ja kõige suurema mõjuga samm kohalikus otsingus. Tee see kohe
pärast lehe avaldamist.

**Mis andmed sisestada**

- Nimi täpselt nii: A-MAJA OÜ
- Kategooria: Arhitekt. Lisakategooria: Projekteerimisbüroo
- Telefon: +372 5387 4959
- Veebileht: https://amaja.ee
- Teeninduspiirkond: vali kõik viisteist maakonda, sest tööd võetakse
  vastu üle Eesti
- Kui vastuvõttu aadressil ei toimu, märgi profiil teeninduspiirkonna
  ettevõtteks, mitte poeks. Siis aadressi kaardil ei näidata.
- Teenused: lisa needsamad, mis on teenuste lehel

**Mis fotod lisada**

- Logo profiilipildiks
- Kaanepildiks üks valminud objekt
- Vähemalt viis fotot töödest. Samad failid, mis lehel, sobivad.

**Kuidas arvustusi küsida**

Küsi arvustust siis, kui ehitusluba on käes, sest see on kliendi jaoks
kõige selgem võiduhetk. Saada lühike kiri koos otselingiga arvustuse
vormile, mille leiad profiili haldusvaates. Ära paku vastutasu, sest
Google eemaldab sellised arvustused.

Hange.ee hinnangud jäävad sinna, kus nad on. Neid Google'i profiilile üle
tõsta ei saa, aga sama klient võib mõlemas kohas arvustuse jätta.

---

## 7. Struktuur

```
index.html          Avaleht, täisekraan avapilt ja tööde ruudustik
tood.html           Portfoolio, 16 tööd, joonised avanevad pildi pealt
teenused.html       Kuus teenust eraldi alajaotustena
meist.html          Miks meid, näitajad
tagasiside.html     Klientide hinnangud
kontakt.html        Hinnapäringu vorm ja kontaktandmed
aitah.html          Tänuleht, noindex
privaatsus.html     Privaatsustingimused
404.html            Vealeht, noindex
stiil.css           Jagatud stiil
skript.js           Ülekattemenüü, valgusti, vormi valideerimine
_headers            Turvapäised ja vahemälu
_redirects          Ümbersuunamised, praegu tühi
fondid/             IBM Plex Sans ja Mono, latin ja latin-ext
pildid/             Töödeldud WebP-d ja logo
jagamispilt.png     og:image, 1200x630
```

Kõik ülal loetletu on kaustas `public/`. Juurtasandil on ainult:

```
worker.js           Hinnapäringu vorm, /api/kontakt
wrangler.jsonc      Workeri seadistus, osutab kausta public
ehita.py            Genereerib HTML-failid kausta public
README.md           See fail
```

### Portfooliokeskne ülesehitus

Avaleht algab täisekraan avapildiga, millel on ainult logo ja üks rida
teksti. Menüü on ülekattes, mis avaneb paremal ülal olevast nupust ja
katab kogu ekraani suurte linkidega. Kohe avapildi järel algavad tööde
pildid, ilma vahepealse tekstiplokita.

Tekstiraskus on avalehelt maha võetud. Pikem sisu elab nüüd eraldi
lehtedel: teenused, meist ja tagasiside.

**Artiklite lehte ei ole.** Jätsin selle teadlikult välja, sest sisu
selle jaoks praegu ei ole ja tühi artiklite nimekiri kahjustaks pigem kui
aitaks. Kui artiklid tulevad, teen lehe koos Article ja ItemList
struktuurandmetega juurde.

---

## 8. Mida ma ise ei kinnitanud

Need punktid vajavad sinu või kliendi ülevaatust, sest mina neid
kontrollida ei saa.

- **PageSpeed skoor.** Eesmärgiks võetud 90 või rohkem mobiilis. Testida
  saab alles siis, kui leht on päris aadressil. Ma ei väida, et testisin.
- **Postiindeks** JSON-LD plokis, vaata punkt 1.
- **Fotode õigused.** Enne avaldamist kinnita, et fotod on kliendi omad
  või on luba olemas. Droonipildid ja profifotod kuuluvad sageli
  fotograafile, mitte tellijale.
- **Hinnad, garantiid, sertifikaadid.** Lehel ei ole ühtegi hinda ega
  garantiid, sest neid mulle ei antud. Kui need lisada, siis ainult
  kliendi kinnitusel.

---

## 9. Mobiili murdepunktid

CSS-i on lisatud järgmised murdepunktid. Testida ma ei saa, seega
loetlen ainult selle, mis koodis on.

| Murdepunkt | Mis muutub |
|---|---|
| kuni 900 px | Menüü läheb hamburgeri alla, avaneb päise all täislaiuses. Menüülinkide puutekõrgus 52 px. |
| alates 700 px | Teenusekaardid kahte veergu, galerii kahte veergu, jaluse plokid kahte veergu. |
| alates 768 px | Näitajate riba neljaveeruliseks. |
| alates 800 px | Tsitaadid kahte veergu. |
| alates 820 px | Hinnangud kahte veergu. |
| alates 900 px | Teenuse plokk kaheveeruliseks, kaks veergu jaotus, kutseplokk kaheveeruliseks. |
| alates 1000 px | Kontaktileht kaheveeruliseks, jalus neljaveeruliseks. |
| alates 1024 px | Hero kaheveeruliseks. |
| alates 1100 px | Teenusekaardid neljaveeruliseks, galerii kolmeveeruliseks. |
| alates 1240 px | Sisu laius lukustub, veerised kasvavad. |

Päise kõrgus on muutuja `--pais-korgus`, praegu 78 px. Kõik ankrud
kasutavad seda `scroll-margin-top` sees, seetõttu ei jää sihtkoht
kleepuva päise alla peitu. Kui päise kõrgust muuta, piisab muutuja
muutmisest ühes kohas.

Puutealad on vähemalt 44 px, nupud 48 px, vormiväljad 50 px.
Pikad e-posti aadressid murduvad `overflow-wrap` abil.
Kerivas konteineris absoluutselt positsioneeritud elemente ei ole.

---

## 10. Kontrollnimekiri, läbitud

1. Kõik JSON-LD plokid parsivad vigadeta. Kontrollitud koodiga.
2. Igal lehel täpselt üks h1, tasemed ei hüppa.
3. Igal lehel unikaalne title ja description, kontrollitud koodiga.
4. Kõik sisemised lingid ja ankrud viitavad olemasolevale failile.
5. HTML-i sildid tasakaalus, kontrollitud parseriga.
6. Ühtegi pikka mõttekriipsu ei ole, kontrollitud koodiga.
7. Koma ei ole rinnastava sidesõna ees. Kaks järelejäänud juhtu on
   kõrvallauset sulgevad, mis on reeglipärane.
8. Kohatäiteid nagu `[NIMI]` koodis ei ole.
9. Kõik pildiviited on olemas või asendatud triibulise kohatäitega.
10. `jagamispilt.png` on päriselt olemas, genereeritud lehe värvide ja
    logoga.
11. Jaluses on täisnimi, õiguslik vorm, registrikood, KMKR, aadress,
    e-post ja telefon.
12. Privaatsusleht on olemas ja lingitud nii vormi juurest kui jalusest.
13. Väljamõeldud fakte, tagasisidet ega numbreid ei ole. Kõik hinnangud
    on need, mis Hange.ee-st tulid. Hinnangute arvu lehel ei nimetata,
    et see ei vananeks uute hinnangute lisandudes.
14. Iga värvipaar vastab kontrastile 4.5:1, kontrollitud arvutusega.
    Madalaim on 5,57.
15. Fookusraam on klaviatuuriga nähtav, `:focus-visible` 2 px aktsent.
16. Murdepunktid loetletud punktis 9.
17. Fondid tulevad kaustast `fondid/`, mitte Google'i serverist.
    Kontrollitud, et õ ä ö ü on latin-alamhulgas ja ž š latin-ext-is.
18. API võtit üheski failis ei ole, ainult `process.env.RESEND_API_KEY`.
19. Vana lehte ei olnud, seega ümbersuunamisi vaja ei ole.

---

## 11. SEO baas, mis otsingutega leitakse

Lehel ei ole ostetud reklaami ega nippe. Baas koosneb kolmest asjast:
iga leht sihib ühte päris küsimust, sisu on eesti keeles ja konkreetne,
ning struktuurandmed ütlevad Google'ile otse, mis ettevõttega on tegu.

### Iga lehe siht

| Leht | Title | Mida sihib |
|---|---|---|
| `index.html` | Arhitektuurne projekteerimine üle Eesti | üldotsing, brändiotsing |
| `teenused.html` | Projekteerimisteenused | teenusepõhised otsingud |
| `tood.html` | Tehtud tööd ja joonised | portfoolio, pildiotsing |
| `tagasiside.html` | Klientide tagasiside | usaldusotsingud, brändi + arvustus |
| `kontakt.html` | Kontakt ja hinnapäring | ostuvalmis otsingud |

### Realistlikud otsingud, kus leht võib kuvada

**Brändiotsingud, tugevaim positsioon.** Siin peaks leht jõudma esikohale
üsna kiiresti, sest konkurentsi ei ole.

- a-maja, a-maja oü, amaja arhitekt
- kaspar lätt arhitekt

**Teenusotsingud, keskmine konkurents.** Nendes on realistlik jõuda
esilehele mõne kuu jooksul, kui Google'i ettevõtteprofiil on ka tehtud.

- eramu projekt, eramu ehitusprojekt, üksikelamu projekteerimine
- juurdeehituse projekt, rekonstrueerimise projekt
- abihoone projekt, aiamaja projekt, saunamaja projekt
- moodulmaja ehitusprojekt
- eelprojekt ehitusteatise mahus, ehitusteatise projekt
- arhitektuurne põhiprojekt, arhitektuurne projekteerimine
- korterelamu projekteerimine, ärihoone projekteerimine

**Pika sabaga otsingud, kus võit on kõige tõenäolisem.** Need on
väiksema mahuga, aga otsija on ostuvalmis.

- kas mul on vaja ehitusluba või ehitusteatis
- kes suhtleb omavalitsusega ehitusloa taotlemisel
- diplomeeritud arhitekt tase 7
- arhitekt kes mõtleb kaasa
- eramu projekt üle eesti

**Kohalikud otsingud.** Siin on praegu suurim puudujääk, vaata allpool.

- arhitekt tallinn, arhitektibüroo tallinn, projekteerija harjumaa

### Mis otsingutega leiab pilte

Pildiotsing käib kolme asja pealt: failinimi, alt-tekst ja `sitemap.xml`
`image:image` plokk, kus on iga pildi pealkiri ja kirjeldus. Kõik kolm on
igal pildil olemas, mis on see osa, mille enamik lehti tegemata jätab.

**Fotod ja visualiseeringud leitakse otsingutega nagu:**

- tume puitfassaad eramu, vertikaalne puitlaudis maja
- punane puitfassaad eramu, punane viilkatusega maja
- päikesepaneelidega eramu, kelpkatus päikesepaneelid
- eramu juurdeehitus puitribifassaad
- korterelamu puitfassaad visualiseering
- suvekohvik projekt, katuseterrassiga kohvik

**Joonised leitakse otsingutega nagu:**

- eramu lõige joonis, sektsioon A-A joonis
- korruse plaan joonis, esimese korruse plaan
- katuseplaan joonis
- eramu vaated joonis, eestvaade mõõtkava 1:50
- konstruktsioonisõlmed joonis, välisseina tarind

Joonised on siin ootamatult väärtuslik vara. Enamik arhitektibüroosid ei
pane jooniseid üldse üles, seetõttu on konkurents nendel otsingutel
väike ja need toovad täpselt õiget tüüpi külastajat, kes teab, mida
projekt sisaldab.

### Mis on tehtud

- Igal lehel unikaalne title ja description, mitte kopeeritud
- Canonical URL igal lehel
- `ProfessionalService` struktuurandmed: nimi, telefon, e-post, aadress,
  KMKR, kutsetunnistus 203786 ja kõik 15 maakonda `areaServed` all
- `Service` ja `Offer` iga kuue teenuse kohta
- `BreadcrumbList` igal alamlehel
- `sitemap.xml` kõigi lehtede ja 21 pildiga
- `robots.txt`, mis lubab indekseerida ja blokeerib `/api/`
- Semantiline HTML, üks h1 lehel, tasemed ei hüppa
- Sisemised lingid sisu sees, mitte ainult menüüs

### Mis on tegemata ja mida see maksab

**Google'i ettevõtteprofiil, kõige suurem üksik võit.** Ilma selleta ei
kuvata lehte kaardil ega kohalikus kolmikus, mis on enamiku
teenuseotsingute puhul see osa, mida päriselt vaadatakse. Tasuta, tund
aega tööd. Juhend on punktis 6.

**Kohanimed piltide juures.** Praegu on ainult suvekohvikul asukoht
teada. Kui saadad ülejäänud objektide asukohad, saab failinimed ja
alt-tekstid täiendada kujul `eramu-punane-puitfassaad-viimsi.webp`. See
avab otsingud stiilis "eramu projekt viimsi", mis on palju vähem
konkurentsi kui üldine "eramu projekt".

**Artiklid.** Jätsin artiklite lehe teadlikult välja, sest sisu ei ole ja
tühi nimekiri kahjustaks. Aga just artiklid oleksid see, mis toob pika
sabaga otsinguid. Kaks kuni kolm sisulist teksti, näiteks "millal
piisab ehitusteatisest ja millal on vaja ehitusluba", tooksid tõenäoliselt
rohkem külastajaid kui kogu ülejäänud leht kokku.

**Aeg.** Uus domeen ei asu esikohale kohe. Indekseerimine võtab
tavaliselt paar nädalat, positsioonid stabiliseeruvad paari kuuga.
Lisa leht Google Search Console'i kohe pärast avaldamist ja esita
`sitemap.xml`. Domain-property puhul käib väljale terve aadress,
URL-prefix-property puhul ainult `sitemap.xml`.

---

## 12. Kuidas lehte muuta

HTML-faile ei muudeta käsitsi. Kõik HTML genereeritakse failist
`ehita.py`. Töövoog:

1. muuda `ehita.py`
2. jooksuta `python3 ehita.py`
3. lae muudetud failid üles

Kui muudad HTML-i otse, kirjutatakse see järgmisel jooksutamisel üle.

Failis `CLAUDE-ULESANNE.md` on eraldi juhend jooniste ja fotode
sidumiseks, kirjutatud Claude Code jaoks.
