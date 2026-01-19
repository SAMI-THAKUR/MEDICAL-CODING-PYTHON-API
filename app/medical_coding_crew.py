from crewai import Crew
from app.agents.input_structuring_agent import Input_Structuring_Agent
from app.agents.icd_coding_agent import ICD_Coding_Agent
from app.agents.hcpcs_coding_agent import HCPCS_Coding_Agent
from app.agents.cpt_coding_agent import CPT_Coding_Agent

from app.tasks.input_structuring_task import Input_Structuring_Task
from app.tasks.icd_coding_task import ICD_Coding_Task
from app.tasks.hcpcs_coding_task import HCPCS_Coding_Task
from app.tasks.cpt_coding_task import CPT_Coding_Task




# Initialize Crew
Medical_Coding_Crew = Crew(
    name="MediSuite AI",
    description="""MediSuite AI is a medical coding assistant that 
    helps healthcare providers to code their procedures and diagnoses.""",
    agents=[
        Input_Structuring_Agent,
        ICD_Coding_Agent,
        HCPCS_Coding_Agent,
        CPT_Coding_Agent
        
    ],
    tasks=[
        Input_Structuring_Task,
        ICD_Coding_Task,
        HCPCS_Coding_Task,
        CPT_Coding_Task
    ],
)
