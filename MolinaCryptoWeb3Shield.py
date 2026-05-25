import json
import base64
import re
import threading
import urllib.parse
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timezone
from functools import partial
from typing import Any, List, Tuple


APP_NAME = "MolinaCrypto Web3 Shield"
APP_VERSION = "0.5"
AUTHOR = "Paolo Molina"
WEBSITE = "https://www.molinacrypto.eu"
RESOURCES_URL = "https://www.molinacrypto.eu/risorse.html"

BTC_PATTERNS = [
    re.compile(r"^(bc1)[a-z0-9]{25,90}$", re.IGNORECASE),
    re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"),
]

EVM_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
BTC_TXID_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")
URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)
WWW_PATTERN = re.compile(r"^www\.[^\s]+\.[a-zA-Z]{2,}(/.*)?$", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
LIGHTNING_INVOICE_PATTERN = re.compile(r"^ln(bc|tb|bcrt)[a-z0-9]+$", re.IGNORECASE)
LNURL_PATTERN = re.compile(r"^lnurl[0-9a-z]+$", re.IGNORECASE)
LIGHTNING_ADDRESS_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


MEMPOOL_ADDRESS_API = "https://mempool.space/api/address/{address}"
MEMPOOL_FEES_API = "https://mempool.space/api/v1/fees/recommended"
MEMPOOL_TX_API = "https://mempool.space/api/tx/{txid}"

SUSPICIOUS_WORDS = [
    "airdrop", "claim", "bonus", "reward", "rewards", "free", "giveaway",
    "mint", "whitelist", "verify", "verification", "validate", "validation",
    "sync", "rectify", "restore", "recover", "walletconnect", "wallet-connect",
    "connect-wallet", "metamask", "seed", "phrase", "privatekey", "support",
    "helpdesk", "urgent", "limited", "presale", "drop", "tokenclaim", "auth",
    "unlock", "migration", "redeem"
]

KNOWN_BRANDS = [
    "metamask", "walletconnect", "uniswap", "opensea", "aave", "compound",
    "curve", "sushiswap", "pancakeswap", "1inch", "blur", "magiceden",
    "ledger", "trezor", "coinbase", "binance", "kraken", "phantom",
    "rabby", "revoke", "etherscan", "basescan", "polygonscan", "arbiscan"
]

SIGNATURE_RULES: List[Tuple[str, int, str, str, str]] = [
    ("setApprovalForAll", 35, "HIGH", "Può autorizzare un operatore a gestire tutti i token/NFT di una collezione.", "Can authorize an operator to manage all tokens/NFTs in a collection."),
    ("approve", 22, "MEDIUM", "Può autorizzare uno spender a muovere token dal wallet.", "Can authorize a spender to move tokens from the wallet."),
    ("increaseAllowance", 22, "MEDIUM", "Aumenta la quantità di token che uno spender può muovere.", "Increases the amount of tokens a spender can move."),
    ("permit", 25, "MEDIUM", "Può concedere autorizzazioni tramite firma senza una classica transazione approve on-chain.", "Can grant permissions by signature without a classic on-chain approve transaction."),
    ("permit2", 35, "HIGH", "Meccanismo di autorizzazione potente: controllare spender, token, scadenza e limiti.", "Powerful permission mechanism: check spender, token, expiry and limits."),
    ("eth_sign", 35, "HIGH", "Firma cieca/legacy: rischiosa se il contenuto non è leggibile.", "Blind/legacy signature: risky when the content is not readable."),
    ("personal_sign", 12, "LOW", "Firma messaggio spesso usata per login, ma abusabile su siti malevoli.", "Message signature often used for login, but it can be abused on malicious sites."),
    ("eth_signTypedData", 18, "MEDIUM", "Firma strutturata: verificare bene dominio, spender, token e contenuto.", "Typed-data signature: carefully verify domain, spender, token and content."),
    ("transferFrom", 35, "HIGH", "Operazione che può muovere asset se esiste autorizzazione.", "Operation that may move assets if authorization exists."),
    ("safeTransferFrom", 35, "HIGH", "Operazione che può muovere NFT se esiste autorizzazione.", "Operation that may move NFTs if authorization exists."),
]


TEXT = {
    "it": {
        "subtitle": "Controlla wallet, transazioni, link, contratti, firme e Lightning prima di rischiare fondi.",
        "claim": "Non richiede seed phrase · Non collega il wallet · Non firma transazioni",
        "tab_wallet": "Wallet & TX",
        "tab_web": "Web Risk",
        "tab_lightning": "Lightning",
        "section_wallet_title": "Wallet & Transaction",
        "section_wallet_desc": "Controlli Bitcoin/EVM e verifica transazioni Bitcoin pubbliche.",
        "section_web_title": "Web Risk",
        "section_web_desc": "Analisi preliminare di URL, e-mail, dApp, contratti e firme/approval Web3.",
        "section_lightning_title": "Lightning Network",
        "section_lightning_desc": "Controllo preventivo di invoice Lightning, LNURL e Lightning Address.",
        "wallet_card": "Wallet / Address Check",
        "wallet_hint": "Incolla indirizzo BTC o ETH/EVM pubblico",
        "wallet_btn": "Analizza wallet",
        "btc_tx_card": "Bitcoin TX Check",
        "btc_tx_hint": "Incolla un TXID Bitcoin pubblico da 64 caratteri",
        "btc_tx_btn": "Analizza transazione",
        "link_card": "Check URL / e-mail / dApp",
        "link_hint": "Incolla URL con https://, http:// o www.; oppure una e-mail sospetta",
        "link_btn": "Check URL / e-mail / dApp",
        "contract_card": "Smart Contract Check",
        "contract_hint": "Incolla indirizzo contratto o address EVM",
        "contract_btn": "Controlla contratto",
        "signature_card": "Signature / Approval Check",
        "signature_hint": "Incolla firma, approve, permit, setApprovalForAll o testo tecnico",
        "signature_btn": "Traduci firma",
        "lightning_card": "Lightning Invoice / LNURL Check",
        "lightning_hint": "Incolla invoice lnbc..., LNURL lnurl1... o Lightning Address nome@dominio.com",
        "lightning_btn": "Analizza Lightning",
        "result_title": "Risultato",
        "empty_result": "Seleziona una scheda, incolla un dato e avvia l’analisi. Il risultato comparirà qui in forma sintetica e leggibile.",
        "actions_title": "Azioni rapide",
        "report_btn": "Esporta report .txt",
        "clear_btn": "Pulisci",
        "site_btn": "molinacrypto.eu",
        "resources_btn": "Risorse",
        "language_label": "Language IT/EN:",
        "language_btn": "EN",
        "missing": "Inserisci un dato da analizzare.",
        "score": "Score",
        "risk_low": "Rischio basso",
        "risk_medium": "Rischio medio",
        "risk_high": "Rischio alto",
        "type": "Tipo",
        "recommendation": "Azione consigliata",
        "indicators": "Indicatori rilevati",
        "limits": "Limite del controllo",
        "copy": "Copia",
        "paste": "Incolla",
        "cut": "Taglia",
        "select_all": "Seleziona tutto",
        "report_missing": "Prima genera un risultato da esportare.",
        "report_saved": "Report salvato correttamente.",
        "save_error": "Errore durante il salvataggio.",
    },
    "en": {
        "subtitle": "Check wallets, transactions, links, contracts, signatures and Lightning before risking funds.",
        "claim": "No seed phrases · No wallet connection · No transaction signing",
        "tab_wallet": "Wallet & TX",
        "tab_web": "Web Risk",
        "tab_lightning": "Lightning",
        "section_wallet_title": "Wallet & Transaction",
        "section_wallet_desc": "Bitcoin/EVM checks and public Bitcoin transaction verification.",
        "section_web_title": "Web Risk",
        "section_web_desc": "Preliminary analysis of URLs, e-mails, dApps, contracts and Web3 signatures/approvals.",
        "section_lightning_title": "Lightning Network",
        "section_lightning_desc": "Preventive check for Lightning invoices, LNURL and Lightning Address.",
        "wallet_card": "Wallet / Address Check",
        "wallet_hint": "Paste public BTC or ETH/EVM address",
        "wallet_btn": "Analyze wallet",
        "btc_tx_card": "Bitcoin TX Check",
        "btc_tx_hint": "Paste a public 64-character Bitcoin TXID",
        "btc_tx_btn": "Analyze transaction",
        "link_card": "Check URL / e-mail / dApp",
        "link_hint": "Paste a URL with https://, http:// or www.; or a suspicious e-mail address",
        "link_btn": "Check URL / e-mail / dApp",
        "contract_card": "Smart Contract Check",
        "contract_hint": "Paste contract address or EVM address",
        "contract_btn": "Check contract",
        "signature_card": "Signature / Approval Check",
        "signature_hint": "Paste signature, approve, permit, setApprovalForAll or technical text",
        "signature_btn": "Translate signature",
        "lightning_card": "Lightning Invoice / LNURL Check",
        "lightning_hint": "Paste lnbc... invoice, lnurl1... LNURL or Lightning Address name@domain.com",
        "lightning_btn": "Analyze Lightning",
        "result_title": "Result",
        "empty_result": "Choose a tab, paste data and run the analysis. The result will appear here in a compact readable format.",
        "actions_title": "Quick actions",
        "report_btn": "Export .txt report",
        "clear_btn": "Clear",
        "site_btn": "molinacrypto.eu",
        "resources_btn": "Resources",
        "language_label": "Language IT/EN:",
        "language_btn": "IT",
        "missing": "Enter something to analyze.",
        "score": "Score",
        "risk_low": "Low risk",
        "risk_medium": "Medium risk",
        "risk_high": "High risk",
        "type": "Type",
        "recommendation": "Recommended action",
        "indicators": "Detected indicators",
        "limits": "Check limitation",
        "copy": "Copy",
        "paste": "Paste",
        "cut": "Cut",
        "select_all": "Select all",
        "report_missing": "Generate a result before exporting it.",
        "report_saved": "Report saved successfully.",
        "save_error": "Save error.",
    }
}


BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def fetch_json(url, timeout=15):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": f"MolinaCryptoWeb3Shield/{APP_VERSION}"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def normalize_url(value):
    raw = value.strip()
    if raw.lower().startswith("www."):
        raw = "https://" + raw
    parsed = urllib.parse.urlparse(raw)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0].strip()
    return raw, parsed, host


def is_valid_url_input(value):
    raw = value.strip()
    if not raw:
        return False
    if URL_PATTERN.match(raw):
        parsed = urllib.parse.urlparse(raw)
        return bool(parsed.scheme in ("http", "https") and parsed.netloc and "." in parsed.netloc)
    if WWW_PATTERN.match(raw):
        return True
    return False


def build_virustotal_url(normalized_url):
    encoded = base64.urlsafe_b64encode(normalized_url.encode("utf-8")).decode("ascii").rstrip("=")
    return f"https://www.virustotal.com/gui/url/{encoded}"


def build_urlscan_search_url(normalized_url):
    parsed = urllib.parse.urlparse(normalized_url)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0].strip()
    if not host:
        host = normalized_url.replace("https://", "").replace("http://", "").split("/")[0]
    encoded = urllib.parse.quote(f'domain:"{host}"', safe="")
    return f"https://urlscan.io/search/#{encoded}"


def analyze_email_address(email, lang="it"):
    email = email.strip()
    local_part, domain = email.split("@", 1)
    domain = domain.lower()
    local_part = local_part.lower()
    score = 100
    indicators = []

    indicators.append(f"E-mail analizzata: {email}" if lang == "it" else f"Analyzed e-mail: {email}")
    indicators.append(f"Dominio e-mail: {domain}" if lang == "it" else f"E-mail domain: {domain}")

    if "-" in domain:
        score -= 15
        indicators.append("Dominio con trattini: possibile imitazione o dominio artificiale." if lang == "it" else "Domain contains hyphens: possible imitation or artificial domain.")

    if any(word in local_part for word in ["support", "security", "helpdesk", "admin", "verify"]):
        score -= 18
        indicators.append("Local-part sensibile usata spesso nel phishing: support/security/helpdesk/admin/verify." if lang == "it" else "Sensitive local-part often used in phishing: support/security/helpdesk/admin/verify.")

    if any(word in domain for word in SUSPICIOUS_WORDS):
        score -= 22
        indicators.append("Il dominio contiene parole tipiche di campagne phishing/Web3." if lang == "it" else "The domain contains words commonly used in phishing/Web3 scams.")

    brand_hits = [brand for brand in KNOWN_BRANDS if brand in domain]
    if brand_hits:
        official_like = any(domain == f"{brand}.com" or domain.endswith(f".{brand}.com") for brand in brand_hits)
        if not official_like:
            score -= 25
            indicators.append(("Contiene brand noti ma non sembra dominio ufficiale: " if lang == "it" else "Contains known brands but does not look official: ") + ", ".join(brand_hits[:5]))

    if score == 100:
        indicators.append("Nessun indicatore statico forte rilevato, ma verifica comunque il mittente tramite canali ufficiali." if lang == "it" else "No strong static indicator detected, but still verify the sender through official channels.")

    return max(0, min(100, score)), indicators


def detect_wallet_type(value):
    value = value.strip()
    if EVM_PATTERN.match(value):
        return "EVM"
    for pattern in BTC_PATTERNS:
        if pattern.match(value):
            return "BTC"
    return "UNKNOWN"


def sats_to_btc(sats):
    try:
        return float(sats) / 100_000_000
    except Exception:
        return 0.0


def fmt_btc(sats):
    return f"{sats_to_btc(sats):.8f} BTC"


def fmt_sats(sats):
    try:
        return f"{int(sats):,} sats".replace(",", ".")
    except Exception:
        return "—"


def is_ip_host(host):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host))


def format_unix_time(ts):
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "—"


def bech32_polymod(values):
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            if (top >> i) & 1:
                chk ^= generator[i]
    return chk


def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_decode(bech):
    if ((any(ord(x) < 33 or ord(x) > 126 for x in bech)) or
            (bech.lower() != bech and bech.upper() != bech)):
        return None, None

    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos + 7 > len(bech):
        return None, None

    if any(c not in BECH32_CHARSET for c in bech[pos + 1:]):
        return None, None

    hrp = bech[:pos]
    data = [BECH32_CHARSET.find(c) for c in bech[pos + 1:]]
    if bech32_polymod(bech32_hrp_expand(hrp) + data) != 1:
        return None, None

    return hrp, data[:-6]


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def parse_lightning_amount_msat(hrp):
    # BOLT11 HRP examples: lnbc2500u, lnbc20m, lnbc1p.
    match = re.match(r"^ln(?:bc|tb|bcrt)(\d+)?([munp])?$", hrp, re.IGNORECASE)
    if not match:
        return None

    number, multiplier = match.groups()
    if not number:
        return None

    value = int(number)
    if multiplier == "m":
        return value * 100_000_000
    if multiplier == "u":
        return value * 100_000
    if multiplier == "n":
        return value * 100
    if multiplier == "p":
        return max(1, value // 10)
    return value * 100_000_000_000


def msat_to_btc(msat):
    try:
        return float(msat) / 100_000_000_000
    except Exception:
        return 0.0


def format_msat_amount(msat):
    if msat is None:
        return "non specificato / not specified"
    sats = msat / 1000
    return f"{sats:.0f} sats · {msat_to_btc(msat):.8f} BTC"


def fivebit_to_int(values):
    result = 0
    for value in values:
        result = (result << 5) | value
    return result


def fivebit_to_bytes(values):
    converted = convertbits(values, 5, 8, False)
    if converted is None:
        return b""
    return bytes(converted)


def decode_lightning_invoice(invoice):
    hrp, data = bech32_decode(invoice)
    if not hrp or data is None:
        raise ValueError("Invalid or unsupported Bech32 Lightning invoice.")

    if len(data) < 7:
        raise ValueError("Invoice payload too short.")

    timestamp = fivebit_to_int(data[:7])
    payload = data[7:]
    parsed = {
        "hrp": hrp,
        "network": "mainnet" if hrp.startswith("lnbc") else ("testnet" if hrp.startswith("lntb") else "regtest/signet"),
        "amount_msat": parse_lightning_amount_msat(hrp),
        "timestamp": timestamp,
        "description": None,
        "payment_hash": None,
        "expiry": 3600,
        "payee_pubkey": None,
        "min_final_cltv": None,
        "tags": [],
    }

    index = 0
    while index + 3 <= len(payload):
        tag = payload[index]
        data_length = (payload[index + 1] << 5) + payload[index + 2]
        index += 3

        tag_data = payload[index:index + data_length]
        if len(tag_data) < data_length:
            break
        index += data_length

        tag_char = BECH32_CHARSET[tag] if 0 <= tag < len(BECH32_CHARSET) else "?"
        parsed["tags"].append(tag_char)

        try:
            if tag_char == "p":
                parsed["payment_hash"] = fivebit_to_bytes(tag_data).hex()
            elif tag_char == "d":
                parsed["description"] = fivebit_to_bytes(tag_data).decode("utf-8", errors="replace")
            elif tag_char == "x":
                parsed["expiry"] = fivebit_to_int(tag_data)
            elif tag_char == "n":
                parsed["payee_pubkey"] = fivebit_to_bytes(tag_data).hex()
            elif tag_char == "c":
                parsed["min_final_cltv"] = fivebit_to_int(tag_data)
        except Exception:
            continue

    return parsed


def decode_lnurl_to_url(value):
    hrp, data = bech32_decode(value)
    if hrp != "lnurl" or data is None:
        raise ValueError("Invalid LNURL.")
    decoded = convertbits(data, 5, 8, False)
    if decoded is None:
        raise ValueError("Invalid LNURL payload.")
    return bytes(decoded).decode("utf-8", errors="replace")


class Web3ShieldApp:
    def __init__(self, window):
        self.root = window
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1360x820")
        self.root.minsize(1120, 700)

        self.lang = "it"
        self.last_report = ""
        self.current_links = []
        self.active_section = "web"

        self.bg = "#071021"
        self.panel = "#0d1728"
        self.panel2 = "#111f35"
        self.card = "#10213a"
        self.card_soft = "#132944"
        self.border = "#214263"
        self.text = "#e7f3ff"
        self.muted = "#9eb6d6"
        self.accent = "#2dd4bf"
        self.accent2 = "#38bdf8"
        self.warning = "#fbbf24"
        self.danger = "#fb7185"
        self.ok = "#34d399"
        self.input_bg = "#10243d"
        self.input_border = "#2a5b7c"

        self.widgets_for_context = []
        self.card_registry: List[Tuple[tk.Label, tk.Label, tk.Button, str, str, str]] = []
        self.section_buttons = {}

        self.wallet_input = None
        self.btc_tx_input = None
        self.link_input = None
        self.contract_input = None
        self.signature_input = None
        self.lightning_input = None

        self.setup_root()
        self.build_ui()
        self.build_context_menu()
        self.render_empty_result()
        self.root.after(100, self.show_startup_disclaimer)

    def t(self, key):
        return TEXT[self.lang].get(key, key)

    def setup_root(self):
        self.root.configure(bg=self.bg)

    def draw_molinacrypto_logo(self, parent, bg_color, size=58):
        canvas = tk.Canvas(parent, width=size, height=size, bg=bg_color, highlightthickness=0, bd=0)
        outer_shadow = "#06111f"
        blue_top = "#168df7"
        blue_mid = "#0b6ee8"
        blue_bottom = "#064db8"
        pad = 2
        x1, y1, x2, y2 = pad, pad, size - pad, size - pad
        r = int(size * 0.28)

        canvas.create_oval(x1, y1, x1 + r, y1 + r, fill=outer_shadow, outline=outer_shadow)
        canvas.create_oval(x2 - r, y1, x2, y1 + r, fill=outer_shadow, outline=outer_shadow)
        canvas.create_oval(x1, y2 - r, x1 + r, y2, fill=outer_shadow, outline=outer_shadow)
        canvas.create_oval(x2 - r, y2 - r, x2, y2, fill=outer_shadow, outline=outer_shadow)
        canvas.create_rectangle(x1 + r / 2, y1, x2 - r / 2, y2, fill=outer_shadow, outline=outer_shadow)
        canvas.create_rectangle(x1, y1 + r / 2, x2, y2 - r / 2, fill=outer_shadow, outline=outer_shadow)

        ix1 = int(size * 0.09)
        iy1 = int(size * 0.09)
        ix2 = int(size * 0.91)
        iy2 = int(size * 0.91)
        ir = int(size * 0.24)

        canvas.create_oval(ix1, iy1, ix1 + ir, iy1 + ir, fill=blue_top, outline=blue_top)
        canvas.create_oval(ix2 - ir, iy1, ix2, iy1 + ir, fill=blue_top, outline=blue_top)
        canvas.create_oval(ix1, iy2 - ir, ix1 + ir, iy2, fill=blue_bottom, outline=blue_bottom)
        canvas.create_oval(ix2 - ir, iy2 - ir, ix2, iy2, fill=blue_bottom, outline=blue_bottom)
        canvas.create_rectangle(ix1 + ir / 2, iy1, ix2 - ir / 2, iy2, fill=blue_mid, outline=blue_mid)
        canvas.create_rectangle(ix1, iy1 + ir / 2, ix2, iy2 - ir / 2, fill=blue_mid, outline=blue_mid)

        canvas.create_rectangle(
            ix1 + int(size * 0.12),
            iy1 + int(size * 0.07),
            ix2 - int(size * 0.12),
            iy1 + int(size * 0.30),
            fill=blue_top,
            outline=blue_top
        )

        canvas.create_text(size / 2, size / 2 + int(size * 0.03), text="M", fill="white", font=("Arial", int(size * 0.48), "bold"))
        return canvas

    def show_startup_disclaimer(self):
        disclaimer = tk.Toplevel(self.root)
        disclaimer.title(f"{APP_NAME} · Disclaimer")
        disclaimer.configure(bg=self.bg)
        disclaimer.resizable(False, False)
        disclaimer.transient(self.root)
        disclaimer.overrideredirect(True)
        disclaimer.attributes("-topmost", True)

        width = 740
        height = 430
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        disclaimer.geometry(f"{width}x{height}+{x}+{y}")

        outer = tk.Frame(disclaimer, bg=self.bg, padx=18, pady=18)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(outer, bg=self.panel, highlightbackground=self.accent2, highlightcolor=self.accent2, highlightthickness=2, padx=22, pady=18)
        card.pack(fill="both", expand=True)

        header = tk.Frame(card, bg=self.panel)
        header.pack(fill="x", pady=(0, 14))

        icon_canvas = self.draw_molinacrypto_logo(header, self.panel, size=54)
        icon_canvas.pack(side="left", padx=(0, 12))

        title_box = tk.Frame(header, bg=self.panel)
        title_box.pack(side="left", fill="x", expand=True)

        title = tk.Label(title_box, text="MolinaCrypto Web3 Shield", bg=self.panel, fg=self.text, font=("Arial", 20, "bold"))
        title.pack(anchor="w")

        subtitle = tk.Label(title_box, text="Disclaimer · Informational security check", bg=self.panel, fg=self.accent2, font=("Arial", 10, "bold"))
        subtitle.pack(anchor="w", pady=(3, 0))

        line = tk.Frame(card, bg=self.border, height=1)
        line.pack(fill="x", pady=(0, 14))

        text_box = tk.Text(card, bg=self.panel, fg=self.text, relief="flat", wrap="word", font=("Arial", 10), padx=4, pady=4, height=13, cursor="arrow")
        text_box.pack(fill="both", expand=True)

        disclaimer_text = (
            "ITALIANO\n"
            "Questo tool può effettuare richieste a servizi esterni e utilizza controlli matematici ed euristici "
            "su dati pubblici e indicatori di rischio. I risultati forniscono un grado di rischio orientativo, "
            "non una certezza assoluta di sicurezza, e non costituiscono consulenza finanziaria, legale, fiscale "
            "o professionale. La responsabilità delle decisioni operative resta dell’utente.\n\n"
            "ENGLISH\n"
            "This tool may query external services and uses mathematical and heuristic checks based on public data "
            "and risk indicators. The results provide an indicative risk level, not an absolute guarantee of safety, "
            "and do not constitute financial, legal, tax or professional advice. The user remains responsible for "
            "any operational decision."
        )

        text_box.insert("1.0", disclaimer_text)
        text_box.tag_configure("heading", foreground=self.accent2, font=("Arial", 10, "bold"))
        text_box.tag_add("heading", "1.0", "1.end")
        text_box.tag_add("heading", "4.0", "4.end")
        text_box.configure(state="disabled")

        button_row = tk.Frame(card, bg=self.panel)
        button_row.pack(fill="x", pady=(16, 0))

        def accept_disclaimer():
            try:
                disclaimer.grab_release()
            except Exception:
                pass
            try:
                disclaimer.attributes("-topmost", False)
            except Exception:
                pass
            try:
                disclaimer.destroy()
            except Exception:
                pass
            self.root.after(100, self.root.focus_force)

        def reject_disclaimer():
            try:
                disclaimer.grab_release()
            except Exception:
                pass
            try:
                disclaimer.attributes("-topmost", False)
            except Exception:
                pass
            try:
                disclaimer.destroy()
            except Exception:
                pass
            self.root.after(50, self.root.destroy)

        reject_btn = tk.Button(button_row, text="Rifiuta / Reject", command=reject_disclaimer, bg="#7f1d1d", fg="white", activebackground="#991b1b", activeforeground="white", relief="flat", padx=18, pady=8, font=("Arial", 10, "bold"), cursor="hand2")
        reject_btn.pack(side="right", padx=(10, 0))

        ok_btn = tk.Button(button_row, text="Ho capito / I understand", command=accept_disclaimer, bg="#0f766e", fg="white", activebackground="#14b8a6", activeforeground="white", relief="flat", padx=18, pady=8, font=("Arial", 10, "bold"), cursor="hand2")
        ok_btn.pack(side="right")

        disclaimer.bind("<Escape>", lambda event: "break")
        disclaimer.bind("<Alt-F4>", lambda event: "break")

        def bring_disclaimer_to_front():
            disclaimer.lift()
            disclaimer.focus_force()
            ok_btn.focus_force()
            disclaimer.attributes("-topmost", True)

        disclaimer.after(100, bring_disclaimer_to_front)
        ok_btn.focus_set()
        disclaimer.grab_set()
        disclaimer.wait_window()

        try:
            self.root.focus_force()
        except Exception:
            pass

    def build_ui(self):
        self.main = tk.Frame(self.root, bg=self.bg)
        self.main.pack(fill="both", expand=True, padx=14, pady=8)
        self.build_header()
        self.build_footer()
        self.build_body()

    def build_header(self):
        header = tk.Frame(self.main, bg=self.bg)
        header.pack(fill="x", pady=(0, 10))

        left = tk.Frame(header, bg=self.bg)
        left.pack(side="left", fill="x", expand=True)

        title_row = tk.Frame(left, bg=self.bg)
        title_row.pack(anchor="w")

        logo_canvas = self.draw_molinacrypto_logo(title_row, self.bg, size=58)
        logo_canvas.pack(side="left", padx=(0, 10))

        title_box = tk.Frame(title_row, bg=self.bg)
        title_box.pack(side="left")

        self.title_label = tk.Label(title_box, text=APP_NAME, bg=self.bg, fg=self.text, font=("Arial", 26, "bold"))
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(title_box, text=self.t("subtitle"), bg=self.bg, fg=self.muted, font=("Arial", 12))
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        self.claim_label = tk.Label(left, text=self.t("claim"), bg=self.bg, fg=self.accent, font=("Arial", 10, "bold"))
        self.claim_label.pack(anchor="w", pady=(8, 0))

        right = tk.Frame(header, bg=self.bg)
        right.pack(side="right", anchor="ne")

        version = tk.Label(right, text=f"v{APP_VERSION} · © 2026 {AUTHOR}", bg=self.bg, fg=self.muted, font=("Arial", 9))
        version.pack(anchor="e", pady=(0, 8))

        language_row = tk.Frame(right, bg=self.bg)
        language_row.pack(anchor="e")

        self.language_small_label = tk.Label(language_row, text=self.t("language_label"), bg=self.bg, fg=self.muted, font=("Arial", 9))
        self.language_small_label.pack(side="left", padx=(0, 8))

        self.lang_btn = self.small_button(language_row, self.t("language_btn"), self.toggle_language)
        self.lang_btn.pack(side="left")

        line = tk.Frame(self.main, bg=self.border, height=1)
        line.pack(fill="x", pady=(0, 10))

    def build_body(self):
        body = tk.Frame(self.main, bg=self.bg)
        body.pack(side="top", fill="both", expand=True)

        left = self.create_scrollable_control_panel(body)
        right = tk.Frame(body, bg=self.bg)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.build_section_controls(left)

        self.build_actions_panel(right)
        self.build_result_panel(right)

    def create_scrollable_control_panel(self, parent):
        outer = tk.Frame(parent, bg=self.bg, width=470)
        outer.pack(side="left", fill="both", padx=(0, 10))
        outer.pack_propagate(False)

        self.left_canvas = tk.Canvas(outer, bg=self.bg, highlightthickness=0, bd=0)
        self.left_canvas.pack(side="left", fill="both", expand=True)

        self.left_scrollbar = tk.Scrollbar(outer, orient="vertical", command=self.left_canvas.yview)
        self.left_scrollbar.pack(side="right", fill="y")
        self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

        self.left_scrollable_frame = tk.Frame(self.left_canvas, bg=self.bg)
        self.left_canvas_window = self.left_canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor="nw")

        self.left_scrollable_frame.bind("<Configure>", self.update_left_scroll_region)
        self.left_canvas.bind("<Configure>", self.update_left_canvas_width)
        self.left_canvas.bind_all("<MouseWheel>", self.on_mousewheel_windows)
        self.left_canvas.bind_all("<Button-4>", self.on_mousewheel_linux)
        self.left_canvas.bind_all("<Button-5>", self.on_mousewheel_linux)

        return self.left_scrollable_frame

    def update_left_scroll_region(self, _event=None):
        try:
            self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
        except Exception:
            pass

    def update_left_canvas_width(self, event):
        try:
            self.left_canvas.itemconfigure(self.left_canvas_window, width=event.width)
        except Exception:
            pass

    def on_mousewheel_windows(self, event):
        try:
            self.left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def on_mousewheel_linux(self, event):
        try:
            if event.num == 4:
                self.left_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.left_canvas.yview_scroll(1, "units")
        except Exception:
            pass

    def build_section_controls(self, parent):
        tabs_card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1,
            padx=10,
            pady=10
        )
        tabs_card.pack(fill="x", pady=(0, 10))

        self.tabs_frame = tk.Frame(tabs_card, bg=self.panel)
        self.tabs_frame.pack(fill="x")

        self.section_buttons = {}

        for section_key, label_key in [
            ("wallet", "tab_wallet"),
            ("web", "tab_web"),
            ("lightning", "tab_lightning"),
        ]:
            btn = tk.Button(
                self.tabs_frame,
                text=self.t(label_key),
                command=partial(self.show_section, section_key),
                relief="flat",
                padx=12,
                pady=8,
                font=("Arial", 9, "bold"),
                cursor="hand2"
            )
            btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
            self.section_buttons[section_key] = btn

        self.section_title = tk.Label(
            parent,
            text="",
            bg=self.bg,
            fg=self.text,
            font=("Arial", 16, "bold")
        )
        self.section_title.pack(anchor="w", pady=(4, 2))

        self.section_desc = tk.Label(
            parent,
            text="",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9),
            wraplength=430,
            justify="left"
        )
        self.section_desc.pack(anchor="w", pady=(0, 10))

        self.cards_container = tk.Frame(parent, bg=self.bg)
        self.cards_container.pack(fill="both", expand=True)

        self.show_section(self.active_section)

    def style_section_buttons(self):
        for key, btn in self.section_buttons.items():
            if key == self.active_section:
                btn.configure(bg=self.accent2, fg="#06111f", activebackground=self.accent, activeforeground="#06111f")
            else:
                btn.configure(bg=self.card_soft, fg=self.text, activebackground=self.border, activeforeground="white")

    def show_section(self, section):
        self.active_section = section
        self.style_section_buttons()
        self.card_registry = []

        for child in self.cards_container.winfo_children():
            child.destroy()

        self.wallet_input = None
        self.btc_tx_input = None
        self.link_input = None
        self.contract_input = None
        self.signature_input = None
        self.lightning_input = None

        if section == "wallet":
            self.section_title.configure(text=self.t("section_wallet_title"))
            self.section_desc.configure(text=self.t("section_wallet_desc"))
            self.build_wallet_section(self.cards_container)
        elif section == "lightning":
            self.section_title.configure(text=self.t("section_lightning_title"))
            self.section_desc.configure(text=self.t("section_lightning_desc"))
            self.build_lightning_section(self.cards_container)
        else:
            self.section_title.configure(text=self.t("section_web_title"))
            self.section_desc.configure(text=self.t("section_web_desc"))
            self.build_web_risk_section(self.cards_container)

        self.update_left_scroll_region()

    def build_wallet_section(self, parent):
        self.wallet_input = self.create_check_card(parent, "wallet_card", "wallet_hint", "wallet_btn", self.analyze_wallet, multiline=False)
        self.btc_tx_input = self.create_check_card(parent, "btc_tx_card", "btc_tx_hint", "btc_tx_btn", self.analyze_btc_transaction, multiline=False)

    def build_web_risk_section(self, parent):
        self.link_input = self.create_check_card(parent, "link_card", "link_hint", "link_btn", self.analyze_link, multiline=False)
        self.contract_input = self.create_check_card(parent, "contract_card", "contract_hint", "contract_btn", self.analyze_contract, multiline=False)
        self.signature_input = self.create_check_card(parent, "signature_card", "signature_hint", "signature_btn", self.analyze_signature, multiline=True)

    def build_lightning_section(self, parent):
        self.lightning_input = self.create_check_card(parent, "lightning_card", "lightning_hint", "lightning_btn", self.analyze_lightning, multiline=True)

    def create_check_card(self, parent, title_key, hint_key, button_key, command, multiline=False):
        card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1,
            padx=14,
            pady=10
        )
        card.pack(fill="x", pady=(0, 10))

        title_label = tk.Label(
            card,
            text=self.t(title_key),
            bg=self.panel,
            fg=self.accent2,
            font=("Arial", 14, "bold")
        )
        title_label.pack(anchor="w")

        hint_label = tk.Label(
            card,
            text=self.t(hint_key),
            bg=self.panel,
            fg=self.muted,
            font=("Arial", 9),
            wraplength=410,
            justify="left"
        )
        hint_label.pack(anchor="w", pady=(2, 8))

        input_widget: Any

        if multiline:
            text_field = tk.Text(
                card,
                height=5,
                bg=self.input_bg,
                fg=self.text,
                insertbackground=self.text,
                selectbackground=self.accent2,
                selectforeground="#06111f",
                relief="flat",
                font=("Arial", 10),
                padx=10,
                pady=8,
                wrap="word"
            )
            text_field.pack(fill="x", pady=(0, 10))
            text_field.configure(
                highlightthickness=1,
                highlightbackground=self.input_border,
                highlightcolor=self.accent
            )
            self.register_context_widget(text_field)
            input_widget = text_field
        else:
            entry_field = tk.Entry(
                card,
                bg=self.input_bg,
                fg=self.text,
                insertbackground=self.text,
                selectbackground=self.accent2,
                selectforeground="#06111f",
                relief="flat",
                font=("Arial", 11)
            )
            entry_field.pack(fill="x", ipady=8, pady=(0, 10))
            entry_field.bind("<Return>", lambda event: command())
            entry_field.configure(
                highlightthickness=1,
                highlightbackground=self.input_border,
                highlightcolor=self.accent
            )
            self.register_context_widget(entry_field)
            input_widget = entry_field

        button = self.primary_button(card, self.t(button_key), command)
        button.pack(anchor="e")

        self.card_registry.append(
            (title_label, hint_label, button, title_key, hint_key, button_key)
        )

        return input_widget

    def build_result_panel(self, parent):
        result_card = tk.Frame(parent, bg=self.panel, highlightbackground=self.border, highlightthickness=1, padx=16, pady=14)
        result_card.pack(side="top", fill="both", expand=True)

        self.result_title = tk.Label(result_card, text=self.t("result_title"), bg=self.panel, fg=self.text, font=("Arial", 18, "bold"))
        self.result_title.pack(anchor="w")

        self.result_badge = tk.Label(result_card, text="—", bg=self.card_soft, fg=self.muted, font=("Arial", 12, "bold"), padx=10, pady=5)
        self.result_badge.pack(anchor="w", pady=(8, 10))

        self.result_text = tk.Text(result_card, bg=self.panel, fg=self.text, insertbackground=self.text, relief="flat", wrap="word", font=("Arial", 11), padx=0, pady=0)
        self.result_text.pack(fill="both", expand=True)
        self.result_text.configure(state="disabled")
        self.register_context_widget(self.result_text)

    def build_actions_panel(self, parent):
        actions_card = tk.Frame(parent, bg=self.panel, highlightbackground=self.border, highlightthickness=1, padx=14, pady=10)
        actions_card.pack(side="bottom", fill="x", pady=(8, 0))

        self.actions_title = tk.Label(actions_card, text=self.t("actions_title"), bg=self.panel, fg=self.accent2, font=("Arial", 13, "bold"))
        self.actions_title.pack(anchor="w", pady=(0, 6))

        self.actions_frame = tk.Frame(actions_card, bg=self.panel)
        self.actions_frame.pack(fill="x")

        bottom = tk.Frame(actions_card, bg=self.panel)
        bottom.pack(fill="x", pady=(10, 0))

        self.report_btn = self.primary_button(bottom, self.t("report_btn"), self.export_report)
        self.report_btn.pack(side="left")

        self.clear_btn = self.secondary_button(bottom, self.t("clear_btn"), self.clear_all)
        self.clear_btn.pack(side="left", padx=(8, 0))

    def build_footer(self):
        footer = tk.Frame(self.main, bg=self.bg)
        footer.pack(side="bottom", fill="x", pady=(8, 0))

        self.status_label = tk.Label(footer, text="Ready", bg=self.bg, fg=self.muted, font=("Arial", 9))
        self.status_label.pack(side="left")

        site = self.secondary_button(footer, self.t("site_btn"), lambda: webbrowser.open(WEBSITE))
        site.pack(side="right")

        resources = self.secondary_button(footer, self.t("resources_btn"), lambda: webbrowser.open(RESOURCES_URL))
        resources.pack(side="right", padx=(0, 8))

    def primary_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg="#0f766e", fg="white", activebackground="#14b8a6", activeforeground="white", relief="flat", padx=14, pady=7, font=("Arial", 10, "bold"), cursor="hand2")

    def secondary_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg=self.card_soft, fg=self.text, activebackground=self.border, activeforeground="white", relief="flat", padx=12, pady=7, font=("Arial", 9, "bold"), cursor="hand2")

    def small_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, bg=self.card_soft, fg=self.text, activebackground=self.border, activeforeground="white", relief="flat", padx=12, pady=5, font=("Arial", 9, "bold"), cursor="hand2")

    def build_context_menu(self):
        self.context_target = None
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.panel2, fg=self.text, activebackground=self.accent2, activeforeground="#06111f")
        self.refresh_context_menu_labels()
        self.root.bind("<Button-1>", self.hide_context_menu_global, add="+")
        self.root.bind("<Escape>", lambda event: self.hide_context_menu())

    def refresh_context_menu_labels(self):
        self.context_menu.delete(0, "end")
        self.context_menu.add_command(label=self.t("cut"), command=self.context_cut)
        self.context_menu.add_command(label=self.t("copy"), command=self.context_copy)
        self.context_menu.add_command(label=self.t("paste"), command=self.context_paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.t("select_all"), command=self.context_select_all)

    def register_context_widget(self, widget):
        self.widgets_for_context.append(widget)
        widget.bind("<Button-3>", self.show_context_menu)
        widget.bind("<Button-2>", self.show_context_menu)
        widget.bind("<Control-a>", self.select_all_event)
        widget.bind("<Control-A>", self.select_all_event)

    def show_context_menu(self, event):
        self.context_target = event.widget
        self.hide_context_menu()
        self.context_target.focus_set()
        self.context_menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def hide_context_menu_global(self, event=None):
        try:
            if event and event.widget == self.context_menu:
                return
            self.hide_context_menu()
        except Exception:
            pass

    def hide_context_menu(self):
        try:
            self.context_menu.unpost()
        except Exception:
            pass

    def context_cut(self):
        if self.context_target:
            self.context_target.event_generate("<<Cut>>")
        self.hide_context_menu()

    def context_copy(self):
        if self.context_target:
            self.context_target.event_generate("<<Copy>>")
        self.hide_context_menu()

    def context_paste(self):
        if self.context_target:
            self.context_target.event_generate("<<Paste>>")
        self.hide_context_menu()

    def context_select_all(self):
        if self.context_target:
            self.select_all_widget(self.context_target)
        self.hide_context_menu()

    def select_all_event(self, event):
        self.select_all_widget(event.widget)
        return "break"

    def select_all_widget(self, widget):
        try:
            widget.focus_set()
            if isinstance(widget, tk.Text):
                widget.tag_add("sel", "1.0", "end-1c")
                widget.mark_set("insert", "end-1c")
            else:
                widget.selection_range(0, "end")
                widget.icursor("end")
        except Exception:
            pass

    def get_widget_text(self, widget):
        if widget is None:
            return ""
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()
        return widget.get().strip()

    def set_result_text(self, text, badge_text="—", badge_color=None):
        self.result_badge.configure(text=badge_text, fg="white", bg=badge_color or self.card_soft)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", text)
        self.result_text.configure(state="disabled")
        self.last_report = text

    def clear_actions(self):
        for child in self.actions_frame.winfo_children():
            child.destroy()
        self.current_links = []

    def add_action_button(self, label, url):
        self.current_links.append((label, url))
        btn = self.secondary_button(self.actions_frame, label, lambda link=url: webbrowser.open(link))
        btn.pack(side="left", padx=(0, 8), pady=(0, 6))

    def render_empty_result(self):
        self.clear_actions()
        self.set_result_text(self.t("empty_result"), "Web3 Shield", self.card_soft)

    def clear_all(self):
        for widget in [self.wallet_input, self.btc_tx_input, self.link_input, self.contract_input]:
            try:
                if widget is not None:
                    widget.delete(0, "end")
            except Exception:
                pass
        for widget in [self.signature_input, self.lightning_input]:
            try:
                if widget is not None:
                    widget.delete("1.0", "end")
            except Exception:
                pass
        self.last_report = ""
        self.render_empty_result()
        self.status_label.configure(text="Ready")

    def risk_label_and_color(self, score):
        if score >= 80:
            return self.t("risk_low"), self.ok
        if score >= 55:
            return self.t("risk_medium"), self.warning
        return self.t("risk_high"), self.danger

    def format_result(self, kind, score, recommendation, indicators, limitation):
        risk, _ = self.risk_label_and_color(score)
        lines = [
            f"{self.t('type')}: {kind}",
            f"{self.t('score')}: {score}/100 · {risk}",
            "",
            f"{self.t('recommendation')}:",
            recommendation,
            "",
            f"{self.t('indicators')}:",
        ]
        for item in indicators:
            lines.append(f"• {item}")
        lines.extend(["", f"{self.t('limits')}:", limitation])
        return "\n".join(lines)

    def analyze_wallet(self):
        value = self.get_widget_text(self.wallet_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        wallet_type = detect_wallet_type(value)
        if wallet_type == "BTC":
            self.status_label.configure(text="Loading Bitcoin public data...")
            self.set_result_text("Analisi Bitcoin in corso..." if self.lang == "it" else "Bitcoin analysis in progress...", "BTC", self.warning)
            threading.Thread(target=self.load_btc_wallet, args=(value,), daemon=True).start()
            return

        if wallet_type == "EVM":
            self.render_evm_wallet(value)
            return

        if BTC_TXID_PATTERN.match(value):
            self.set_result_text(
                "Questo sembra un TXID Bitcoin: usa la scheda Wallet & TX → Bitcoin TX Check." if self.lang == "it" else "This looks like a Bitcoin TXID: use Wallet & TX → Bitcoin TX Check.",
                "TXID",
                self.warning
            )
            return

        score = 25
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato non riconosciuto come Bitcoin o Ethereum/EVM." if self.lang == "it" else "Format not recognized as Bitcoin or Ethereum/EVM.",
            "Potrebbe essere copiato male o appartenere a una chain non ancora supportata." if self.lang == "it" else "It may be copied incorrectly or belong to an unsupported chain.",
        ]
        recommendation = "Ricontrolla l’indirizzo dalla fonte originale. Non inviare fondi a indirizzi di formato incerto." if self.lang == "it" else "Re-check the address from the original source. Do not send funds to uncertain address formats."
        limitation = "Il controllo verifica solo pattern di formato, non la proprietà dell’indirizzo." if self.lang == "it" else "The check verifies only format patterns, not address ownership."
        text = self.format_result("UNKNOWN ADDRESS", score, recommendation, indicators, limitation)
        self.clear_actions()
        self.set_result_text(text, risk, color)

    def load_btc_wallet(self, address):
        try:
            quoted = urllib.parse.quote(address, safe="")
            data = fetch_json(MEMPOOL_ADDRESS_API.format(address=quoted), timeout=18)
            fees = fetch_json(MEMPOOL_FEES_API, timeout=15)

            chain = data.get("chain_stats", {}) or {}
            mempool = data.get("mempool_stats", {}) or {}

            funded = int(chain.get("funded_txo_sum", 0) or 0)
            spent = int(chain.get("spent_txo_sum", 0) or 0)
            tx_count = int(chain.get("tx_count", 0) or 0)

            mem_funded = int(mempool.get("funded_txo_sum", 0) or 0)
            mem_spent = int(mempool.get("spent_txo_sum", 0) or 0)
            mem_tx_count = int(mempool.get("tx_count", 0) or 0)

            confirmed_balance = funded - spent
            mempool_delta = mem_funded - mem_spent
            fastest_fee = fees.get("fastestFee", "—")

            self.root.after(0, lambda: self.render_btc_wallet(address, confirmed_balance, mempool_delta, tx_count, mem_tx_count, fastest_fee))
        except Exception as error:
            self.root.after(0, lambda: self.render_btc_error(address, str(error)))

    def render_btc_wallet(self, address, confirmed_balance, mempool_delta, tx_count, mem_tx_count, fastest_fee):
        score = 100
        indicators = []

        if self.lang == "it":
            indicators.extend([
                "Indirizzo Bitcoin valido.",
                f"Saldo confermato: {fmt_btc(confirmed_balance)}.",
                f"Saldo non confermato/mempool: {fmt_btc(mempool_delta)}.",
                f"Transazioni confermate: {tx_count}.",
                f"Transazioni non confermate: {mem_tx_count}.",
                f"Fee veloce stimata: {fastest_fee} sat/vB.",
            ])
        else:
            indicators.extend([
                "Valid Bitcoin address.",
                f"Confirmed balance: {fmt_btc(confirmed_balance)}.",
                f"Unconfirmed/mempool balance: {fmt_btc(mempool_delta)}.",
                f"Confirmed transactions: {tx_count}.",
                f"Unconfirmed transactions: {mem_tx_count}.",
                f"Estimated fastest fee: {fastest_fee} sat/vB.",
            ])

        if tx_count > 25:
            score -= 18
            indicators.append("Indirizzo molto riutilizzato: privacy più debole." if self.lang == "it" else "Heavily reused address: weaker privacy.")
        elif tx_count > 5:
            score -= 8
            indicators.append("Indirizzo già riutilizzato più volte." if self.lang == "it" else "Address reused several times.")

        if confirmed_balance > 0:
            score -= 6
            indicators.append("Saldo positivo: attenzione prima di condividere o usare questo address." if self.lang == "it" else "Positive balance: be careful before sharing or using this address.")

        if mempool_delta != 0:
            score -= 12
            indicators.append("Movimenti non confermati presenti." if self.lang == "it" else "Unconfirmed movements present.")

        try:
            fee = float(fastest_fee)
            if fee > 50:
                score -= 12
                indicators.append("Fee Bitcoin elevate: evitare operazioni frettolose se non urgenti." if self.lang == "it" else "High Bitcoin fees: avoid rushed non-urgent operations.")
        except Exception:
            score -= 3

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)
        recommendation = "Verifica movimenti su explorer, valuta le fee prima di inviare BTC e non inserire mai seed phrase in nessun tool." if self.lang == "it" else "Verify movements on explorers, check fees before sending BTC and never enter seed phrases into any tool."
        limitation = "Il controllo usa dati pubblici mempool.space. Non identifica il proprietario dell’indirizzo e non garantisce assenza di rischio operativo." if self.lang == "it" else "The check uses public mempool.space data. It does not identify address ownership and does not guarantee absence of operational risk."
        text = self.format_result("BITCOIN ADDRESS", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Mempool.space", f"https://mempool.space/address/{address}")
        self.add_action_button("Blockstream", f"https://blockstream.info/address/{address}")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="BTC analysis completed")

    def render_btc_error(self, address, error):
        score = 55
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato Bitcoin valido, ma lettura API non riuscita." if self.lang == "it" else "Valid Bitcoin format, but API reading failed.",
            f"Errore: {error}" if self.lang == "it" else f"Error: {error}",
        ]
        recommendation = "Apri manualmente gli explorer e verifica connessione/API." if self.lang == "it" else "Open explorers manually and check connection/API."
        limitation = "Il controllo dipende dalla disponibilità delle API pubbliche." if self.lang == "it" else "The check depends on public API availability."
        text = self.format_result("BITCOIN ADDRESS", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Mempool.space", f"https://mempool.space/address/{address}")
        self.add_action_button("Blockstream", f"https://blockstream.info/address/{address}")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="BTC API error")

    def render_evm_wallet(self, address):
        score = 72
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato Ethereum/EVM valido." if self.lang == "it" else "Valid Ethereum/EVM format.",
            "Il solo indirizzo pubblico non consente di spendere fondi." if self.lang == "it" else "The public address alone cannot spend funds.",
            "Il rischio principale deriva da approvals, firme e siti collegati al wallet." if self.lang == "it" else "Main risk comes from approvals, signatures and websites connected to the wallet.",
        ]
        recommendation = "Controlla approvals su Revoke.cash/Etherscan e non usare il wallet principale su dApp sconosciute." if self.lang == "it" else "Check approvals on Revoke.cash/Etherscan and do not use the main wallet on unknown dApps."
        limitation = "Senza API key dedicate il tool non legge saldo/token EVM in automatico: apre però gli strumenti corretti con un click." if self.lang == "it" else "Without dedicated API keys the tool does not automatically read EVM balances/tokens, but opens the correct tools with one click."
        text = self.format_result("ETHEREUM / EVM ADDRESS", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_evm_links(address)
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="EVM analysis completed")

    def analyze_btc_transaction(self):
        txid = self.get_widget_text(self.btc_tx_input).lower()
        if not txid:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return
        if not BTC_TXID_PATTERN.match(txid):
            score = 25
            risk, color = self.risk_label_and_color(score)
            indicators = [
                "Il TXID Bitcoin deve essere una stringa esadecimale di 64 caratteri." if self.lang == "it" else "A Bitcoin TXID must be a 64-character hexadecimal string.",
                "Ricontrolla di non aver copiato spazi, URL completi o dati incompleti." if self.lang == "it" else "Check that you did not copy spaces, full URLs or incomplete data.",
            ]
            recommendation = "Copia solo l'identificativo della transazione, non tutto il link dell'explorer." if self.lang == "it" else "Copy only the transaction identifier, not the full explorer URL."
            limitation = "Il controllo non può analizzare stringhe che non sono TXID Bitcoin validi." if self.lang == "it" else "The check cannot analyze strings that are not valid Bitcoin TXIDs."
            self.clear_actions()
            self.set_result_text(self.format_result("INVALID BITCOIN TXID", score, recommendation, indicators, limitation), risk, color)
            return

        self.status_label.configure(text="Loading Bitcoin transaction...")
        self.set_result_text("Analisi transazione Bitcoin in corso..." if self.lang == "it" else "Bitcoin transaction analysis in progress...", "BTC TX", self.warning)
        threading.Thread(target=self.load_btc_transaction, args=(txid,), daemon=True).start()

    def load_btc_transaction(self, txid):
        try:
            data = fetch_json(MEMPOOL_TX_API.format(txid=urllib.parse.quote(txid, safe="")), timeout=18)
            self.root.after(0, lambda: self.render_btc_transaction(txid, data))
        except Exception as error:
            self.root.after(0, lambda: self.render_btc_transaction_error(txid, str(error)))

    def render_btc_transaction(self, txid, data):
        score = 100
        indicators = []
        status = data.get("status", {}) or {}
        vin = data.get("vin", []) or []
        vout = data.get("vout", []) or []
        fee = int(data.get("fee", 0) or 0)
        weight = int(data.get("weight", 0) or 0)
        vsize = max(1, int((weight + 3) / 4)) if weight else int(data.get("size", 1) or 1)
        fee_rate = fee / max(1, vsize)

        confirmed = bool(status.get("confirmed"))
        output_total = sum(int(out.get("value", 0) or 0) for out in vout)

        if confirmed:
            indicators.append("Transazione confermata." if self.lang == "it" else "Transaction confirmed.")
            if status.get("block_height"):
                indicators.append((f"Blocco: {status.get('block_height')}." if self.lang == "it" else f"Block: {status.get('block_height')}."))
            if status.get("block_time"):
                indicators.append((f"Ora blocco: {format_unix_time(status.get('block_time'))}." if self.lang == "it" else f"Block time: {format_unix_time(status.get('block_time'))}."))
        else:
            score -= 28
            indicators.append("Transazione non ancora confermata/mempool." if self.lang == "it" else "Transaction not yet confirmed / in mempool.")

        indicators.extend([
            (f"Input: {len(vin)}." if self.lang == "it" else f"Inputs: {len(vin)}."),
            (f"Output: {len(vout)}." if self.lang == "it" else f"Outputs: {len(vout)}."),
            (f"Totale output: {fmt_btc(output_total)}." if self.lang == "it" else f"Output total: {fmt_btc(output_total)}."),
            (f"Fee: {fmt_sats(fee)}." if self.lang == "it" else f"Fee: {fmt_sats(fee)}."),
            (f"Fee rate stimato: {fee_rate:.2f} sat/vB." if self.lang == "it" else f"Estimated fee rate: {fee_rate:.2f} sat/vB."),
        ])

        if not confirmed and fee_rate < 2:
            score -= 22
            indicators.append("Fee rate molto basso: possibile conferma lenta o necessità di RBF/CPFP." if self.lang == "it" else "Very low fee rate: possible slow confirmation or need for RBF/CPFP.")
        elif not confirmed and fee_rate < 5:
            score -= 10
            indicators.append("Fee rate basso: la conferma potrebbe richiedere tempo." if self.lang == "it" else "Low fee rate: confirmation may take time.")

        if len(vin) > 20 or len(vout) > 20:
            score -= 8
            indicators.append("Transazione complessa con molti input/output." if self.lang == "it" else "Complex transaction with many inputs/outputs.")

        if output_total > 100_000_000:
            score -= 3
            indicators.append("Importo complessivo superiore a 1 BTC: verificare con attenzione contesto e destinatari." if self.lang == "it" else "Total output amount above 1 BTC: carefully verify context and recipients.")

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)
        recommendation = "Se la transazione non è confermata, controlla fee rate e mempool prima di considerarla definitiva." if self.lang == "it" else "If the transaction is unconfirmed, check fee rate and mempool before considering it final."
        limitation = "Il controllo usa dati pubblici mempool.space. Non identifica il proprietario degli address e non garantisce finalità economica della transazione." if self.lang == "it" else "The check uses public mempool.space data. It does not identify address ownership or guarantee the economic purpose of the transaction."
        text = self.format_result("BITCOIN TRANSACTION", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Mempool.space TX", f"https://mempool.space/tx/{txid}")
        self.add_action_button("Blockstream TX", f"https://blockstream.info/tx/{txid}")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Bitcoin transaction analysis completed")

    def render_btc_transaction_error(self, txid, error):
        score = 55
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato TXID valido, ma lettura API non riuscita." if self.lang == "it" else "Valid TXID format, but API reading failed.",
            f"Errore: {error}" if self.lang == "it" else f"Error: {error}",
        ]
        recommendation = "Apri manualmente gli explorer e verifica che il TXID esista." if self.lang == "it" else "Open explorers manually and verify that the TXID exists."
        limitation = "Il controllo dipende dalla disponibilità delle API pubbliche." if self.lang == "it" else "The check depends on public API availability."
        text = self.format_result("BITCOIN TRANSACTION", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Mempool.space TX", f"https://mempool.space/tx/{txid}")
        self.add_action_button("Blockstream TX", f"https://blockstream.info/tx/{txid}")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Bitcoin TX API error")

    def analyze_link(self):
        value = self.get_widget_text(self.link_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        if EMAIL_PATTERN.match(value):
            score, indicators = analyze_email_address(value, self.lang)
            risk, color = self.risk_label_and_color(score)
            recommendation = "Verifica il mittente da canali ufficiali. Non cliccare link ricevuti via e-mail se dominio o contesto non sono chiari." if self.lang == "it" else "Verify the sender through official channels. Do not click links received by e-mail if domain or context is unclear."
            limitation = "Il controllo valuta formato e indicatori statici dell’indirizzo e-mail; non verifica la casella reale né l’autenticità del mittente." if self.lang == "it" else "The check evaluates e-mail format and static indicators; it does not verify the mailbox or sender authenticity."
            text = self.format_result("EMAIL / PHISHING CHECK", score, recommendation, indicators, limitation)

            domain = value.split("@", 1)[1].lower()
            self.clear_actions()
            self.add_action_button("Google search", f"https://www.google.com/search?q={urllib.parse.quote(domain, safe='')}")
            self.set_result_text(text, risk, color)
            self.status_label.configure(text="Email analysis completed")
            return

        if not is_valid_url_input(value):
            title = "Formato URL non valido" if self.lang == "it" else "Invalid URL format"
            msg = (
                "Inserisci un URL completo in uno di questi formati:\n\nhttps://sito.com\nhttp://sito.com\nwww.sito.com\n\nOppure inserisci un indirizzo e-mail valido."
                if self.lang == "it"
                else "Enter a complete URL in one of these formats:\n\nhttps://site.com\nhttp://site.com\nwww.site.com\n\nOr enter a valid e-mail address."
            )
            messagebox.showwarning(title, msg)
            return

        normalized, parsed, host = normalize_url(value)
        score = 100
        indicators = []

        if not host:
            score = 15
            indicators.append("URL non interpretabile." if self.lang == "it" else "URL cannot be parsed.")
        else:
            indicators.append(f"Dominio analizzato: {host}" if self.lang == "it" else f"Analyzed domain: {host}")

            if parsed.scheme != "https":
                score -= 25
                indicators.append("Non usa HTTPS." if self.lang == "it" else "Does not use HTTPS.")

            if "xn--" in host:
                score -= 30
                indicators.append("Dominio punycode: possibile uso di caratteri ingannevoli." if self.lang == "it" else "Punycode domain: possible deceptive characters.")

            if is_ip_host(host):
                score -= 25
                indicators.append("Usa un indirizzo IP invece di un dominio leggibile." if self.lang == "it" else "Uses an IP address instead of a readable domain.")

            if host.count("-") >= 3:
                score -= 12
                indicators.append("Molti trattini nel dominio." if self.lang == "it" else "Many hyphens in domain.")

            if len(host) > 38:
                score -= 10
                indicators.append("Dominio molto lungo." if self.lang == "it" else "Very long domain.")

            full_lower = normalized.lower()
            suspicious_hits = [word for word in SUSPICIOUS_WORDS if word in full_lower]
            if suspicious_hits:
                score -= min(35, len(suspicious_hits) * 7)
                indicators.append(("Parole sospette: " if self.lang == "it" else "Suspicious words: ") + ", ".join(suspicious_hits[:8]))

            brand_hits = [brand for brand in KNOWN_BRANDS if brand in host]
            if brand_hits:
                official_like = any(host == f"{brand}.com" or host.endswith(f".{brand}.com") for brand in brand_hits)
                if not official_like:
                    score -= 18
                    indicators.append(("Contiene brand noti ma non sembra dominio ufficiale: " if self.lang == "it" else "Contains known brands but does not look official: ") + ", ".join(brand_hits[:5]))

            if len(indicators) == 1:
                indicators.append("Nessun indicatore statico forte emerso." if self.lang == "it" else "No strong static indicator detected.")

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)
        recommendation = "Se il rischio è medio/alto, non collegare il wallet principale. Verifica il dominio partendo dal sito ufficiale del progetto." if self.lang == "it" else "If risk is medium/high, do not connect the main wallet. Verify the domain starting from the official project website."
        limitation = "Il controllo non visita il sito e non analizza codice JavaScript: valuta solo indicatori statici del link." if self.lang == "it" else "The check does not visit the website or analyze JavaScript code: it only evaluates static link indicators."
        text = self.format_result("WEB3 LINK / DAPP", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Apri link" if self.lang == "it" else "Open link", normalized)
        self.add_action_button("Google search", f"https://www.google.com/search?q={urllib.parse.quote(host, safe='')}")
        self.add_action_button("VirusTotal URL", build_virustotal_url(normalized))
        self.add_action_button("URLScan", build_urlscan_search_url(normalized))

        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Link analysis completed")

    def analyze_contract(self):
        value = self.get_widget_text(self.contract_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        if not EVM_PATTERN.match(value):
            score = 25
            risk, color = self.risk_label_and_color(score)
            indicators = [
                "Il formato non è un indirizzo EVM valido." if self.lang == "it" else "The format is not a valid EVM address.",
                "Potrebbe essere stato copiato male o appartenere a una chain non supportata." if self.lang == "it" else "It may have been copied incorrectly or belong to an unsupported chain.",
            ]
            recommendation = "Non interagire con contratti se l’indirizzo non è chiaro." if self.lang == "it" else "Do not interact with contracts if the address is unclear."
            limitation = "Questo controllo verifica il formato, non il bytecode o la reputazione on-chain." if self.lang == "it" else "This check verifies format, not bytecode or on-chain reputation."
            text = self.format_result("UNKNOWN CONTRACT", score, recommendation, indicators, limitation)
            self.clear_actions()
            self.set_result_text(text, risk, color)
            return

        score = 68
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato EVM valido." if self.lang == "it" else "Valid EVM format.",
            "Un formato valido non significa contratto sicuro." if self.lang == "it" else "A valid format does not mean the contract is safe.",
            "Verificare codice sorgente, proxy, owner, funzioni admin e cronologia." if self.lang == "it" else "Check source code, proxy, owner, admin functions and history.",
        ]
        recommendation = "Apri gli explorer e verifica se il contratto è verificato, se è proxy e se mantiene funzioni sensibili." if self.lang == "it" else "Open explorers and check whether the contract is verified, proxied and has sensitive functions."
        limitation = "Il tool non esegue decompilazione o analisi automatica del bytecode in questa versione." if self.lang == "it" else "The tool does not perform bytecode decompilation or automatic bytecode analysis in this version."
        text = self.format_result("SMART CONTRACT / EVM ADDRESS", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_evm_links(value)
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Contract analysis completed")

    def analyze_signature(self):
        value = self.get_widget_text(self.signature_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        lower_value = value.lower()
        score = 100
        indicators = []

        for needle, risk_value, level, explanation_it, explanation_en in SIGNATURE_RULES:
            explanation = explanation_it if self.lang == "it" else explanation_en
            if needle.lower() in lower_value:
                score -= risk_value
                indicators.append(f"{needle} · {level}: {explanation}")

        if "ffffffffffffffff" in lower_value or "maxuint" in lower_value or "unlimited" in lower_value:
            score -= 30
            indicators.append("Possibile approval illimitata o importo estremamente elevato." if self.lang == "it" else "Possible unlimited approval or extremely large amount.")

        if re.search(r"0x[a-fA-F0-9]{40}", value):
            score -= 4
            indicators.append("Sono presenti indirizzi EVM nel testo: controllare spender/contract." if self.lang == "it" else "EVM addresses found in text: check spender/contract.")

        if len(value.strip()) < 12:
            score -= 25
            indicators.append("Input molto breve o incompleto: impossibile valutare dominio, spender, token, importo e scopo della firma." if self.lang == "it" else "Very short or incomplete input: domain, spender, token, amount and signature purpose cannot be assessed.")

        if not indicators:
            score = min(score, 65)
            indicators.append("Nessuna keyword critica riconosciuta. Il testo non è sufficiente per considerare la firma sicura: potrebbe essere incompleto, casuale o non interpretabile." if self.lang == "it" else "No critical keyword recognized. The text is not enough to consider the signature safe: it may be incomplete, random or not interpretable.")

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)

        if score < 55:
            recommendation = "Non firmare se non capisci chiaramente spender, token, importo, dominio e scopo della richiesta." if self.lang == "it" else "Do not sign if you do not clearly understand spender, token, amount, domain and purpose."
        elif score < 80:
            recommendation = "Procedi solo se il sito è ufficiale e il contenuto della firma è coerente con ciò che volevi fare." if self.lang == "it" else "Proceed only if the site is official and the signature content matches what you intended to do."
        else:
            recommendation = "Rischio statico basso, ma verifica sempre dominio e contesto prima di firmare." if self.lang == "it" else "Low static risk, but always verify domain and context before signing."

        limitation = "Il tool interpreta testo e parole chiave. Non simula la transazione e non sostituisce un wallet simulator." if self.lang == "it" else "The tool interprets text and keywords. It does not simulate the transaction and does not replace a wallet simulator."
        text = self.format_result("WEB3 SIGNATURE / APPROVAL", score, recommendation, indicators, limitation)

        self.clear_actions()
        address_matches = re.findall(r"0x[a-fA-F0-9]{40}", value)

        if address_matches:
            first_address = address_matches[0]
            self.add_action_button("Revoke.cash address", f"https://revoke.cash/address/{first_address}")
            self.add_action_button("Etherscan address", f"https://etherscan.io/address/{first_address}")
            self.add_action_button("Etherscan approvals", f"https://etherscan.io/tokenapprovalchecker?search={first_address}")
        else:
            indicators.append("Nessun address EVM rilevato nel testo: non vengono mostrati link rapidi generici perché richiederebbero inserimento manuale del wallet." if self.lang == "it" else "No EVM address detected in the text: generic quick links are not shown because the wallet would need to be entered manually.")
            text = self.format_result("WEB3 SIGNATURE / APPROVAL", score, recommendation, indicators, limitation)

        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Signature analysis completed")

    def analyze_lightning(self):
        value = self.get_widget_text(self.lightning_input).strip()
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        compact = value.strip().replace("\n", "").replace(" ", "")
        lower_value = compact.lower()

        if LIGHTNING_INVOICE_PATTERN.match(lower_value):
            self.render_lightning_invoice(lower_value)
            return

        if LNURL_PATTERN.match(lower_value):
            self.status_label.configure(text="Loading LNURL data...")
            self.set_result_text("Analisi LNURL in corso..." if self.lang == "it" else "LNURL analysis in progress...", "LNURL", self.warning)
            threading.Thread(target=self.load_lnurl, args=(lower_value,), daemon=True).start()
            return

        if LIGHTNING_ADDRESS_PATTERN.match(value):
            self.status_label.configure(text="Loading Lightning Address data...")
            self.set_result_text("Analisi Lightning Address in corso..." if self.lang == "it" else "Lightning Address analysis in progress...", "LN ADDRESS", self.warning)
            threading.Thread(target=self.load_lightning_address, args=(value,), daemon=True).start()
            return

        score = 25
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato non riconosciuto come invoice Lightning, LNURL o Lightning Address." if self.lang == "it" else "Format not recognized as Lightning invoice, LNURL or Lightning Address.",
            "Controlla di aver copiato tutta la stringa senza spazi o caratteri mancanti." if self.lang == "it" else "Check that you copied the full string without spaces or missing characters.",
        ]
        recommendation = "Non pagare o autenticarti se non capisci chiaramente origine, importo e scopo della richiesta." if self.lang == "it" else "Do not pay or authenticate if you do not clearly understand origin, amount and purpose."
        limitation = "Lightning è off-chain: il tool controlla il contenuto preventivo della richiesta, non può confermare un pagamento già eseguito." if self.lang == "it" else "Lightning is off-chain: the tool checks the preventive request content, it cannot confirm a completed payment."
        self.clear_actions()
        self.set_result_text(self.format_result("UNKNOWN LIGHTNING DATA", score, recommendation, indicators, limitation), risk, color)

    def render_lightning_invoice(self, invoice):
        try:
            parsed = decode_lightning_invoice(invoice)
            score = 100
            indicators = []
            expiry = int(parsed.get("expiry") or 3600)
            created = int(parsed.get("timestamp") or 0)
            expires_at = created + expiry
            now = int(datetime.now(tz=timezone.utc).timestamp())

            indicators.append(("Rete: " if self.lang == "it" else "Network: ") + parsed.get("network", "—"))
            indicators.append(("Importo: " if self.lang == "it" else "Amount: ") + format_msat_amount(parsed.get("amount_msat")))
            indicators.append(("Creata: " if self.lang == "it" else "Created: ") + format_unix_time(created))
            indicators.append(("Scadenza: " if self.lang == "it" else "Expires: ") + format_unix_time(expires_at))
            indicators.append(("Descrizione: " if self.lang == "it" else "Description: ") + (parsed.get("description") or "—"))
            indicators.append(("Payment hash presente." if parsed.get("payment_hash") else "Payment hash assente o non decodificato.") if self.lang == "it" else ("Payment hash present." if parsed.get("payment_hash") else "Payment hash missing or not decoded."))

            if parsed.get("amount_msat") is None:
                score -= 12
                indicators.append("Invoice senza importo: il wallet potrebbe chiedere di inserirlo manualmente." if self.lang == "it" else "Amountless invoice: the wallet may ask you to enter the amount manually.")

            if not parsed.get("description"):
                score -= 10
                indicators.append("Descrizione assente: meno contesto sul motivo del pagamento." if self.lang == "it" else "Missing description: less context about payment purpose.")

            if expires_at < now:
                score -= 45
                indicators.append("Invoice scaduta: non dovrebbe essere pagata." if self.lang == "it" else "Expired invoice: it should not be paid.")
            elif expires_at - now < 300:
                score -= 12
                indicators.append("Invoice vicina alla scadenza." if self.lang == "it" else "Invoice close to expiry.")

            if parsed.get("network") != "mainnet":
                score -= 8
                indicators.append("Rete non mainnet: verificare che sia voluta." if self.lang == "it" else "Non-mainnet invoice: verify this is intentional.")

            score = max(0, min(100, score))
            risk, color = self.risk_label_and_color(score)
            recommendation = "Verifica importo, descrizione e scadenza prima di pagare. Non usare invoice scadute o senza contesto." if self.lang == "it" else "Verify amount, description and expiry before paying. Do not use expired or contextless invoices."
            limitation = "Il tool decodifica l’invoice localmente. Non può sapere se il pagamento è stato già eseguito o se il destinatario è affidabile." if self.lang == "it" else "The tool decodes the invoice locally. It cannot know whether payment was completed or whether the recipient is trustworthy."
            text = self.format_result("LIGHTNING INVOICE", score, recommendation, indicators, limitation)
            self.clear_actions()
            self.add_action_button("Lightning invoice info", "https://docs.lightning.engineering/the-lightning-network/payment-lifecycle/understanding-lightning-invoices")
            self.set_result_text(text, risk, color)
            self.status_label.configure(text="Lightning invoice analysis completed")
        except Exception as error:
            score = 35
            risk, color = self.risk_label_and_color(score)
            indicators = [
                "La stringa sembra una invoice Lightning, ma non è stata decodificata correttamente." if self.lang == "it" else "The string looks like a Lightning invoice, but it could not be decoded correctly.",
                f"Errore: {error}" if self.lang == "it" else f"Error: {error}",
            ]
            recommendation = "Non pagare invoice non decodificabili o copiate parzialmente." if self.lang == "it" else "Do not pay invoices that cannot be decoded or may have been partially copied."
            limitation = "Parser BOLT11 locale semplificato: alcune invoice particolari potrebbero non essere interpretate completamente." if self.lang == "it" else "Simplified local BOLT11 parser: some special invoices may not be fully interpreted."
            self.clear_actions()
            self.set_result_text(self.format_result("LIGHTNING INVOICE", score, recommendation, indicators, limitation), risk, color)

    def load_lnurl(self, lnurl):
        try:
            url = decode_lnurl_to_url(lnurl)
            data = fetch_json(url, timeout=15)
            self.root.after(0, lambda: self.render_lnurl(url, data))
        except Exception as error:
            self.root.after(0, lambda: self.render_lnurl_error(str(error)))

    def load_lightning_address(self, address):
        try:
            name, domain = address.split("@", 1)
            safe_name = urllib.parse.quote(name, safe="")
            url = f"https://{domain}/.well-known/lnurlp/{safe_name}"
            data = fetch_json(url, timeout=15)
            self.root.after(0, lambda: self.render_lightning_address(address, url, data))
        except Exception as error:
            self.root.after(0, lambda: self.render_lightning_address_error(address, str(error)))

    def render_lnurl(self, url, data):
        self.render_lnurl_like("LNURL", url, data)

    def render_lightning_address(self, address, url, data):
        self.render_lnurl_like("LIGHTNING ADDRESS", url, data, address=address)

    def render_lnurl_like(self, kind, url, data, address=None):
        score = 85
        indicators = []
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc.lower()

        indicators.append((f"Endpoint: {url}" if self.lang == "it" else f"Endpoint: {url}"))
        indicators.append((f"Dominio: {host}" if self.lang == "it" else f"Domain: {host}"))

        tag = data.get("tag", "—") if isinstance(data, dict) else "—"
        callback = data.get("callback", "—") if isinstance(data, dict) else "—"
        min_sendable = data.get("minSendable") if isinstance(data, dict) else None
        max_sendable = data.get("maxSendable") if isinstance(data, dict) else None
        comment_allowed = data.get("commentAllowed") if isinstance(data, dict) else None

        indicators.append((f"Tipo LNURL: {tag}." if self.lang == "it" else f"LNURL type: {tag}."))
        indicators.append((f"Callback: {callback}." if self.lang == "it" else f"Callback: {callback}."))

        if min_sendable is not None and max_sendable is not None:
            indicators.append((f"Importo min/max: {format_msat_amount(min_sendable)} / {format_msat_amount(max_sendable)}." if self.lang == "it" else f"Min/max amount: {format_msat_amount(min_sendable)} / {format_msat_amount(max_sendable)}."))

        if comment_allowed is not None:
            indicators.append((f"Commenti supportati: {comment_allowed} caratteri." if self.lang == "it" else f"Comments supported: {comment_allowed} characters."))

        if parsed.scheme != "https":
            score -= 30
            indicators.append("Endpoint non HTTPS: rischio maggiore." if self.lang == "it" else "Non-HTTPS endpoint: higher risk.")

        if tag == "login":
            score -= 18
            indicators.append("LNURL-auth/login: è una richiesta di autenticazione, non un semplice pagamento." if self.lang == "it" else "LNURL-auth/login: this is an authentication request, not a simple payment.")

        if not isinstance(data, dict) or data.get("status") == "ERROR":
            score -= 35
            indicators.append("Risposta LNURL in errore o non valida." if self.lang == "it" else "LNURL response is invalid or returned an error.")

        suspicious_hits = [word for word in SUSPICIOUS_WORDS if word in host.lower()]
        if suspicious_hits:
            score -= 12
            indicators.append(("Parole sospette nel dominio: " if self.lang == "it" else "Suspicious words in domain: ") + ", ".join(suspicious_hits[:5]))

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)
        recommendation = "Verifica il dominio del servizio prima di pagare o autenticarti via Lightning." if self.lang == "it" else "Verify the service domain before paying or authenticating via Lightning."
        limitation = "Il tool interroga l’endpoint LNURL pubblico. Non può confermare pagamenti Lightning già eseguiti né verificare l’identità reale del destinatario." if self.lang == "it" else "The tool queries the public LNURL endpoint. It cannot confirm completed Lightning payments or verify the real identity of the recipient."
        text = self.format_result(kind, score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Open endpoint", url)
        if address:
            self.add_action_button("Google domain", f"https://www.google.com/search?q={urllib.parse.quote(address.split('@', 1)[1], safe='')}")
        else:
            self.add_action_button("Google domain", f"https://www.google.com/search?q={urllib.parse.quote(host, safe='')}")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text=f"{kind} analysis completed")

    def render_lnurl_error(self, error):
        score = 35
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "LNURL non decodificabile o endpoint non raggiungibile." if self.lang == "it" else "LNURL cannot be decoded or endpoint cannot be reached.",
            f"Errore: {error}" if self.lang == "it" else f"Error: {error}",
        ]
        recommendation = "Non usare LNURL non decodificabili o provenienti da domini non verificati." if self.lang == "it" else "Do not use LNURLs that cannot be decoded or come from unverified domains."
        limitation = "Il controllo dipende da decodifica Bech32 e disponibilità endpoint." if self.lang == "it" else "The check depends on Bech32 decoding and endpoint availability."
        self.clear_actions()
        self.set_result_text(self.format_result("LNURL", score, recommendation, indicators, limitation), risk, color)

    def render_lightning_address_error(self, address, error):
        score = 35
        risk, color = self.risk_label_and_color(score)
        indicators = [
            f"Lightning Address analizzato: {address}" if self.lang == "it" else f"Analyzed Lightning Address: {address}",
            "Endpoint LNURLp non raggiungibile o non valido." if self.lang == "it" else "LNURLp endpoint cannot be reached or is invalid.",
            f"Errore: {error}" if self.lang == "it" else f"Error: {error}",
        ]
        recommendation = "Verifica che il dominio supporti Lightning Address e che l’indirizzo sia corretto." if self.lang == "it" else "Verify that the domain supports Lightning Address and that the address is correct."
        limitation = "Il controllo dipende dalla disponibilità del dominio e dell’endpoint /.well-known/lnurlp/." if self.lang == "it" else "The check depends on the domain and /.well-known/lnurlp/ endpoint availability."
        self.clear_actions()
        try:
            domain = address.split("@", 1)[1]
            self.add_action_button("Google domain", f"https://www.google.com/search?q={urllib.parse.quote(domain, safe='')}")
        except Exception:
            pass
        self.set_result_text(self.format_result("LIGHTNING ADDRESS", score, recommendation, indicators, limitation), risk, color)

    def add_evm_links(self, address):
        self.add_action_button("Etherscan", f"https://etherscan.io/address/{address}")
        self.add_action_button("Revoke.cash", f"https://revoke.cash/address/{address}")
        self.add_action_button("BaseScan", f"https://basescan.org/address/{address}")
        self.add_action_button("PolygonScan", f"https://polygonscan.com/address/{address}")
        self.add_action_button("Arbiscan", f"https://arbiscan.io/address/{address}")

    def export_report(self):
        if not self.last_report:
            messagebox.showinfo(APP_NAME, self.t("report_missing"))
            return

        path = filedialog.asksaveasfilename(title=self.t("report_btn"), defaultextension=".txt", initialfile="MolinaCrypto_Web3_Shield_Report.txt", filetypes=[("Text file", "*.txt"), ("All files", "*.*")])
        if not path:
            return

        header = (
            f"{APP_NAME}\n"
            f"Version: {APP_VERSION}\n"
            f"Author: {AUTHOR}\n"
            f"Website: {WEBSITE}\n"
            f"Report date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "Informational report only. This tool does not provide financial, tax, legal, investment or professional cybersecurity advice.\n"
            "The tool does not request seed phrases, private keys, wallet connection or transaction signing.\n"
            + "=" * 72
            + "\n\n"
        )

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(header + self.last_report)
            messagebox.showinfo(APP_NAME, self.t("report_saved"))
        except Exception as error:
            messagebox.showerror(APP_NAME, f"{self.t('save_error')}\n{error}")

    def toggle_language(self):
        self.lang = "en" if self.lang == "it" else "it"
        self.refresh_language()

    def refresh_language(self):
        self.subtitle_label.configure(text=self.t("subtitle"))
        self.claim_label.configure(text=self.t("claim"))
        self.lang_btn.configure(text=self.t("language_btn"))
        self.language_small_label.configure(text=self.t("language_label"))
        self.result_title.configure(text=self.t("result_title"))
        self.actions_title.configure(text=self.t("actions_title"))
        self.report_btn.configure(text=self.t("report_btn"))
        self.clear_btn.configure(text=self.t("clear_btn"))
        self.refresh_context_menu_labels()
        self.show_section(self.active_section)
        self.render_empty_result()


if __name__ == "__main__":
    app_window = tk.Tk()
    app = Web3ShieldApp(app_window)
    app_window.mainloop()
