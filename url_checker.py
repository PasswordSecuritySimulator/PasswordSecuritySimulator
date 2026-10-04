from urllib.parse import urlparse, unquote
import ipaddress
import re


# Common suspicious words found in phishing/social-engineering URLs.
SUSPICIOUS_WORDS = {
    "login", "signin", "verify", "verification", "account",
    "secure", "security", "update", "password", "bank",
    "wallet", "payment", "billing", "confirm", "support",
    "free", "gift", "prize", "winner", "win", "bonus",
    "recover", "reset", "unlock", "alert"
}

# Commonly abused or high-risk URL shortener domains.
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly",
    "rb.gy", "shorturl.at", "ow.ly", "buff.ly"
}

# Reserved/example domains are useful for testing and are not public sites.
RESERVED_SUFFIXES = (".invalid", ".example", ".test", ".localhost")

# Basic domain-label validation.
DOMAIN_LABEL = re.compile(
    r"^(?=.{1,63}$)(?!-)[A-Za-z0-9-]+(?<!-)$"
)


def _is_ip_address(hostname):
    """Return True when hostname is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def _valid_hostname(hostname):
    """Validate a normal DNS hostname."""
    if not hostname or len(hostname) > 253:
        return False

    # IDN/punycode is allowed, but flagged separately as a risk indicator.
    labels = hostname.rstrip(".").split(".")
    if len(labels) < 2:
        return False

    return all(DOMAIN_LABEL.match(label) for label in labels)


def _get_suspicious_indicators(parsed):
    """Collect URL indicators without claiming the URL is definitely malicious."""
    indicators = []
    hostname = (parsed.hostname or "").lower().rstrip(".")
    decoded_url = unquote(parsed.geturl()).lower()

    if _is_ip_address(hostname):
        indicators.append("استخدام عنوان IP بدل اسم النطاق")

    if hostname.startswith("xn--") or ".xn--" in hostname:
        indicators.append("استخدام نطاق Punycode/IDN")

    if "@" in parsed.netloc:
        indicators.append("وجود @ داخل الرابط")

    if parsed.port is not None and parsed.port not in (80, 443):
        indicators.append(f"منفذ غير معتاد: {parsed.port}")

    if hostname in SHORTENER_DOMAINS:
        indicators.append("خدمة اختصار روابط")

    if any(hostname.endswith(suffix) for suffix in RESERVED_SUFFIXES):
        indicators.append("نطاق محجوز للاختبار")

    # Look for suspicious words in the hostname, not the whole path.
    words_found = sorted(
        word for word in SUSPICIOUS_WORDS
        if word in hostname
    )
    if words_found:
        indicators.append("كلمات حساسة في النطاق: " + ", ".join(words_found))

    # Excessive subdomains can be used in deceptive URLs.
    subdomain_count = max(0, len(hostname.split(".")) - 2)
    if subdomain_count >= 3:
        indicators.append("عدد كبير من النطاقات الفرعية")

    # Very long URLs can be a phishing/evasion indicator.
    if len(parsed.geturl()) > 180:
        indicators.append("الرابط طويل بشكل غير معتاد")

    # Obfuscated percent-encoding in a URL can deserve review.
    if "%" in decoded_url and re.search(r"%[0-9a-f]{2}", parsed.geturl(), re.I):
        indicators.append("وجود ترميز URL قد يُستخدم للإخفاء")

    return indicators


def check_url(url):
    """Analyze a URL using local heuristics.

    This is a defensive heuristic checker. It does not guarantee that a URL
    is safe or malicious. Definitive threat detection requires a trusted
    threat-intelligence/reputation service.
    """
    url = url.strip()

    if not url:
        return "❌ لم يتم إدخال رابط."

    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url

    try:
        parsed = urlparse(url)

        # Only web URLs are accepted by this checker.
        if parsed.scheme.lower() not in ("http", "https"):
            return "❌ نوع الرابط غير مدعوم."

        if not parsed.netloc or not parsed.hostname:
            return "❌ الرابط غير صالح."

        hostname = parsed.hostname.lower().rstrip(".")

        # Reject invalid/reserved test domains used for demonstrations.
        if any(hostname.endswith(suffix) for suffix in RESERVED_SUFFIXES):
            return (
                "❌ الرابط غير صالح.\n"
                f"🌐 الرابط: {url}\n"
                "ℹ️ النطاق محجوز للاختبار وليس موقعًا عامًا."
            )

        # A raw IP is accepted for analysis but flagged as suspicious.
        if not _is_ip_address(hostname) and not _valid_hostname(hostname):
            return (
                "❌ اسم النطاق غير صالح.\n"
                f"🌐 الرابط: {url}"
            )

        indicators = _get_suspicious_indicators(parsed)

        if indicators:
            return (
                "⚠️ الرابط يحتوي على مؤشرات قد تدل على خطر.\n"
                f"🌐 الرابط: {url}\n"
                "🔎 المؤشرات:\n"
                + "\n".join(f"• {item}" for item in indicators)
                + "\nℹ️ هذه نتيجة تحليل مبدئي وليست حكمًا نهائيًا بأن الرابط خبيث."
            )

        return (
            "✅ لم يتم العثور على مؤشرات خطر واضحة مبدئيًا.\n"
            f"🌐 الرابط: {url}\n"
            "ℹ️ هذا الفحص محلي ولا يضمن أن الموقع آمن 100%."
        )

    except Exception:
        return "❌ حدث خطأ أثناء فحص الرابط."
