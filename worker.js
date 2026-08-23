// A-MAJA OÜ koduleht.
// Staatilised failid tulevad kaustast public/ ja neid serveerib Cloudflare ise.
// Ainus dünaamiline osa on hinnapäringu vorm aadressil /api/kontakt.

const piirang = new Map();

function puhasta(v, max) {
  return String(v == null ? "" : v)
    .slice(0, max)
    .replace(/[<>&"']/g, function (c) {
      return { "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;", "'": "&#39;" }[c];
    })
    .trim();
}

function lubatud(ip) {
  const nyyd = Date.now();
  const aken = 60 * 60 * 1000;
  const varsked = (piirang.get(ip) || []).filter((t) => nyyd - t < aken);
  if (varsked.length >= 5) return false;
  varsked.push(nyyd);
  piirang.set(ip, varsked);
  return true;
}

const vastus = (kood, keha) =>
  new Response(JSON.stringify(keha), {
    status: kood,
    headers: { "Content-Type": "application/json" },
  });

async function kontakt(request, env) {
  if (request.method !== "POST") {
    return new Response(JSON.stringify({ ok: false }), {
      status: 405,
      headers: { "Content-Type": "application/json", Allow: "POST" },
    });
  }

  const ip =
    request.headers.get("CF-Connecting-IP") ||
    (request.headers.get("x-forwarded-for") || "").split(",")[0].trim() ||
    "tundmatu";

  if (!lubatud(ip)) return vastus(429, { ok: false });

  let k;
  try {
    k = await request.json();
  } catch (viga) {
    return vastus(400, { ok: false });
  }

  // Meepott: robot täitis peidetud välja. Vastame edukalt, aga kirja ei saada.
  if (k.veebiaadress) return vastus(200, { ok: true });

  const nimi = puhasta(k.nimi, 120);
  const epost = puhasta(k.epost, 160);
  const sonum = puhasta(k.sonum, 5000);
  const ettevote = puhasta(k.ettevote, 160);
  const telefon = puhasta(k.telefon, 60);
  const olemasolev = puhasta(k.olemasolev, 200);

  const liigid = { uus: "Uus hoone", uuendus: "Olemasoleva uuendus", muu: "Muu" };
  const liik = liigid[k.liik] || "Uus hoone";

  if (!nimi || !epost || !sonum) return vastus(400, { ok: false });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(epost)) return vastus(400, { ok: false });

  const read = [
    ["Nimi", nimi],
    ["Ettevõte", ettevote],
    ["E-post", epost],
    ["Telefon", telefon],
    ["Töö laad", liik],
    ["Olemasolev objekt", olemasolev],
  ]
    .filter((r) => r[1])
    .map((r) => "<p><strong>" + r[0] + ":</strong> " + r[1] + "</p>")
    .join("");

  const html =
    "<h2>Uus hinnapäring amaja.ee lehelt</h2>" +
    read +
    "<h3>Kirjeldus</h3><p>" +
    sonum.replace(/\n/g, "<br>") +
    "</p>";

  if (!env.RESEND_API_KEY || !env.SAATJA || !env.SAAJA) {
    console.error("Puudub muutuja: RESEND_API_KEY, SAATJA või SAAJA");
    return vastus(500, { ok: false });
  }

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + env.RESEND_API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.SAATJA,
        to: [env.SAAJA],
        reply_to: epost,
        subject: "Hinnapäring: " + nimi + (ettevote ? " (" + ettevote + ")" : ""),
        html: html,
      }),
    });

    if (!r.ok) {
      const tekst = await r.text();
      console.error("Resend viga", r.status, tekst);
      return vastus(502, { ok: false });
    }
    return vastus(200, { ok: true });
  } catch (viga) {
    console.error("Saatmise viga", viga && viga.message);
    return vastus(500, { ok: false });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/kontakt") {
      return kontakt(request, env);
    }

    // Kõik muu on staatiline fail kaustast public/
    return env.ASSETS.fetch(request);
  },
};
