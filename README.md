# AgriChain

A multi agent AI system that helps Nigerian smallholder farmers decide what to plant, when to plant, what to spray, when to sell, and where to get financing. The farmer answers a few questions about their location and crop, and five specialized agents dispatch in parallel to research soil conditions, weather forecasts, market prices, available finance, and pest risks. Their findings are synthesized into a single weekly plan delivered in the farmer's preferred Nigerian language (Hausa, Yoruba, Igbo, or English) and sent to their WhatsApp.

**Submission:** DSN x BCT LLM Agent Challenge 3.0, Task B (Recommendation)

- **Live deployment:** https://gilded-salmiakki-9cfe3e.netlify.app
- **Backend API:** https://agri-chain-production.up.railway.app

---

## The Problem

Nigeria has over 36 million smallholder farmers. Most of them lose nearly 40 percent of their harvest each season to bad timing, wrong inputs, pest outbreaks, or selling at the lowest market price. The information that would prevent these losses exists. It just lives in places farmers cannot reach: government meteorology databases, agricultural research portals, commodity exchanges, and bank loan registries.

AgriChain bridges that gap. It takes a few simple inputs from the farmer and replies with a clear, personalized action plan in a language they actually speak.

---

## How It Works

The system uses an orchestrator with five specialized agents working in parallel. Each agent owns one domain, calls live external data sources, and returns structured output with a confidence level.

```
Farmer Input (web form or WhatsApp)
                              ↓
                     ┌─────────────────┐
                     │   Orchestrator  │
                     └────────┬────────┘
                              ↓
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    ↓          ↓          ↓          ↓          ↓
┌───────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Soil  │ │Weather │ │ Market │ │Finance │ │  Pest  │
│ Agent │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │
└───┬───┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    └──────────┴──────────┴──────────┴──────────┘
                              ↓
                   ┌─────────────────────┐
                   │  LLM Synthesis      │
                   │  (one clean plan)   │
                   └──────────┬──────────┘
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
          Web Result                   WhatsApp Delivery
```

### The Five Agents and Their Data Sources

| Agent | What It Does | External APIs / Data |
|---|---|---|
| Soil and Crop | Determines soil type, pH, nutrient profile, and crop suitability score | **iSDA Africa Soil API** (`api.isda-africa.com`, `api.isdasoil.org`), Nigerian state-crop matching tables |
| Weather | Produces a 7 day forecast, flags flood and drought risk, recommends planting day | **NASA POWER** (`power.larc.nasa.gov`) for historical climatology, **Open-Meteo** (`api.open-meteo.com`) for short-range forecast |
| Market Price | Returns current crop price, best regional markets, and price trends | **WFP HungerMap** (`api.hungermapdata.org`) Nigeria market prices, optional **Brave Search API** for live commodity news |
| Finance | Matches the farmer with eligible loan programmes and explains next steps | Curated registry: Bank of Agriculture, NIRSAL, CBN Anchor Borrowers, cooperatives |
| Pest and Disease | Scans for crop specific pest threats based on weather and season, recommends action | Agricultural research datasets, weather-conditioned pest rule base |

**Geocoding** of farmer-supplied LGA / state is done via **Open-Meteo Geocoding** and **OpenStreetMap Nominatim** (`nominatim.openstreetmap.org`).

**Synthesis** is performed by an LLM. The Python `agrichain/ai/` agent stack uses the **OpenAI API** (`OPENAI_API_KEY`). The Node.js backend tries an internal ML service first (`ML_SERVICE_URL`) and falls back to the **Anthropic Claude API** if the ML service is unavailable.

**Delivery** uses the **Meta WhatsApp Cloud API** (`graph.facebook.com/v18.0`) for both outbound plans and inbound multi-turn conversation, with **Africa's Talking** (`api.africastalking.com`) available as an SMS fallback.

Each agent returns a confidence label (high, medium, low) so the synthesized plan is transparent about which recommendations rest on solid data versus reasoned estimation.

---

## Why This Fits Task B

The brief asks for a recommendation agent that goes beyond collaborative filtering, handles cold start and cross domain scenarios, supports multi turn conversation, and reasons before recommending. AgriChain satisfies each:

| Requirement | How AgriChain Meets It |
|---|---|
| Personalized recommendations | Tailored to crop, location, soil, scale, and language |
| Beyond collaborative filtering | Uses live external data plus agent reasoning, not historical user behavior |
| Cold start | No prior user history needed. A new farmer gets useful output on first contact |
| Cross domain | Five domains: agronomy, meteorology, commerce, finance, biosecurity |
| Multi turn conversational | WhatsApp inbound webhook lets farmers ask follow up questions ("what if rain comes late?") |
| Agentic workflows that reason before recommending | Orchestrator dispatches specialized agents and synthesizes their findings |
| Nigerian context bonus | Built end to end for Nigerian smallholders in their own languages |

---

## Tech Stack

**Frontend:** React 18, Vite, Tailwind CSS, Motion (Framer Motion successor), React Router, Lucide React. Deployed on Netlify.

**Backend (Node.js):** Express, `@anthropic-ai/sdk` (Claude fallback synthesis), Axios, individual agent modules with live API integrations. Deployed on Railway.

**AI prototype (Python):** `agrichain/ai/` — OpenAI Python SDK, httpx, async orchestration, Brave Search, NASA POWER, iSDA, Open-Meteo, Nominatim.

**Messaging:** Meta WhatsApp Cloud API for both outbound delivery and inbound multi turn conversation; Africa's Talking for SMS fallback.

---

## External Data Sources at a Glance

| Source | Used For | Endpoint |
|---|---|---|
| NASA POWER | Long-range climate / agroclimatology | `power.larc.nasa.gov/api/temporal/daily/point` |
| Open-Meteo | Short-range weather forecast | `api.open-meteo.com/v1/forecast` |
| Open-Meteo Geocoding | Place → lat/lon | `geocoding-api.open-meteo.com/v1/search` |
| OpenStreetMap Nominatim | Geocoding fallback | `nominatim.openstreetmap.org/search` |
| iSDA Africa | Soil pH, nutrients, texture | `api.isda-africa.com/v1/soilproperty`, `api.isdasoil.org/v1/properties` |
| WFP HungerMap | Nigerian commodity / market prices | `api.hungermapdata.org/v2/foodsecurity/country/NGA/marketprices` |
| Brave Search | Live commodity / agronomy news lookup | `api.search.brave.com/res/v1/web/search` |
| Meta WhatsApp Cloud API | Plan delivery + inbound webhook | `graph.facebook.com/v18.0` |
| Africa's Talking | SMS fallback | `api.africastalking.com/version1/messaging` |
| OpenAI API | LLM synthesis (Python agents) | `api.openai.com` |
| Anthropic Claude API | LLM synthesis fallback (Node backend) | `api.anthropic.com` |

---

## Running It Locally

### Prerequisites

Node.js 18+ and npm for the backend and frontend. Python 3.10+ for the `agrichain/ai/` prototype. An OpenAI API key for the Python agents; the Node backend will use Claude as a fallback synthesizer if `CLAUDE_API_KEY` is set, otherwise it returns a deterministic template plan.

### Backend Setup (Node.js)

```bash
cd backend
npm install

cat > .env <<'EOF'
CLAUDE_API_KEY=optional_anthropic_key_for_fallback
ML_SERVICE_URL=https://your-ml-service.example.com
WHATSAPP_TOKEN=your_meta_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_meta_phone_number_id
WHATSAPP_VERIFY_TOKEN=any_string_you_choose
ISDA_API_KEY=optional_isda_soil_key
AT_API_KEY=optional_africas_talking_key
AT_USERNAME=optional_africas_talking_username
FRONTEND_URL=http://localhost:5173
PORT=8000
EOF

npm start
```

Open-Meteo, NASA POWER, WFP HungerMap, and OpenStreetMap Nominatim require no keys.

### Frontend Setup

```bash
cd frontend
npm install

echo "VITE_API_URL=http://localhost:8000" > .env

npm run dev
```

The frontend will start on `http://localhost:5173`.

### Python AI Prototype Setup

```bash
cd agrichain/ai
pip install -r requirements.txt

cat > .env <<'EOF'
OPENAI_API_KEY=sk-your-openai-key
BRAVE_API_KEY=optional_brave_search_key
RESEND_API_KEY=optional_resend_email_key
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEMO_MODE=True
EOF

python main.py
```

---

## API Reference

### POST /api/farm-plan

Main orchestrator endpoint. Dispatches all five agents in parallel, then synthesizes a plan.

**Request:**
```json
{
  "name": "Amina",
  "crop": "rice",
  "state": "Kebbi",
  "lga": "Birnin Kebbi",
  "farmSize": 2,
  "language": "english",
  "phoneNumber": "+2348012345678"
}
```

**Response:**
```json
{
  "requestId": "abc123",
  "status": "success",
  "coords": { "lat": 12.45, "lon": 4.20 },
  "agentResults": {
    "soil":    { "data": { "ph": 6.2, "nitrogen": "medium-high", "texture": "loamy", "suitability": 94 }, "confidence": "high" },
    "weather": { "data": { "avgTemp": 27.4, "bestPlantingDay": "Wednesday", "floodRisk": "low" }, "confidence": "high" },
    "market":  { "data": { "price": 42000, "unit": "50kg bag", "bestMarkets": ["Kano", "Birnin Kebbi"] }, "confidence": "high" },
    "finance": { "data": { "programmes": [{ "name": "Bank of Agriculture Smallholder Loan", "maxAmount": 500000 }] }, "confidence": "high" },
    "pest":    { "data": { "alerts": [{ "name": "Blast Disease", "risk": "high", "action": "Apply tricyclazole before Wednesday's rain" }] }, "confidence": "high" }
  },
  "farmPlan": {
    "weeklyActions": "Plant rice on Wednesday...",
    "weatherSummary": "...",
    "marketAdvice": "...",
    "financeOptions": "...",
    "pestAlert": "...",
    "language": "english"
  },
  "whatsappSent": true
}
```

If `phoneNumber` is provided in the request, the synthesized plan is also sent to that number via WhatsApp.

### POST /webhook/whatsapp

Inbound WhatsApp webhook. Receives messages from farmers, maintains conversation state, and replies in their preferred language. Enables multi turn recommendation.

### GET /health

Returns `{ "status": "healthy" }` if the server is reachable.

---

## Reproducing the Demo

1. Open the live deployment at https://gilded-salmiakki-9cfe3e.netlify.app
2. Either fill out the 5 step form, or click one of the three sample farmer profiles (Chukwuemeka, Adaeze, or Bashir) for instant results
3. Wait roughly 30 seconds for the agents to complete and the LLM to synthesize the plan
4. Click any agent card to see the underlying data and confidence level
5. Click "Send to WhatsApp" to deliver the plan to a Nigerian number

---

## Repository Layout

```
agri-chain/
├── backend/         Node.js + Express API, orchestrator, and the five agents
│   ├── agents/      soilAgent, weatherAgent, marketAgent, financeAgent, pestAgent
│   ├── orchestrator/  parallel dispatch + LLM synthesis
│   ├── routes/      /api/farm-plan and /webhook/whatsapp
│   └── server.js    Express entry point
├── frontend/        React 18 + Vite + Tailwind web app (Netlify)
├── agrichain/ai/    Python multi-agent prototype (OpenAI, NASA POWER, iSDA, Brave)
└── README.md
```

---

## License

This codebase is submitted for the DSN x BCT LLM Agent Challenge 3.0 and is intended for evaluation by the organizing judges. All third party APIs (OpenAI, Anthropic, Meta WhatsApp, Africa's Talking, NASA POWER, Open-Meteo, iSDA Africa, WFP HungerMap, Brave Search, OpenStreetMap Nominatim) are used under their respective terms.
