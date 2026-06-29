from utils.gemini_client import generate_json

def create_briefing(df):
    total_spend = df['spend_rm'].sum()
    total_rev = df['revenue_rm'].sum()
    blended = total_rev / total_spend if total_spend > 0 else 0
    winners = df[df['ROAS'] >= 10].sort_values('ROAS', ascending=False)
    losers = df[df['ROAS'] < 2.5]

    top_winner = winners.iloc[0] if len(winners) > 0 else None
    top_loser = losers.iloc[0] if len(losers) > 0 else None

    # Gather actions from Money Guardian if you've stored them, but here we'll compute inline
    actions = []
    for _, row in df.iterrows():
        roas = float(row['ROAS'])
        if roas < 2.5:
            actions.append(f"STOP {row['campaign_name']}")
        elif roas >= 8:
            actions.append(f"SCALE {row['campaign_name']}")

    prompt = f"""
You are the CEO briefing agent. Summarise yesterday's performance in a concise WhatsApp‑style message with emojis.

Data:
Total spend: RM{total_spend:.0f}
Revenue: RM{total_rev:.0f}
Blended ROAS: {blended:.1f}x
Top campaign: {top_winner['campaign_name'] if top_winner is not None else 'None'} (ROAS {top_winner['ROAS']:.1f}x) 
Urgent: {len(losers)} campaigns below breakeven 2.5x
Recommended actions: {', '.join(actions[:4])}

Format exactly like this:
📊 *Fusion Daily Briefing*
Spend RM{total_spend:.0f} | Rev RM{total_rev:.0f} | ROAS {blended:.1f}x
🚨 {len(losers)} alerts • 🏆 {len(winners)} winners
👉 Key actions: [list 2-3 top moves]
End with "Reply STOP/SCALE to approve."
"""
    return generate_json(prompt)  # We'll just return the text; the JSON wrapper is okay.
