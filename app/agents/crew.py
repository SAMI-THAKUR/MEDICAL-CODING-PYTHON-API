"""
CrewAI Crew Configuration
Orchestrates all agents and tasks for medical coding pipeline
"""

from crewai import Crew
from app.agents.entity_structuring_agent import (
    create_entity_structuring_agent,
    create_entity_structuring_task
)
from app.agents.icd_coding_agent import (
    create_icd_coding_agent,
    create_icd_coding_task
)
from app.agents.cpt_coding_agent import (
    create_cpt_coding_agent,
    create_cpt_coding_task
)
from app.agents.hcpcs_coding_agent import (
    create_hcpcs_coding_agent,
    create_hcpcs_coding_task
)


class MedicalCodingCrew:
    """Medical coding crew with all agents and tasks"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._crew = None
        self._initialized = False
    
    def initialize(self):
        """Initialize all agents and tasks"""
        if not self._initialized:
            # Create agents
            self.entity_agent = create_entity_structuring_agent()
            self.icd_agent = create_icd_coding_agent()
            self.cpt_agent = create_cpt_coding_agent()
            self.hcpcs_agent = create_hcpcs_coding_agent()
            
            # Create tasks
            self.entity_task = create_entity_structuring_task(self.entity_agent)
            self.icd_task = create_icd_coding_task(self.icd_agent)
            self.hcpcs_task = create_hcpcs_coding_task(self.hcpcs_agent)
            self.cpt_task = create_cpt_coding_task(self.cpt_agent)
            
            # Create crew
            self._crew = Crew(
                agents=[
                    self.entity_agent,
                    self.icd_agent,
                    self.hcpcs_agent,
                    self.cpt_agent
                ],
                tasks=[
                    self.entity_task,
                    self.icd_task,
                    self.hcpcs_task,
                    self.cpt_task
                ],
                verbose=self.verbose
            )
            
            self._initialized = True
    
    def kickoff(self, medical_report_text: str):
        """
        Execute the medical coding pipeline.
        
        Args:
            medical_report_text: The clinical text to process
            
        Returns:
            CrewOutput with results from all tasks
        """
        self.initialize()
        return self._crew.kickoff(inputs={"medical_report_text": medical_report_text})
    
    @property
    def crew(self) -> Crew:
        """Get the crew instance"""
        self.initialize()
        return self._crew


def get_medical_coding_crew(verbose: bool = False) -> MedicalCodingCrew:
    """Factory function to create medical coding crew"""
    return MedicalCodingCrew(verbose=verbose)
