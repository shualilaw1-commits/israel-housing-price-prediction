"""Tools for Data Scientist Crew - כלים לצוות מדעני הנתונים"""
import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime
import time


class FeatureEngineeringInput(BaseModel):
    """Input schema for Feature Engineering Tool"""
    input_file: str = Field(default="outputs/clean_data.csv")
    output_dir: str = Field(default="outputs")


class FeatureEngineeringTool(BaseTool):
    name: str = "Feature Engineering Tool"
    description: str = "יוצר פיצ'רים חדשים ומשמעותיים מהנתונים"

    def _run(self, input_file: str = "outputs/clean_data.csv", output_dir: str = "outputs") -> str:
        try:
            # קריאת הנתונים
            df = pd.read_csv(input_file)
            original_features = df.columns.tolist()

            # 0. המרת עמודת City למספרים (Label Encoding)
            if 'City' in df.columns:
                df['City_encoded'] = pd.Categorical(df['City']).codes
                # שמירת המיפוי לשימוש עתידי
                city_mapping = {city: code for code, city in enumerate(df['City'].unique())}
                import json
                mapping_path = os.path.join(output_dir, "city_mapping.json")
                with open(mapping_path, 'w', encoding='utf-8') as f:
                    json.dump(city_mapping, f, ensure_ascii=False, indent=2)
                # הסרת העמודה המקורית
                df = df.drop('City', axis=1)

            # 1. יחסים (Ratios) - מותאם לנתוני ישראל
            # הסרנו price_per_sqm כי זה data leakage (תלוי במחיר שאנחנו מנסים לחזות)
            df['rooms_per_size'] = df['Rooms'] / (df['Size_sqm'] + 0.001)  # חדרים למ"ר
            df['income_per_size'] = df['AvgIncome'] / (df['Size_sqm'] + 0.001)  # הכנסה למ"ר

            # 2. פיצ'רים גיאוגרפיים - מותאם לישראל
            # מרכז ישראל (בערך ירושלים)
            center_lat, center_lon = 31.7683, 35.2137
            df['distance_to_center_israel'] = np.sqrt(
                (df['Latitude'] - center_lat)**2 +
                (df['Longitude'] - center_lon)**2
            )
            # קרבה לחוף הים התיכון
            df['coastal_proximity'] = (df['DistanceSea_km'] < 10).astype(int)
            # שימוש במרחק מהים הקיים
            df['sea_proximity_score'] = 1 / (df['DistanceSea_km'] + 1)

            # 3. טרנספורמציות - מותאם לנתוני ישראל
            df['log_avg_income'] = np.log1p(df['AvgIncome'])
            df['income_category'] = pd.cut(df['AvgIncome'],
                                          bins=[0, 10, 15, 25],
                                          labels=['Low', 'Medium', 'High'])
            # המר קטגוריות למספרים
            df['income_category_encoded'] = df['income_category'].cat.codes
            
            # גיל הדירה (כבר קיים, אבל נוסיף קטגוריות)
            df['age_category'] = pd.cut(df['Age'],
                                       bins=[0, 10, 30, 100],
                                       labels=['New', 'Medium', 'Old'])
            df['age_category_encoded'] = df['age_category'].cat.codes

            # 4. אינטראקציות - מותאם לנתוני ישראל
            df['income_per_room'] = df['AvgIncome'] * df['Rooms']
            df['size_income'] = df['Size_sqm'] * df['AvgIncome']
            # הסרנו location_price כי זה data leakage (תלוי במחיר)
            df['location_score'] = df['Latitude'] * df['Longitude']  # רק מיקום ללא מחיר
            df['city_size_interaction'] = df['Size_sqm'] * df['Rooms']

            # הסרת עמודות קטגוריה זמניות
            if 'income_category' in df.columns:
                df = df.drop('income_category', axis=1)
            if 'age_category' in df.columns:
                df = df.drop('age_category', axis=1)

            # שמירת הנתונים עם פיצ'רים
            features_path = os.path.join(output_dir, "features.csv")
            df.to_csv(features_path, index=False)

            # יצירת דוח Feature Engineering
            new_features = [col for col in df.columns if col not in original_features]

            # חישוב קורלציה עם Target
            correlations = {}
            target_col = 'Price_Millions'
            if target_col not in df.columns:
                # נסה למצוא את עמודת המחיר
                possible_targets = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower()]
                if possible_targets:
                    target_col = possible_targets[0]
            
            for feature in new_features:
                if feature != target_col and df[feature].dtype in [np.number]:
                    try:
                        corr = df[feature].corr(df[target_col])
                        if not np.isnan(corr):
                            correlations[feature] = float(corr)
                    except:
                        pass

            report = f"""# Feature Engineering Report

## תאריך: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## פיצ'רים מקוריים
סך הכל: {len(original_features)} פיצ'רים
- {', '.join(original_features)}

## פיצ'רים חדשים שנוצרו
סך הכל: {len(new_features)} פיצ'רים חדשים

### 1. יחסים (Ratios) - מותאם לישראל
- **rooms_per_size**: חדרים למ"ר
  - קורלציה עם מחיר: {correlations.get('rooms_per_size', 0):.3f}
- **income_per_size**: הכנסה למ"ר
  - קורלציה עם מחיר: {correlations.get('income_per_size', 0):.3f}

### 2. פיצ'רים גיאוגרפיים - מותאם לישראל
- **distance_to_center_israel**: מרחק ממרכז ישראל
  - קורלציה עם מחיר: {correlations.get('distance_to_center_israel', 0):.3f}
- **coastal_proximity**: קרבה לחוף הים התיכון (0/1)
  - קורלציה עם מחיר: {correlations.get('coastal_proximity', 0):.3f}
- **sea_proximity_score**: ציון קרבה לים
  - קורלציה עם מחיר: {correlations.get('sea_proximity_score', 0):.3f}

### 3. טרנספורמציות - מותאם לישראל
- **log_avg_income**: לוג של הכנסה ממוצעת
  - קורלציה עם מחיר: {correlations.get('log_avg_income', 0):.3f}
- **income_category_encoded**: קטגוריית הכנסה (0=נמוכה, 1=בינונית, 2=גבוהה)
  - קורלציה עם מחיר: {correlations.get('income_category_encoded', 0):.3f}
- **age_category_encoded**: קטגוריית גיל דירה (0=חדש, 1=בינוני, 2=ישן)
  - קורלציה עם מחיר: {correlations.get('age_category_encoded', 0):.3f}

### 4. אינטראקציות - מותאם לישראל
- **income_per_room**: הכנסה כפול מספר חדרים
  - קורלציה עם מחיר: {correlations.get('income_per_room', 0):.3f}
- **size_income**: גודל כפול הכנסה
  - קורלציה עם מחיר: {correlations.get('size_income', 0):.3f}
- **location_score**: אינטראקציה גיאוגרפית (Latitude × Longitude)
  - קורלציה עם מחיר: {correlations.get('location_score', 0):.3f}
- **city_size_interaction**: אינטראקציה בין גודל לחדרים
  - קורלציה עם מחיר: {correlations.get('city_size_interaction', 0):.3f}

## סיכום
- **סך פיצ'רים לאחר הנדסה**: {len(df.columns)}
- **פיצ'רים בעלי קורלציה גבוהה** (>0.3): {sum(1 for c in correlations.values() if abs(c) > 0.3)}
- **פיצ'ר הכי חזק**: {max(correlations.items(), key=lambda x: abs(x[1]))[0]} ({max(correlations.values(), key=abs):.3f})

## המלצות למודל
1. השתמש בכל הפיצ'רים החדשים
2. שקול feature selection לפיצ'רים חלשים
3. בדוק multicollinearity בין פיצ'רים דומים

---
*נוצר אוטומטית על ידי Feature Engineering Agent*
"""

            report_path = os.path.join(output_dir, "feature_engineering_report.md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            return f"✓ הנדסת פיצ'רים הושלמה!\n" \
                   f"- פיצ'רים מקוריים: {len(original_features)}\n" \
                   f"- פיצ'רים חדשים: {len(new_features)}\n" \
                   f"- סך פיצ'רים: {len(df.columns)}"

        except Exception as e:
            return f"❌ שגיאה בהנדסת פיצ'רים: {str(e)}"


class ModelTrainingInput(BaseModel):
    """Input schema for Model Training Tools"""
    input_file: str = Field(default="outputs/features.csv")
    output_dir: str = Field(default="outputs")


class LinearRegressionTrainer(BaseTool):
    name: str = "Linear Regression Trainer"
    description: str = "מאמן מודל Linear Regression עם regularization"

    def _run(self, input_file: str = "outputs/features.csv", output_dir: str = "outputs") -> dict:
        try:
            df = pd.read_csv(input_file)
            # מציאת עמודת המחיר
            target_col = 'Price_Millions'
            if target_col not in df.columns:
                # נסה למצוא את עמודת המחיר
                possible_targets = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower()]
                if possible_targets:
                    target_col = possible_targets[0]
                else:
                    return {'error': f'לא נמצאה עמודת מחיר. עמודות זמינות: {list(df.columns)}'}
            
            X = df.drop(target_col, axis=1)
            y = df[target_col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Scaling
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # אימון Linear Regression רגיל
            start_time = time.time()
            lr = LinearRegression()
            lr.fit(X_train_scaled, y_train)
            train_time = time.time() - start_time

            # חיזוי
            y_train_pred = lr.predict(X_train_scaled)
            y_test_pred = lr.predict(X_test_scaled)

            # מטריקות
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            test_r2 = r2_score(y_test, y_test_pred)

            # Cross-validation
            cv_scores = cross_val_score(lr, X_train_scaled, y_train, cv=5,
                                       scoring='neg_root_mean_squared_error')

            return {
                'model_name': 'Linear Regression',
                'train_rmse': float(train_rmse),
                'test_rmse': float(test_rmse),
                'test_r2': float(test_r2),
                'cv_rmse_mean': float(-cv_scores.mean()),
                'cv_rmse_std': float(cv_scores.std()),
                'training_time': float(train_time),
                'model': lr,
                'scaler': scaler
            }

        except Exception as e:
            return {'error': str(e)}


class RandomForestTrainer(BaseTool):
    name: str = "Random Forest Trainer"
    description: str = "מאמן Random Forest עם GridSearch"

    def _run(self, input_file: str = "outputs/features.csv", output_dir: str = "outputs") -> dict:
        try:
            df = pd.read_csv(input_file)
            # מציאת עמודת המחיר
            target_col = 'Price_Millions'
            if target_col not in df.columns:
                # נסה למצוא את עמודת המחיר
                possible_targets = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower()]
                if possible_targets:
                    target_col = possible_targets[0]
                else:
                    return {'error': f'לא נמצאה עמודת מחיר. עמודות זמינות: {list(df.columns)}'}
            
            X = df.drop(target_col, axis=1)
            y = df[target_col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # GridSearch
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }

            start_time = time.time()
            rf = RandomForestRegressor(random_state=42, n_jobs=-1)
            grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
            grid_search.fit(X_train, y_train)
            train_time = time.time() - start_time

            best_model = grid_search.best_estimator_

            # חיזוי
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # מטריקות
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            test_r2 = r2_score(y_test, y_test_pred)

            return {
                'model_name': 'Random Forest',
                'train_rmse': float(train_rmse),
                'test_rmse': float(test_rmse),
                'test_r2': float(test_r2),
                'cv_rmse_mean': float(-grid_search.best_score_),
                'best_params': grid_search.best_params_,
                'training_time': float(train_time),
                'model': best_model,
                'scaler': None
            }

        except Exception as e:
            return {'error': str(e)}


class GradientBoostingTrainer(BaseTool):
    name: str = "Gradient Boosting Trainer"
    description: str = "מאמן Gradient Boosting עם GridSearch"

    def _run(self, input_file: str = "outputs/features.csv", output_dir: str = "outputs") -> dict:
        try:
            df = pd.read_csv(input_file)
            # מציאת עמודת המחיר
            target_col = 'Price_Millions'
            if target_col not in df.columns:
                # נסה למצוא את עמודת המחיר
                possible_targets = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower()]
                if possible_targets:
                    target_col = possible_targets[0]
                else:
                    return {'error': f'לא נמצאה עמודת מחיר. עמודות זמינות: {list(df.columns)}'}
            
            X = df.drop(target_col, axis=1)
            y = df[target_col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # GridSearch
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            }

            start_time = time.time()
            gb = GradientBoostingRegressor(random_state=42)
            grid_search = GridSearchCV(gb, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
            grid_search.fit(X_train, y_train)
            train_time = time.time() - start_time

            best_model = grid_search.best_estimator_

            # חיזוי
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # מטריקות
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            test_r2 = r2_score(y_test, y_test_pred)

            return {
                'model_name': 'Gradient Boosting',
                'train_rmse': float(train_rmse),
                'test_rmse': float(test_rmse),
                'test_r2': float(test_r2),
                'cv_rmse_mean': float(-grid_search.best_score_),
                'best_params': grid_search.best_params_,
                'training_time': float(train_time),
                'model': best_model,
                'scaler': None
            }

        except Exception as e:
            return {'error': str(e)}


class ModelComparisonTool(BaseTool):
    name: str = "Model Comparison Tool"
    description: str = "משווה בין כל המודלים ובוחר את הטוב ביותר"

    def _run(self, models_results: list, output_dir: str = "outputs") -> str:
        try:
            # מיון לפי test_rmse
            models_results = sorted(models_results, key=lambda x: x.get('test_rmse', float('inf')))
            best_model_result = models_results[0]

            # שמירת המודל הטוב ביותר
            model_path = os.path.join(output_dir, "model.pkl")
            model_data = {
                'model': best_model_result['model'],
                'scaler': best_model_result.get('scaler'),
                'model_name': best_model_result['model_name'],
                'metrics': {
                    'train_rmse': best_model_result['train_rmse'],
                    'test_rmse': best_model_result['test_rmse'],
                    'test_r2': best_model_result['test_r2']
                }
            }
            joblib.dump(model_data, model_path)

            # שמירת השוואה
            comparison = []
            for result in models_results:
                comparison.append({
                    'model_name': result['model_name'],
                    'train_rmse': result['train_rmse'],
                    'test_rmse': result['test_rmse'],
                    'test_r2': result['test_r2'],
                    'cv_rmse_mean': result.get('cv_rmse_mean'),
                    'training_time': result['training_time'],
                    'best_params': result.get('best_params', {})
                })

            comparison_path = os.path.join(output_dir, "all_models_comparison.json")
            with open(comparison_path, 'w', encoding='utf-8') as f:
                json.dump(comparison, f, ensure_ascii=False, indent=2)

            return f"✓ השוואת מודלים הושלמה!\n" \
                   f"- מודל זוכה: {best_model_result['model_name']}\n" \
                   f"- Test RMSE: {best_model_result['test_rmse']:.4f}\n" \
                   f"- Test R²: {best_model_result['test_r2']:.4f}"

        except Exception as e:
            return f"❌ שגיאה בהשוואת מודלים: {str(e)}"


class ModelTrainingTools:
    """מחלקה המכילה את כל כלי אימון המודלים"""

    @staticmethod
    def get_tools():
        return [
            LinearRegressionTrainer(),
            RandomForestTrainer(),
            GradientBoostingTrainer(),
            ModelComparisonTool()
        ]


class ModelEvaluationTool(BaseTool):
    name: str = "Model Evaluation Tool"
    description: str = "מעריך את המודל ויוצר דוח הערכה מפורט"

    def _run(self, model_path: str = "outputs/model.pkl",
             data_path: str = "outputs/features.csv",
             output_dir: str = "outputs") -> str:
        try:
            # טעינת המודל והנתונים
            model_data = joblib.load(model_path)
            model = model_data['model']
            scaler = model_data.get('scaler')

            df = pd.read_csv(data_path)
            # מציאת עמודת המחיר
            target_col = 'Price_Millions'
            if target_col not in df.columns:
                # נסה למצוא את עמודת המחיר
                possible_targets = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower()]
                if possible_targets:
                    target_col = possible_targets[0]
                else:
                    return f"❌ שגיאה: לא נמצאה עמודת מחיר. עמודות זמינות: {list(df.columns)}"
            
            X = df.drop(target_col, axis=1)
            y = df[target_col]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            if scaler:
                X_test = scaler.transform(X_test)

            # חיזוי
            y_pred = model.predict(X_test)

            # מטריקות
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # יצירת figures directory
            fig_dir = os.path.join(output_dir, "evaluation_figures")
            os.makedirs(fig_dir, exist_ok=True)

            # Predicted vs Actual plot
            plt.figure(figsize=(10, 6))
            plt.scatter(y_test, y_pred, alpha=0.5)
            plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            plt.xlabel('Actual Values')
            plt.ylabel('Predicted Values')
            plt.title('Predicted vs Actual')
            plt.tight_layout()
            plt.savefig(os.path.join(fig_dir, "predicted_vs_actual.png"), dpi=300)
            plt.close()

            # Residuals plot
            residuals = y_test - y_pred
            plt.figure(figsize=(10, 6))
            plt.scatter(y_pred, residuals, alpha=0.5)
            plt.axhline(y=0, color='r', linestyle='--')
            plt.xlabel('Predicted Values')
            plt.ylabel('Residuals')
            plt.title('Residual Plot')
            plt.tight_layout()
            plt.savefig(os.path.join(fig_dir, "residuals.png"), dpi=300)
            plt.close()

            # יצירת דוח הערכה
            report = f"""# Model Evaluation Report

## תאריך: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## מודל: {model_data['model_name']}

## מטריקות ביצוע

### על Test Set
- **RMSE**: {rmse:.4f}
- **MAE**: {mae:.4f}
- **R² Score**: {r2:.4f}

### פירוש
- RMSE של {rmse:.4f} משמעו שהשגיאה הממוצעת בחיזוי היא כ-${rmse*100000:,.0f}
- R² של {r2:.3f} אומר שהמודל מסביר {r2*100:.1f}% מהשונות במחירים

## ניתוח שגיאות

### סטטיסטיקות Residuals
- ממוצע: {residuals.mean():.4f}
- סטיית תקן: {residuals.std():.4f}
- מינימום: {residuals.min():.4f}
- מקסימום: {residuals.max():.4f}

## ויזואליזציות
ראה תיקייה: `evaluation_figures/`
- `predicted_vs_actual.png` - השוואה בין ערכים חזויים לאמיתיים
- `residuals.png` - התפלגות שגיאות

## המלצות

### נקודות חוזק
- ביצועים {'טובים' if r2 > 0.7 else ('סבירים' if r2 > 0.5 else 'חלשים')} עם R² של {r2:.3f}
- {'אין overfitting חמור' if abs(model_data.get('metrics', {}).get('train_rmse', 0) - rmse) < 0.1 else 'יש סימנים ל-overfitting'}

### נקודות לשיפור
1. {'שקול feature selection' if len(X.columns) > 15 else 'מספר הפיצרים סביר'}
2. {'נסה ensemble methods נוספים' if model_data.get('model_name') == 'Linear Regression' else 'שקול hyperparameter tuning נוסף'}
3. בדוק outliers בחיזויים החריגים

---
*נוצר אוטומטית על ידי Model Evaluation Agent*
"""

            report_path = os.path.join(output_dir, "evaluation_report.md")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            return f"✓ הערכת מודל הושלמה!\n" \
                   f"- RMSE: {rmse:.4f}\n" \
                   f"- R²: {r2:.4f}"

        except Exception as e:
            return f"❌ שגיאה בהערכת מודל: {str(e)}"


class ModelCardGenerator(BaseTool):
    name: str = "Model Card Generator"
    description: str = "יוצר Model Card מקצועי"

    def _run(self, model_path: str = "outputs/model.pkl",
             comparison_path: str = "outputs/all_models_comparison.json",
             output_dir: str = "outputs") -> str:
        try:
            # טעינת מידע
            model_data = joblib.load(model_path)

            with open(comparison_path, 'r') as f:
                comparison = json.load(f)

            model_card = f"""# Model Card: Israel Housing Price Prediction

## Model Details

### Basic Information
- **Model Name**: {model_data['model_name']}
- **Model Version**: 1.0
- **Model Date**: {datetime.now().strftime("%Y-%m-%d")}
- **Model Type**: Regression
- **Framework**: scikit-learn

### Developers
- Created by: שוקי שועלי
- Contact: shuali.law1@gmail.com

## Intended Use

### Primary Use Cases
- חיזוי מחירי דירות בישראל
- הערכת שווי נכסים למשקיעים
- תמיכה בהחלטות השקעה בנדל"ן בישראל

### Out-of-Scope Uses
- ❌ חיזוי מחירים מחוץ לישראל
- ❌ שימוש כבסיס יחיד להחלטות פיננסיות חשובות
- ❌ חיזויים לטווח ארוך (מעל שנה)

## Training Data

### Dataset
- **Name**: Israel Housing Dataset
- **Source**: Generated synthetic dataset based on Israeli real estate market
- **Size**: ~20,000 samples
- **Time Period**: Current (synthetic data)
- **Features**: 12 original + {len(model_data['model'].feature_names_in_) - 12 if hasattr(model_data['model'], 'feature_names_in_') else 'multiple'} engineered features

### Preprocessing
1. ניקוי ערכים חסרים
2. זיהוי והסרת outliers
3. הנדסת פיצ'רים:
   - יחסים (ratios)
   - פיצ'רים גיאוגרפיים
   - טרנספורמציות לוגריתמיות
   - אינטראקציות בין משתנים

## Model Performance

### Metrics
- **RMSE**: {model_data['metrics']['test_rmse']:.4f}
- **R² Score**: {model_data['metrics']['test_r2']:.4f}
- **Training Time**: {[m for m in comparison if m['model_name'] == model_data['model_name']][0]['training_time']:.2f} seconds

### Model Comparison
נבדקו {len(comparison)} מודלים שונים:

{chr(10).join([f"- {m['model_name']}: RMSE={m['test_rmse']:.4f}, R²={m['test_r2']:.4f}" for m in comparison])}

**מודל זה נבחר** בגלל הביצועים הטובים ביותר על ה-test set.

## Limitations

### Known Limitations
1. **נתונים ישנים**: הנתונים מ-1990, עשויים להיות לא רלוונטיים לשוק הנוכחי
2. **גיאוגרפיה מוגבלת**: המודל מאומן רק על קליפורניה
3. **משתנים חסרים**: אין מידע על:
   - מצב הנכס
   - שכונה ספציפית
   - מתקנים קרובים

### Recommendations
- השתמש במודל זה כחלק מניתוח רחב יותר
- בצע validation נוספת עם נתונים עדכניים
- שקול גורמים נוספים שאינם במודל

## Ethical Considerations

### Fairness
- המודל עלול להכיל הטיות גיאוגרפיות/כלכליות
- יש לבדוק ביצועים על תת-אוכלוסיות שונות

### Privacy
- הנתונים הם אגרגטיביים ואנונימיים
- אין מידע אישי זיהוי

### Transparency
- כל התהליך מתועד ב-Git
- ניתן לשחזר את התוצאות
- הקוד פתוח לבדיקה

## Caveats and Recommendations

⚠️ **אזהרות חשובות**:
1. אל תסמוך על המודל לבדו
2. התייעץ עם מומחה נדל"ן
3. בדוק את הנתונים באופן ידני

✅ **המלצות שימוש**:
1. השתמש כאינדיקציה ראשונית
2. שלב עם ניתוחים נוספים
3. עדכן את המודל עם נתונים חדשים

## Updates and Maintenance

### Version History
- **v1.0** ({datetime.now().strftime("%Y-%m-%d")}): גרסה ראשונית

### Planned Updates
- [ ] הוספת נתונים עדכניים
- [ ] בדיקת fairness מעמיקה
- [ ] שיפור feature engineering

---
*Model Card זה נוצר לפי [Model Cards for Model Reporting (Mitchell et al.)](https://arxiv.org/abs/1810.03993)*
"""

            card_path = os.path.join(output_dir, "model_card.md")
            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(model_card)

            return f"✓ Model Card נוצר בהצלחה!"

        except Exception as e:
            return f"❌ שגיאה ביצירת Model Card: {str(e)}"


class ModelEvaluationTools:
    """מחלקה המכילה את כל כלי הערכת המודלים"""

    @staticmethod
    def get_tools():
        return [
            ModelEvaluationTool(),
            ModelCardGenerator()
        ]
