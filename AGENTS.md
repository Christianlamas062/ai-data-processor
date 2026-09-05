# Project Context & Agent Operating Rules: AI Data Processor

## 1. Executive Summary & Objective
- **Repository:** `ai-data-processor`
- **Purpose:** Public GitHub portfolio piece demonstrating production-grade Python engineering, automated ETL/data cleaning, AI-powered analytical synthesis, and autonomous agent extensibility for Upwork enterprise clients.
- **Current Runtime:** Python 3.10+, Pandas, Google Generative AI (Gemini 1.5 Flash), Colorama, PyYAML, Pytest.
- **Migration Target:** Google Antigravity SDK (`google-antigravity`) to enable programmatic autonomous execution, tools invocation (shell, code execution, local file I/O), and MCP integration.

## 2. Architecture & File Structure
ai-data-processor/
├── AGENTS.md             # This context & instructions manifest
├── config.yaml           # Runtime configuration parameters
├── requirements.txt      # Dependency constraints
├── .env.example          # Environment secrets template
├── src/
│   ├── init.py
│   ├── agent.py          # Central workflow orchestrator
│   ├── data_loader.py    # CSV file loading & defensive validations
│   ├── cleaner.py        # Deterministic pandas data cleaning & normalization
│   ├── analyzer.py       # AI inference layer (Gemini / Antigravity integration point)
│   ├── reporter.py       # Disk persistence (cleaned CSVs and Markdown report)
│   └── logger.py         # Colorama-enhanced logging handler
├── tests/
│   ├── init.py
│   ├── test_data_loader.py
│   └── test_cleaner.py
├── data/
│   └── sample.csv        # Mock CSV with dirty data (spaces, nulls, duplicates)
└── output/               # Output destination for cleaned artifacts and reports


## 3. Engineering Guidelines & Coding Standards
1. **Defensive Programming:** Always enforce type annotations (`typing`), handle edge cases (empty files, missing env vars, schema mismatches), and fail with informative exceptions.
2. **Decoupled Logic:** No hardcoded paths or settings in `src/`. All operational settings must resolve through `config.yaml`.
3. **Observability:** Do not use bare `print()`. Use `logger = setup_logger(...)` from `src.logger` to provide clean, timestamped, colored console status.
4. **Test-Driven Reliability:** Every feature or modification added to `src/cleaner.py` or `src/data_loader.py` must include corresponding tests in `tests/` passing with `pytest`.

## 4. Antigravity Migration Roadmap
- **Phase 1 (Active):** Structured deterministic pipeline with Gemini API (`google-generativeai`).
- **Phase 2 (Next):** Implement `google.antigravity.Agent` using `LocalAgentConfig` inside `src/analyzer.py` or `src/agent.py` to enable dynamic code generation and self-correction on dirty data schemas.
- **Phase 3:** Integrate MCP (Model Context Protocol) tool exposure.