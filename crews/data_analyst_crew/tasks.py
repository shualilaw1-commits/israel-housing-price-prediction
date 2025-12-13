"""Data Analyst Crew Tasks - משימות לצוות מנתחי הנתונים"""
from crewai import Task
from typing import List


class DataAnalystTasks:
    """מחלקה המגדירה את המשימות של צוות מנתחי הנתונים"""

    def data_ingestion_task(self, agent) -> Task:
        """משימה 1: טעינת הנתונים"""
        return Task(
            description="""
            טען את מאגר הנתונים Israel Housing Dataset.

            בצע את הפעולות הבאות:
            1. טען את הנתונים מ-outputs/raw_data.csv (נתונים שנוצרו על ידי create_israel_dataset.py)
            2. המר ל-DataFrame של pandas
            3. בדוק את מבנה הנתונים:
               - כמה שורות ועמודות
               - סוגי הנתונים
               - בדיקה ראשונית לערכים חסרים
            4. שמור סטטיסטיקות בסיסיות
            5. צור קובץ dataset_contract.json עם:
               - שמות העמודות וסוגיהן
               - מספר שורות
               - תאריך הטעינה
               - מקור הנתונים

            שמור את התוצאה ב: outputs/raw_data.csv
            שמור את החוזה ב: outputs/dataset_contract.json
            """,
            agent=agent,
            expected_output="קובץ CSV עם הנתונים הגולמיים וקובץ JSON עם חוזה הנתונים"
        )

    def data_cleaning_task(self, agent) -> Task:
        """משימה 2: ניקוי הנתונים"""
        return Task(
            description="""
            נקה את הנתונים שנטענו ב-outputs/raw_data.csv.

            בצע את הפעולות הבאות:
            1. זהה ערכים חסרים (NULL, NaN, inf)
            2. זהה ערכים חריגים (outliers) עם IQR method
            3. החלט על אסטרטגיית טיפול:
               - ערכים חסרים: מחיקה/מילוי/אינטרפולציה
               - ערכים חריגים: השארה/מחיקה/תיקון
            4. תקן סוגי נתונים אם נדרש
            5. בדוק עקביות הנתונים
            6. עדכן את dataset_contract.json עם:
               - מספר שורות שנמחקו
               - שינויים שבוצעו
               - החלטות ניקוי

            שמור את התוצאה ב: outputs/clean_data.csv
            עדכן: outputs/dataset_contract.json
            """,
            agent=agent,
            expected_output="קובץ CSV עם נתונים מנוקים וחוזה נתונים מעודכן",
            context=[self.data_ingestion_task(agent)]  # תלוי במשימה הקודמת
        )

    def eda_task(self, agent) -> Task:
        """משימה 3: ניתוח גרפי (EDA)"""
        return Task(
            description="""
            צור ניתוח חזוני מעמיק (EDA) על הנתונים המנוקים.

            צור את הויזואליזציות הבאות:
            1. התפלגויות (distributions):
               - היסטוגרמות לכל משתנה מספרי
               - Box plots לזיהוי outliers
            2. קורלציות:
               - Correlation matrix heatmap
               - Pairplot למשתנים החשובים
            3. ניתוח גיאוגרפי:
               - Scatter plot של latitude vs longitude
               - צבוע לפי מחיר
            4. ניתוח יחסים:
               - מחיר לפי מיקום
               - מחיר לפי גודל בית
               - מחיר לפי גיל הבית

            הפק תובנות:
            1. מהו המשתנה הכי קשור למחיר?
            2. האם יש דפוסים גיאוגרפיים?
            3. האם יש קבוצות ברורות בנתונים?
            4. המלצות לבניית המודל

            שמור:
            - outputs/eda_report.html (דוח אינטראקטיבי)
            - outputs/figures/ (כל הגרפים)
            - outputs/insights.md (תובנות בעברית)
            """,
            agent=agent,
            expected_output="דוח EDA מלא עם ויזואליזציות ותובנות",
            context=[self.data_cleaning_task(agent)]  # תלוי בנתונים המנוקים
        )

    def get_all_tasks(self, agents_dict: dict) -> List[Task]:
        """מחזירה את כל המשימות בסדר הנכון"""
        return [
            self.data_ingestion_task(agents_dict['data_ingestion']),
            self.data_cleaning_task(agents_dict['data_cleaning']),
            self.eda_task(agents_dict['eda'])
        ]
