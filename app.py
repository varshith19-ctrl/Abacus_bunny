# app.py
import streamlit as st
import detect_spike         # The Math
import agent_explain           # The AI
import cleanup    # The Zombie Hunter

# --- PAGE SETUP ---
st.set_page_config(page_title="FinOps Guardian", page_icon="💰")
st.title("💰 Autonomous FinOps Guardian")
st.write("Detect cloud cost spikes and get AI-powered explanations.")

# --- SIDEBAR ---
st.sidebar.header("Control Panel")
days_to_simulate = st.sidebar.slider("Days to Simulate", 10, 60, 30)
spike_amount = st.sidebar.number_input("Spike Amount ($)", value=500)

if st.button("🚀 Run Full Analysis"):
    
    # --- PART 1: BILLING ANALYSIS ---
    st.subheader("1. Cloud Billing Data")
    
    # Call detect_spike to get data
    df = detect_spike.generate_billing_data(days_to_simulate, spike_amount)
    st.line_chart(df.set_index('date'))
    
    # --- PART 2: ANOMALY DETECTION ---
    st.subheader("2. Anomaly Detection (IQR Method)")
    
    # Call detect_spike to do the math
    spikes, threshold = detect_spike.detect_anomalies(df)
    
    if not spikes.empty:
        st.error(f"⚠️ Alert! Found {len(spikes)} cost spike(s).")
        st.dataframe(spikes)
        
        # --- PART 3: AI EXPLANATION ---
        st.subheader("3. AI Root Cause Analysis")
        
        mock_logs = """
        [LOG 14:00] Auto-scaling group triggered by CPU > 80%.
        [LOG 14:05] Scale out: Increased from 2 to 50 instances.
        [LOG 14:10] Error: Infinite loop detected in 'video-transcode' job.
        """
        
        with st.spinner("Asking Gemini AI to analyze logs..."):
            # Call agent_explain to talk to Google
            ai_response = agent_explain.get_gemini_response(spikes.iloc[-1], mock_logs)
            st.markdown(ai_response)
    else:
        st.success("✅ No anomalies detected. Costs are within normal range.")

    st.markdown("---")

    # --- PART 4: RESOURCE HYGIENE ---
    st.subheader("4. Resource Hygiene Check (Zombie Hunter)")
    
    # Call cleanup to find zombies
    inventory_df, zombie_ids = cleanup.get_zombie_resources()
    
    st.caption("Scanning Active Cloud Inventory...")
    st.dataframe(inventory_df)
    
    if zombie_ids:
        st.error(f"⚠️ Waste Detected! Found {len(zombie_ids)} zombie instance(s).")
        st.write(f"**Action Plan:** Stop the following instances immediately:")
        st.code(f"IDS: {zombie_ids}", language="json")
    else:
        st.success("✅ Resource Hygiene is Good. No idle zombies found.")
    st.subheader("5. Smart Right-Sizing Engine")
    
    # Call the new function
    optimizations_df = cleanup.get_optimization_recommendations()
    
    if not optimizations_df.empty:
        st.info("💡 Efficiency Opportunities Found!")
        st.dataframe(optimizations_df)
    else:
        st.success("All workloads are optimized.")    

else:
    st.info("Click 'Run Full Analysis' to scan your cloud.")

# ... inside app.py ...
    
   
