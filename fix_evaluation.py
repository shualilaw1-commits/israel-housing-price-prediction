# -*- coding: utf-8 -*-
"""Quick script to create missing evaluation files"""
import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    except (AttributeError, ValueError):
        # If already detached or not available, use io
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime
import json

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def create_evaluation_report():
    """Create evaluation_report.md"""
    print("Creating evaluation_report.md...")
    
    try:
        # Load model with error handling for numpy random state
        import warnings
        warnings.filterwarnings('ignore')
        
        try:
            # נשתמש ב-joblib.load תמיד - זה עובד נכון
            model_data = joblib.load("outputs/model.pkl")
            # בדיקה ש-model_data הוא dict
            if not isinstance(model_data, dict):
                print(f"ERROR: model_data is not a dict, it's {type(model_data)}")
                return False
        except Exception as e:
            # אם joblib נכשל, נציג שגיאה
            print(f"ERROR: Failed to load model with joblib: {str(e)}")
            print(f"ERROR: Exception type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
        
        model = model_data['model']
        scaler = model_data.get('scaler')
        
        # Load data
        df = pd.read_csv("outputs/features.csv")
        target_col = 'Price_Millions' if 'Price_Millions' in df.columns else 'MedHouseVal'
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if scaler:
            X_test_scaled = scaler.transform(X_test)
            y_pred = model.predict(X_test_scaled)
        else:
            y_pred = model.predict(X_test)
        
        # Metrics
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        residuals = y_test - y_pred
        
        # Create figures directory
        fig_dir = "outputs/evaluation_figures"
        os.makedirs(fig_dir, exist_ok=True)
        
        # Predicted vs Actual
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title('Predicted vs Actual')
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "predicted_vs_actual.png"), dpi=300)
        plt.close()
        
        # Residuals
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "residuals.png"), dpi=300)
        plt.close()
        
        # בדיקה סופית ש-model_data הוא dict (לפני השימוש)
        if not isinstance(model_data, dict):
            print(f"ERROR: model_data is not a dict, it's {type(model_data)}")
            return False
        
        # Create report
        report = f"""# Model Evaluation Report

## תאריך: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## מודל: {model_data.get('model_name', 'Unknown')}

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
        
        with open("outputs/evaluation_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("SUCCESS: evaluation_report.md created")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_model_card():
    """Create model_card.md"""
    print("Creating model_card.md...")
    
    try:
        # Load model with error handling for numpy random state
        import warnings
        warnings.filterwarnings('ignore')
        
        try:
            # נשתמש ב-joblib.load תמיד - זה עובד נכון
            model_data = joblib.load("outputs/model.pkl")
            # בדיקה ש-model_data הוא dict
            if not isinstance(model_data, dict):
                print(f"ERROR: model_data is not a dict, it's {type(model_data)}")
                return False
        except Exception as e:
            # אם joblib נכשל, נציג שגיאה
            print(f"ERROR: Failed to load model with joblib: {str(e)}")
            print(f"ERROR: Exception type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
        
        # בדיקה סופית ש-model_data הוא dict (לפני השימוש)
        if not isinstance(model_data, dict):
            print(f"ERROR: model_data is not a dict, it's {type(model_data)}")
            return False
        
        with open("outputs/all_models_comparison.json", 'r', encoding='utf-8') as f:
            comparison = json.load(f)
        
        model_card = f"""# Model Card: Israel Housing Price Prediction

## Model Details

### Basic Information
- **Model Name**: {model_data.get('model_name', 'Unknown')}
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
- **Features**: 12 original + multiple engineered features

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
- **Train RMSE**: {model_data['metrics']['train_rmse']:.4f}

### Model Comparison
"""
        
        for comp in comparison:
            model_card += f"- **{comp['model_name']}**: Test RMSE = {comp['test_rmse']:.4f}, R² = {comp['test_r2']:.4f}\n"
        
        model_card += f"""
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
        
        with open("outputs/model_card.md", 'w', encoding='utf-8') as f:
            f.write(model_card)
        
        print("SUCCESS: model_card.md created")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("Creating missing evaluation files")
    print("="*60)
    
    success1 = create_evaluation_report()
    success2 = create_model_card()
    
    print("\n" + "="*60)
    if success1 and success2:
        print("All files created successfully!")
    else:
        print("Some files failed to create")
    print("="*60)

