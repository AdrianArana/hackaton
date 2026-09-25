# PCI-DSS v4.0 Compliance Directive: PII & PAN Logging Sanitization

## 1. Primary Account Number (PAN) Protection
Under Requirement 3.4 of PCI-DSS v4.0, full Primary Account Numbers (credit/debit card numbers) must NEVER appear in clear text within application logs, debug messages, error traces, or external integrations.

## 2. Masking Rules
- Valid card numbers must display only the first 6 digits (BIN) and the last 4 digits.
- All intermediate digits must be replaced with `X`.
- Example format: `4532-XXXXXXXX-8921` or `4532XXXXXXXX8921`.

## 3. Middleware & Payload Auditing
- Raw HTTP request body dumps containing payment payloads are strictly prohibited in application middlewares.
- Middleware loggers must scrub or exclude the `card_number` and `cvv` keys before writing entries to standard output.