---
name: alphaxiv-paper-lookup
description: Fetch structured, AI-friendly paper overviews from alphaXiv. Use when user provides an arXiv URL, paper title, or asks to explain/summarize a research paper. Much better than reading raw PDFs - returns structured data that AI can understand well.
---

# alphaXiv Paper Lookup

Use the alphaXiv MCP server tools to fetch structured research paper data. This is superior to reading raw PDFs because alphaXiv returns structured, AI-friendly data.

## When to Use

- User provides an arXiv URL (e.g., `https://arxiv.org/abs/XXXX.XXXXX`)
- User asks to explain, summarize, or analyze a research paper
- User wants to find trending papers or search by topic/organization
- User asks about recent research in a field

## Available MCP Tools

The alphaXiv MCP server (`alphaxiv`) provides these tools:

1. **search_for_paper_by_title** - Find papers by title (exact or partial match)
2. **find_organizations** - Search for canonical organization names
3. **find_papers_feed** - Discover trending/popular papers by topic, org, time range
4. **answer_pdf_queries** - Ask questions about a specific paper given its URL
5. **read_files_from_github_repository** - Read code from a paper's GitHub repo
6. **answer_research_query** - Synthesize answers from multiple recent papers

## Workflow

### For a specific paper URL:
1. Use `answer_pdf_queries` with the URL and a query like "Provide a comprehensive overview of this paper including: title, authors, key contributions, methodology, results, and conclusions"
2. If the paper has a GitHub repo, use `read_files_from_github_repository` to explore the code

### For finding papers:
1. Use `search_for_paper_by_title` for known papers
2. Use `find_papers_feed` for discovering papers by topic/trend
3. Use `find_organizations` first if filtering by organization

### For research questions:
1. Use `answer_research_query` for broad questions requiring synthesis from multiple papers
2. Follow up with `answer_pdf_queries` on specific papers of interest

## Output Format

Present paper information in a clean, structured format:
- **Title** and authors
- **Key contributions** (bullet points)
- **Methodology** summary
- **Main results** and findings
- **Code availability** (GitHub link if available)
- **Related topics** and categories

## Notes

- The MCP server uses OAuth 2.0 authentication via SSE transport
- Endpoint: `https://api.alphaxiv.org/mcp/v1`
- Supports arXiv, alphaXiv, Semantic Scholar URLs, and direct PDF URLs
