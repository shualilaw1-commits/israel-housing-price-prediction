"""Data Analyst Crew - צוות מנתחי הנתונים המלא"""
from crewai import Crew, Process
from .agents import DataAnalystAgents
from .tasks import DataAnalystTasks


class DataAnalystCrew:
    """צוות מנתחי נתונים - 3 agents לניתוח וחקר הנתונים"""

    def __init__(self):
        """אתחול הצוות"""
        self.agents_factory = DataAnalystAgents()
        self.tasks_factory = DataAnalystTasks()

    def run(self) -> dict:
        """מריץ את צוות מנתחי הנתונים"""

        # יצירת ה-agents
        agents = {
            'data_ingestion': self.agents_factory.data_ingestion_agent(),
            'data_cleaning': self.agents_factory.data_cleaning_agent(),
            'eda': self.agents_factory.eda_agent()
        }

        # יצירת המשימות
        tasks = self.tasks_factory.get_all_tasks(agents)

        # יצירת ה-crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,  # המשימות רצות ברצף
            verbose=True
        )

        # הרצת הצוות
        result = crew.kickoff()

        return {
            'status': 'success',
            'result': result,
            'outputs': {
                'raw_data': 'outputs/raw_data.csv',
                'clean_data': 'outputs/clean_data.csv',
                'dataset_contract': 'outputs/dataset_contract.json',
                'insights': 'outputs/insights.md',
                'figures': 'outputs/figures/'
            }
        }
