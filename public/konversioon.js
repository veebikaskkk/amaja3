/* Google Ads konversioon "Submit lead form", laetakse ainult lehel aitah.html.
   Konversioon loetakse ainult siis, kui külastaja jõudis siia vormi saatmise
   järel. skript.js paneb enne suunamist sessionStorage-sse lipu, see fail
   kustutab selle kohe ära. Nii ei teki konversiooni, kui keegi avab aadressi
   otse või värskendab lehte. Nõusoleku olek tuleb failist jalgimine.js. */
(function () {
  var lipp = null;
  try {
    lipp = sessionStorage.getItem("paring_saadetud");
    sessionStorage.removeItem("paring_saadetud");
  } catch (e) {}
  if (!lipp || typeof window.gtag !== "function") return;

  window.gtag("event", "conversion", {
    send_to: "AW-18565603728/YBiHCIeBm7UdEJDD4pRF",
    value: 1.0,
    currency: "EUR"
  });
})();
