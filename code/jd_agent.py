import autogen
from autogen import ConversableAgent
import os

class JD_agent: 
    def __init__(self, jd):
        self.jd = jd
        self.jd_agent = self.jd_agent()

    def jd_agent(self):
        """Create an agent specialized in jd analysis."""
        config_list_gemini = autogen.config_list_from_json("model_config.json")
        return ConversableAgent(
            name="JDAnalyzer",
            system_message="""You are a specialized Job Description(JD) analysis agent. Your tasks include:
            1. Understanding JD content
            2. Extracting key information like skills, experience, education etc required by company 
            3. Categorize information on Skill, Knowledge,attitude, Evidence, Evaluation bases which candidate can add in resume
            Please analyze the provided content and respond with structured insights.""",
            llm_config={"config_list": config_list_gemini},
            code_execution_config=False,
            human_input_mode="NEVER"
        )
    
    def analyze_jd(self): 
        """Analyze jd using the agent."""
        analysis_prompt = f"""
        Please analyze the following resume content and provide insights:
        
        {self.jd}
        
        Please provide:
        1. Categorize information on Knowledge, skill, attitude required by candidate 
        2. Evaluation bases which candidate can add in resume
        """
        
        response = self.jd_agent.generate_reply(
            messages=[{"content": analysis_prompt, "role": "user"}]
        )
        return response