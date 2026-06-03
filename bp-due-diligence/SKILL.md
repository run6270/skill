---
name: bp-due-diligence
description: Deep due diligence workflow for startup BP, pitch decks, company profiles, investment memos, and related PDFs/docs. Use when Codex is asked to verify a BP/project/company/founding team, check founder resumes, ownership/shareholder structure, papers and citation quality, open-source metrics, competitors, product demos, public customer feedback, risks, red flags, or to generate a Chinese deep research report and one-page PDF summary for investment review meetings.
---

# BP Due Diligence

## Outcome

Produce an evidence-grounded Chinese due diligence package from one or more BP/company documents:

1. A deep Markdown report.
2. A concise one-page HTML/PDF summary when requested or when the user asks for review-meeting materials.
3. A research-data folder with extracted text, screenshots, product-test notes, and machine-readable source snapshots where useful.

Keep verified facts, inferences, and unresolved gaps separate. Do not treat BP claims as true unless independently verified.

## Default Workflow

1. **Ingest documents**
   - Copy or reference the original BP files in the working directory.
   - Extract PDF text with `scripts/extract_pdf_text.py` when text extraction is needed.
   - Read the BP for company name, product claims, founder names, legal entities, URLs, roadmap, customers, funding, technical claims, and requested use of funds.

2. **Build a claim table**
   - Extract claims into categories: company/legal, founders, cap table, product, technology, papers, patents/IP, open source, customers, market, competitors, financials.
   - Label each claim as `verified`, `partially verified`, `unverified`, `contradicted`, or `not publicly verifiable`.

3. **Verify public facts**
   - Search current web sources for modern/company/person facts; browse because these are time-sensitive.
   - Prefer primary/official sources: company registry, official websites, university pages, official app stores, GitHub/Hugging Face, papers, Google Scholar/OpenAlex/Semantic Scholar, ICP/备案, app signatures, legal notices, customer pages.
   - Use public aggregators only as secondary hints. Flag cap-table and legal facts as needing official registry documents when only aggregators are available.

4. **Founder and research verification**
   - Verify roles, education, employment, academic pages, LinkedIn-like public profiles, official news, and consistency across sources.
   - For relevant researchers, check papers in the project domain: venue, year, author position, citations, awards, code availability, and whether the work actually supports the BP claim.
   - Use citation counts as directional snapshots with source/date; do not overstate precision.

5. **Open-source and ecosystem verification**
   - Check GitHub/Hugging Face/model hubs/package registries for stars, forks, releases, commits, contributors, issues, downloads, likes, license, recency, and whether the project looks externally adopted.
   - Compare against larger alternatives and incumbents, not only against direct clones.

6. **Product and customer evidence**
   - If a public product/demo exists, test beyond the website: register or log in if allowed, download/install where safe, run a minimal workflow, inspect app signing/notarization when applicable, and capture blockers.
   - Do not expose secrets, tokens, verification codes, or credentials in the report.
   - Search customer feedback, public reviews, GitHub issues, social posts, forums, launch pages, app store reviews, and docs. Distinguish vendor marketing from customer evidence.

7. **Analyze concepts in plain language**
   - Translate vague concepts into concrete product mechanics.
   - Ask: what exists today, what is a roadmap, what must be invented, what current tools already do, and what measurable delta would prove value?
   - For “Agent Hugging Face”, “AI OS”, “offline AI”, “model marketplace”, “revenue sharing”, or similar concepts, require supply/demand/liquidity/governance/evaluation/monetization evidence.

8. **Report**
   - Use `references/checklist.md` as the coverage checklist.
   - Use `assets/deep-report-template.md` as a report skeleton when useful.
   - If generating one-page output, adapt `assets/one-pager-template.html`, then render and verify PDF with `scripts/render_one_pager_pdf.js`.

## Evidence Standards

- Cite URLs or local artifact paths for important claims.
- Separate “I verified” from “BP says” and “I infer”.
- State public-depth boundaries explicitly: what could not be verified without paid registries, private documents, customer calls, or privileged accounts.
- For product tests, record exact date, OS/app version, account path, steps attempted, pass/fail result, and screenshots/log excerpts that do not leak secrets.
- For cross-border teams, analyze operational implications: time zones, compliance, data transfer, customer support, hiring, sales, governance, and benefits such as market access or talent density.

## Output Shape

Use Chinese unless the user asks otherwise.

Recommended deep report sections:

1. Executive judgment.
2. Source documents and research scope.
3. Company/legal/entity/shareholder verification.
4. Founder/resume verification.
5. Papers, patents, awards, and technical provenance.
6. Product concept analysis in plain language.
7. Product hands-on test and customer feedback.
8. Open-source metrics and technical ecosystem.
9. Competitors and substitutes.
10. Business model, GTM, customers, and pricing.
11. Key doubts/red flags.
12. Review-meeting questions and required supplemental materials.
13. Public-depth boundaries.
14. Source list and local artifacts.

Recommended one-page summary sections:

- One-sentence investment judgment.
- Verified facts.
- Founder/team credibility.
- Product test result.
- Main doubts/red flags.
- Competitor pressure.
- Review-meeting questions.
- Dimension scores.

## Tools and Resources

- `scripts/extract_pdf_text.py`: extract text from PDF BP files into `.txt` files.
- `scripts/render_one_pager_pdf.js`: render an HTML one-pager to A4 PDF and check likely single-page layout.
- `references/checklist.md`: due diligence coverage and red-flag checklist.
- `assets/deep-report-template.md`: Markdown report skeleton.
- `assets/one-pager-template.html`: compact A4 one-page report template.

Use existing local skills/plugins when relevant:

- Use browser/Chrome/Playwright tools for product testing and screenshots.
- Use `kami` or this skill's HTML template for one-page PDF summaries.
- Use `html-to-pdf` only if available; otherwise use `scripts/render_one_pager_pdf.js`.
