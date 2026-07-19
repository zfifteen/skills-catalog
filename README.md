# 🌌 Platform Skills Catalog & Caching Engine

[![GitHub License](https://img.shields.io/github/license/zfifteen/skills-catalog?style=flat-square&color=blue)](LICENSE)
[![GitHub Repository Size](https://img.shields.io/github/repo-size/zfifteen/skills-catalog?style=flat-square&color=emerald)](https://github.com/zfifteen/skills-catalog)
[![Status](https://img.shields.io/badge/Lumos_Engine-Active-purple?style=flat-square)](#-lumos-workspace-caching)

Welcome to the **Platform Skills Catalog**, the central repository and interactive interface housing 790+ platform-specific capability specifications for agentic systems, alongside advanced workspace caching utilities.

This repository serves as both a high-fidelity frontend exploration interface for developer tools and the engineering cradle for **Lumos**—the persistent cognitive bridge designed to eradicate state amnesia for transient AI developers.

---

## 🚀 Key Features

*   **⚡ High-Performance Catalog Search**: Web client with instant search filtering for indexing and examining hundreds of platform skills.
*   **🧠 Lumos Workspace Caching**: Local caching engine capturing branch changes, git diff logs, recent commands, and task resumes.
*   **📜 Invariant Learner Ledgers**: A local gotchas record storing build parameters, environment configs, and platform quirks.
*   **🛠️ Automation Tooling**: Simple Python utilities to compile metadata and synchronize capability definition folders.

---

## 📂 Project Directory Structure

```bash
skills-catalog/
├── ⚙️ .gitignore             # Git ignore configuration
├── 📄 LICENSE               # MIT Open Source License
├── 📝 PLAN.md                # Project roadmap for metadata enhancement
├── 📄 README.md              # This documentation portal
├── 📦 data.js                # Compiled JSON database of metadata
├── 🎨 index.html             # UI Catalog Explorer dashboard
├── 🎨 index.css              # Custom UI stylesheets & typography
├── ⚡ script.js              # Live filtering & card renderer
├── 📂 scripts/
│   ├── 🐍 build_catalog.py   # Python parser indexing frontmatter yaml
│   └── 🐚 copy_skills.sh     # Sync shell scripts for skills folders
├── 📂 automations/
│   └── 📂 lumos/             # Caching engine engineering cradle
│       ├── 📜 proposed_agent_automation.md
│       ├── 📜 implementation_plan.md
│       └── 📜 validation_strategy.md
└── 📂 skills/                # 790+ Platform skill definition modules
```

---

## 🔮 Lumos Caching Engine

AI agents are ephemeral. Every turn begins with a blank slate, leading to high context consumption and repeating errors. **Lumos** solves this by caching project state, logs, and development invariants in a lightweight `.lumos/workspace_state.json` file.

```
       +---------------------------------------------+
       |             Agent Session N                 |
       |  - Solves bugs & finds build rules          |
       +----------------------+----------------------+
                              | (On Turn End)
                              v
             [ .lumos/workspace_state.json ]
                              | (On Session N+1 Startup)
                              v
       +----------------------+----------------------+
       |            Agent Session N+1                |
       |  - Pre-oriented and fully updated           |
       +---------------------------------------------+
```

### Quick Run Runbook
Initialize, save, and restore states locally:

```bash
# Initialize Lumos in the active directory
python3 -m lumos.cli init

# Save current branch, diffs, and successful history logs
python3 -m lumos.cli save

# Ingest and display the state payload to resume work
python3 -m lumos.cli load
```

*For step-by-step verification, see the [Validation Strategy](automations/lumos/validation_strategy.md).*

---

## ⚙️ Building the UI Catalog

The skills catalog catalog reads markdown YAML frontmatter headers to render the web interface. To update or regenerate the database payload:

```bash
# Run the catalog builder script
python3 scripts/build_catalog.py
```

This compiles active skill states and updates `data.js` automatically.

---

## 📜 License

Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.
