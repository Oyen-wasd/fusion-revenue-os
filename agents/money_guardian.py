def evaluate_campaign(campaign: dict, breakeven_roas=2.5, spend_ceiling=300):
    roas = float(campaign.get('ROAS', 0))
    spend = float(campaign.get('spend_rm', 0))
    if roas < breakeven_roas:
        return {"action": "⏸️ PAUSE", "reason": f"ROAS {roas:.1f}x below breakeven {breakeven_roas}x"}
    elif roas >= 8 and spend <= spend_ceiling:
        return {"action": "🚀 SCALE", "reason": f"ROAS {roas:.1f}x strong, budget RM{spend:.0f} under ceiling"}
    elif spend > spend_ceiling:
        return {"action": "⏸️ PAUSE (ceiling)", "reason": f"Spend RM{spend:.0f} exceeds ceiling RM{spend_ceiling}"}
    else:
        return {"action": "👀 MONITOR", "reason": "Within acceptable range"}
