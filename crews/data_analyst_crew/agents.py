"""Data Analyst Crew Agents - 3 סוכנים לניתוח נתונים"""
from crewai import Agent
from .tools import DataIngestionTool, DataCleaningTool, EDATools


class DataAnalystAgents:
    """מחלקה המגדירה את 3 הסוכנים של צוות מנתחי הנתונים"""

    def data_ingestion_agent(self) -> Agent:
        """Agent 1: Data Ingestion - טוען ומנתח את מאגר הנתונים"""
        return Agent(
            role="Data Ingestion Specialist",
            goal="טעינה ובדיקה ראשונית של מאגר הנתונים California Housing",
            backstory="""אתה מומחה לטעינת נתונים עם ניסיון רב בעבודה עם מאגרי נתונים גדולים.
            אתה יודע לזהות בעיות פוטנציאליות מוקדם ולתעד את מבנה הנתונים בצורה מדויקת.""",
            tools=[DataIngestionTool()],
            verbose=True,
            allow_delegation=False
        )

    def data_cleaning_agent(self) -> Agent:
        """Agent 2: Data Cleaning - מנקה ומעבד את הנתונים"""
        return Agent(
            role="Data Cleaning Expert",
            goal="ניקוי ועיבוד הנתונים כולל טיפול בערכים חסרים וחריגים",
            backstory="""אתה מומחה בניקוי נתונים עם עין חדה לפרטים.
            אתה יודע להחליט מתי למחוק, מתי למלא ומתי לתקן ערכים בעייתיים.
            אתה תמיד מתעד את ההחלטות שלך ב-Dataset Contract.""",
            tools=[DataCleaningTool()],
            verbose=True,
            allow_delegation=False
        )

    def eda_agent(self) -> Agent:
        """Agent 3: EDA - יוצר ויזואליזציות ותובנות"""
        return Agent(
            role="Exploratory Data Analysis Specialist",
            goal="יצירת ויזואליזציות מעמיקות והפקת תובנות עסקיות מהנתונים",
            backstory="""אתה אנליסט נתונים מבריק שיודע למצוא סיפורים בנתונים.
            אתה יוצר ויזואליזציות ברורות ומפיק תובנות שימושיות לקבלת החלטות.
            אתה מומחה ב-matplotlib, seaborn ו-plotly.""",
            tools=EDATools().get_tools(),
            verbose=True,
            allow_delegation=False
        )
