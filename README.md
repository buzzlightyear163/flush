# FLUSHED ($FLUSHED)

"Buys when the snipers are out."
En sida, `index.html`, med CSS och JS inbakade. `og.png` och `fav.png` ligger bredvid. Grafiken till X ligger i `grafik/`.

## 1. Fyll i CONFIG (överst i scriptet i index.html, sök på `CONFIG`)

| Fält | Vad |
|---|---|
| `ca` | $FLUSHED-minten. Tom = "posted here and on X at launch". Ifylld = köpknapparna går till pump.fun och holders får CLEAN 20 sekunder före alla andra. |
| `x` | X-länken (förifylld: https://x.com/FlushedEngine) |
| `site` | Domänen som står på delningskorten, t.ex. `flushedengine.fun`. Tom = adressen sajten ligger på |
| `engine` | Motorns publika plånbok. Tom = "posted here at launch". Ifylld = live-flöde av motorns köp och sälj, träffprocent och netto räknat från kedjan. |
| `earlySeconds` | Hur många sekunder före andra som holders ser CLEAN (20) |
| `R` | Gränserna: snipers 2 %, bundles 3 %, dev 3 %, max dip 50 %, 8 plånböcker, LOADED över 10 %, 2x och −25 % |

## 2. Deploy

GitHub → Vercel. Framework: **Other**, ingen build, root = mappen där `index.html` ligger.

## 3. Kolla efter deploy

- **Typsnitt:** JetBrains Mono laddas (allt ska vara monospace).
- **X-förhandsvisning:** klistra in länken i ett utkast på X. Då ska `og.png` visas.
- **Live-data:** inom ungefär en minut fylls tavlan med coins och lamporna blir gröna. Klicka på en coin för sniper-kartan och checklistan.
- **Exempeldata:** lägg till `?preview` i adressen. Allt märks då "preview · sample data".
- **Felsökning:** `?debug` visar status för varje datakälla.

## Funktioner

- **Kolla valfri coin:** klistra in en CA (eller en pump.fun-länk) högst upp. Coinen fästs överst på tavlan med sin rapport öppen.
- **Länk till en coin:** `?c=<mint>` öppnar den coinens rapport direkt. Det är länken som delningskortet och X-knappen använder.
- **Delningskort:** knappen "share card ↗" i en coins rapport ger en bild på 1600×900 med mätare, %, de sex checkarna och flush-grafen. Man kan kopiera bilden, ladda ner den som PNG, posta på X (med text och länk) eller kopiera länken.
- **Flush-graf:** påsen (rött), priset och antalet holders över tid, med markering för flushens start och CLEAN. För coins som redan var igång när sidan öppnades är tiden innan dess tonad.
- **Live-larm:** varje coin som blir CLEAN medan sidan är öppen syns i en remsa och som en notis. Ljud och webbläsarnotis slås på uppe till höger på tavlan. Holders får larmet 20 s tidigare.

## Datakällor (alla gratis, inga nycklar)

- **PumpPortal** (`subscribeNewToken`): nya coins på pump.fun och LaunchLab (bonk) i samma sekund de skapas. PumpPortals trade-ström per coin kostar numera, så den används inte.
- **Solana RPC** (publicnode, `logsSubscribe` per coin): varje köp och sälj på pump.fun avkodas direkt ur kedjan, med slot. Därifrån räknas överhänget live.
- **Jupiter** (`datapi.jup.ag`): de första blocken läses tillbaka (`/txs`, med slot per trade), topp 100 holders med finansieringsadress (`/holders`), holders, pris och 5-minutersflöde (`/assets/search`), och coins som redan var igång när sidan öppnades (`/pools/gems`).
- **Jupiter Ultra** (`lite-api.jup.ag/ultra/v1/holdings`): "verify bags" och holder-kollen för $FLUSHED.

## Hur betygen räknas

- **Sniper:** första köpet i block 0, 1 eller 2.
- **Bundle:** 3+ plånböcker vars första köp landar i samma block (block 0–5), eller tidiga plånböcker finansierade från samma adress inom 3 block från varandra, eller från devven.
- **De sex checkarna:** snipers < 2 %, bundles < 3 %, dev < 3 %, holders växte medan de sålde, priset föll max 50 % under flushen, fler köp än sälj senaste 5 min från 8+ plånböcker.
- **Betyg:** alla sex = CLEAN. En miss = DRAINING. Två missar eller snipers över 10 % = LOADED.

## Ärliga begränsningar

- **Flush-loggen** byggs av besökarens egen webbläsare och sparas där. Den gemensamma siffran är motorns egen träffprocent, räknad från plånbokens transaktioner on-chain.
- **Coins som redan var igång** när sidan öppnades: de första blocken läses tillbaka och påsarna kommer från en holder-snapshot som uppdateras var 2,5 min. "Holders" och "price held" märks då "est." i checklistan.
- **Överföringar:** en sniper som flyttar sin påse till en ny plånbok syns vid nästa snapshot eller när man trycker "verify bags", inte direkt.
- **LaunchLab** pollas var 6:e sekund i stället för att avkodas live, eftersom LaunchLabs trade-loggar inte innehåller plånboken.
- **Motorn är beta:** köp och sälj görs manuellt från den publika plånboken, och det står så på sajten.

## Ändra sajten

Källfilerna ligger i `src/`. `python src/build.py src` bygger `src/index.html` med allt inbakat. Kopiera den till roten.
