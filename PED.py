"""Rule-based educational phishing-email indicator.

This program flags simple suspicious patterns. It is not a trained AI model
and must not be treated as proof that an email is malicious or safe.
"""
import re

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
URGENT_TERMS = (
    "urgent", "immediately", "verify your account", "account suspended",
    "password expires", "act now", "payment failed", "claim your prize",
)
SENSITIVE_TERMS = (
    "password", "one-time password", "otp", "bank details",
    "credit card", "login credentials",
)


def analyze_email(sender: str, subject: str, body: str) -> tuple[int, list[str]]:
    text = f"{subject}\n{body}".lower()
    score = 0
    findings = []

    if any(term in text for term in URGENT_TERMS):
        score += 1
        findings.append("Urgent or pressure-based wording found.")
    if any(term in text for term in SENSITIVE_TERMS):
        score += 1
        findings.append("A request or reference to sensitive information was found.")

    urls = URL_RE.findall(body)
    if urls:
        findings.append(f"{len(urls)} link(s) found; inspect their destinations carefully.")
        for url in urls:
            host_match = re.search(r"https?://([^/]+)", url, re.IGNORECASE)
            host = host_match.group(1).lower() if host_match else ""
            if "@" in host or host.startswith("xn--"):
                score += 1
                findings.append("A link contains a potentially deceptive hostname pattern.")
                break

    sender_domain = sender.rsplit("@", 1)[-1].lower() if "@" in sender else ""
    if not sender_domain or "." not in sender_domain:
        score += 1
        findings.append("Sender address/domain looks incomplete or unusual.")

    if not findings:
        findings.append("No listed warning pattern was found; this does not prove the email is safe.")

    return score, findings


def main() -> None:
    print("=== Phishing Email Detector (rule-based demo) ===")
    sender = input("Sender email: ").strip()
    subject = input("Email subject: ").strip()
    print("Paste the email body. Finish with an empty line:")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    score, findings = analyze_email(sender, subject, "\n".join(lines))
    print(f"\nRisk indicator score: {score}")
    print("Review level:", "Higher risk indicators" if score >= 2 else "Some indicators" if score == 1 else "No listed indicators")
    for finding in findings:
        print("-", finding)
    print("\nThis educational tool can produce false positives and false negatives. Verify messages independently.")


if __name__ == "__main__":
    main()
