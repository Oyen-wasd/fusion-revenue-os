from utils.gemini_client import generate_json

def diagnose(row: dict) -> dict:
    ctr = float(row.get('CTR', 0))
    cpm = float(row.get('CPM', 0))
    click_to_atc = float(row.get('Click_to_ATC', 0))
    atc_to_purchase = float(row.get('ATC_to_Purchase', 0))

    # Pre‑compute initial break
    if ctr < 1.0 and cpm > 20:
        funnel_break = "Hook/Thumbstop Failure"
        break_detail = f"CTR {ctr}% with CPM RM{cpm:.2f} – ad isn't stopping scroll."
    elif click_to_atc < 0.15:
        funnel_break = "Landing Page/Product Page Failure"
        break_detail = f"Click→ATC {click_to_atc:.1%} – message-to-page mismatch."
    elif atc_to_purchase < 0.20:
        funnel_break = "Checkout/Offer Failure"
        break_detail = f"ATC→Purchase {atc_to_purchase:.1%} – price/trust/urgency missing."
    else:
        funnel_break = "Healthy Funnel"
        break_detail = "All stages within acceptable range."

    prompt = f"""
You are a world-class performance marketing diagnostician. Identify root causes with surgical precision.

Campaign: {row.get('campaign_name')}
Platform: {row.get('platform')}
Brand: {row.get('brand')}
Spend: RM{row.get('spend_rm')}
CTR: {ctr}%
CPM: RM{cpm}
Click-to-ATC: {click_to_atc}
ATC-to-Purchase: {atc_to_purchase}
ROAS: {row.get('ROAS')}x
Revenue: RM{row.get('revenue_rm')}
Pre‑computed funnel break: {funnel_break}
Pre‑computed detail: {break_detail}

Your task:
1. Confirm or challenge the funnel break diagnosis. Explain why if you disagree.
2. Write ONE specific, actionable fix (e.g., "The first 2 seconds show the bottle. Reshoot with a before‑after in frame one. Reference: Farah's 17.16x session opens with texture demonstration.")
3. Assign a confidence score (1-10).
4. Give a "Test This First" — the single highest‑leverage change.

Return JSON:
{{
  "diagnosis_confirmed": true/false,
  "revised_diagnosis": "",
  "specific_fix": "",
  "confidence": 5,
  "test_this_first": "",
  "reasoning": "2 sentences max"
}}
"""
    return generate_json(prompt)
