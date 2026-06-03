# Evidence Base For `dajia`

This reference records the corpus and source anchors used to distill the skill. It is not required for normal use; load it when a task needs provenance or a reminder of how the method was derived.

## Corpus Read

- Primary source: Bilibili space `https://space.bilibili.com/1732848825`, UP 主 `耿同学讲故事`.
- Collection date: 2026-06-02.
- Video manifest: 134 videos.
- Audio corpus: 134 downloaded audio files.
- Subtitle availability: no official subtitles were found in the harvested metadata.
- Transcript method: complete audio transcription with local MLX Whisper large-v3-turbo-q4, then full transcript reading in chronological batches.
- Validation: 134 transcript JSON files and 134 transcript TXT files, zero missing transcripts, zero transcription error rows in the final status table.
- Transcript volume: about 398k Chinese characters across the corpus.

The distilled method therefore comes from full audio-transcript reading plus public external material, not from thumbnails or isolated clips.

## Recurrent Method Anchors From Videos

The following anchors are representative rather than exhaustive. The complete manifest was included in the corpus read.

### Academic Fraud And Paper-Integrity Cases

- `BV1dbdPB5E8Y` / `BV1G1wdeRENi` / `BV1V59rYnErH`: academic-fraud lead selection, public reporting, and the first large-scale "paper-review" mode.
- `BV1Ek98YpEFW` / `BV1oY5Bz7Eo5` / `BV1z63Cz9Eci`: fast evaluation of paper anomalies and institutional/official response framing.
- `BV1nTB5YsEV3` / `BV1uS5BzoE1u` / `BV1AA5BzpEq9`: author-role, paper-quality, and evidence-boundary handling.
- `BV13YuxzqEiT` / `BV1qPEPzCErW` / `BV1GiLEzdE3Y`: high-profile scholar or doctor cases where title, paper, and institutional responsibility must be separated.
- `BV16nEsz8EBv` / `BV1f6E3zaEGt`: correction, apology, and follow-up logic; the public story continues after the first exposure.
- `BV1FMBEzKEMB` / `BV1mMBHzqEEx`: official complaint and "paper investigation" as a repeatable process, not a one-off performance.

### Data And Image Anomaly Logic

- `BV1z63Cz9Eci`: "5GH" style review, repeated checks, and anomaly classification.
- `BV1oY5Bz7Eo5`: obvious paper problems versus final responsibility claims.
- `BV1iLT1zeEAm` / `BV1iMEGzCE9S`: precision, number patterns, and the danger of confusing visible anomalies with final legal conclusions.
- `BV1EG8HzMEtk` / `BV1WKEczUEdH`: image and experimental-record evidence must be mapped before public certainty.
- `BV1e4wDeJEDw` / `BV1CsxmeLEAy`: graduation, paper, and data issues require role-specific responsibility mapping.

### Repeated Experiment And Self-Check

- `BV1hCNjzTEW3`: repeated experiment as narrow verification, not public punishment.
- `BV1aE3EzYEim`: how to interpret responses when institutions or labs are pushed to self-check.
- `BV1HoE3zNE4t` / `BV1uVE3zeE7v`: mass cases can create numbness; self-check and reform may be more useful than dumping every case at once.
- `BV1vKEVzNErr`: the value of correction, review, and continued monitoring after the public phase.

### Science, Medicine, And Product Skepticism

- `BV1XC5EzHEF1` / `BV1CQEwzUEAW`: health-product and medical-effect claims must be separated into mechanism, evidence layer, safety, and practical usefulness.
- `BV1baE5zsERw` / `BV1d7E5zFEm6`: hospital, clinical, and patient-facing contexts require higher caution and clearer action asks.
- `BV1AH5izfE9n` / `BV12c5ezZEpV`: public-health narratives require denominator, population, and causal-claim discipline.
- `BV1s75izHEJ8` / `BV1cG5SzhEma`: longevity and future-tech claims are separated into current reality, theoretical direction, ethics, and fiction.
- `BV1EdHYzMED8` / `BV12UXzYnEN2`: AI, robots, and neural-interface topics are explained by concrete technical constraints, not hype vocabulary.

### Education, Incentives, And System Critique

- `BV1bFRRY8Enj` / `BV1ZX36Y4E9t`: schooling and research incentives are treated as systems, not just individual morality.
- `BV1Jw411c7mp` / `BV1nB421H7g3`: admissions, hierarchy, and "genius" stories need evidence and institutional context.
- `BV1shHyeHEP8` / `BV1wgrEYcET5`: scholar narratives are tested against public records and role incentives.
- `BV1ZAREYdEhz` / `BV1zrQ1YtE4W`: public controversy is used to explain incentives, responsibility, and policy design.

### Self-Media Workflow And Narrative Craft

- `BV1G7RkBVEMp`: low-cost self-media workflow: choose a real interest domain, publish first, use AI as assistant, and keep human judgment/style.
- `BV1xH4y1G7pN` / `BV1ML411H7Zq`: story openings start from concrete public confusion, then reconstruct evidence.
- `BV1gS2pYME6B` / `BV1xjQPYCEDv`: satire works only when it carries an evidence point and then returns to sources.
- `BV1f5HNesEwV` / `BV1iiQZYBEEd`: the most durable scripts combine humor, student/public standpoint, and a precise technical boundary.

## External Public Sources Reviewed

- [Bilibili personal space](https://space.bilibili.com/1732848825): primary public video corpus.
- [Douyin user page](https://www.douyin.com/user/MS4wLjABAAAA9s0yrAQhOh6o3lHJ1cdo8dUu901Pjw1LHGLvprmDFuM): matching social-account surface.
- [新华社/北京日报转载](https://xinwen.bjd.com.cn/content/s6a1641aee4b03fa51a7ee007.html): describes tip intake from students/researchers, programmatic comparison, complaint letters, videos, repeated-experiment suggestion, and stricter review for major grants/high-impact labs.
- [界面新闻](https://www.jiemian.com/article/14445703.html): details decimal-distribution checks, visible repeated data, software and 5GH re-checking, and the difference between image mistakes and arithmetic/data-fabrication suspicion.
- [新黄河](https://www.jinantimes.com.cn/news-216-5259637.html): describes netizen submissions, downloading raw data, checking all raw data, early manual review, later programming help, and volunteer participation.
- [每日经济新闻](https://www.nbd.com.cn/articles/2026-05-23/4405793.html): covers motivation, business boundary, MCN/ad income, and the tension between public-interest work and platform operation.
- [新浪/上观转载](https://finance.sina.com.cn/jjxw/2026-05-27/doc-inhzikrs9314322.shtml): mentions WeChat-group leads, software/program checks plus 5GH cross-check, monthly cadence, and the refusal of a lone-hero framing.
- [长江云/新浪转载](https://finance.sina.com.cn/wm/2026-05-28/doc-inhznkuh8433363.shtml): records the decision to pause mass exposure because excessive dumping can create numbness and "法不责众", shifting emphasis toward self-check and reform.
- [海报新闻](https://hb.dzwww.com/p/p38c5rY8e.html): records the origin story from classmates pointing to raw-data inspection, the focus on biological/medical papers, and the goal of retraction, correction, and self-check rather than only personal downfall.
- [中国新闻网](https://www.chinanews.com.cn/edu/2026/05-20/10624774.shtml): frames the work as a group of young researchers behind the account, highlights small-decimal anomalies, and notes the potential for AI-assisted scanning.
- [HELL event archive](https://hellpress.org/columns/geng-stories): used only as third-party timeline/context, not as primary evidence.

## Distilled Principles

1. Public interest comes before spectacle: prioritize grants, titles, clinical risk, student burden, and institutional accountability.
2. A lead is not evidence. Convert every lead into paper passages, raw data, figures, official records, and reproducible checks.
3. Raw data can incriminate, exonerate, or expose a new inconsistency. It is not automatically a shield.
4. Numeric patterns are strong when they are tied to sample size, denominator, precision, biological context, and independent repeatability.
5. Image anomalies must be mapped visually and contextually before assigning intent.
6. The person who operated a tool may not be the same as the person who benefited, supervised, signed, funded, promoted, or ignored the problem.
7. Institutions need answerable requests: release data, correct figures, investigate authorship, re-check grant outputs, or explain title/publicity wording.
8. Repeated experiments are useful only when narrow, fair, key-node focused, and designed to test reliability.
9. In mass cases, exposure strategy matters; overwhelming the public can reduce accountability.
10. Humor is an accessibility device, not evidence.
11. Science communication must keep evidence layers separate: cell, animal, human, clinical, product, policy, and fiction.
12. System critique should explain incentives without erasing individual responsibility where evidence supports it.
