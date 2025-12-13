"""Data Scientist Crew Tasks - משימות לצוות מדעני הנתונים"""
from crewai import Task
from typing import List


class DataScientistTasks:
    """מחלקה המגדירה את המשימות של צוות מדעני הנתונים"""

    def feature_engineering_task(self, agent) -> Task:
        """משימה 1: הנדסת פיצ'רים"""
        return Task(
            description="""
            צור פיצ'רים חדשים מהנתונים המנוקים ב-outputs/clean_data.csv.

            פיצ'רים לייצר:
            1. **יחסים (Ratios)**:
               - rooms_per_size = Rooms / Size_sqm (חדרים למ"ר)
               - income_per_size = AvgIncome / Size_sqm (הכנסה למ"ר)

            2. **פיצ'רים גיאוגרפיים**:
               - distance_to_center_israel = מרחק ממרכז ישראל
               - coastal_proximity = האם קרוב לחוף הים התיכון
               - sea_proximity_score = ציון קרבה לים

            3. **טרנספורמציות**:
               - log_avg_income = log של ההכנסה הממוצעת
               - income_category = קטגוריות הכנסה (Low/Medium/High)
               - age_category = קטגוריות גיל דירה

            4. **אינטראקציות**:
               - income_per_room = AvgIncome * Rooms
               - size_income = Size_sqm * AvgIncome
               - location_score = Latitude * Longitude
               - city_size_interaction = Size_sqm * Rooms

            דרישות:
            - שמור את כל הפיצ'רים המקוריים + החדשים
            - תעד את כל פיצ'ר חדש ב-feature_engineering_report.md
            - שמור correlation של הפיצ'רים החדשים עם Target

            שמור ב: outputs/features.csv
            תעד ב: outputs/feature_engineering_report.md
            """,
            agent=agent,
            expected_output="קובץ CSV עם פיצ'רים מהונדסים ודוח הנדסת פיצ'רים"
        )

    def model_training_task(self, agent) -> Task:
        """משימה 2: אימון מודלים"""
        return Task(
            description="""
            אמן 3 מודלים שונים על הנתונים עם הפיצ'רים ב-outputs/features.csv.

            מודלים לאימון:
            1. **Linear Regression**
               - Baseline פשוט
               - עם regularization (Ridge)

            2. **Random Forest Regressor**
               - n_estimators: [100, 200]
               - max_depth: [10, 20, None]
               - השתמש ב-GridSearchCV

            3. **Gradient Boosting Regressor**
               - n_estimators: [100, 200]
               - learning_rate: [0.01, 0.1]
               - max_depth: [3, 5]

            תהליך:
            1. פצל את הנתונים: 80% train, 20% test
            2. אמן כל מודל עם cross-validation (5-fold)
            3. שמור את הביצועים של כל מודל:
               - Train RMSE
               - Test RMSE
               - Cross-validation score
               - Training time
            4. בחר את המודל הטוב ביותר
            5. שמור את המודל הטוב ביותר

            שמור:
            - outputs/model.pkl (המודל הטוב ביותר)
            - outputs/all_models_comparison.json (השוואת כל המודלים)
            - outputs/training_metrics.json
            """,
            agent=agent,
            expected_output="מודל מאומן עם דוח השוואה של כל המודלים",
            context=[self.feature_engineering_task(agent)]
        )

    def model_evaluation_task(self, agent) -> Task:
        """משימה 3: הערכה ותיעוד"""
        return Task(
            description="""
            העריך את המודל שנבחר ותעד אותו בצורה מקצועית.

            הערכה:
            1. **מטריקות ביצוע**:
               - RMSE, MAE, R²
               - על Train ועל Test
               - עם cross-validation

            2. **ניתוח שגיאות**:
               - התפלגות של residuals
               - Predicted vs Actual plot
               - זיהוי outliers בחיזוי

            3. **Feature Importance**:
               - אילו פיצ'רים הכי משפיעים?
               - SHAP values אם אפשר

            4. **בדיקות נוספות**:
               - Overfitting check
               - Prediction intervals
               - ביצועים לפי קטגוריות שונות

            תיעוד:
            1. **Evaluation Report (evaluation_report.md)**:
               - כל המטריקות
               - ויזואליזציות
               - ניתוח שגיאות
               - המלצות לשיפור

            2. **Model Card (model_card.md)**:
               - פרטי המודל
               - מטרת השימוש
               - כיצד אומן
               - ביצועים
               - מגבלות
               - שיקולים אתיים

            שמור:
            - outputs/evaluation_report.md
            - outputs/model_card.md
            - outputs/evaluation_figures/ (כל הגרפים)
            """,
            agent=agent,
            expected_output="דוח הערכה מלא ו-Model Card מקצועי",
            context=[self.model_training_task(agent)]
        )

    def get_all_tasks(self, agents_dict: dict) -> List[Task]:
        """מחזירה את כל המשימות בסדר הנכון"""
        return [
            self.feature_engineering_task(agents_dict['feature_engineer']),
            self.model_training_task(agents_dict['model_trainer']),
            self.model_evaluation_task(agents_dict['model_evaluator'])
        ]
