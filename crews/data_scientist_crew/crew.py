"""Data Scientist Crew - צוות מדעני הנתונים המלא"""
from crewai import Crew, Process
from .agents import DataScientistAgents
from .tasks import DataScientistTasks


class DataScientistCrew:
    """צוות מדעני נתונים - 3 agents לבניית והערכת מודלים"""

    def __init__(self):
        """אתחול הצוות"""
        self.agents_factory = DataScientistAgents()
        self.tasks_factory = DataScientistTasks()

    def run(self) -> dict:
        """מריץ את צוות מדעני הנתונים"""

        # יצירת ה-agents
        agents = {
            'feature_engineer': self.agents_factory.feature_engineer_agent(),
            'model_trainer': self.agents_factory.model_trainer_agent(),
            'model_evaluator': self.agents_factory.model_evaluator_agent()
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
                'features': 'outputs/features.csv',
                'model': 'outputs/model.pkl',
                'model_comparison': 'outputs/all_models_comparison.json',
                'evaluation_report': 'outputs/evaluation_report.md',
                'model_card': 'outputs/model_card.md',
                'figures': 'outputs/evaluation_figures/'
            }
        }
