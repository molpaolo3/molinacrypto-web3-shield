MolinaCrypto Web3 Shield v0.5
Pacchetto Linux/source

MolinaCrypto Web3 Shield è un tool desktop open source per controlli preliminari di sicurezza e consapevolezza su wallet, transazioni Bitcoin, URL, e-mail, dApp, smart contract, firme/approval Web3 e dati Lightning.

Il programma non richiede seed phrase, private key, password o collegamento del wallet. Non firma transazioni e non sposta fondi. Lavora solo con dati pubblici o testo incollato manualmente dall’utente.

Collegato al progetto:
https://www.molinacrypto.eu


REQUISITI LINUX

È necessario avere Python 3 e Tkinter installati.

Su Linux Mint / Ubuntu / Debian:

sudo apt update
sudo apt install python3 python3-tk


AVVIO RAPIDO

Dalla cartella del programma:

python3 MolinaCryptoWeb3Shield.py

Se presente lo script avvia.sh:

chmod +x avvia.sh
./avvia.sh


NOVITÀ VERSIONE 0.5

La versione 0.5 introduce una nuova interfaccia a schede, più pulita e scalabile:

- Wallet & TX
- Web Risk
- Lightning

Questa struttura evita una schermata iniziale troppo piena e prepara il programma all’aggiunta di nuove funzioni future.


SEZIONE WALLET & TX

Wallet / Address Check:
- riconoscimento indirizzi Bitcoin;
- controllo indirizzo Bitcoin pubblico tramite mempool.space;
- saldo confermato;
- saldo non confermato/mempool;
- numero transazioni confermate e non confermate;
- snapshot fee consigliate;
- riconoscimento indirizzi Ethereum/EVM;
- azioni rapide verso Etherscan, Revoke.cash, BaseScan, PolygonScan e Arbiscan.

Bitcoin TX Check:
- controllo TXID Bitcoin pubblici;
- stato transazione confermata/non confermata;
- blocco e orario blocco quando disponibili;
- numero input/output;
- totale output;
- fee e fee rate stimato in sat/vB;
- link rapidi verso mempool.space e Blockstream.


SEZIONE WEB RISK

Check URL / e-mail / dApp:
- validazione URL nei formati https://, http:// e www.;
- controllo preliminare e-mail sospette;
- rilevamento parole tipiche di phishing/Web3 scam;
- indicatori di possibile imitazione brand/dominio;
- avvisi su HTTPS mancante, IP al posto del dominio, punycode e domini lunghi;
- azioni rapide corrette verso VirusTotal, URLScan, Google Search e apertura link.

Smart Contract Check:
- riconoscimento indirizzi EVM;
- avvisi sul fatto che un formato valido non garantisce sicurezza del contratto;
- link rapidi agli explorer principali e Revoke.cash.

Signature / Approval Check:
- rilevamento keyword rischiose come approve, setApprovalForAll, permit, permit2, eth_sign, transferFrom, safeTransferFrom;
- miglioramento scoring su testi casuali, incompleti o non interpretabili;
- link diretti a Revoke.cash ed Etherscan quando nel testo viene rilevato un address EVM;
- nessun link rapido generico inutile quando non viene rilevato un address EVM.


SEZIONE LIGHTNING

Lightning Invoice / LNURL Check:
- decodifica locale di invoice Lightning BOLT11 dove supportato;
- rilevamento rete invoice;
- importo, creazione, scadenza, descrizione e payment hash quando disponibili;
- avviso invoice scaduta;
- avviso invoice senza importo;
- avviso descrizione mancante;
- decodifica LNURL;
- controllo endpoint LNURL;
- controllo Lightning Address tramite endpoint standard /.well-known/lnurlp/;
- avviso per LNURL-auth/login;
- avviso per endpoint non HTTPS.


SERVIZI ESTERNI

A seconda del controllo selezionato il programma può interrogare o aprire servizi esterni, tra cui:

- mempool.space;
- Blockstream explorer;
- Etherscan;
- Revoke.cash;
- BaseScan;
- PolygonScan;
- Arbiscan;
- VirusTotal;
- URLScan;
- Google Search;
- endpoint pubblici Lightning Address / LNURL.

L’utente resta responsabile nel valutare se l’interrogazione o apertura di tali servizi sia appropriata nel proprio contesto.


LIMITI DEL CONTROLLO

Il programma fornisce uno score indicativo basato su controlli statici, dati pubblici e indicatori euristici.

Non garantisce che un wallet, URL, contratto, firma, transazione, invoice o LNURL siano sicuri. Non identifica il proprietario reale degli indirizzi e non verifica identità, intenzioni economiche o pagamenti Lightning già completati.

Lightning è off-chain: il tool può analizzare preventivamente invoice, LNURL e Lightning Address, ma non può confermare universalmente l’esecuzione di un pagamento Lightning.


DISCLAIMER

Questo tool ha finalità informative, educative e di security awareness. Non costituisce consulenza finanziaria, fiscale, legale, di investimento o professionale in ambito cybersecurity. La responsabilità delle decisioni operative resta dell’utente.


FILE INCLUSI NEL PACCHETTO LINUX/SOURCE

- MolinaCryptoWeb3Shield.py
- README.md
- README_IT.txt
- README_EN.txt
- CHANGELOG.md
- LICENSE
- requirements.txt
- avvia.sh


SITO E RISORSE

Sito:
https://www.molinacrypto.eu

Risorse:
https://www.molinacrypto.eu/risorse.html
