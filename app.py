import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Fusion Revenue OS | Campaign Doctor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 800; color: #1a1a2e; }
    .sub-header { font-size: 1.1rem; color: #4a4a6a; margin-bottom: 20px; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; }
    .alert-critical { background-color: #fee2e2; border-left: 5px solid #dc2626; padding: 15px; border-radius: 8px; }
    .alert-warning { background-color: #fef3c7; border-left: 5px solid #f59e0b; padding: 15px; border-radius: 8px; }
    .alert-success { background-color: #d1fae5; border-left: 5px solid #10b981; padding: 15px; border-radius: 8px; }
    .insight-box { background-color: #eff6ff; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 8px; margin: 10px 0; }
    .ceo-brief { background-color: #1a1a2e; color: #e0e0e0; padding: 25px; border-radius: 12px; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown('<p class="main-header">🩺 Campaign Doctor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Revenue Operating System v0.1 | Built for Fusion Cosmetics — 26 Brands, 800 POS, Zero Blind Spots</p>', unsafe_allow_html=True)
st.divider()

# ============================================
# SIDEBAR — CONTEXT
# ============================================
with st.sidebar:
    st.image("https://via.placeholder.com/150x60?text=FUSION+OS", use_container_width=True)
    st.markdown("### 🎯 System Status")
    st.success("Campaign Doctor: ONLINE")
    st.info("Live Session Analyst: ONLINE")
    st.warning("CEO Briefing: AUTO-GENERATED")
    st.divider()
    st.markdown("### 📊 Diagnostic Thresholds")
    breakeven_roas = st.slider("Breakeven ROAS", 1.0, 5.0, 2.5, 0.1)
    scale_threshold = st.slider("Scale Threshold ROAS", 3.0, 20.0, 8.0, 0.5)
    st.divider()
    st.markdown("**Built by:** AD Satiman")
    st.markdown("**Stack:** Python + Streamlit + Plotly")
    st.markdown("**Tier:** Cloud-Native | Zero Infrastructure Cost")

# ============================================
# TAB 1: CAMPAIGN DIAGNOSTIC
# ============================================
tab1, tab2, tab3 = st.tabs(["📊 Campaign Doctor", "📹 Live Session Analyst", "📱 CEO Briefing"])

with tab1:
    st.header("Upload Campaign Performance Data")
    
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        uploaded_file = st.file_uploader(
            "Drop your campaign CSV here (or use sample data)",
            type=['csv'],
            help="Expected columns: campaign_name, brand, platform, funnel_stage, spend_rm, revenue_rm, impressions, clicks, add_to_cart, orders"
        )
    with col_u2:
        use_sample = st.checkbox("📁 Use Sample Data (Celimax + Mustela)", value=True if uploaded_file is None else False)
    
    # Load data
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} campaigns from your file")
    elif use_sample:
        try:
            df = pd.read_csv("data/sample_campaigns.csv")
            st.info("📁 Using sample data: Celimax TT, Mustela Google, NL Alchemist, Phyto, Embryolisse")
        except:
            st.error("Sample data not found. Please upload a CSV.")
            st.stop()
    else:
        st.warning("Please upload a CSV or check 'Use Sample Data'")
        st.stop()
    
    # Validate columns
    required_cols = ['campaign_name', 'brand', 'platform', 'funnel_stage', 'spend_rm', 'revenue_rm', 
                     'impressions', 'clicks', 'add_to_cart', 'orders']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"❌ Missing columns: {missing}. Your CSV must have: {required_cols}")
        st.stop()
    
    # Calculate core metrics
    df['ROAS'] = df['revenue_rm'] / df['spend_rm'].replace(0, np.nan)
    df['CPM'] = (df['spend_rm'] / df['impressions'].replace(0, np.nan)) * 1000
    df['CTR'] = (df['clicks'] / df['impressions'].replace(0, np.nan)) * 100
    df['CVR'] = (df['orders'] / df['clicks'].replace(0, np.nan)) * 100
    df['CPA'] = df['spend_rm'] / df['orders'].replace(0, np.nan)
    df['Cost_per_ATC'] = df['spend_rm'] / df['add_to_cart'].replace(0, np.nan)
    df['Net_Contribution'] = df['revenue_rm'] - (df['spend_rm'] * breakeven_roas)
    
    # ========================================
    # DIAGNOSTIC ENGINE
    # ========================================
    def generate_diagnosis(row):
        diagnoses = []
        actions = []
        severity = "normal"
        
        # ROAS Analysis
        if pd.isna(row['ROAS']):
            diagnoses.append("⚠️ **NO DATA:** Cannot calculate ROAS — check spend/revenue values")
            actions.append("🔍 Verify data integrity for this campaign")
            severity = "warning"
        elif row['ROAS'] < 1.0:
            diagnoses.append(f"🚨 **HEMORRHAGE:** ROAS {row['ROAS']:.2f}x. Losing RM {row['spend_rm'] - row['revenue_rm']:.2f} on every ringgit spent.")
            actions.append(f"⏸️ **KILL IMMEDIATELY:** Pause campaign. Reallocate RM {row['spend_rm']:.0f} to proven performers.")
            severity = "critical"
        elif row['ROAS'] < breakeven_roas:
            diagnoses.append(f"🩸 **BLEEDING:** ROAS {row['ROAS']:.2f}x is below {breakeven_roas}x breakeven. Net loss: RM {abs(row['Net_Contribution']):.2f}")
            actions.append("⏸️ **PAUSE:** Stop spend. Audit creative, audience, and landing page before relaunch.")
            severity = "critical"
        elif row['ROAS'] >= scale_threshold:
            diagnoses.append(f"🏆 **GOLDMINE:** ROAS {row['ROAS']:.2f}x is exceptional. Net profit: RM {row['Net_Contribution']:.2f}")
            actions.append(f"🚀 **SCALE:** Increase budget 30-50%. Test lookalike audiences. Book streamer immediately if live campaign.")
            severity = "success"
        else:
            diagnoses.append(f"⚠️ **MARGINAL:** ROAS {row['ROAS']:.2f}x is above breakeven but not exceptional.")
            actions.append("🔬 **TEST:** A/B test hook, audience, or offer before scaling.")
        
        # Funnel-Stage Specific Analysis
        stage = str(row['funnel_stage']).strip()
        
        if stage == "Awareness":
            if not pd.isna(row['CPM']) and row['CPM'] > 50:
                diagnoses.append(f"💸 **REACH TAX:** CPM RM {row['CPM']:.2f} is expensive for cold reach. Algorithm is fighting for narrow audience.")
                actions.append("🎯 **BROADEN:** Expand targeting. Test broader interests. PMax needs volume, not precision.")
            if not pd.isna(row['CTR']) and row['CTR'] < 1:
                diagnoses.append(f"👎 **HOOK FAILURE:** CTR {row['CTR']:.2f}% on awareness campaign. Creative assumes product knowledge audience doesn't have.")
                actions.append("📝 **EDUCATE:** Lead with problem, not product. 'Struggling with baby rash?' not 'Mustela is great.'")
                
        elif stage == "Conversion":
            if not pd.isna(row['CVR']) and row['CVR'] < 1:
                diagnoses.append(f"🛒 **CHECKOUT LEAK:** CVR {row['CVR']:.2f}% is critically low. High intent traffic not converting.")
                actions.append("🔧 **AUDIT:** Price vs competitor? Shipping cost shock? Payment friction? Review landing page heatmap.")
            if not pd.isna(row['Cost_per_ATC']) and row['Cost_per_ATC'] > row['CPA'] * 0.8:
                diagnoses.append(f"🧺 **CART ABANDON:** Cost per ATC (RM {row['Cost_per_ATC']:.2f}) is close to CPA (RM {row['CPA']:.2f}). People add but don't buy.")
                actions.append("💰 **RETARGET:** Launch abandoned cart sequence within 1 hour. Offer 10% urgency discount.")
        
        # Platform-specific
        platform = str(row['platform']).strip()
        if platform == "Google Ads" and not pd.isna(row['ROAS']) and row['ROAS'] < breakeven_roas:
            diagnoses.append("🔍 **PMAX TRAP:** Google's algorithm optimizes for its own goals, not yours. It may be spending on 'similar audiences' outside your ICP.")
            actions.append("🎛️ **SEGMENT:** Split PMax into Standard Shopping + Display Remarketing. Control budget allocation manually.")
        
        if platform == "TikTok Shop" and not pd.isna(row['ROAS']) and row['ROAS'] > 10:
            streamer = row.get('streamer_name', '')
            if pd.notna(streamer) and streamer != '':
                diagnoses.append(f"🎥 **STREAMER ALPHA:** {streamer} is a proven converter. This is not luck — this is repeatable.")
                actions.append(f"📅 **LOCK IN:** Book {streamer} for 5 slots next month. Test same time slot (currently {row.get('slot_time', 'unknown')}).")
        
        return "  \n".join(diagnoses), "  \n".join(actions), severity
    
    df['Diagnosis'], df['Actions'], df['Severity'] = zip(*df.apply(generate_diagnosis, axis=1))
    
    # ========================================
    # EXECUTIVE SUMMARY CARDS
    # ========================================
    st.subheader("📈 Portfolio Snapshot")
    c1, c2, c3, c4, c5 = st.columns(5)
    
    total_spend = df['spend_rm'].sum()
    total_rev = df['revenue_rm'].sum()
    blended_roas = total_rev / total_spend if total_spend > 0 else 0
    critical_count = len(df[df['Severity'] == 'critical'])
    goldmine_count = len(df[df['Severity'] == 'success'])
    
    with c1:
        st.metric("Total Spend", f"RM {total_spend:,.0f}")
    with c2:
        st.metric("Total Revenue", f"RM {total_rev:,.0f}")
    with c3:
        st.metric("Blended ROAS", f"{blended_roas:.2f}x")
    with c4:
        st.metric("🚨 Bleeding", f"{critical_count} campaigns", delta="- Stop Now")
    with c5:
        st.metric("🏆 Goldmines", f"{goldmine_count} campaigns", delta="Scale Now")
    
    st.divider()
    
    # ========================================
    # INDIVIDUAL CAMPAIGN DIAGNOSTICS
    # ========================================
    st.subheader("🔬 Individual Campaign Diagnostics")
    
    for idx, row in df.iterrows():
        severity_class = {
            "critical": "alert-critical",
            "warning": "alert-warning", 
            "success": "alert-success",
            "normal": "insight-box"
        }.get(row['Severity'], "insight-box")
        
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 3])
            
            with col1:
                st.markdown(f"**{row['campaign_name']}**")
                st.caption(f"Brand: {row['brand']} | Platform: {row['platform']}")
                st.caption(f"Funnel: {row['funnel_stage']}")
                if pd.notna(row.get('streamer_name')) and row['streamer_name']:
                    st.caption(f"🎤 Streamer: {row['streamer_name']} | Slot: {row.get('slot_time', 'N/A')}")
                
                st.metric("ROAS", f"{row['ROAS']:.2f}x" if not pd.isna(row['ROAS']) else "N/A")
                st.metric("Spend", f"RM {row['spend_rm']:,.0f}")
                st.metric("Rev", f"RM {row['revenue_rm']:,.0f}")
            
            with col2:
                st.markdown(f'<div class="{severity_class}">', unsafe_allow_html=True)
                st.markdown("**🏥 Diagnosis:**")
                st.markdown(row['Diagnosis'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**🎯 Prescribed Actions:**")
                st.markdown(row['Actions'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
    
    # ========================================
    # BRAND PORTFOLIO ANALYSIS
    # ========================================
    if len(df['brand'].unique()) > 1:
        st.subheader("🏢 Brand Portfolio Intelligence")
        st.caption("Are your brands eating each other's lunch?")
        
        brand_perf = df.groupby('brand').agg({
            'spend_rm': 'sum',
            'revenue_rm': 'sum',
            'orders': 'sum'
        }).reset_index()
        brand_perf['ROAS'] = brand_perf['revenue_rm'] / brand_perf['spend_rm']
        brand_perf['Net_Profit'] = brand_perf['revenue_rm'] - (brand_perf['spend_rm'] * breakeven_roas)
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            fig = px.bar(brand_perf, x='brand', y='ROAS', color='ROAS',
                        color_continuous_scale=['red', 'yellow', 'green'],
                        title="ROAS by Brand")
            fig.add_hline(y=breakeven_roas, line_dash="dash", line_color="red", 
                         annotation_text=f"Breakeven ({breakeven_roas}x)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b2:
            fig2 = px.bar(brand_perf, x='brand', y='Net_Profit', 
                         color='Net_Profit',
                         color_continuous_scale=['red', 'green'],
                         title=f"Net Contribution (after {breakeven_roas}x ROAS cost)")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Cannibalization warning
        worst_brand = brand_perf.loc[brand_perf['ROAS'].idxmin()]
        if worst_brand['ROAS'] < breakeven_roas:
            st.error(f"⚠️ **CANNIBALIZATION RISK:** {worst_brand['brand']} is losing RM {abs(worst_brand['Net_Profit']):,.0f}. "
                    f"Check if it's targeting same audiences as your winners on {df[df['brand']==worst_brand['brand']]['platform'].iloc[0]}.")
    
    # ========================================
    # CROSS-PLATFORM COMPARISON
    # ========================================
    if len(df['platform'].unique()) > 1:
        st.subheader("🌐 Platform Efficiency Matrix")
        platform_perf = df.groupby('platform').agg({
            'spend_rm': 'sum',
            'revenue_rm': 'sum',
            'clicks': 'sum',
            'orders': 'sum'
        }).reset_index()
        platform_perf['ROAS'] = platform_perf['revenue_rm'] / platform_perf['spend_rm']
        platform_perf['CVR'] = (platform_perf['orders'] / platform_perf['clicks']) * 100
        
        fig3 = px.scatter(platform_perf, x='spend_rm', y='ROAS', size='revenue_rm', 
                         color='platform', text='platform',
                         title="Platform Efficiency: Spend vs ROAS (bubble size = revenue)")
        fig3.add_hline(y=breakeven_roas, line_dash="dash", line_color="red")
        st.plotly_chart(fig3, use_container_width=True)

# ============================================
# TAB 2: LIVE SESSION ANALYST
# ============================================
with tab2:
    st.header("📹 Live Session Temporal Analysis")
    st.caption("When do viewers buy? When do they leave? Where should the offer land?")
    
    col_l1, col_l2 = st.columns([3, 1])
    with col_l1:
        live_file = st.file_uploader("Upload live session minute-by-minute CSV", type=['csv'])
    with col_l2:
        use_sample_live = st.checkbox("📁 Use Farah Sample Data", value=True if live_file is None else False)
    
    if live_file is not None:
        live_df = pd.read_csv(live_file)
    elif use_sample_live:
        try:
            live_df = pd.read_csv("data/sample_live_session.csv")
            st.info("📁 Using Farah's 60-minute live session sample data")
        except:
            st.error("Sample live data not found")
            st.stop()
    else:
        st.warning("Upload live session CSV or use sample")
        st.stop()
    
    # Validate
    live_required = ['minute', 'viewers', 'purchases', 'gmv_rm']
    live_missing = [c for c in live_required if c not in live_df.columns]
    if live_missing:
        st.error(f"Missing columns: {live_missing}. Need: {live_required}")
        st.stop()
    
    # Calculate derived metrics
    live_df['purchase_rate'] = (live_df['purchases'] / live_df['viewers'].replace(0, np.nan)) * 100
    live_df['viewer_drop'] = live_df['viewers'].diff()
    live_df['cumulative_gmv'] = live_df['gmv_rm'].cumsum()
    live_df['cumulative_purchases'] = live_df['purchases'].cumsum()
    
    # Find golden windows
    peak_purchase_minute = live_df.loc[live_df['purchases'].idxmax(), 'minute']
    peak_gmv_minute = live_df.loc[live_df['gmv_rm'].idxmax(), 'minute']
    
    # Find drop-off cliff (where viewers drop >20% from peak)
    peak_viewers = live_df['viewers'].max()
    cliff_threshold = peak_viewers * 0.8
    cliff_df = live_df[live_df['viewers'] < cliff_threshold]
    cliff_minute = cliff_df['minute'].iloc[0] if len(cliff_df) > 0 else live_df['minute'].max()
    
    # KPI Cards
    st.subheader("Session Vital Signs")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Peak Viewers", f"{peak_viewers:,.0f}")
    with k2:
        st.metric("Total GMV", f"RM {live_df['gmv_rm'].sum():,.0f}")
    with k3:
        st.metric("Total Orders", f"{live_df['purchases'].sum()}")
    with k4:
        st.metric("Avg Order Value", f"RM {live_df['gmv_rm'].sum()/live_df['purchases'].sum():.0f}" 
                 if live_df['purchases'].sum() > 0 else "N/A")
    
    # Charts
    st.subheader("Temporal Intelligence")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_live = go.Figure()
        fig_live.add_trace(go.Scatter(x=live_df['minute'], y=live_df['viewers'],
                                     mode='lines+markers', name='Viewers', line=dict(color='#6366f1')))
        fig_live.add_trace(go.Scatter(x=live_df['minute'], y=live_df['purchases']*100,
                                     mode='lines+markers', name='Purchases (x100)', 
                                     line=dict(color='#10b981'), yaxis='y2'))
        fig_live.add_vline(x=peak_purchase_minute, line_dash="dash", line_color="green",
                          annotation_text=f"Peak Purchase @ {peak_purchase_minute}min")
        fig_live.add_vline(x=cliff_minute, line_dash="dash", line_color="red",
                          annotation_text=f"Cliff @ {cliff_minute}min")
        fig_live.update_layout(
            title="Viewers vs Purchases Over Time",
            xaxis_title="Minute",
            yaxis_title="Viewers",
            yaxis2=dict(title="Purchases", overlaying='y', side='right'),
            hovermode='x unified'
        )
        st.plotly_chart(fig_live, use_container_width=True)
    
    with col_g2:
        fig_cum = px.area(live_df, x='minute', y='cumulative_gmv',
                         title="Cumulative GMV Curve",
                         color_discrete_sequence=['#8b5cf6'])
        fig_cum.add_vline(x=peak_gmv_minute, line_dash="dash", line_color="gold",
                         annotation_text=f"Peak GMV @ {peak_gmv_minute}min")
        st.plotly_chart(fig_cum, use_container_width=True)
    
    # Strategic recommendations
    st.subheader("🎯 Live Session Prescription")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="alert-success">', unsafe_allow_html=True)
        st.markdown("**🟢 GOLDEN WINDOW**")
        st.markdown(f"Peak purchases happen at **{peak_purchase_minute} minutes**. "
                   f"Front-load your strongest offer, social proof, and urgency at **{max(0, peak_purchase_minute-2)}-{peak_purchase_minute+2} minutes**.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_r2:
        st.markdown('<div class="alert-critical">', unsafe_allow_html=True)
        st.markdown("**🔴 CLIFF WARNING**")
        st.markdown(f"Viewer cliff starts at **{cliff_minute} minutes** "
                   f"(drop from {peak_viewers:,.0f} to {live_df[live_df['minute']==cliff_minute]['viewers'].iloc[0]:,.0f}). "
                   f"**Never place critical offers after {cliff_minute} minutes.**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("**🧠 Strategic Insight for Fusion:**")
    
    early_gmv = live_df[live_df['minute'] <= 15]['gmv_rm'].sum()
    late_gmv = live_df[live_df['minute'] > 15]['gmv_rm'].sum()
    early_ratio = early_gmv / (early_gmv + late_gmv) * 100 if (early_gmv + late_gmv) > 0 else 0
    
    st.markdown(f"""
    - **{early_ratio:.0f}%** of GMV is captured in the first 15 minutes
    - **Recommendation:** For Farah's slot ({df[df['streamer_name']=='Farah']['slot_time'].iloc[0] if 'Farah' in str(df.get('streamer_name', [])) else '1600-1800'}), 
      script the offer reveal at minute {peak_purchase_minute-2}, not minute 30.
    - **Test:** A/B 90-minute vs 60-minute slots. If cliff is at {cliff_minute}min, 
      the last {live_df['minute'].max() - cliff_minute} minutes are wasted capacity.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 3: CEO BRIEFING
# ============================================
with tab3:
    st.header("📱 Daily CEO Briefing")
    st.caption("Auto-generated every morning. One screen. Three actions. No dashboards.")
    
    if 'df' in locals() and len(df) > 0:
        # Generate briefing
        today_spend = df['spend_rm'].sum()
        today_rev = df['revenue_rm'].sum()
        today_roas = today_rev / today_spend if today_spend > 0 else 0
        today_profit = today_rev - (today_spend * breakeven_roas)
        
        bleeding = df[df['Severity'] == 'critical'].sort_values('Net_Contribution')
        goldmines = df[df['Severity'] == 'success'].sort_values('ROAS', ascending=False)
        
        st.markdown('<div class="ceo-brief">', unsafe_allow_html=True)
        st.markdown(f"""
        ```
        FUSION REVENUE OS — DAILY BRIEFING
        Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
        =======================================
        
        💰 FINANCIALS
        Spend Today:    RM {today_spend:>10,.0f}
        Revenue Today:  RM {today_rev:>10,.0f}
        Blended ROAS:   {today_roas:>10.2f}x
        Net Position:   RM {today_profit:>10,.0f} ({'PROFIT' if today_profit > 0 else 'LOSS'})
        
        🚨 IMMEDIATE ACTIONS REQUIRED
        """)
        
        if len(bleeding) > 0:
            for _, row in bleeding.head(3).iterrows():
                st.markdown(f"   [STOP] {row['campaign_name'][:30]:<30} | ROAS {row['ROAS']:.2f}x | Save RM {row['spend_rm']:,.0f}")
        else:
            st.markdown("   ✅ No critical alerts. Portfolio is healthy.")
        
        st.markdown("""
        
        🏆 SCALE OPPORTUNITIES
        """)
        
        if len(goldmines) > 0:
            for _, row in goldmines.head(3).iterrows():
                st.markdown(f"   [SCALE] {row['campaign_name'][:30]:<30} | ROAS {row['ROAS']:.2f}x | Add RM {row['spend_rm']*0.3:,.0f}")
        else:
            st.markdown("   ⚠️ No scale-ready campaigns. Review creative fatigue.")
        
        st.markdown(f"""
        
        📊 PORTFOLIO HEALTH
        Total Active:   {len(df)} campaigns
        Bleeding:       {len(bleeding)} campaigns
        Goldmines:      {len(goldmines)} campaigns
        Avg ROAS:       {df['ROAS'].mean():.2f}x
        
        🎯 TODAY'S TOP PRIORITY
        """)
        
        if len(bleeding) > 0:
            top_bleeder = bleeding.iloc[0]
            st.markdown(f"   Fix {top_bleeder['campaign_name']}. It's costing RM {abs(top_bleeder['Net_Contribution']):,.0f}/day.")
        else:
            st.markdown(f"   Scale {goldmines.iloc[0]['campaign_name'] if len(goldmines) > 0 else 'top performer'}. Capture the momentum.")
        
        st.markdown("""
        =======================================
        Reply STOP [ID] to pause campaign
        Reply SCALE [ID] to increase budget 30%
        ```
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # WhatsApp-style visualization
        st.subheader("💬 WhatsApp Business API Preview")
        st.caption("This is what the CEO receives at 7:00 AM daily")
        
        w1, w2 = st.columns([1, 3])
        with w1:
            st.image("https://via.placeholder.com/80x80?text=CEO", width=80)
        with w2:
            st.markdown(f"""
            **Fusion Revenue OS** · Today 7:00 AM
            
            📊 *Daily Briefing*
            
            Spend: RM {today_spend:,.0f} | Rev: RM {today_rev:,.0f} | ROAS: {today_roas:.2f}x
            
            {'🚨' if len(bleeding) > 0 else '✅'} {len(bleeding)} alert(s) · {len(goldmines)} opportunity(s)
            
            *Tap to view full report →*
            """)
    else:
        st.info("Upload campaign data in Tab 1 to generate CEO briefing")

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption("Fusion Revenue OS v0.1 | Built by AD Satiman | POC for Round 2 Interview | 6-Agent ROS Roadmap Available")
