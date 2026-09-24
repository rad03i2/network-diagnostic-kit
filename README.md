# Network Diagnostic Kit

A small, dependency-free Python toolkit for practical network troubleshooting from the terminal or Python code. It checks DNS resolution, TCP reachability, HTTP(S) health, ICMP ping availability, and local network identity without requiring administrator access for its normal workflows.

> **Privacy-first:** checks run from your machine. The project has no telemetry, accounts, API keys, or analytics.

## Why this project exists

Network failures are often ambiguous: a hostname may fail to resolve, a port may be closed, or an HTTP service may return an error even when TCP works. Network Diagnostic Kit separates these layers into explicit checks with predictable exit codes that are useful both interactively and in scripts.

## Features

- DNS lookup with unique resolved addresses.
- TCP connectivity checks with configurable timeout and port validation.
- HTTP/HTTPS `HEAD` health checks with status and latency.
- Single ICMP ping through the operating system's `ping` utility.
- Local hostname, non-loopback addresses, platform, and Python information.
- Combined `diagnose` workflow for DNS + TCP + optional ping.
- Human-readable and JSON output.
- Python API plus the `netdiag` CLI.
- Cross-platform design for Windows, macOS, and Linux.
- No runtime third-party dependencies.

## Preview

```text
$ netdiag diagnose example.com --port 443 --no-ping
[PASS] dns   example.com 12.41 ms — 93.184.216.34
[PASS] tcp   example.com:443 24.08 ms — connection established
```

Actual addresses, status and latency depend on your network. The example above is illustrative output, not live data.

## Requirements & installation

- Python 3.10+
- The OS `ping` command only if you use the `ping` check

```bash
git clone https://github.com/rad03i2/network-diagnostic-kit.git
cd network-diagnostic-kit
python -m pip install -e .
```

For development/tests:

```bash
python -m pip install -e . pytest
python -m pytest
```

## Usage

```bash
netdiag dns example.com
netdiag tcp example.com 443 --timeout 2
netdiag http https://example.com --timeout 5
netdiag ping example.com
netdiag info --json
netdiag diagnose example.com --port 443 --no-ping --json
```

The same CLI is available without the installed entry point:

```bash
python -m network_diagnostic_kit dns example.com
```

Exit codes are `0` when the requested check(s) pass, `1` when a valid diagnostic check fails, and `2` for invalid user input.

### Python API

```python
from network_diagnostic_kit import dns_lookup, tcp_connect

print(dns_lookup("example.com"))
print(tcp_connect("example.com", 443, timeout=2))
```

Every network check returns an immutable `CheckResult` with `check`, `target`, `ok`, `latency_ms`, and `detail` fields.

## Configuration

There is intentionally no config file or `.env` requirement. Host, port and timeout are explicit command/API inputs. This keeps behavior visible and avoids secret management for a tool that does not need credentials.

## Project structure

```text
src/network_diagnostic_kit/
  core.py       diagnostic engine
  cli.py        command-line interface
  __init__.py   public API
  __main__.py   python -m entry point
tests/          unit/CLI tests
.github/workflows/ci.yml
pyproject.toml
```

## Testing

Tests mock external network operations so the core suite does not depend on public Internet availability. CI runs compile checks, pytest, version output, and a local-info smoke test on Windows, macOS, and Linux using multiple supported Python versions.

## Security & privacy

The toolkit performs outbound checks only to targets you explicitly provide. It does not scan address ranges, discover LAN devices, capture packets, elevate privileges, store results, or transmit telemetry. Use it only on systems and services you are authorized to test. See [SECURITY.md](SECURITY.md).

## Limitations

- ICMP behavior depends on the OS `ping` executable and network/firewall policy.
- HTTP checks use `HEAD`; servers that reject or mishandle `HEAD` can report failure despite serving `GET` requests.
- This is a troubleshooting toolkit, not a port scanner, packet analyzer, bandwidth benchmark, vulnerability scanner, or uptime service.
- Latency is wall-clock timing from the local process and is not a precision network benchmark.
- Local address discovery is best-effort and may not enumerate every interface on complex hosts.

## Optional roadmap

Potential future additions include traceroute parsing, selectable HTTP methods, richer interface enumeration, and machine-readable batch target files. These are not required for the current core workflow.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), add tests for behavioral changes, and keep network operations bounded and explicit.

## License

MIT License — see [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

# العربية — حزمة تشخيص الشبكة

حزمة Python صغيرة وعملية لتشخيص مشكلات الشبكة من الطرفية أو من داخل الكود. تفصل الأداة بين فحص DNS، والاتصال بمنفذ TCP، وصحة HTTP/HTTPS، واختبار ping، ومعلومات الشبكة المحلية، لكي تعرف طبقة المشكلة بدل الاكتفاء برسالة اتصال عامة.

> **الخصوصية أولًا:** الفحوصات تعمل من جهازك، ولا توجد حسابات أو مفاتيح API أو تتبع أو تحليلات استخدام.

## لماذا هذا المشروع؟

قد يبدو انقطاع الخدمة مشكلة واحدة بينما يكون السبب الحقيقي فشل DNS أو منفذًا مغلقًا أو خادم HTTP يعيد حالة خطأ. توفر الحزمة فحوصات مستقلة ونتائج واضحة ورموز خروج مناسبة للاستخدام اليدوي أو داخل السكربتات وCI.

## المزايا

- حل أسماء DNS وإظهار العناوين الفريدة.
- اختبار اتصال TCP مع مهلة قابلة للتحديد والتحقق من صحة المنفذ.
- فحص HTTP/HTTPS بطريقة `HEAD` مع الحالة وزمن الاستجابة.
- إرسال ping واحد باستخدام أداة نظام التشغيل.
- عرض اسم الجهاز والعناوين غير المحلية والنظام وإصدار Python.
- أمر `diagnose` يجمع DNS وTCP وping الاختياري.
- مخرجات نصية أو JSON.
- واجهة Python وCLI باسم `netdiag`.
- تصميم متعدد الأنظمة: Windows وmacOS وLinux.
- لا توجد اعتماديات تشغيل خارج مكتبة Python القياسية.

## المعاينة

```text
netdiag diagnose example.com --port 443 --no-ping
```

ستظهر نتيجة PASS أو FAIL لكل طبقة مع الزمن والتفاصيل. القيم الفعلية تعتمد على شبكتك.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث، كما يتطلب أمر `ping` الموجود في النظام فقط عند استخدام فحص ping.

```bash
git clone https://github.com/rad03i2/network-diagnostic-kit.git
cd network-diagnostic-kit
python -m pip install -e .
```

للاختبارات:

```bash
python -m pip install -e . pytest
python -m pytest
```

## الاستخدام

```bash
netdiag dns example.com
netdiag tcp example.com 443 --timeout 2
netdiag http https://example.com
netdiag ping example.com
netdiag info --json
netdiag diagnose example.com --port 443 --no-ping --json
```

رمز الخروج `0` يعني نجاح الفحص، و`1` يعني أن فحصًا صالحًا فشل، و`2` يعني أن مدخلات المستخدم غير صحيحة.

### واجهة Python

```python
from network_diagnostic_kit import dns_lookup, tcp_connect

print(dns_lookup("example.com"))
print(tcp_connect("example.com", 443, timeout=2))
```

## الإعداد

لا يحتاج المشروع إلى ملف إعداد أو `.env`. الهدف والمنفذ والمهلة مدخلات صريحة، ولا توجد أسرار أو مفاتيح مطلوبة.

## بنية المشروع

المحرك موجود في `src/network_diagnostic_kit/core.py`، والـCLI في `cli.py`، والاختبارات في `tests/`، وسير CI في `.github/workflows/ci.yml`.

## الاختبارات

تعزل الاختبارات عمليات الشبكة الخارجية باستخدام mocks، لذلك لا تعتمد الاختبارات الأساسية على توفر الإنترنت العام. يقوم GitHub Actions بفحص التجميع وتشغيل pytest وفحوصات CLI على Windows وmacOS وLinux وعدة إصدارات Python مدعومة.

## الأمان والخصوصية

لا تفحص الأداة نطاقات IP ولا تكتشف أجهزة الشبكة ولا تلتقط الحزم ولا ترفع الصلاحيات ولا تخزن النتائج أو ترسل telemetry. الاتصالات الصادرة تكون فقط نحو الهدف الذي تدخله أنت. استخدمها فقط مع الأنظمة والخدمات التي لديك صلاحية لاختبارها. راجع [SECURITY.md](SECURITY.md).

## القيود

- ping يعتمد على أداة النظام وسياسة الجدار الناري والشبكة.
- فحص HTTP يستخدم `HEAD`؛ بعض الخوادم لا تدعمه جيدًا رغم نجاح `GET`.
- المشروع ليس ماسح منافذ أو محلل حزم أو اختبار سرعة أو ماسح ثغرات أو خدمة مراقبة مستمرة.
- قياس الزمن تقريبي من العملية المحلية وليس benchmark دقيقًا.
- اكتشاف العناوين المحلية best-effort وقد لا يعرض كل الواجهات في الأنظمة المعقدة.

## تطوير اختياري مستقبلًا

يمكن مستقبلًا إضافة traceroute، واختيار طريقة HTTP، وعرض واجهات الشبكة بتفصيل أكبر، وملفات أهداف للمعالجة الدفعية. هذه إضافات اختيارية وليست وظائف ناقصة من الغرض الحالي.

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وأضف اختبارات لأي تغيير سلوكي، وحافظ على كون عمليات الشبكة محددة وواضحة.

## الترخيص

المشروع مرخص برخصة MIT. راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
