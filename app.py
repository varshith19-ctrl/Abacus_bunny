# app.py
import streamlit as st
import detect_spike         # The Math
import agent_explain        # The AI
import cleanup              # The Zombie Hunter
import plotly.express as px # For the charts

# --- PAGE SETUP ---
st.set_page_config(page_title="FinOps Guardian", page_icon="💰", layout="wide")
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
    
    # Create columns for side-by-side view
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.line_chart(df.set_index('date'))
        
    with col2:
        # --- NEW: SERVICE BREAKDOWN ---
        with st.expander("📊 View Cost Breakdown", expanded=True):
            service_df = detect_spike.generate_service_breakdown()
            
            fig = px.treemap(
                service_df, 
                path=['Parent', 'Service'], 
                values='Cost',
                color='Cost',
                color_continuous_scale='RdBu_r',
                title='Where is the money going?'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # --- PART 2: ANOMALY DETECTION ---
    st.subheader("2. Anomaly Detection (IQR Method)")
    
    # Call detect_spike to do the math
    spikes, threshold = detect_spike.detect_anomalies(df)
    
    if not spikes.empty:
        st.error(f" Alert! Found {len(spikes)} cost spike(s).")
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
        st.success(" No anomalies detected. Costs are within normal range.")

    st.markdown("---")

    # --- PART 4: RESOURCE HYGIENE (Interactive Auto-Fix) ---
    st.subheader("4. Resource Hygiene Check (Zombie Hunter)")
    
    # Initialize State: Has the user clicked the button yet?
    if 'zombies_fixed' not in st.session_state:
        st.session_state.zombies_fixed = False

    # Get the list of zombies from our logic file
    inventory_df, zombie_ids = cleanup.get_zombie_resources()

    # LOGIC: Show the problem OR show the solution
    if not st.session_state.zombies_fixed:
        
        # STATE A: Problem Detected (Show the zombies)
        if zombie_ids:
            st.caption("Scanning Active Cloud Inventory...")
            st.dataframe(inventory_df)  # Show full inventory
            
            st.error(f" Waste Detected! Found {len(zombie_ids)} zombie instance(s).")
            st.code(f"IDS: {zombie_ids}", language="json")
            
            # The "Trigger" Button
            if st.button("🔧 Auto-Fix: Terminate Zombies"):
                import time
                
                # Visual effect to make it look real
                with st.status("Initializing Cleanup Protocol...", expanded=True) as status:
                    st.write("🔌 Connecting to AWS API...")
                    time.sleep(0.5)
                    st.write(f"🚫 Stopping instances: {zombie_ids}...")
                    time.sleep(1)
                    st.write("✅ Resources terminated.")
                    status.update(label="Cleanup Complete!", state="complete", expanded=False)
                
                # Update State to "Fixed" and refresh page
                st.session_state.zombies_fixed = True
                st.rerun()
                
        else:
            st.success("Resource Hygiene is Good. No idle zombies found.")
            
    else:
        # STATE B: Problem Fixed (Show success message)
        st.success(f"✅ Automaton Complete: {len(zombie_ids)} zombie instances have been terminated.")
        
        # Reset Button (To run the demo again)
        if st.button("🔄 Reset Simulation"):
            st.session_state.zombies_fixed = False
            st.rerun()

    # --- PART 5: SMART RIGHT-SIZING ENGINE ---
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