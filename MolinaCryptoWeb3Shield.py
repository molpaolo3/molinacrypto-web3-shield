import json
import re
import threading
import urllib.parse
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from typing import List, Tuple, Union


APP_NAME = "MolinaCrypto Web3 Shield"
APP_VERSION = "0.2"
AUTHOR = "Paolo Molina"
WEBSITE = "https://www.molinacrypto.eu"
RESOURCES_URL = "https://www.molinacrypto.eu/risorse.html"

BTC_PATTERNS = [
    re.compile(r"^(bc1)[a-z0-9]{25,90}$", re.IGNORECASE),
    re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"),
]

EVM_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)

MEMPOOL_ADDRESS_API = "https://mempool.space/api/address/{address}"
MEMPOOL_FEES_API = "https://mempool.space/api/v1/fees/recommended"
MEMPOOL_TXS_API = "https://mempool.space/api/address/{address}/txs"

SUSPICIOUS_WORDS = [
    "airdrop", "claim", "bonus", "reward", "rewards", "free", "giveaway",
    "mint", "whitelist", "verify", "verification", "validate", "validation",
    "sync", "rectify", "restore", "recover", "walletconnect", "wallet-connect",
    "connect-wallet", "metamask", "seed", "phrase", "privatekey", "support",
    "helpdesk", "urgent", "limited", "presale", "drop", "tokenclaim", "auth",
    "unlock", "bonus", "migration", "redeem"
]

KNOWN_BRANDS = [
    "metamask", "walletconnect", "uniswap", "opensea", "aave", "compound",
    "curve", "sushiswap", "pancakeswap", "1inch", "blur", "magiceden",
    "ledger", "trezor", "coinbase", "binance", "kraken", "phantom",
    "rabby", "revoke", "etherscan", "basescan", "polygonscan", "arbiscan"
]

SIGNATURE_RULES: List[Tuple[str, int, str, str, str]] = [
    (
        "setApprovalForAll",
        35,
        "HIGH",
        "Può autorizzare un operatore a gestire tutti i token/NFT di una collezione.",
        "Can authorize an operator to manage all tokens/NFTs in a collection."
    ),
    (
        "approve",
        22,
        "MEDIUM",
        "Può autorizzare uno spender a muovere token dal wallet.",
        "Can authorize a spender to move tokens from the wallet."
    ),
    (
        "increaseAllowance",
        22,
        "MEDIUM",
        "Aumenta la quantità di token che uno spender può muovere.",
        "Increases the amount of tokens a spender can move."
    ),
    (
        "permit",
        25,
        "MEDIUM",
        "Può concedere autorizzazioni tramite firma senza una classica transazione approve on-chain.",
        "Can grant permissions by signature without a classic on-chain approve transaction."
    ),
    (
        "permit2",
        35,
        "HIGH",
        "Meccanismo di autorizzazione potente: controllare spender, token, scadenza e limiti.",
        "Powerful permission mechanism: check spender, token, expiry and limits."
    ),
    (
        "eth_sign",
        35,
        "HIGH",
        "Firma cieca/legacy: rischiosa se il contenuto non è leggibile.",
        "Blind/legacy signature: risky when the content is not readable."
    ),
    (
        "personal_sign",
        12,
        "LOW",
        "Firma messaggio spesso usata per login, ma abusabile su siti malevoli.",
        "Message signature often used for login, but it can be abused on malicious sites."
    ),
    (
        "eth_signTypedData",
        18,
        "MEDIUM",
        "Firma strutturata: verificare bene dominio, spender, token e contenuto.",
        "Typed-data signature: carefully verify domain, spender, token and content."
    ),
    (
        "transferFrom",
        35,
        "HIGH",
        "Operazione che può muovere asset se esiste autorizzazione.",
        "Operation that may move assets if authorization exists."
    ),
    (
        "safeTransferFrom",
        35,
        "HIGH",
        "Operazione che può muovere NFT se esiste autorizzazione.",
        "Operation that may move NFTs if authorization exists."
    ),
]


TEXT = {
    "it": {
        "subtitle": "Controlla wallet, link, contratti e firme prima di rischiare fondi.",
        "claim": "Non richiede seed phrase · Non collega il wallet · Non firma transazioni",
        "wallet_card": "Wallet / Address Check",
        "wallet_hint": "Incolla indirizzo BTC o ETH/EVM pubblico",
        "wallet_btn": "Analizza wallet",
        "link_card": "Link / dApp Check",
        "link_hint": "Incolla link dApp, claim, mint, airdrop o sito sospetto",
        "link_btn": "Controlla link",
        "contract_card": "Smart Contract Check",
        "contract_hint": "Incolla indirizzo contratto o address EVM",
        "contract_btn": "Controlla contratto",
        "signature_card": "Signature / Approval Check",
        "signature_hint": "Incolla firma, approve, permit, setApprovalForAll o testo tecnico",
        "signature_btn": "Traduci firma",
        "result_title": "Risultato",
        "empty_result": "Seleziona un controllo, incolla un dato e avvia l’analisi. Il risultato comparirà qui in forma sintetica e leggibile.",
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
        "subtitle": "Check wallets, links, contracts and signatures before risking funds.",
        "claim": "No seed phrases · No wallet connection · No transaction signing",
        "wallet_card": "Wallet / Address Check",
        "wallet_hint": "Paste public BTC or ETH/EVM address",
        "wallet_btn": "Analyze wallet",
        "link_card": "Link / dApp Check",
        "link_hint": "Paste dApp, claim, mint, airdrop or suspicious website link",
        "link_btn": "Check link",
        "contract_card": "Smart Contract Check",
        "contract_hint": "Paste contract address or EVM address",
        "contract_btn": "Check contract",
        "signature_card": "Signature / Approval Check",
        "signature_hint": "Paste signature, approve, permit, setApprovalForAll or technical text",
        "signature_btn": "Translate signature",
        "result_title": "Result",
        "empty_result": "Choose a check, paste data and run the analysis. The result will appear here in a compact readable format.",
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


def fetch_json(url, timeout=15):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": f"MolinaCryptoWeb3Shield/{APP_VERSION}"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def normalize_url(value):
    raw = value.strip()
    if raw and not URL_PATTERN.match(raw):
        raw = "https://" + raw
    parsed = urllib.parse.urlparse(raw)
    host = parsed.netloc.lower().split("@")[-1].split(":")[0].strip()
    return raw, parsed, host


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


def is_ip_host(host):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host))


class Web3ShieldApp:
    def __init__(self, window):
        self.root = window
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1280x900")
        self.root.minsize(1180, 840)

        self.lang = "it"
        self.last_report = ""
        self.current_links = []

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

        self.setup_root()
        self.build_ui()
        self.build_context_menu()
        self.render_empty_result()

    def t(self, key):
        return TEXT[self.lang].get(key, key)

    def setup_root(self):
        self.root.configure(bg=self.bg)

    def build_ui(self):
        self.main = tk.Frame(self.root, bg=self.bg)
        self.main.pack(fill="both", expand=True, padx=16, pady=12)

        self.build_header()
        self.build_body()
        self.build_footer()

    def build_header(self):
        header = tk.Frame(self.main, bg=self.bg)
        header.pack(fill="x", pady=(0, 10))

        left = tk.Frame(header, bg=self.bg)
        left.pack(side="left", fill="x", expand=True)

        title_row = tk.Frame(left, bg=self.bg)
        title_row.pack(anchor="w")

        logo = tk.Label(
            title_row,
            text="🛡",
            bg=self.bg,
            fg=self.accent,
            font=("Arial", 30, "bold")
        )
        logo.pack(side="left", padx=(0, 10))

        title_box = tk.Frame(title_row, bg=self.bg)
        title_box.pack(side="left")

        self.title_label = tk.Label(
            title_box,
            text=APP_NAME,
            bg=self.bg,
            fg=self.text,
            font=("Arial", 26, "bold")
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            title_box,
            text=self.t("subtitle"),
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 12)
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        self.claim_label = tk.Label(
            left,
            text=self.t("claim"),
            bg=self.bg,
            fg=self.accent,
            font=("Arial", 10, "bold")
        )
        self.claim_label.pack(anchor="w", pady=(8, 0))

        right = tk.Frame(header, bg=self.bg)
        right.pack(side="right", anchor="ne")

        version = tk.Label(
            right,
            text=f"v{APP_VERSION} · © 2026 {AUTHOR}",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        version.pack(anchor="e", pady=(0, 8))

        language_row = tk.Frame(right, bg=self.bg)
        language_row.pack(anchor="e")

        self.language_small_label = tk.Label(
        language_row,
        text=self.t("language_label"),
        bg=self.bg,
        fg=self.muted,
        font=("Arial", 9)
        )
        self.language_small_label.pack(side="left", padx=(0, 8))

        self.lang_btn = self.small_button(language_row, self.t("language_btn"), self.toggle_language)
        self.lang_btn.pack(side="left")

        line = tk.Frame(self.main, bg=self.border, height=1)
        line.pack(fill="x", pady=(0, 10))

    def build_body(self):
        body = tk.Frame(self.main, bg=self.bg)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=self.bg)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(body, bg=self.bg)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.build_control_cards(left)
        self.build_result_panel(right)
        self.build_actions_panel(right)

    def build_control_cards(self, parent):
        self.wallet_input = self.create_check_card(
            parent=parent,
            title_key="wallet_card",
            hint_key="wallet_hint",
            button_key="wallet_btn",
            command=self.analyze_wallet,
            multiline=False
        )

        self.link_input = self.create_check_card(
            parent=parent,
            title_key="link_card",
            hint_key="link_hint",
            button_key="link_btn",
            command=self.analyze_link,
            multiline=False
        )

        self.contract_input = self.create_check_card(
            parent=parent,
            title_key="contract_card",
            hint_key="contract_hint",
            button_key="contract_btn",
            command=self.analyze_contract,
            multiline=False
        )

        self.signature_input = self.create_check_card(
            parent=parent,
            title_key="signature_card",
            hint_key="signature_hint",
            button_key="signature_btn",
            command=self.analyze_signature,
            multiline=True
        )

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
            font=("Arial", 9)
        )
        hint_label.pack(anchor="w", pady=(2, 8))

        input_widget: Union[tk.Entry, tk.Text]

        if multiline:
            text_field = tk.Text(
                card,
                height=4,
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
        result_card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1,
            padx=16,
            pady=14
        )
        result_card.pack(fill="both", expand=True)

        self.result_title = tk.Label(
            result_card,
            text=self.t("result_title"),
            bg=self.panel,
            fg=self.text,
            font=("Arial", 18, "bold")
        )
        self.result_title.pack(anchor="w")

        self.result_badge = tk.Label(
            result_card,
            text="—",
            bg=self.card_soft,
            fg=self.muted,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        )
        self.result_badge.pack(anchor="w", pady=(8, 10))

        self.result_text = tk.Text(
            result_card,
            bg=self.panel,
            fg=self.text,
            insertbackground=self.text,
            relief="flat",
            wrap="word",
            font=("Arial", 11),
            padx=0,
            pady=0
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.configure(state="disabled")
        self.register_context_widget(self.result_text)

    def build_actions_panel(self, parent):
        actions_card = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1,
            padx=14,
            pady=10
        )
        actions_card.pack(fill="x", pady=(12, 0))

        self.actions_title = tk.Label(
            actions_card,
            text=self.t("actions_title"),
            bg=self.panel,
            fg=self.accent2,
            font=("Arial", 13, "bold")
        )
        self.actions_title.pack(anchor="w", pady=(0, 8))

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
        footer.pack(fill="x", pady=(12, 0))

        self.status_label = tk.Label(
            footer,
            text="Ready",
            bg=self.bg,
            fg=self.muted,
            font=("Arial", 9)
        )
        self.status_label.pack(side="left")

        site = self.secondary_button(footer, self.t("site_btn"), lambda: webbrowser.open(WEBSITE))
        site.pack(side="right")

        resources = self.secondary_button(footer, self.t("resources_btn"), lambda: webbrowser.open(RESOURCES_URL))
        resources.pack(side="right", padx=(0, 8))

    def primary_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#0f766e",
            fg="white",
            activebackground="#14b8a6",
            activeforeground="white",
            relief="flat",
            padx=14,
            pady=7,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

    def secondary_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.card_soft,
            fg=self.text,
            activebackground=self.border,
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=7,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )

    def small_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.card_soft,
            fg=self.text,
            activebackground=self.border,
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=5,
            font=("Arial", 9, "bold"),
            cursor="hand2"
        )

    def build_context_menu(self):
        self.context_target = None
        self.context_menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=self.panel2,
            fg=self.text,
            activebackground=self.accent2,
            activeforeground="#06111f"
        )
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
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()
        return widget.get().strip()

    def set_result_text(self, text, badge_text="—", badge_color=None):
        self.result_badge.configure(
            text=badge_text,
            fg="white",
            bg=badge_color or self.card_soft
        )
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
        for widget in [self.wallet_input, self.link_input, self.contract_input]:
            widget.delete(0, "end")
        self.signature_input.delete("1.0", "end")
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
        lines = []
        lines.append(f"{self.t('type')}: {kind}")
        lines.append(f"{self.t('score')}: {score}/100 · {risk}")
        lines.append("")
        lines.append(f"{self.t('recommendation')}:")
        lines.append(recommendation)
        lines.append("")
        lines.append(f"{self.t('indicators')}:")
        for item in indicators:
            lines.append(f"• {item}")
        lines.append("")
        lines.append(f"{self.t('limits')}:")
        lines.append(limitation)
        return "\n".join(lines)

    def analyze_wallet(self):
        value = self.get_widget_text(self.wallet_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
            return

        wallet_type = detect_wallet_type(value)
        if wallet_type == "BTC":
            self.status_label.configure(text="Loading Bitcoin public data...")
            self.set_result_text("Analisi Bitcoin in corso...", "BTC", self.warning)
            threading.Thread(target=self.load_btc_wallet, args=(value,), daemon=True).start()
            return

        if wallet_type == "EVM":
            self.render_evm_wallet(value)
            return

        score = 25
        risk, color = self.risk_label_and_color(score)
        indicators = [
            "Formato non riconosciuto come Bitcoin o Ethereum/EVM." if self.lang == "it" else "Format not recognized as Bitcoin or Ethereum/EVM.",
            "Potrebbe essere copiato male o appartenere a una chain non ancora supportata." if self.lang == "it" else "It may be copied incorrectly or belong to an unsupported chain.",
        ]
        recommendation = (
            "Ricontrolla l’indirizzo dalla fonte originale. Non inviare fondi a indirizzi di formato incerto."
            if self.lang == "it"
            else "Re-check the address from the original source. Do not send funds to uncertain address formats."
        )
        limitation = (
            "Il controllo verifica solo pattern di formato, non la proprietà dell’indirizzo."
            if self.lang == "it"
            else "The check verifies only format patterns, not address ownership."
        )
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

            self.root.after(
                0,
                lambda: self.render_btc_wallet(
                    address,
                    confirmed_balance,
                    mempool_delta,
                    tx_count,
                    mem_tx_count,
                    fastest_fee
                )
            )
        except Exception as error:
            self.root.after(0, lambda: self.render_btc_error(address, str(error)))

    def render_btc_wallet(self, address, confirmed_balance, mempool_delta, tx_count, mem_tx_count, fastest_fee):
        score = 100
        indicators = []

        if self.lang == "it":
            indicators.append("Indirizzo Bitcoin valido.")
            indicators.append(f"Saldo confermato: {fmt_btc(confirmed_balance)}.")
            indicators.append(f"Saldo non confermato/mempool: {fmt_btc(mempool_delta)}.")
            indicators.append(f"Transazioni confermate: {tx_count}.")
            indicators.append(f"Transazioni non confermate: {mem_tx_count}.")
            indicators.append(f"Fee veloce stimata: {fastest_fee} sat/vB.")
        else:
            indicators.append("Valid Bitcoin address.")
            indicators.append(f"Confirmed balance: {fmt_btc(confirmed_balance)}.")
            indicators.append(f"Unconfirmed/mempool balance: {fmt_btc(mempool_delta)}.")
            indicators.append(f"Confirmed transactions: {tx_count}.")
            indicators.append(f"Unconfirmed transactions: {mem_tx_count}.")
            indicators.append(f"Estimated fastest fee: {fastest_fee} sat/vB.")

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

        recommendation = (
            "Verifica movimenti su explorer, valuta le fee prima di inviare BTC e non inserire mai seed phrase in nessun tool."
            if self.lang == "it"
            else "Verify movements on explorers, check fees before sending BTC and never enter seed phrases into any tool."
        )
        limitation = (
            "Il controllo usa dati pubblici mempool.space. Non identifica il proprietario dell’indirizzo e non garantisce assenza di rischio operativo."
            if self.lang == "it"
            else "The check uses public mempool.space data. It does not identify address ownership and does not guarantee absence of operational risk."
        )

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
        recommendation = (
            "Apri manualmente gli explorer e verifica connessione/API."
            if self.lang == "it"
            else "Open explorers manually and check connection/API."
        )
        limitation = (
            "Il controllo dipende dalla disponibilità delle API pubbliche."
            if self.lang == "it"
            else "The check depends on public API availability."
        )
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
        recommendation = (
            "Controlla approvals su Revoke.cash/Etherscan e non usare il wallet principale su dApp sconosciute."
            if self.lang == "it"
            else "Check approvals on Revoke.cash/Etherscan and do not use the main wallet on unknown dApps."
        )
        limitation = (
            "Senza API key dedicate il tool non legge saldo/token EVM in automatico: apre però gli strumenti corretti con un click."
            if self.lang == "it"
            else "Without dedicated API keys the tool does not automatically read EVM balances/tokens, but opens the correct tools with one click."
        )
        text = self.format_result("ETHEREUM / EVM ADDRESS", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_evm_links(address)
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="EVM analysis completed")

    def analyze_link(self):
        value = self.get_widget_text(self.link_input)
        if not value:
            messagebox.showwarning(APP_NAME, self.t("missing"))
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
                indicators.append(
                    ("Parole sospette: " if self.lang == "it" else "Suspicious words: ")
                    + ", ".join(suspicious_hits[:8])
                )

            brand_hits = [brand for brand in KNOWN_BRANDS if brand in host]
            if brand_hits:
                official_like = any(host == f"{brand}.com" or host.endswith(f".{brand}.com") for brand in brand_hits)
                if not official_like:
                    score -= 18
                    indicators.append(
                        ("Contiene brand noti ma non sembra dominio ufficiale: " if self.lang == "it" else "Contains known brands but does not look official: ")
                        + ", ".join(brand_hits[:5])
                    )

            if len(indicators) == 1:
                indicators.append("Nessun indicatore statico forte emerso." if self.lang == "it" else "No strong static indicator detected.")

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)

        recommendation = (
            "Se il rischio è medio/alto, non collegare il wallet principale. Verifica il dominio partendo dal sito ufficiale del progetto."
            if self.lang == "it"
            else "If risk is medium/high, do not connect the main wallet. Verify the domain starting from the official project website."
        )
        limitation = (
            "Il controllo non visita il sito e non analizza codice JavaScript: valuta solo indicatori statici del link."
            if self.lang == "it"
            else "The check does not visit the website or analyze JavaScript code: it only evaluates static link indicators."
        )
        text = self.format_result("WEB3 LINK / DAPP", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Apri link" if self.lang == "it" else "Open link", normalized)
        self.add_action_button("Google search", f"https://www.google.com/search?q={urllib.parse.quote(host)}")
        self.add_action_button("VirusTotal URL", f"https://www.virustotal.com/gui/search/{urllib.parse.quote(normalized)}")

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
            recommendation = (
                "Non interagire con contratti se l’indirizzo non è chiaro."
                if self.lang == "it"
                else "Do not interact with contracts if the address is unclear."
            )
            limitation = (
                "Questo controllo verifica il formato, non il bytecode o la reputazione on-chain."
                if self.lang == "it"
                else "This check verifies format, not bytecode or on-chain reputation."
            )
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
        recommendation = (
            "Apri gli explorer e verifica se il contratto è verificato, se è proxy e se mantiene funzioni sensibili."
            if self.lang == "it"
            else "Open explorers and check whether the contract is verified, proxied and has sensitive functions."
        )
        limitation = (
            "Il tool non esegue decompilazione o analisi automatica del bytecode in questa versione."
            if self.lang == "it"
            else "The tool does not perform bytecode decompilation or automatic bytecode analysis in this version."
        )
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
            indicators.append(
                "Possibile approval illimitata o importo estremamente elevato."
                if self.lang == "it"
                else "Possible unlimited approval or extremely large amount."
            )

        if re.search(r"0x[a-fA-F0-9]{40}", value):
            score -= 4
            indicators.append(
                "Sono presenti indirizzi EVM nel testo: controllare spender/contract."
                if self.lang == "it"
                else "EVM addresses found in text: check spender/contract."
            )

        if not indicators:
            indicators.append(
                "Nessuna keyword critica riconosciuta, ma questo non basta per considerare la firma sicura."
                if self.lang == "it"
                else "No critical keyword recognized, but this is not enough to consider the signature safe."
            )

        score = max(0, min(100, score))
        risk, color = self.risk_label_and_color(score)

        if score < 55:
            recommendation = (
                "Non firmare se non capisci chiaramente spender, token, importo, dominio e scopo della richiesta."
                if self.lang == "it"
                else "Do not sign if you do not clearly understand spender, token, amount, domain and purpose."
            )
        elif score < 80:
            recommendation = (
                "Procedi solo se il sito è ufficiale e il contenuto della firma è coerente con ciò che volevi fare."
                if self.lang == "it"
                else "Proceed only if the site is official and the signature content matches what you intended to do."
            )
        else:
            recommendation = (
                "Rischio statico basso, ma verifica sempre dominio e contesto prima di firmare."
                if self.lang == "it"
                else "Low static risk, but always verify domain and context before signing."
            )

        limitation = (
            "Il tool interpreta testo e parole chiave. Non simula la transazione e non sostituisce un wallet simulator."
            if self.lang == "it"
            else "The tool interprets text and keywords. It does not simulate the transaction and does not replace a wallet simulator."
        )
        text = self.format_result("WEB3 SIGNATURE / APPROVAL", score, recommendation, indicators, limitation)

        self.clear_actions()
        self.add_action_button("Revoke.cash", "https://revoke.cash")
        self.add_action_button("Etherscan Token Approval", "https://etherscan.io/tokenapprovalchecker")
        self.set_result_text(text, risk, color)
        self.status_label.configure(text="Signature analysis completed")

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

        path = filedialog.asksaveasfilename(
            title=self.t("report_btn"),
            defaultextension=".txt",
            initialfile="MolinaCrypto_Web3_Shield_Report.txt",
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )

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

        for title_label, hint_label, button, title_key, hint_key, button_key in self.card_registry:
            title_label.configure(text=self.t(title_key))
            hint_label.configure(text=self.t(hint_key))
            button.configure(text=self.t(button_key))

        self.render_empty_result()


if __name__ == "__main__":
    app_window = tk.Tk()
    app = Web3ShieldApp(app_window)
    app_window.mainloop()
