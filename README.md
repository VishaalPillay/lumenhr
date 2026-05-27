# LumenHR 🧠

> **Burnout is invisible until it's too late. Lumen sheds light on the invisible signals.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Microsoft 365](https://img.shields.io/badge/Microsoft%20365-Copilot%20Chat-blue.svg)](https://www.microsoft.com/en-us/microsoft-365)
[![Azure](https://img.shields.io/badge/Azure-Key%20Vault%20%7C%20Entra%20ID-0078D4.svg)](https://azure.microsoft.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)](https://www.postgresql.org/)
[![Azure Functions](https://img.shields.io/badge/Azure%20Functions-Timer%20Trigger-0078D4.svg)](https://learn.microsoft.com/en-us/azure/azure-functions/)
[![Hackathon](https://img.shields.io/badge/Agents%20League-Enterprise%20Track-purple.svg)](https://aka.ms/agentsleague/discord)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Folder Structure](#-folder-structure)
- [Installation Guide](#-installation-guide)
- [Environment Variables](#-environment-variables)
- [Usage Guide](#-usage-guide)
- [Screenshots & Demo](#-screenshots--demo)
- [API Documentation](#-api-documentation)
- [Database Design](#-database-design)
- [AI & IQ Workflow](#-ai--iq-workflow)
- [Security Features](#-security-features)
- [Challenges Faced](#-challenges-faced)
- [Future Improvements](#-future-improvements)
- [Contributors](#-contributors)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 Project Overview

### What is LumenHR?

**LumenHR** is a privacy-first, AI-powered workforce wellbeing agent built natively inside **Microsoft 365 Copilot Chat**. It uses Microsoft 365 behavioral signals — calendar density, after-hours email activity, focus time erosion, and meeting overload — to detect cognitive burnout risk in enterprise teams before it becomes a crisis.

### The Problem

Enterprise burnout is invisible until it's too late. People managers have no real-time signal that their team is quietly breaking down. By the time someone resigns or goes on leave, the cost — financial, operational, and human — has already been paid.

Existing solutions are either:
- **Too reactive** (engagement surveys sent quarterly, after damage is done)
- **Too invasive** (surveillance tools that destroy psychological safety)
- **Too disconnected** (dashboards nobody opens, not integrated into where managers work)

### Why LumenHR?

LumenHR solves this by embedding intelligence **directly into the tools managers already use** — Microsoft Teams and M365 Copilot Chat — with a privacy-first architecture that aggregates signals without surveilling individuals.

| Without LumenHR | With LumenHR |
|---|---|
| Manager finds out about burnout at resignation | Manager receives risk signal 3–4 weeks early |
| Advice from intuition or generic Google searches | Recommendations cited from company's own HR & EAP policies |
| No audit trail of manager actions | Every intervention logged for HR compliance |
| Employee has no agency in the process | Employee self-service agent with consent-based opt-in |

### Core Philosophy

> **Signals without surveillance.** LumenHR detects patterns, not people. Raw Microsoft Graph data never reaches the manager interface — only aggregated, anonymized risk scores tied to policy-grounded recommendations.

---

## ✨ Features

### Manager Agent (Macro View)
- 🔍 **Team Risk Dashboard** — Aggregated burnout risk scores per team member (anonymized), updated nightly
- 📈 **4-Week Trend Analysis** — Identifies whether overload is a temporary spike or a worsening pattern
- 📋 **Policy-Grounded Recommendations** — Every intervention suggestion cited from company EAP, Manager Handbook, or Leave Policy via Foundry IQ
- 📅 **One-Click Wellbeing Check-ins** — Agent writes directly to Outlook Calendar with pre-populated conversation framework
- 👥 **Cognitive Load-Aware Task Assignment** — When assigning new work, agent compares both skills AND current cognitive load: *"Jordan has the right skills and 40% free capacity. Alex is at 95% load — not recommended."*
- 📊 **Systemic Insights** — Team-level patterns surfaced: *"Your team's average focus time dropped 40% this week. Recommend: No-Meeting Fridays."*
- 🗂️ **HR Audit Trail** — Every manager action logged for compliance and accountability

### Employee Agent (Micro View — Consent-First)
- 🙋 **Voluntary Opt-In** — Employees explicitly choose to enable their personal LumenHR view
- 📊 **Personal Signal Dashboard** — *"You've been in back-to-back meetings for 4 days. Here's what your week looks like."*
- 📄 **EAP Policy Access** — Agent surfaces relevant entitlements: *"Your company policy entitles you to 6 free counseling sessions."*
- ✉️ **Workload Discussion Drafts** — Employee requests help drafting a workload email to their manager; agent drafts, employee reviews and sends manually (never auto-sent)
- 🔒 **Zero Upward Reporting** — Employee signals are never shared with manager without explicit employee consent

### Platform & Infrastructure
- ⚡ **Pre-computed Scores** — Nightly Azure Functions Timer Trigger pre-computes all risk scores so Copilot Chat queries return in <50ms
- 🔐 **OAuth 2.0 + Entra ID** — Enterprise-grade authentication on every MCP tool call
- 📦 **MCP App Packaging** — Fully packaged as a reusable MCP App for extensibility
- 🕐 **Data Freshness Transparency** — Every response surfaces *"Based on signals computed at 6:00 AM today"* — no hidden data latency

---

## 🛠 Tech Stack

### Platform & Hosting

| Layer | Technology | Purpose |
|---|---|---|
| Agent Host | Microsoft 365 Copilot Chat | Native agent surface for managers & employees |
| Agent Type | Declarative Agent (DA) | Config-driven JSON agent via M365 Agents Toolkit |
| IDE | VS Code + M365 Agents Toolkit | Agent development and sideloading |

### Backend

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core MCP server language |
| FastAPI | 0.110+ | MCP server REST framework |
| Azure Functions | v4 (Python) | Nightly Timer Trigger for async signal processing |
| azure-functions | 1.x | Python SDK for Azure Functions runtime |
| Uvicorn | 0.29+ | ASGI server for FastAPI |

### Database

| Technology | Purpose |
|---|---|
| PostgreSQL 15+ | Pre-computed scores, role baselines, intervention logs, employee preferences |
| SQLAlchemy | ORM for Python ↔ PostgreSQL |
| Alembic | Database migration management |

### Microsoft Intelligence Layers (IQ Stack)

| IQ Layer | Integration | Role in LumenHR |
|---|---|---|
| **Work IQ** | Microsoft Graph API | Source of all M365 behavioral signals (calendar, presence, mail metadata) |
| **Foundry IQ** | Azure AI Foundry Knowledge Base | Grounds all recommendations in company HR/EAP/policy documents with citations |
| **Fabric IQ** | Microsoft Fabric Semantic Model | Org-level semantic reasoning — roles, departments, structural overload patterns |

### Security & Auth

| Technology | Purpose |
|---|---|
| Microsoft Entra ID (Azure AD) | Primary user authentication |
| OAuth 2.0 | MCP server authorization |
| Azure Key Vault | Secret management (production) |
| python-dotenv | Secret management (local development) |

### Deployment

| Technology | Purpose |
|---|---|
| Azure Container Apps | MCP server hosting |
| Azure Functions | Nightly signal processing (Timer Trigger, serverless) |
| Azure Container Registry | Container image registry |
| Docker | Containerization |
| GitHub Actions | CI/CD pipeline |

---

## 🏗 System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Microsoft 365 Copilot Chat                │
│  ┌──────────────────┐      ┌──────────────────────────┐  │
│  │  Manager Agent   │      │    Employee Agent         │  │
│  │  (Macro View)    │      │  (Consent-First, Micro)   │  │
│  └────────┬─────────┘      └────────────┬─────────────┘  │
└───────────┼─────────────────────────────┼────────────────┘
            │  MCP Protocol (OAuth 2.0)   │
            ▼                             ▼
┌─────────────────────────────────────────────────────────┐
│              Python MCP Server (FastAPI)                 │
│                                                          │
│  READ Tools:              WRITE Tools:                   │
│  get_team_signals()       create_checkin_event()         │
│  get_member_trend()       log_intervention()             │
│  get_intervention_        draft_workload_email()         │
│    playbook()             escalate_to_hr()               │
│  get_org_risk_map()                                      │
│  recommend_task_                                         │
│    assignment()                                          │
└──────┬──────────────────────────────────┬───────────────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                 ┌────────────────────┐
│  PostgreSQL  │                 │    IQ Layer Stack   │
│  Database    │                 │                     │
│              │                 │  Work IQ:           │
│  - scores    │                 │  Microsoft Graph    │
│  - baselines │                 │  (nightly pull)     │
│  - logs      │                 │                     │
│  - prefs     │                 │  Foundry IQ:        │
└──────┬───────┘                 │  Policy Documents   │
       │                         │  (cited retrieval)  │
       ▼                         │                     │
┌──────────────┐                 │  Fabric IQ:         │
│    Azure     │                 │  Org Semantic Graph │
│  Functions   │◄────────────────│  (role reasoning)   │
│ (Timer Trig) │                 └────────────────────┘
│              │
│  Nightly:    │
│  Graph API   │
│  → Aggregate │
│  → Score     │
│  → Store     │
└──────────────┘
```

### Data Flow: Manager Query

```
1. Manager types: "Who on my team needs attention this week?"
          │
          ▼
2. M365 Copilot Chat routes to LumenHR Declarative Agent
          │
          ▼
3. Agent calls MCP tool: get_team_signals(manager_id, "7d")
          │
          ▼
4. MCP Server: SELECT pre-computed scores FROM PostgreSQL  (<50ms)
          │
          ▼
5. Agent calls: get_org_risk_map() → Fabric IQ semantic query
   → Contextualise scores against role baselines
          │
          ▼
6. Agent calls: get_intervention_playbook(risk_level, role_type)
   → Foundry IQ retrieves cited policy recommendations
          │
          ▼
7. Agent synthesises response:
   - Anonymised risk summary
   - Trend direction (spike vs. worsening)
   - Cited intervention steps
   - Offers write actions (calendar, survey, log)
          │
          ▼
8. Manager confirms → Agent executes write tool
   → Calendar event created in Outlook
   → Intervention logged to PostgreSQL audit table
```

### Nightly Async Pipeline

```
11:00 PM — Azure Functions Timer Trigger fires (cron: "0 0 23 * * *")
          │
          ▼
Azure Function: nightly_signal_sync()
          │
          ├── Authenticate with Entra ID (Managed Identity — no stored secrets)
          │
          ├── Microsoft Graph API calls (per opted-in user)
          │   ├── GET /me/calendarView → meeting hours
          │   ├── GET /me/mailFolders/inbox/messages → email timestamps
          │   └── GET /users/{id}/presence → availability status
          │
          ├── Privacy Aggregation Pipeline
          │   ├── Strip identifiers
          │   ├── Compute signal scores per category
          │   └── Apply role-adjusted baselines from PostgreSQL
          │
          ├── Burnout Risk Score Computation
          │   ├── Weighted composite score (0–100)
          │   ├── Risk tier: LOW / MODERATE / HIGH / CRITICAL
          │   └── Trend delta vs. prior 4 weeks
          │
          └── Write to PostgreSQL: pre_computed_scores table
              (timestamp, member_id, score, tier, trend_delta)

Note: Azure Functions spins up, executes, and scales back to zero.
      Completely decoupled from the MCP server container lifecycle.
```

### Authentication Flow

```
User → M365 Copilot Chat
     → Entra ID SSO (managed by M365 platform)
     → Agent calls MCP Server
     → MCP Server validates OAuth 2.0 Bearer token
     → Token introspection against Entra ID
     → Minimum-scope Graph permissions verified
     → Tool execution authorised
```

---

## 📁 Folder Structure

```
lumenhr/
│
├── 📁 agent/                        # M365 Declarative Agent config
│   ├── manifest.json                # Teams App manifest
│   ├── declarative-agent.json       # DA instructions, persona, MCP connection
│   ├── manager-instructions.md      # Manager agent system prompt
│   └── employee-instructions.md     # Employee agent system prompt
│
├── 📁 mcp_server/                   # Python FastAPI MCP Server
│   ├── main.py                      # FastAPI app entrypoint
│   ├── auth.py                      # OAuth 2.0 + Entra ID validation
│   ├── 📁 tools/                    # MCP tool definitions
│   │   ├── read_tools.py            # get_team_signals, get_member_trend, etc.
│   │   └── write_tools.py           # create_checkin_event, log_intervention, etc.
│   ├── 📁 services/                 # Business logic layer
│   │   ├── graph_service.py         # Microsoft Graph API client
│   │   ├── foundry_service.py       # Foundry IQ knowledge retrieval
│   │   ├── fabric_service.py        # Fabric IQ semantic queries
│   │   └── scoring_service.py       # Burnout risk score computation
│   └── 📁 schemas/                  # Pydantic models
│       ├── signals.py
│       ├── scores.py
│       └── interventions.py
│
├── 📁 scheduler/                        # Azure Functions Timer Trigger project
│   ├── nightly_signal_sync/
│   │   ├── __init__.py                  # Function entry point — calls pipeline.py
│   │   └── function.json                # Timer trigger config (cron expression)
│   ├── shared/
│   │   └── pipeline.py                  # Privacy aggregation + scoring pipeline
│   ├── host.json                        # Azure Functions host configuration
│   ├── requirements.txt                 # Python deps for the function only
│   └── local.settings.json              # Local dev settings (gitignored)
│
├── 📁 database/                     # Database layer
│   ├── models.py                    # SQLAlchemy ORM models
│   ├── connection.py                # PostgreSQL connection management
│   └── 📁 migrations/               # Alembic migration scripts
│       ├── env.py
│       └── versions/
│
├── 📁 knowledge_base/               # Foundry IQ source documents
│   ├── eap_policy.pdf               # Employee Assistance Program policy
│   ├── manager_handbook.pdf         # Manager wellbeing conversation guide
│   ├── leave_policy.pdf             # Mental health leave entitlements
│   └── escalation_playbook.pdf      # HR escalation procedures
│
├── 📁 synthetic_data/               # Demo & testing data (NO real PII)
│   ├── seed_employees.sql           # EMP-001 to EMP-050
│   ├── seed_departments.sql         # DEPT-ENG, DEPT-SALES, DEPT-HR, etc.
│   └── seed_baselines.sql           # Role baseline configurations
│
├── 📁 infrastructure/               # Deployment configuration
│   ├── Dockerfile                   # MCP server container
│   ├── docker-compose.yml           # Local dev stack (API + DB only)
│   └── 📁 azure/
│       ├── key_vault.bicep          # Azure Key Vault provisioning
│       ├── container_app.bicep      # Azure Container Apps deployment
│       └── function_app.bicep       # Azure Functions app provisioning
│
├── 📁 .github/
│   └── 📁 workflows/
│       ├── ci.yml                   # Run tests on every PR
│       └── deploy.yml               # Build & push to Azure Container Registry
│
├── 📁 tests/
│   ├── test_tools.py                # MCP tool unit tests
│   ├── test_scoring.py              # Risk scoring logic tests
│   └── test_pipeline.py             # Azure Function pipeline tests
│
├── .env.example                     # Environment variable template (no secrets)
├── .gitignore                       # Includes .env, *.pem, __pycache__, etc.
├── requirements.txt                 # Python dependencies
├── alembic.ini                      # Alembic migration config
└── README.md                        # This file
```

---

## 🚀 Installation Guide

### Prerequisites

Before you begin, ensure you have the following:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Docker & Docker Compose** — [Download](https://www.docker.com/products/docker-desktop/)
- **VS Code** + [M365 Agents Toolkit Extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.ms-teams-vscode-extension)
- **Azure Functions Core Tools v4** — [Install](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- **Microsoft 365 Developer Tenant** — [Get a free M365 Dev Tenant](https://developer.microsoft.com/en-us/microsoft-365/dev-program)
- **Azure CLI** — [Install](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Git**

> ⚠️ **Important:** You need admin consent on your M365 developer tenant for the Microsoft Graph API scopes used by LumenHR. See [Graph Permissions Setup](#graph-permissions-setup) below.

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/lumenhr.git
cd lumenhr
```

---

### Step 2: Set Up Python Virtual Environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env
```

Open `.env` and fill in your values. See the [Environment Variables](#-environment-variables) section for full details.

> 🔒 **Never commit `.env` to version control.** It is already in `.gitignore`.

---

### Step 5: Start Local Infrastructure (Docker)

```bash
# Start PostgreSQL — no Redis or broker needed with Azure Functions
docker-compose up -d postgres
```

Verify the database is running:

```bash
docker-compose ps
```

---

### Step 6: Run Database Migrations

```bash
# Apply all migrations
alembic upgrade head

# Seed synthetic demo data
psql $DATABASE_URL -f synthetic_data/seed_employees.sql
psql $DATABASE_URL -f synthetic_data/seed_departments.sql
psql $DATABASE_URL -f synthetic_data/seed_baselines.sql
```

---

### Step 7: Start the MCP Server

```bash
uvicorn mcp_server.main:app --reload --port 8000
```

Verify the server is running:

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "1.0.0"}
```

---

### Step 8: Set Up the Azure Functions Scheduler (Local)

Navigate to the scheduler project and install its dependencies:

```bash
cd scheduler
pip install -r requirements.txt
```

Start the Azure Functions runtime locally:

```bash
func start
```

You should see:

```
Functions:
  nightly_signal_sync: timerTrigger
```

---

### Step 9: Trigger a Manual Signal Sync (for Demo)

To populate pre-computed scores without waiting for the 11PM nightly trigger:

```bash
# Invoke the function manually via the local runtime
func run nightly_signal_sync --no-interactive
```

Or call it directly during development:

```bash
cd scheduler
python -c "from shared.pipeline import run_signal_aggregation_pipeline; run_signal_aggregation_pipeline()"
```

---

### Step 9b: Deploy the Azure Function to Azure

```bash
# Login to Azure
az login

# Deploy the function app
cd scheduler
func azure functionapp publish lumenhr-scheduler
```

> 💡 **Tip:** The Azure Function uses a **Managed Identity** to authenticate with Entra ID and PostgreSQL in production — no secrets stored in the function configuration.

---

### Step 10: Sideload the Declarative Agent to M365 Copilot Chat

1. Open **VS Code** with the **M365 Agents Toolkit** extension
2. Open the `agent/` folder
3. Update `declarative-agent.json` with your MCP server URL (ngrok or Azure URL)
4. Press `F5` or click **"Provision"** in the Agents Toolkit panel
5. Follow the prompts to sideload to your developer tenant
6. Open [Microsoft Teams](https://teams.microsoft.com) and find **LumenHR** in your app list

---

### Graph Permissions Setup

In your Azure Portal → Entra ID → App Registrations → LumenHR App:

1. Navigate to **API Permissions**
2. Add the following **Microsoft Graph** delegated permissions:

```
Calendars.Read
Mail.Read
Presence.Read.All
User.Read.All
```

3. Click **Grant admin consent** for your tenant

---

## 🔑 Environment Variables

> 🔒 All secrets must be stored in Azure Key Vault in production. Use `.env` for local development only.

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/lumenhr` |
| `AZURE_TENANT_ID` | Your Azure / Entra ID tenant ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_CLIENT_ID` | App registration client ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_CLIENT_SECRET` | App registration client secret | `your-client-secret` |
| `GRAPH_API_ENDPOINT` | Microsoft Graph base URL | `https://graph.microsoft.com/v1.0` |
| `FOUNDRY_ENDPOINT` | Azure AI Foundry knowledge base URL | `https://your-foundry.azure.com` |
| `FOUNDRY_API_KEY` | Foundry IQ API key | `your-foundry-api-key` |
| `FABRIC_ENDPOINT` | Microsoft Fabric semantic model URL | `https://api.fabric.microsoft.com` |
| `FABRIC_WORKSPACE_ID` | Fabric workspace identifier | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `KEY_VAULT_URL` | Azure Key Vault URL (production) | `https://lumenhr-kv.vault.azure.net/` |
| `MCP_SERVER_URL` | Public URL of MCP server | `https://lumenhr-mcp.azurecontainerapps.io` |
| `AZURE_FUNCTION_APP_NAME` | Azure Functions app name | `lumenhr-scheduler` |
| `SECRET_KEY` | JWT signing secret | `your-256-bit-secret` |
| `ENVIRONMENT` | Deployment environment | `development` / `production` |

---

## 📖 Usage Guide

### For People Managers

**Open Microsoft Teams or M365 Copilot Chat and find LumenHR in your apps.**

#### Check Team Wellbeing Status
```
You: "How is my team doing this week?"

LumenHR: "Here's your team's wellbeing snapshot for the week of June 9–13.

  🟡 Moderate Risk (2 members) — showing elevated meeting load
  🔴 High Risk (1 member) — back-to-back meetings for 8 days, zero focus time

  Based on your Manager's Handbook (§4.2), I recommend initiating a 
  private check-in with your high-risk team member this week.
  
  Would you like me to schedule a 30-minute wellbeing check-in?"
```

#### Schedule a Wellbeing Check-in
```
You: "Yes, schedule it for Thursday afternoon."

LumenHR: "Done. I've added a 30-minute check-in to your Outlook calendar 
  for Thursday at 2:00 PM, with a conversation guide attached based on 
  your company's EAP policy. The intervention has been logged."
```

#### Get Task Assignment Recommendations
```
You: "Who can take on this urgent security audit task?"

LumenHR: "Reviewing skills and cognitive load across your team:
  
  ✅ Jordan Chen — skills match confirmed, 38% meeting utilization this week
  ⚠️  Alex Rivera — skills match confirmed, but at 94% meeting capacity
  
  I recommend assigning to Jordan. Shall I draft the assignment message?"
```

---

### For Employees (After Opt-In)

**Access LumenHR from M365 Copilot Chat for your personal view.**

#### Check Your Own Signals
```
You: "How does my week look?"

LumenHR: "Here's your personal workload snapshot:
  
  📅 Meetings: 34 hours this week (your typical average: 18 hours)
  🎯 Focus time: 2 hours (recommended: 8+ hours)
  🌙 After-hours activity: 3 evenings this week
  
  Your company's Flexible Work Policy (§3.1) includes options for 
  workload adjustment. Would you like help drafting a conversation 
  with your manager?"
```

---

## 🖼 Screenshots & Demo

### Demo Video
> 📽️ **[Watch the 90-second demo](https://your-demo-link-here.com)**

### Architecture Diagram
> ![Architecture Diagram](docs/architecture-diagram.png)
> *(See `docs/architecture-diagram.png`)*

### Agent in M365 Copilot Chat
> ![Manager View](docs/screenshots/manager-view.png)
> *(Manager asking about team wellbeing)*

> ![Employee View](docs/screenshots/employee-view.png)
> *(Employee self-service wellbeing check)*

> ![Calendar Integration](docs/screenshots/calendar-write.png)
> *(Agent writing check-in event to Outlook)*

### Risk Score Dashboard Response
> ![Risk Summary](docs/screenshots/risk-summary.png)

---

## 📡 API Documentation

### Base URL
```
Local:      http://localhost:8000
Production: https://lumenhr-mcp.azurecontainerapps.io
```

### Authentication
All endpoints require a valid OAuth 2.0 Bearer token issued by Entra ID.

```
Authorization: Bearer <access_token>
```

---

### MCP Tools (Exposed via MCP Protocol)

#### `GET /tools/get_team_signals`

Returns pre-computed, anonymised burnout risk scores for all members of a manager's team.

**Request**
```json
{
  "manager_id": "EMP-001",
  "time_window": "7d"
}
```

**Response**
```json
{
  "last_updated": "2026-06-09T06:00:00Z",
  "team_summary": {
    "low_risk": 5,
    "moderate_risk": 2,
    "high_risk": 1,
    "critical_risk": 0
  },
  "members": [
    {
      "member_ref": "MEMBER-A",
      "risk_tier": "HIGH",
      "score": 78,
      "trend": "worsening",
      "trend_delta": +12,
      "primary_signals": ["meeting_overload", "zero_focus_time"]
    }
  ]
}
```

---

#### `GET /tools/get_intervention_playbook`

Returns Foundry IQ-grounded intervention recommendations cited from company policy documents.

**Request**
```json
{
  "risk_level": "HIGH",
  "role_type": "SOFTWARE_ENGINEER"
}
```

**Response**
```json
{
  "recommendations": [
    {
      "step": 1,
      "action": "Schedule a private, non-evaluative 1:1 conversation focused on workload, not performance.",
      "citation": {
        "document": "Manager's Handbook",
        "section": "§4.2 — Recognizing Early Signs of Burnout",
        "page": 34
      }
    },
    {
      "step": 2,
      "action": "Inform the employee of their EAP entitlement: 6 free counseling sessions.",
      "citation": {
        "document": "EAP Policy",
        "section": "§2.1 — Employee Entitlements",
        "page": 12
      }
    }
  ]
}
```

---

#### `POST /tools/create_checkin_event`

Writes a wellbeing check-in event to the manager's Outlook calendar via Microsoft Graph.

**Request**
```json
{
  "manager_id": "EMP-001",
  "suggested_time": "2026-06-12T14:00:00Z",
  "duration_minutes": 30,
  "agenda_template_id": "WELLBEING_CHECKIN_V1"
}
```

**Response**
```json
{
  "status": "created",
  "event_id": "graph_event_abc123",
  "calendar_url": "https://outlook.office.com/calendar/...",
  "logged": true
}
```

---

#### `POST /tools/recommend_task_assignment`

Returns a cognitive-load-aware task assignment recommendation.

**Request**
```json
{
  "task_description": "Conduct Q3 security audit review",
  "candidate_member_ids": ["EMP-005", "EMP-009", "EMP-014"]
}
```

**Response**
```json
{
  "recommendation": "EMP-009",
  "reasoning": "EMP-009 has the required skill match (Security, Compliance) and is at 38% cognitive load this week. EMP-005 is skill-matched but at 94% capacity. EMP-014 does not have the required skill profile.",
  "candidates": [
    {"member_ref": "MEMBER-B", "skill_match": true, "cognitive_load_pct": 38, "recommended": true},
    {"member_ref": "MEMBER-C", "skill_match": true, "cognitive_load_pct": 94, "recommended": false},
    {"member_ref": "MEMBER-D", "skill_match": false, "cognitive_load_pct": 45, "recommended": false}
  ]
}
```

---

### Health & Monitoring

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Service health check |
| `/health/db` | GET | PostgreSQL connectivity check |
| `/health/function` | GET | Azure Functions scheduler last-run status check |
| `/health/graph` | GET | Microsoft Graph API connectivity check |

---

## 🗄 Database Design

### Schema Overview

```sql
-- Pre-computed burnout risk scores (nightly populated)
CREATE TABLE pre_computed_scores (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id       VARCHAR(20) NOT NULL,   -- e.g., EMP-005
    computed_at     TIMESTAMP NOT NULL,
    score           INTEGER NOT NULL,        -- 0–100
    risk_tier       VARCHAR(10) NOT NULL,    -- LOW/MODERATE/HIGH/CRITICAL
    trend_delta     INTEGER,                 -- change vs. prior period
    trend_direction VARCHAR(10),             -- stable/improving/worsening
    signal_summary  JSONB                    -- anonymised signal breakdown
);

-- Role and department baselines (Fabric IQ operational mirror)
CREATE TABLE role_baselines (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_type             VARCHAR(50) NOT NULL,   -- e.g., SENIOR_ENGINEER
    department            VARCHAR(50) NOT NULL,   -- e.g., DEPT-ENG
    expected_meeting_hrs  DECIMAL(4,1) NOT NULL,
    focus_time_min_hrs    DECIMAL(4,1) NOT NULL,
    overload_threshold    DECIMAL(4,1) NOT NULL,
    context_notes         TEXT
);

-- Manager intervention audit log
CREATE TABLE intervention_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    manager_id      VARCHAR(20) NOT NULL,
    action_type     VARCHAR(50) NOT NULL,   -- CHECKIN_SCHEDULED, HR_ESCALATED, etc.
    risk_tier       VARCHAR(10),
    context_summary TEXT,                   -- anonymised, no raw signals
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Employee opt-in preferences
CREATE TABLE employee_preferences (
    member_id           VARCHAR(20) PRIMARY KEY,
    opted_in            BOOLEAN NOT NULL DEFAULT FALSE,
    opted_in_at         TIMESTAMP,
    alert_threshold     VARCHAR(10) DEFAULT 'MODERATE',
    notification_pref   VARCHAR(20) DEFAULT 'AGENT_ONLY'
);
```

### Relationships

```
role_baselines ──────────────────► scoring_service.py
                                    (contextualises raw signals)

pre_computed_scores ─────────────► get_team_signals() MCP tool
                                    (SELECT query, <50ms)

employee_preferences ────────────► Azure Functions nightly worker
                                    (filters opted-in users only)

intervention_log ────────────────► get_audit_trail() MCP tool
                                    (manager accountability)
```

---

## 🤖 AI & IQ Workflow

### Work IQ — Signal Collection

```
Microsoft Graph API (OAuth 2.0)
        │
        ├── /me/calendarView?startDateTime=...&endDateTime=...
        │   → Extract: total meeting hours, back-to-back ratio,
        │     earliest/latest meeting times
        │
        ├── /me/mailFolders/inbox/messages?$select=receivedDateTime,sentDateTime
        │   → Extract: after-hours send timestamps (metadata only, never body)
        │
        └── /users/{id}/presence
            → Extract: availability status, activity patterns
```

### Privacy Aggregation Pipeline

```python
def aggregate_signals(raw_signals: RawSignals, role_baseline: RoleBaseline) -> BurnoutScore:
    """
    Raw Graph data → Anonymised risk score.
    No raw data persisted. No individual data surfaced to managers.
    """
    meeting_score    = score_meeting_load(raw_signals.meeting_hrs, role_baseline.expected_hrs)
    focus_score      = score_focus_erosion(raw_signals.focus_blocks, role_baseline.focus_min)
    afterhours_score = score_after_hours(raw_signals.late_sends)
    weekend_score    = score_weekend_activity(raw_signals.weekend_messages)
    
    composite = weighted_average([
        (meeting_score,    0.35),
        (focus_score,      0.30),
        (afterhours_score, 0.20),
        (weekend_score,    0.15)
    ])
    
    return BurnoutScore(
        score=composite,
        risk_tier=classify_tier(composite),
        signal_summary=anonymise(raw_signals)   # stored, not raw
    )
```

### Foundry IQ — Knowledge Retrieval

```
Manager query context + risk tier + role type
        │
        ▼
Foundry IQ Knowledge Base Query
(semantic search over uploaded HR policy documents)
        │
        ▼
Ranked document chunks with relevance scores
        │
        ▼
Citation-attached recommendations
("Per Manager's Handbook §4.2...")
        │
        ▼
Agent response grounded in company policy
(not general LLM knowledge)
```

### Fabric IQ — Semantic Org Reasoning

Used for organisation-level pattern queries that require traversing business relationships:

```
Query: "Which departments are structurally at risk this quarter?"

Fabric IQ Semantic Model traversal:
Role → Expected Workload → Actual Workload → Delta → Risk Classification
  +
Department → Team Composition → Aggregate Risk → Systemic Pattern
        │
        ▼
"Engineering Dept: 3/8 members above role-adjusted baseline for 3+ weeks.
 Pattern: Sprint cycles without recovery periods baked into project calendar."
```

---

## 🔐 Security Features

### Authentication & Authorization

| Layer | Implementation |
|---|---|
| User Authentication | Microsoft Entra ID (Azure AD) SSO |
| MCP Server Authorization | OAuth 2.0 Bearer token validation on every tool call |
| Token Introspection | Validated against Entra ID on every request, not cached |
| Scope Enforcement | Minimum required Graph API permissions, explicitly documented |

### Secrets Management

| Environment | Method |
|---|---|
| Local Development | `.env` file (gitignored, never committed) |
| Production | Azure Key Vault (all secrets externalized) |
| CI/CD Pipeline | GitHub Actions encrypted secrets |
| Container Runtime | Azure Container Apps environment variable injection from Key Vault |

### Data Privacy Architecture

- **Aggregation before persistence** — Raw Microsoft Graph signals are never written to the database. Only computed scores and anonymised signal summaries are stored.
- **No raw data in agent responses** — Managers never see individual raw metrics. Only risk tiers, trends, and synthesised insights are surfaced.
- **Employee consent model** — The employee-facing agent only activates for opted-in users. Opt-in is explicit, reversible, and logged.
- **Write action confirmation gates** — All write tools (calendar creation, HR logging, survey dispatch) require explicit manager confirmation before execution. No autonomous writes.

### Input Validation

- All MCP tool inputs validated via **Pydantic models** before processing
- Member ID format enforced (`EMP-\d{3}`) to prevent injection
- Time window parameters bounded (max 90-day lookback)
- All database queries use **parameterised statements** via SQLAlchemy (no raw SQL)

### Compliance

- **Zero PII in codebase** — All demo data uses synthetic identifiers (`EMP-001`, `DEPT-ENG`)
- **Audit trail** — Every manager action is immutably logged with timestamp and anonymised context
- **Data minimisation** — Only the Graph API scopes strictly necessary for scoring are requested

---

## 🧗 Challenges Faced

### 1. Microsoft Graph API Rate Limiting in Real-Time Queries
**Challenge:** Querying the Graph API synchronously during a Copilot Chat session caused intermittent throttling and 3–8 second response delays — unacceptable for a conversational agent.

**Solution:** Implemented an Azure Functions Timer Trigger that runs nightly at 11PM, pre-computes all risk scores, and stores them in PostgreSQL. Chat-time queries become simple `SELECT` statements returning in <50ms. Because Azure Functions is completely decoupled from the MCP server container, a redeployment or container restart never affects the scheduling pipeline.

---

### 2. The Anonymisation Paradox
**Challenge:** Surfacing enough information for managers to take action while protecting individual employee privacy — especially since any signal specific enough to act on is also specific enough to identify the person.

**Solution:** Implemented the Dual-Agent model. The Manager Agent works exclusively with aggregated team-level signals and systemic recommendations. Individual-level detail is only accessible to the employee themselves through the Employee Agent (after explicit opt-in).

---

### 3. Grounding Recommendations Without Hallucination Risk
**Challenge:** Burnout intervention advice generated from a general LLM could contradict company HR policy, local labour law, or EAP guidelines — creating a liability risk that would prevent real enterprise adoption.

**Solution:** All recommendations are retrieval-augmented via Foundry IQ, grounded strictly in uploaded company policy documents. The agent cites the specific document, section, and page for every intervention step. When retrieval confidence is below threshold, the agent explicitly discloses uncertainty rather than fabricating an answer.

---

### 4. OAuth Token Management Across Two Agent Surfaces
**Challenge:** The Manager Agent and Employee Agent have different permission scopes. A manager should not be able to call employee-scoped tools, and vice versa.

**Solution:** Implemented role-based MCP tool access enforced at the server level. OAuth token claims are inspected on every tool call to validate the caller's role. Manager tokens cannot invoke employee-scoped tools regardless of how the request is constructed.

---

## 🔭 Future Improvements

| Feature | Description | Priority |
|---|---|---|
| **Real-Time Signal Mode** | Optional live Graph API queries for critical-risk escalations (bypassing the nightly cache for urgent cases) | High |
| **Longitudinal Trend Analysis** | 12-week rolling burnout history with seasonal adjustment (e.g., normalise for annual planning cycles) | High |
| **Team Calendar Intelligence** | Agent proactively suggests and schedules "No-Meeting Fridays" or focus blocks at team level | Medium |
| **Cross-Team Benchmarking** | Anonymous cross-department risk comparison: *"Engineering is at 2x the company average meeting load"* | Medium |
| **Manager Effectiveness Scoring** | Track whether manager interventions reduce risk scores over 4–6 weeks | Medium |
| **Slack / Google Workspace** | Extend signal collection to non-M365 workplaces | Low |
| **Mobile Copilot App** | Ensure full agent functionality in the M365 Copilot mobile app | Low |
| **HRIS Direct Integration** | Live integration with Workday/SAP SuccessFactors for leave balance and role data | Low |

---

*Built for the [Agents League Hackathon](https://aka.ms/agentsleague/discord) — Microsoft Enterprise Agent Track, June 2026.*

---

## 📄 License

```
MIT License

Copyright (c) 2026 LumenHR Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgements

- **Microsoft Agents League Hackathon** — for the challenge framework and track definition
- **Microsoft Graph API** — the foundational data source that makes Work IQ possible
- **Azure AI Foundry** — for the knowledge retrieval and citation infrastructure
- **Microsoft Fabric** — for the semantic modelling capabilities
- **FastAPI** — for the clean, performant Python API framework
- **Azure Functions** — for the serverless Timer Trigger that powers the nightly async signal pipeline
- **SQLAlchemy & Alembic** — for database ORM and migration management
- **The Microsoft Viva Insights team** — whose privacy-first design principles informed LumenHR's anonymisation architecture
- **M365 Agents Toolkit** — for making Declarative Agent development approachable

---

<div align="center">

**Built with ❤️ for the Agents League Hackathon 2026**

[🏆 View Submission](https://aka.ms/agentsleague/discord) · [📽️ Watch Demo](#) · [🐛 Report Bug](issues) · [💡 Request Feature](issues)

</div>
