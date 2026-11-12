/* Google Tag Manager ja küpsiste nõusolek (Google Consent Mode v2).
   Vaikimisi on reklaami- ja analüütikaküpsised keelatud. Need lubatakse
   alles siis, kui külastaja vajutab ribal "Nõustun". Valik jääb brauseri
   localStorage-sse võtme "kypsised" alla väärtusega "jah" või "ei".
   Fail laetakse <head> sees enne kõike muud, et nõusoleku vaikeolek
   jõuaks dataLayerisse enne GTM-i. */
(function () {
  var GTM = "GTM-MSDT6M3T";
  var VOTI = "kypsised";
  var w = window, d = document;

  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  w.gtag = gtag;

  var valik = null;
  try { valik = localStorage.getItem(VOTI); } catch (e) {}

  function olekud(jah) {
    var o = jah ? "granted" : "denied";
    return { ad_storage: o, ad_user_data: o, ad_personalization: o, analytics_storage: o };
  }

  var vaike = olekud(valik === "jah");
  vaike.functionality_storage = "granted";
  vaike.security_storage = "granted";
  gtag("consent", "default", vaike);
  gtag("set", "ads_data_redaction", true);

  w.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
  var s = d.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtm.js?id=" + GTM;
  d.head.appendChild(s);

  var riba = null;

  function salvesta(jah) {
    try { localStorage.setItem(VOTI, jah ? "jah" : "ei"); } catch (e) {}
    gtag("consent", "update", olekud(jah));
    w.dataLayer.push({ event: jah ? "kypsised_lubatud" : "kypsised_keelatud" });
    if (riba) { riba.remove(); riba = null; }
  }

  function naita() {
    if (riba) return;
    riba = d.createElement("div");
    riba.className = "kypsised";
    riba.setAttribute("role", "region");
    riba.setAttribute("aria-label", "Küpsiste nõusolek");
    riba.innerHTML =
      '<p>Kasutame Google\'i küpsiseid, et näha, kas reklaam toob päringuid. <a href="/privaatsus.html#kypsised">Loe lähemalt</a></p>' +
      '<div class="kypsised-nupud">' +
      '<button type="button" class="nupp nupp-tyhi nupp-vaike" data-valik="ei">Keeldun</button>' +
      '<button type="button" class="nupp nupp-vaike" data-valik="jah">Nõustun</button>' +
      '</div>';
    riba.addEventListener("click", function (e) {
      var v = e.target.getAttribute("data-valik");
      if (v) salvesta(v === "jah");
    });
    d.body.appendChild(riba);
  }

  d.addEventListener("DOMContentLoaded", function () {
    if (valik !== "jah" && valik !== "ei") naita();
    d.addEventListener("click", function (e) {
      var t = e.target.closest && e.target.closest("[data-kypsised]");
      if (t) { e.preventDefault(); naita(); }
    });
  });
})();
