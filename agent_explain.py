# ai_engine.py
import google.generativeai as genai
import config 

def get_gemini_response(spike_row, logs):
    """
    Connects to Gemini and returns a string explanation.
    """
    try:
        # Configure using the key from config.py
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Use the correct model name
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        cost = spike_row['cost']
        date = spike_row['date']
        
        prompt = f"""
        You are a FinOps Cloud Expert. 
        Analyze the following billing alert:
        - Date: {date}
        - Cost: ${cost} (Normal average is $110)
        
        Here are the system logs for that day:
        {logs}
        
        Explain why the cost spiked in plain simple English without jargons for a manager. 
        Structure your answer with:
        1. What happened?
        2. Root Cause
        3. Recommended Action
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"⚠️ Error talking to AI: {e}"