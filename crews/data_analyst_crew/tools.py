"""Tools for Data Analyst Crew - כלים לצוות מנתחי הנתונים"""
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
# Removed: from sklearn.datasets import fetch_california_housing
# Now using Israel housing dataset
from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DataIngestionInput(BaseModel):
    """Input schema for Data Ingestion Tool"""
    output_dir: str = Field(default="outputs", description="Directory to save outputs")


class DataIngestionTool(BaseTool):
    name: str = "Data Ingestion Tool"
    description: str = "טוען את Israel Housing dataset ושומר אותו"

    def _run(self, output_dir: str = "outputs") -> str:
        """טוען את הנתונים ויוצר dataset contract"""
        try:
            # יצירת תיקייה אם לא קיימת
            os.makedirs(output_dir, exist_ok=True)

            # טעינת הנתונים מישראל
            # נבדוק אם קיים קובץ raw_data.csv, אם לא - נטען מהנתיב היחסי
            raw_data_path = os.path.join(output_dir, "raw_data.csv")
            
            # אם הקובץ לא קיים, ננסה לטעון מהתיקייה הראשית
            if not os.path.exists(raw_data_path):
                # ננסה לטעון מהתיקייה הראשית (אם הסקריפט create_israel_dataset.py כבר רץ)
                parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                possible_paths = [
                    os.path.join(parent_dir, "create_israel_dataset.py"),
                    os.path.join(output_dir, "raw_data.csv"),
                    "outputs/raw_data.csv"
                ]
                
                # אם אין נתונים, נצטרך להריץ את create_israel_dataset.py
                return "❌ קובץ raw_data.csv לא נמצא. אנא הרץ תחילה: python create_israel_dataset.py"
            
            # טעינת הנתונים
            df = pd.read_csv(raw_data_path, encoding='utf-8')

            # יצירת dataset contract
            contract = {
                "dataset_name": "Israel Housing Dataset",
                "source": "Generated dataset based on Israeli real estate market",
                "load_date": datetime.now().isoformat(),
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "columns": {
                    col: {
                        "dtype": str(df[col].dtype),
                        "null_count": int(df[col].isnull().sum()),
                        "unique_count": int(df[col].nunique())
                    }
                    for col in df.columns
                },
                "description": "Dataset של דירות בישראל עם מידע על ערים, גודל, חדרים, מיקום ומחירים",
                "target": "Price_Millions"
            }

            # שמירת החוזה
            contract_path = os.path.join(output_dir, "dataset_contract.json")
            with open(contract_path, 'w', encoding='utf-8') as f:
                json.dump(contract, f, ensure_ascii=False, indent=2)

            return f"✓ טעינת נתונים הצליחה!\n" \
                   f"- שורות: {len(df):,}\n" \
                   f"- עמודות: {len(df.columns)}\n" \
                   f"- קבצים נשמרו ב: {output_dir}"

        except Exception as e:
            return f"❌ שגיאה בטעינת הנתונים: {str(e)}"


class DataCleaningInput(BaseModel):
    """Input schema for Data Cleaning Tool"""
    input_file: str = Field(default="outputs/raw_data.csv")
    output_dir: str = Field(default="outputs")


class DataCleaningTool(BaseTool):
    name: str = "Data Cleaning Tool"
    description: str = "מנקה את הנתונים ומטפל בערכים חסרים וחריגים"

    def _run(self, input_file: str = "outputs/raw_data.csv", output_dir: str = "outputs") -> str:
        """מנקה את הנתונים"""
        try:
            # קריאת הנתונים
            df = pd.read_csv(input_file)
            original_rows = len(df)

            # 1. בדיקת ערכים חסרים
            missing_values = df.isnull().sum()
            missing_report = missing_values[missing_values > 0].to_dict()

            # 2. טיפול ב-inf values
            df.replace([np.inf, -np.inf], np.nan, inplace=True)

            # 3. זיהוי outliers עם IQR method
            outliers_count = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                if outliers > 0:
                    outliers_count[col] = int(outliers)

            # 4. מחיקת שורות עם ערכים חסרים (אם יש)
            df.dropna(inplace=True)

            # 5. שמירת הנתונים המנוקים
            clean_data_path = os.path.join(output_dir, "clean_data.csv")
            df.to_csv(clean_data_path, index=False)

            # 6. עדכון dataset contract (אם קיים)
            contract_path = os.path.join(output_dir, "dataset_contract.json")
            if os.path.exists(contract_path):
                try:
                    with open(contract_path, 'r', encoding='utf-8') as f:
                        contract = json.load(f)
                    
                    contract["cleaning"] = {
                        "cleaning_date": datetime.now().isoformat(),
                        "original_rows": original_rows,
                        "cleaned_rows": len(df),
                        "rows_removed": original_rows - len(df),
                        "missing_values_found": missing_report,
                        "outliers_detected": outliers_count,
                        "cleaning_actions": [
                            "הסרת ערכי inf",
                            "מחיקת שורות עם ערכים חסרים",
                            "זוהו outliers אך נשמרו (מומלץ לבדוק)"
                        ]
                    }

                    with open(contract_path, 'w', encoding='utf-8') as f:
                        json.dump(contract, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    pass  # אם יש בעיה בעדכון החוזה, נמשיך

            return f"✓ ניקוי נתונים הושלם!\n" \
                   f"- שורות מקוריות: {original_rows:,}\n" \
                   f"- שורות לאחר ניקוי: {len(df):,}\n" \
                   f"- שורות שהוסרו: {original_rows - len(df):,}\n" \
                   f"- Outliers שזוהו: {sum(outliers_count.values())}"

        except Exception as e:
            return f"❌ שגיאה בניקוי הנתונים: {str(e)}"


class EDAInput(BaseModel):
    """Input schema for EDA Tools"""
    input_file: str = Field(default="outputs/clean_data.csv")
    output_dir: str = Field(default="outputs")


class DistributionAnalysisTool(BaseTool):
    name: str = "Distribution Analysis Tool"
    description: str = "יוצר ניתוח התפלגויות עם היסטוגרמות ו-box plots"

    def _run(self, input_file: str = "outputs/clean_data.csv", output_dir: str = "outputs") -> str:
        try:
            df = pd.read_csv(input_file)
            fig_dir = os.path.join(output_dir, "figures")
            os.makedirs(fig_dir, exist_ok=True)

            # יצירת figure עם subplots
            num_cols = len(df.columns)
            fig, axes = plt.subplots(num_cols, 2, figsize=(15, num_cols * 4))

            for idx, col in enumerate(df.columns):
                # Histogram
                axes[idx, 0].hist(df[col], bins=50, edgecolor='black', alpha=0.7)
                axes[idx, 0].set_title(f'Distribution of {col}')
                axes[idx, 0].set_xlabel(col)
                axes[idx, 0].set_ylabel('Frequency')

                # Box plot
                axes[idx, 1].boxplot(df[col])
                axes[idx, 1].set_title(f'Box Plot of {col}')
                axes[idx, 1].set_ylabel(col)

            plt.tight_layout()
            plt.savefig(os.path.join(fig_dir, "distributions.png"), dpi=300, bbox_inches='tight')
            plt.close()

            return "✓ ניתוח התפלגויות נוצר בהצלחה"

        except Exception as e:
            return f"❌ שגיאה: {str(e)}"


class CorrelationAnalysisTool(BaseTool):
    name: str = "Correlation Analysis Tool"
    description: str = "יוצר מטריצת קורלציות ו-pairplot"

    def _run(self, input_file: str = "outputs/clean_data.csv", output_dir: str = "outputs") -> str:
        try:
            df = pd.read_csv(input_file)
            fig_dir = os.path.join(output_dir, "figures")
            os.makedirs(fig_dir, exist_ok=True)

            # Correlation heatmap
            plt.figure(figsize=(12, 10))
            corr_matrix = df.corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=1, cbar_kws={"shrink": 0.8})
            plt.title('Correlation Matrix', fontsize=16)
            plt.tight_layout()
            plt.savefig(os.path.join(fig_dir, "correlation_heatmap.png"), dpi=300, bbox_inches='tight')
            plt.close()

            # Pairplot אינטראקטיבי עם plotly
            fig = px.scatter_matrix(df, dimensions=df.columns[:5],  # 5 משתנים ראשונים
                                   title="Pairplot - Interactive")
            fig.write_html(os.path.join(fig_dir, "pairplot.html"))

            return "✓ ניתוח קורלציות נוצר בהצלחה"

        except Exception as e:
            return f"❌ שגיאה: {str(e)}"


class GeographicAnalysisTool(BaseTool):
    name: str = "Geographic Analysis Tool"
    description: str = "יוצר ניתוח גיאוגרפי של הנתונים"

    def _run(self, input_file: str = "outputs/clean_data.csv", output_dir: str = "outputs") -> str:
        try:
            df = pd.read_csv(input_file)
            fig_dir = os.path.join(output_dir, "figures")
            os.makedirs(fig_dir, exist_ok=True)

            # Geographic scatter plot
            fig = px.scatter(df, x='Longitude', y='Latitude',
                           color='Price_Millions', size='Population',
                           hover_data=['Rooms', 'Size_sqm'],
                           title='Israel Housing - Geographic Distribution',
                           color_continuous_scale='Viridis')

            fig.update_layout(width=1000, height=800)
            fig.write_html(os.path.join(fig_dir, "geographic_analysis.html"))

            return "✓ ניתוח גיאוגרפי נוצר בהצלחה"

        except Exception as e:
            return f"❌ שגיאה: {str(e)}"


class InsightsGeneratorTool(BaseTool):
    name: str = "Insights Generator Tool"
    description: str = "מפיק תובנות מהנתונים ושומר ב-markdown"

    def _run(self, input_file: str = "outputs/clean_data.csv", output_dir: str = "outputs") -> str:
        try:
            df = pd.read_csv(input_file)

            # חישוב קורלציות עם המשתנה היעד
            target_corr = df.corr()['Price_Millions'].sort_values(ascending=False)

            # יצירת תובנות
            insights = f"""# תובנות מניתוח הנתונים - Israel Housing

## 📊 סטטיסטיקות כלליות
- **סך שורות**: {len(df):,}
- **סך עמודות**: {len(df.columns)}
- **משתנה יעד**: Price_Millions (מחיר במיליוני שקלים)

## 🎯 קורלציות חשובות
המשתנים הכי קשורים למחיר הדירה:
{chr(10).join([f'- **{col}**: {corr:.3f}' for col, corr in target_corr.items() if col != 'Price_Millions'])}

## 💡 תובנות מרכזיות

### 1. משתנה הכי משפיע
המשתנה **{target_corr.index[1]}** הוא הכי קשור למחיר עם קורלציה של {target_corr.iloc[1]:.3f}

### 2. מאפייני התפלגות
- מחיר ממוצע: {df['Price_Millions'].mean():.2f} מיליון ש"ח
- מחיר חציוני: {df['Price_Millions'].median():.2f} מיליון ש"ח
- סטיית תקן: {df['Price_Millions'].std():.2f} מיליון ש"ח

### 3. דפוסים גיאוגרפיים
- התפלגות גיאוגרפית מגוונת בישראל
- מחירים גבוהים יותר באזורים מסוימים (נראה ב-scatter plot)
- ערים מרכזיות כמו תל אביב ורמת גן נוטות להיות יקרות יותר

## 🔍 המלצות למודל

1. **פיצ'רים חשובים**: התמקד ב-{', '.join(target_corr.index[1:4])}
2. **Feature Engineering**:
   - צור יחס של חדרים לגודל (Size_sqm)
   - צור משתנה גיאוגרפי משולב (Latitude, Longitude)
   - צור משתנה מרחק משולב (DistanceSea_km, DistanceCenter_km)
3. **Outliers**: שקול להסיר או לטפל ב-outliers חריפים
4. **מודלים מומלצים**:
   - Linear Regression (baseline)
   - Random Forest (טיפול טוב ב-non-linearity)
   - Gradient Boosting (ביצועים גבוהים)

---
*נוצר אוטומטית ב-{datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""

            # שמירת התובנות
            insights_path = os.path.join(output_dir, "insights.md")
            with open(insights_path, 'w', encoding='utf-8') as f:
                f.write(insights)

            return "✓ תובנות נוצרו ונשמרו ב-insights.md"

        except Exception as e:
            return f"❌ שגיאה: {str(e)}"


class EDATools:
    """מחלקה המכילה את כל כלי ה-EDA"""

    @staticmethod
    def get_tools():
        """מחזירה רשימה של כל הכלים"""
        return [
            DistributionAnalysisTool(),
            CorrelationAnalysisTool(),
            GeographicAnalysisTool(),
            InsightsGeneratorTool()
        ]
