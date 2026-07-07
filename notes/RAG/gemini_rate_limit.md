### 1. How `batch_size=60` alone saved your code

Your first crash happened because your code sent each chunk as an individual API call. Hundreds of chunks meant hundreds of sequential network requests hitting Google in milliseconds, instantly breaching the **100 RPM** gate.

By adding `batch_size=60`:

* Your chunks were grouped into bundles of 60.
* For your 61-page Python Handbook, this compressed the transmission down to only **a few total requests**.
* Since a few requests are way less than 100, the RPM security gate swung open and let your code pass.

### 2. Why you didn't hit the 30K TPM limit this time

You didn't need the `rate_limiter` wrapper because **the total token count of your entire 61-page PDF was likely smaller than 30,000 tokens**.

While a 61-page document with dense, tiny technical text can reach 40K+ tokens, programming handbooks often contain formatting, empty spaces, short lines of code blocks, and diagrams. If your handbook total text came out to say, **22,000 tokens**, sending those two batches back-to-back still equals 22,000 tokens. Since 22,000 is less than 30,000, you cleared the TPM check cleanly.

**The Verdict:** You don't need a rate limiter for short or medium PDFs. Your current script with just `batch_size=60` is fully dialed in for standard documents. Keep the rate limiter concept in your back pocket only if you start parsing massive, multi-hundred-page books!