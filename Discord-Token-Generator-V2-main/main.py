import asyncio
import random
import string
import os
import sys
import json
import httpx
import requests
import zendriver as zd
import pyautogui as ca
import pyperclip
import imaplib
import email
import re
from datetime import datetime
from colorama import Fore, Style, init
from pystyle import Colorate, Colors, Center
import io
import time
import uuid
import concurrent.futures
from base64 import b64encode
from json import dumps, loads, JSONDecodeError
from pathlib import Path
from platform import system, release, version
from random import choice
from typing import Optional, List, Tuple, Any, Dict, Union
from PIL import Image
import tls_client
import websocket

init(autoreset=True)

OUTPUT_DIR = "input"
ONLY_TOKEN_FILE = f"{OUTPUT_DIR}/tokens.txt"
FULL_DATA_FILE = f"{OUTPUT_DIR}/token.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

UA_POOL = []


def refresh_ua_pool():
    global UA_POOL
    UA_POOL = USER_AGENTS.copy()
    random.shuffle(UA_POOL)


class Theme:
    BOLD = "\033[1m"
    END = "\033[0m"

    GRADIENT_GRAY = [
        "\033[90m",
        "\033[38;2;140;140;140m",
        "\033[38;2;100;100;100m",
        "\033[38;2;70;70;70m",
        "\033[38;2;50;50;50m",
    ]

    GRADIENT_WHITE = [
        "\033[38;2;255;255;255m",
        "\033[38;2;230;230;230m",
        "\033[38;2;200;200;200m",
        "\033[38;2;170;170;170m",
        "\033[38;2;140;140;140m",
    ]


def gradient_text(text, colors=None):
    if colors is None:
        colors = Theme.GRADIENT_WHITE
    result = ""
    for i, char in enumerate(text):
        color_index = i % len(colors)
        result += f"{colors[color_index]}{char}"
    return result + Theme.END


def show_glitch_art():
    """Display animated monochrome ASCII art that glitches before settling"""
    os.system("cls" if os.name == "nt" else "clear")

    frame1 = r"""
   _____   ______  __  __
  /__  /  / ____/ / / / /
    / /  / __/   / /_/ / 
   / /  / /___  / __  /  
  /_/  /_____/ /_/ /_/   
"""

    frame2 = r"""
███████ ███████ ██   ██
     ██ ██      ██   ██
   ███  █████   ███████
 ██     ██      ██   ██
███████ ███████ ██   ██
"""

    frame3 = r"""
 _____   ____   _   _ 
|__  /  | ___| | | | |
  / /   | |_   | |_| |
 / /_   |  _|  |  _  |
/____|  |____| |_| |_|
"""

    frame4 = r"""
+-+-+-+
|Z|E|H|
+-+-+-+
"""

    frames = [frame1, frame2, frame3, frame4]

    start_time = time.time()
    current_frame_idx = 0

    while time.time() - start_time < 3.5:
        os.system("cls" if os.name == "nt" else "clear")

        if random.random() < 0.15:
            time.sleep(0.08)
            continue

        art = frames[current_frame_idx % len(frames)]

        colored_art = ""
        for line in art.split("\n"):
            if random.random() < 0.08:
                line = line.replace(" ", random.choice([".", "-", "`", " "]))

            chosen_grad = (
                Theme.GRADIENT_WHITE if random.random() > 0.5 else Theme.GRADIENT_GRAY
            )
            colored_art += gradient_text(line, chosen_grad) + "\n"

        print("\n\n" + colored_art)

        subtitle = (
            "Zeh On Top" if random.random() > 0.5 else "Made By Zeh"
        )
        print(f"\n{gradient_text(subtitle.center(50), Theme.GRADIENT_WHITE)}")

        time.sleep(random.uniform(0.05, 0.2))

        if random.random() > 0.2:
            current_frame_idx += 1

    os.system("cls" if os.name == "nt" else "clear")

    art = frames[0]
    colored_art = ""
    for line in art.split("\n"):
        colored_art += gradient_text(line, Theme.GRADIENT_WHITE) + "\n"
    print("\n\n" + colored_art)
    print(f"\n{gradient_text('Made By Zeh'.center(50), Theme.GRADIENT_WHITE)}")
    time.sleep(1)


def print_banner(banner_type="main"):
    os.system("cls" if os.name == "nt" else "clear")

    if banner_type == "main":
        raw_banner = r"""
 ▒███████▒▓█████  ██░  ██▒
 ▒ ▒ ▒ ▄▀░▓█   ▀  ▓██░ ██▓
 ░ ▒ ▄▀▒░ ▒███    ▒██▀▀██░
   ▄▀▒   ░▒▓█  ▄  ░▓█ ░██ 
 ▒███████▒░▒████▒ ░▓█▒░██▓
 ░▒▒ ▓░▒░▒░░ ▒░ ░  ▒ ░░▒░▒
 ░░▒ ▒ ░ ▒ ░ ░  ░  ▒ ░▒░ ░
  ░ ░ ░ ░    ░      ░  ░░ ░
    ░ ░      ░  ░   ░  ░  ░
      ░                    """
    elif banner_type == "generator":
        raw_banner = r"""
  ______      __                 ______                           __            
 /_  __/___  / /_____  ____     / ____/__  ____  ___  _________ _/ /_____  _____
  / / / __ \/ //_/ _ \/ __ \   / / __/ _ \/ __ \/ _ \/ ___/ __ `/ __/ __ \/ ___/
 / / / /_/ / ,< /  __/ / / /  / /_/ /  __/ / / /  __/ /  / /_/ / /_/ /_/ / /    
/_/  \____/_/|_|\___/_/ /_/   \____/\___/_/ /_/\___/_/   \__,_/\__/\____/_/     """
    elif banner_type == "humanizer":
        raw_banner = r"""
 _____     _                _   _                             _              
|_   _|   | |              | | | |                           (_)             
  | | ___ | | _____ _ __   | |_| |_   _ _ __ ___   __ _ _ __  _ _______ _ __ 
  | |/ _ \| |/ / _ \ '_ \  |  _  | | | | '_ ` _ \ / _` | '_ \| |_  / _ \ '__|
  | | (_) |   <  __/ | | | | | | | |_| | | | | | | (_| | | | | |/ /  __/ |   
  \_/\___/|_|\_\___|_| |_| \_| |_/\__,_|_| |_| |_|\__,_|_| |_|_/___\___|_|   """
    else:
        raw_banner = ""

    colored_banner = ""
    for line in raw_banner.split("\n"):
        if line.strip(" \r\n"):
            colored_banner += gradient_text(line, Theme.GRADIENT_WHITE) + "\n"

    print(f"{Theme.BOLD}\n{colored_banner}")

    print(f"{gradient_text('═' * 60, Theme.GRADIENT_GRAY)}\n")
    print(f"{gradient_text('═' * 60, Theme.GRADIENT_GRAY)}\n")


from TempMail import TempMail


class EmailManager:
    def __init__(self):
        self.tmp = TempMail()
        self.inb = None
        self.email = None
        self.password = (
            "Zeh"
            + "".join(random.choices(string.ascii_letters + string.digits, k=8))
            + "!"
        )

    async def generate_email(self):
        for _ in range(3):
            try:
                self.inb = self.tmp.createInbox()
                if self.inb and self.inb.address:
                    self.email = self.inb.address
                    print(
                        f"{gradient_text(f'[+]  Email Generated: {self.email}', Theme.GRADIENT_WHITE)}"
                    )
                    return self.email
            except Exception:
                await asyncio.sleep(1)

        print(
            f"{gradient_text('[-]  Failed to generate email after 3 attempts.', Theme.GRADIENT_GRAY)}"
        )
        return None

    async def get_verification_link(self):
        if not self.inb:
            return None

        print(f"{gradient_text('⏳ Checking inbox...', Theme.GRADIENT_GRAY)}")

        for _ in range(40):
            try:
                emails = self.tmp.getEmails(self.inb.token)
                for email in emails or []:
                    subject = str(getattr(email, "subject", ""))
                    if "Discord" in subject or "discord" in subject.lower():
                        body = str(getattr(email, "body", "")) + str(
                            getattr(email, "html", "")
                        )

                        body = (
                            body.replace("&amp;", "&")
                            .replace("=\r\n", "")
                            .replace("=\n", "")
                        )

                        patterns = [
                            r'https://click\.discord\.com/ls/click\?[^\s"\'><\]\)]+',
                            r'https://discord\.com/verify\?token=[^\s"\'><\]\)]+',
                            r'https://discord\.com/register\?token=[^\s"\'><\]\)]+',
                        ]
                        for pattern in patterns:
                            match = re.search(pattern, body)
                            if match:
                                print(
                                    f"{gradient_text('[+]  Verification email found!', Theme.GRADIENT_WHITE)}"
                                )
                                return match.group(0)
            except Exception:
                pass

            await asyncio.sleep(3)

        print(
            f"{gradient_text('! No email found in inbox. (Discord likely dropped the email for this IP/Domain)', Theme.GRADIENT_GRAY)}"
        )
        return None


class DiscordBot:
    def __init__(self, index, ua=None):
        self.index = index
        self.email_mgr = EmailManager()
        self.browser = None
        self.email = ""
        self.password = self._generate_pass()
        self.ua = ua
        self.verification_warning_shown = False

    def _generate_pass(self):
        words = [
            "Nxght",
            "V0id",
            "Cyb3r",
            "G1itch",
            "Sy5tem",
            "0perat0r",
            "Zeh",
        ]
        return f"{random.choice(words)}!{random.randint(1000, 9999)}"

    async def extract_token(self, page):
        script = """
        (function() {
            try {
                let m;
                window.webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]);
                let token = m.find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken();
                if (token) return token;
            } catch (e) {}
            try {
                let token = document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token;
                if (token) return token.replace(/"/g, "");
            } catch (e) {}
            return null;
        })();
        """
        try:
            return await page.evaluate(script)
        except:
            return None

    async def check_is_verified(self, token):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    "https://discord.com/api/v9/users/@me",
                    headers={"Authorization": token},
                )
                if res.status_code == 200:
                    data = res.json()
                    return data.get("verified", False)
        except:
            pass
        return False

    async def wait_for_verification(self, page):
        print(
            f"{gradient_text('! Waiting for extraction of token...', Theme.GRADIENT_WHITE)}"
        )
        token = None

        for _ in range(25):
            token = await self.extract_token(page)
            if token and len(str(token)) > 30:
                break
            await asyncio.sleep(2)

        if not token:
            print(
                f"{gradient_text('[-]  Token not found (Captcha or Rate Limit).', Theme.GRADIENT_GRAY)}"
            )
            return None

        is_verified = await self.check_is_verified(token)
        if is_verified:
            return token

        print(
            f"{gradient_text('[+]  Token found, waiting for verification link...', Theme.GRADIENT_GRAY)}"
        )
        verify_link = await self.email_mgr.get_verification_link()

        if verify_link:
            print(
                f"{gradient_text('▶ Navigating to verification link in browser...', Theme.GRADIENT_WHITE)}"
            )
            try:
                verify_tab = await self.browser.get(verify_link)
                await asyncio.sleep(10)
            except Exception as e:
                print(
                    f"{gradient_text(f'[-]  Error navigating to link: {e}', Theme.GRADIENT_GRAY)}"
                )

        for _ in range(4):
            is_verified = await self.check_is_verified(token)
            if is_verified:
                print(
                    f"{gradient_text('[+]  Account auto-verified successfully!', Theme.GRADIENT_GRAY)}"
                )
                return token
            await asyncio.sleep(3)

        print(
            f"{gradient_text('! Email auto-verification failed or delayed.', Theme.GRADIENT_WHITE)}"
        )
        return token

    async def start(self):
        self.email = await self.email_mgr.generate_email()
        if not self.email:
            return

        print(
            f"{gradient_text(f'▶ Opening Browser for Account #{self.index}', Theme.GRADIENT_WHITE)}"
        )

        try:
            selected_ua = self.ua if self.ua else random.choice(USER_AGENTS)
            browser_args = [
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--window-size=1280,720",
                "--disable-infobars",
                "--disable-notifications",
                "--disable-save-password-bubble",
                "--guest",
                f"--user-agent={selected_ua}",
            ]

            self.browser = await zd.start(arguments=browser_args)
            page = await self.browser.get("https://discord.com/register")
            await page.wait_for('input[name="email"]', timeout=60)

            y2k_names = [
                "shadow",
                "ghost",
                "pixel",
                "cyber",
                "nova",
                "vortex",
                "echo",
                "frost",
                "pulse",
                "crypto",
                "nexus",
                "blade",
                "storm",
                "falcon",
                "raven",
                "phantom",
                "titan",
                "matrix",
                "hunter",
                "spark",
                "glitch",
                "solar",
                "lunar",
                "mystic",
                "drift",
                "hyper",
                "atomic",
                "cosmic",
                "sonic",
                "alpha",
                "omega",
                "vector",
                "blaze",
                "viper",
                "turbo",
                "quantum",
                "etipuf",
                "whynot",
                "root",
                "user",
                "windows",
            ]
            suffix_numbers = "".join(
                random.choices(string.digits, k=random.randint(3, 5))
            )
            styles = [
                f"{random.choice(y2k_names)}_{suffix_numbers}",
                f"xX_{random.choice(y2k_names)}_{suffix_numbers}_Xx",
                f"{random.choice(y2k_names)}.{suffix_numbers}",
                f"{random.choice(y2k_names)}{suffix_numbers}",
            ]
            username = random.choice(styles)
            display_name = "Zeh"

            await asyncio.sleep(random.uniform(1.5, 3.0))

            inject_script = f"""
            (async () => {{
                const sleep = ms => new Promise(r => setTimeout(r, ms));

                // 1. Remplir les champs textes
                const setValue = (selector, value) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        setter.call(el, value);
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }};
                setValue('input[name="email"]', '{self.email}');
                setValue('input[name="global_name"]', '{display_name}');
                setValue('input[name="username"]', '{username}');
                setValue('input[name="password"]', '{self.password}');

                await sleep(300);

                // 2. Sélection de la Date de Naissance (supporte Français et Anglais)
                const comboboxes = Array.from(document.querySelectorAll('[role="combobox"]'));
                const getCb = (keywords, fallbackIdx) => {{
                    return comboboxes.find(cb => {{
                        const aria = (cb.getAttribute('aria-label') || '').toLowerCase();
                        return keywords.some(k => aria.includes(k));
                    }}) || comboboxes[fallbackIdx];
                }};

                const monthCb = getCb(['mois', 'month'], 0);
                const dayCb = getCb(['jour', 'day'], 1);
                const yearCb = getCb(['ann', 'year', 'année', 'annee'], 2);

                const selectCombobox = async (cb, downPresses) => {{
                    if (!cb) return;
                    cb.focus();
                    await sleep(40);
                    for (let i = 0; i < downPresses; i++) {{
                        cb.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'ArrowDown', code: 'ArrowDown', keyCode: 40, bubbles: true }}));
                        await sleep(15);
                    }}
                    cb.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }}));
                    await sleep(100);
                }};

                // Mois (1 à 12)
                const monthPresses = Math.floor(Math.random() * 12) + 1;
                await selectCombobox(monthCb, monthPresses);

                // Jour (1 à 28)
                const dayPresses = Math.floor(Math.random() * 28) + 1;
                await selectCombobox(dayCb, dayPresses);

                // Année (< 2010 : 22 à 35 pressions pour une année entre 1991 et 2004)
                const yearPresses = Math.floor(Math.random() * (35 - 22 + 1)) + 22;
                await selectCombobox(yearCb, yearPresses);

                await sleep(300);

                // 3. Cocher les cases (Conditions d'utilisation & notifications)
                const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));
                for (const cb of checkboxes) {{
                    if (!cb.checked) {{
                        cb.click();
                        await sleep(100);
                    }}
                }}

                await sleep(300);

                // 4. Soumettre le formulaire
                const submitBtn = document.querySelector('button[type="submit"]');
                if (submitBtn) {{
                    submitBtn.click();
                }}
            }})();
            """
            await page.evaluate(inject_script, await_promise=True)
            await asyncio.sleep(random.uniform(1.0, 2.0))

            token = await self.wait_for_verification(page)

            if token:
                with open(ONLY_TOKEN_FILE, "a") as f1:
                    f1.write(f"{token}\n")
                with open(FULL_DATA_FILE, "a") as f2:
                    f2.write(f"{self.email}:{self.password}:{token}\n")
                print(
                    f"{gradient_text(f'[+]  Account #{self.index} verified successfully!', Theme.GRADIENT_WHITE)}"
                )

            print(
                f"{gradient_text('⏳ Waiting 5 seconds before closing browser...', Theme.GRADIENT_WHITE)}"
            )
            await asyncio.sleep(5)
            try:
                if self.browser:
                    await self.browser.stop()
            except Exception:
                pass
        except Exception as e:
            print(f"{gradient_text(f'[-]  Error: {e}', Theme.GRADIENT_GRAY)}")
            try:
                if self.browser:
                    await self.browser.stop()
            except Exception:
                pass


class HeaderGenerator:
    def __init__(self) -> None:
        self.base_chrome_version: int = 120
        self.impersonate_target: str = f"chrome_{self.base_chrome_version}"
        self.session: tls_client.Session = tls_client.Session(
            client_identifier=self.impersonate_target
        )
        self.ua_details: Dict[str, Any] = self._generate_ua_details()
        self._header_cache: Dict[Any, Dict[str, Any]] = {}
        self._cookie_cache: Dict[str, Dict[str, Any]] = {}

    def _generate_ua_details(self) -> Dict[str, Any]:
        chrome_major: int = self.base_chrome_version
        full_version: str = f"{chrome_major}.0.0.0"
        os_spec: str = self._get_os_string()
        platform_ua: str = (
            f"Windows NT {release()}; Win64; x64" if "Windows" in os_spec else os_spec
        )
        return {
            "user_agent": f"Mozilla/5.0 ({platform_ua}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{full_version} Safari/537.36",
            "chrome_version": full_version,
            "sec_ch_ua": [
                f'"Google Chrome";v="{chrome_major}"',
                f'"Chromium";v="{chrome_major}"',
                '"Not/A)Brand";v="99"',
            ],
        }

    def _get_os_string(self) -> str:
        os_map: Dict[str, str] = {
            "Windows": f"Windows NT 10.0; Win64; x64",
            "Linux": "X11; Linux x86_64",
            "Darwin": "Macintosh; Intel Mac OS X 10_15_7",
        }
        os_str: str = os_map.get(system(), "Windows NT 10.0; Win64; x64")
        if system() == "Windows":
            win_ver: list[str] = version().split(".")
            if len(win_ver) >= 2:
                os_str = f"Windows NT {win_ver[0]}.{win_ver[1]}; Win64; x64"
        return os_str

    def fetch_cookies(self, token: str) -> str:
        now: float = time.time()
        cache_entry: Optional[Dict[str, Any]] = self._cookie_cache.get(token)
        if cache_entry and now - cache_entry["timestamp"] < 86400:
            return cache_entry["cookie"]
        try:
            resp = self.session.get(
                "https://discord.com/api/v9/users/@me", headers={"Authorization": token}
            )
            cookies: list[str] = []
            if "set-cookie" in resp.headers:
                set_cookie: Union[str, list[str]] = resp.headers["set-cookie"]
                if isinstance(set_cookie, list):
                    set_cookie = ", ".join(set_cookie)
                for cookie in set_cookie.split(", "):
                    cookie_part = cookie.split(";")[0]
                    if "=" in cookie_part:
                        name, value = cookie_part.split("=", 1)
                        cookies.append(f"{name}={value}")
            cookie_str: str = "; ".join(cookies)
            self._cookie_cache[token] = {"cookie": cookie_str, "timestamp": now}
            return cookie_str
        except:
            return ""

    def generate_super_properties(self) -> str:
        sp: Dict[str, Any] = {
            "os": system(),
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": self.ua_details["user_agent"],
            "browser_version": self.ua_details["chrome_version"].split(".0.")[0]
            + ".0.0.0",
            "os_version": str(release()),
            "referrer": "https://discord.com/",
            "referring_domain": "discord.com",
            "search_engine": "google",
            "release_channel": "stable",
            "client_build_number": 438971,
            "client_event_source": None,
            "has_client_mods": False,
            "client_launch_id": str(uuid.uuid4()),
            "launch_signature": str(uuid.uuid4()),
            "client_heartbeat_session_id": str(uuid.uuid4()),
            "client_app_state": "focused",
        }
        return b64encode(dumps(sp, separators=(",", ":")).encode()).decode()

    def generate_headers(
        self, token: str, location: Optional[str] = None, **kwargs
    ) -> Dict[str, str]:
        base_headers: Dict[str, str] = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en;q=1.0",
            "content-type": "application/json",
            "origin": "https://discord.com",
            "priority": "u=1, i",
            "sec-ch-ua": ", ".join(self.ua_details["sec_ch_ua"]),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua_details["user_agent"],
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "America/Los_Angeles",
            "x-super-properties": self.generate_super_properties(),
        }
        headers = base_headers.copy()
        headers["Authorization"] = token
        headers["cookie"] = self.fetch_cookies(token)
        return headers


def get_session_id(token: str) -> Optional[str]:
    ws: websocket.WebSocket = websocket.WebSocket()
    try:
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        hello: dict = loads(ws.recv())
        payload: dict = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {"$os": "Windows", "$browser": "Chrome", "$device": "PC"},
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False,
                },
            },
        }
        ws.send(dumps(payload))
        timeout = time.time() + 10
        while time.time() < timeout:
            response: dict = loads(ws.recv())
            if response.get("t") == "READY":
                session_id = response["d"]["session_id"]
                ws.close()
                return session_id
            if response.get("op") in [9, 429]:
                ws.close()
                return None
        ws.close()
        return None
    except:
        return None


class DiscordHuminazer:
    def __init__(self, worker_id: int) -> None:
        self.header_gen: HeaderGenerator = HeaderGenerator()
        self.profile_dir: Path = Path("io/input/profiles")
        self.avatar_dir: Path = self.profile_dir / "avatars"
        self.worker_id: int = worker_id
        self.bios: Optional[List[str]] = self._load_from_file("bio.txt")
        self.names: Optional[List[str]] = self._load_from_file("names.txt")
        self.pronouns_list: Optional[List[str]] = self._load_from_file("pronouns.txt")
        self.houses: List[str] = ["bravery", "brillance", "balance"]

    def _load_from_file(self, filename: str) -> Optional[List[str]]:
        file_path = self.profile_dir / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        return None

    def _get_random_bio(self) -> Optional[str]:
        return choice(self.bios) if self.bios else None

    def _get_random_display_name(self) -> Optional[str]:
        return choice(self.names) if self.names else None

    def _get_random_pronouns(self) -> Optional[str]:
        return choice(self.pronouns_list) if self.pronouns_list else None

    def _get_random_avatar(self) -> Optional[Path]:
        avatar_files = (
            list(self.avatar_dir.glob("*.png"))
            + list(self.avatar_dir.glob("*.jpg"))
            + list(self.avatar_dir.glob("*.jpeg"))
        )
        return choice(avatar_files) if avatar_files else None

    def _prepare_avatar(self, path: Path) -> Optional[str]:
        try:
            with Image.open(path) as img:
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (0, 0, 0))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(
                        img, mask=img.split()[-1] if img.mode == "RGBA" else None
                    )
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                data = buffer.getvalue()

                max_bytes = 8 * 1024 * 1024
                quality = 85
                while len(data) > max_bytes and quality > 10:
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=quality)
                    data = buffer.getvalue()
                    quality -= 10

                return b64encode(data).decode("utf-8")
        except:
            return None

    def humanize_account(self, token: str) -> bool:
        try:
            headers: dict = self.header_gen.generate_headers(
                token, location="User Profile"
            )
            with tls_client.Session(
                client_identifier="chrome_120", random_tls_extension_order=True
            ) as session:
                session.headers.update(headers)
                success = True

                bio = self._get_random_bio()
                if bio:
                    r = session.patch(
                        "https://discord.com/api/v9/users/@me", json={"bio": bio}
                    )
                    if r.status_code in [400, 401, 403]:
                        print(
                            f"[{self.worker_id}] {gradient_text('[-] Token is Locked/Unverified! Skipping...', Theme.GRADIENT_GRAY)}"
                        )
                        return False
                    if r.status_code == 200:
                        print(
                            f"[{self.worker_id}] {gradient_text('[+]  Bio updated successfully', Theme.GRADIENT_WHITE)}"
                        )
                    else:
                        print(
                            f"[{self.worker_id}] {gradient_text('[-]  Failed to update bio', Theme.GRADIENT_GRAY)}"
                        )
                        success = False

                pronouns = self._get_random_pronouns()
                if pronouns:
                    r = session.patch(
                        "https://discord.com/api/v9/users/@me",
                        json={"pronouns": pronouns},
                    )
                    if r.status_code == 200:
                        print(
                            f"[{self.worker_id}] {gradient_text('[+]  Pronouns updated successfully', Theme.GRADIENT_WHITE)}"
                        )
                    else:
                        print(
                            f"[{self.worker_id}] {gradient_text('[-]  Failed to update pronouns', Theme.GRADIENT_GRAY)}"
                        )
                        success = False

                display_name = self._get_random_display_name()
                if display_name:
                    r = session.patch(
                        "https://discord.com/api/v9/users/@me",
                        json={"global_name": display_name},
                    )
                    if r.status_code == 200:
                        print(
                            f"[{self.worker_id}] {gradient_text('[+]  Display name updated successfully', Theme.GRADIENT_WHITE)}"
                        )
                    else:
                        print(
                            f"[{self.worker_id}] {gradient_text('[-]  Failed to update display name', Theme.GRADIENT_GRAY)}"
                        )
                        success = False

                avatar_path = self._get_random_avatar()
                if avatar_path:
                    print(
                        f"[{self.worker_id}] {gradient_text(f'[~] Preparing avatar from {avatar_path.name}...', Theme.GRADIENT_WHITE)}"
                    )
                    avatar_b64 = self._prepare_avatar(avatar_path)
                    if avatar_b64:
                        session_id = get_session_id(token)
                        if session_id:
                            print(
                                f"[{self.worker_id}] {gradient_text('[~] Got session ID', Theme.GRADIENT_WHITE)}"
                            )
                            r = session.patch(
                                "https://discord.com/api/v9/users/@me",
                                json={"avatar": f"data:image/jpeg;base64,{avatar_b64}"},
                            )
                            if r.status_code == 200:
                                print(
                                    f"[{self.worker_id}] {gradient_text('[+]  Avatar updated successfully', Theme.GRADIENT_WHITE)}"
                                )
                            else:
                                print(
                                    f"[{self.worker_id}] {gradient_text('[-]  Failed to update avatar', Theme.GRADIENT_GRAY)}"
                                )
                                success = False
                        else:
                            print(
                                f"[{self.worker_id}] {gradient_text('[-]  Failed to get session ID', Theme.GRADIENT_GRAY)}"
                            )
                            success = False
                    else:
                        print(
                            f"[{self.worker_id}] {gradient_text('[-]  Failed to prepare avatar', Theme.GRADIENT_GRAY)}"
                        )
                        success = False

                house = choice(self.houses)
                house_id = self.houses.index(house) + 1
                r = session.post(
                    "https://discord.com/api/v9/hypesquad/online",
                    json={"house_id": house_id},
                )
                if r.status_code == 204:
                    print(
                        f"[{self.worker_id}] {gradient_text(f'[+]  Joined Hypesquad {house.capitalize()}', Theme.GRADIENT_WHITE)}"
                    )
                else:
                    print(
                        f"[{self.worker_id}] {gradient_text('[-]  Failed to join Hypesquad', Theme.GRADIENT_GRAY)}"
                    )
                    success = False

                return success
        except Exception as e:
            print(
                f"[{self.worker_id}] {gradient_text(f'[-]  Error: {str(e)}', Theme.GRADIENT_GRAY)}"
            )
            return False


class TokenManager:
    def __init__(self, token_file: str = "input/tokens.txt"):
        self.token_file = Path(token_file)
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> List[str]:
        tokens = []
        if not self.token_file.exists():
            return []
        with open(self.token_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) >= 2:
                    tokens.append(parts[-1])
                else:
                    tokens.append(line)
        return tokens


def process_token(token: str, worker_id: int):
    print(
        f"[{worker_id}] {gradient_text(f'Processing token: {token[:20]}...', Theme.GRADIENT_WHITE)}"
    )
    humanizer = DiscordHuminazer(worker_id=worker_id)
    success = humanizer.humanize_account(token)
    status = (
        f"{gradient_text('Success', Theme.GRADIENT_WHITE)}"
        if success
        else f"{gradient_text('Failed', Theme.GRADIENT_GRAY)}"
    )
    print(
        f"[{worker_id}] {gradient_text(f'Final Result: Success', Theme.GRADIENT_WHITE)}"
    )
    print(f"{gradient_text('─' * 50, Theme.GRADIENT_GRAY)}")


async def humanizer_main():
    print_banner("humanizer")

    token_manager = TokenManager()

    if not token_manager.tokens:
        print(
            f"{gradient_text('[-]  No tokens found in input/tokens.txt!', Theme.GRADIENT_GRAY)}"
        )
        print(
            f"{gradient_text('! Please generate some accounts first using Option 1.', Theme.GRADIENT_WHITE)}"
        )
        input(
            f"\n{gradient_text('→ Press Enter to return to main menu...', Theme.GRADIENT_WHITE)}"
        )
        return

    print(
        f"{gradient_text(f'[+]  Loaded {len(token_manager.tokens)} tokens', Theme.GRADIENT_WHITE)}"
    )

    avatar_dir = Path("io/input/profiles/avatars")
    if avatar_dir.exists():
        avatar_count = len(
            list(avatar_dir.glob("*.png"))
            + list(avatar_dir.glob("*.jpg"))
            + list(avatar_dir.glob("*.jpeg"))
        )
        if avatar_count > 0:
            print(
                f"{gradient_text(f'[+]  Found {avatar_count} avatars', Theme.GRADIENT_WHITE)}"
            )
        else:
            print(f"{gradient_text('! No avatars found', Theme.GRADIENT_WHITE)}")
    else:
        print(
            f"{gradient_text(f'! Avatar folder not found: {avatar_dir}', Theme.GRADIENT_WHITE)}"
        )

    max_workers = int(
        input(
            f"\n{gradient_text('? Number of threads (1-50): ', Theme.GRADIENT_WHITE)}"
        )
        or 10
    )
    max_workers = min(max_workers, 50, len(token_manager.tokens))

    print(
        f"\n{gradient_text(f'▶ Starting humanization with {max_workers} threads...', Theme.GRADIENT_WHITE)}\n"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, token in enumerate(token_manager.tokens, 1):
            futures.append(executor.submit(process_token, token, i))
        concurrent.futures.wait(futures)

    print(f"\n{gradient_text('[+]  Humanization complete!', Theme.GRADIENT_WHITE)}")
    input(
        f"\n{gradient_text('→ Press Enter to return to main menu...', Theme.GRADIENT_WHITE)}"
    )


async def generator_main():
    print_banner("generator")

    delay_min = 0
    try:
        raw_amount = input(
            f"{gradient_text('? How many accounts? ', Theme.GRADIENT_WHITE)}"
        ).strip()
        amount = int(raw_amount) if raw_amount else 1
    except Exception:
        amount = 1
        delay_min = 0

    refresh_ua_pool()

    for i in range(1, amount + 1):
        os.system("cls" if os.name == "nt" else "clear")
        print("proton vpn connected✔️")
        print_banner("generator")
        print(
            f"{gradient_text(f'▶ Generating account {i} of {amount}', Theme.GRADIENT_WHITE)}\n"
        )

        if not UA_POOL:
            refresh_ua_pool()
        current_ua = UA_POOL.pop()

        bot = DiscordBot(i, ua=current_ua)
        try:
            await bot.start()
        except Exception as e:
            print(f"{gradient_text(f'[-]  Error during account #{i}: {e}', Theme.GRADIENT_GRAY)}")

        if i < amount:
            if delay_min > 0:
                print(
                    f"{gradient_text(f'⏳ Waiting {delay_min} minutes before next account...', Theme.GRADIENT_WHITE)}"
                )
                await asyncio.sleep(delay_min * 60)
            else:
                print(
                    f"{gradient_text('⏳ Moving to next account in 5 seconds...', Theme.GRADIENT_WHITE)}"
                )
                await asyncio.sleep(5)

    print(
        f"\n{gradient_text(f'[+]  All {amount} accounts have been processed!', Theme.GRADIENT_WHITE)}"
    )
    input(
        f"\n{gradient_text('→ Press Enter to return to main menu...', Theme.GRADIENT_WHITE)}"
    )


async def main_menu():
    while True:
        print_banner("main")

        print(f"  {gradient_text('1 › Token Generator', Theme.GRADIENT_WHITE)}")
        print(f"  {gradient_text('2 › Token Humanizer', Theme.GRADIENT_WHITE)}")
        print(f"  {gradient_text('3 › Exit', Theme.GRADIENT_WHITE)}")
        print()

        choice = input(
            f"{gradient_text('→ Select option: ', Theme.GRADIENT_WHITE)}"
        ).strip()

        if choice == "1":
            await generator_main()
        elif choice == "2":
            await humanizer_main()
        elif choice == "3":
            print(f"\n{gradient_text('[-]  Exiting...', Theme.GRADIENT_GRAY)}")
            sys.exit(0)
        else:
            print(f"\n{gradient_text('[-]  Invalid option!', Theme.GRADIENT_GRAY)}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        show_glitch_art()
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print(f"\n{gradient_text('[-]  Interrupted by user', Theme.GRADIENT_GRAY)}")
        sys.exit()
