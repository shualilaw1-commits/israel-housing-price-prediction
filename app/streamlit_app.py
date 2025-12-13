"""
Streamlit Dashboard - ממשק אינטראקטיבי לפרויקט חיזוי מחירי דירות
"""
import warnings
# דיכוי אזהרות על גרסאות scikit-learn לא תואמות
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*Trying to unpickle.*')
warnings.filterwarnings('ignore', message='.*version.*when using version.*')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
import joblib
from datetime import datetime

# הוספת נתיב הפרויקט
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# קונפיגורציה
st.set_page_config(
    page_title="House Price Prediction 🏠",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS מותאם
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def check_outputs_exist():
    """בודק אם קיימים קבצי output"""
    required_files = [
        "outputs/clean_data.csv",
        "outputs/model.pkl",
        "outputs/dataset_contract.json"
    ]
    return all(os.path.exists(f) for f in required_files)


def load_data():
    """טוען את כל הנתונים הנדרשים"""
    try:
        data = {}

        # נתונים מנוקים
        if os.path.exists("outputs/clean_data.csv"):
            data['clean_data'] = pd.read_csv("outputs/clean_data.csv")

        # פיצ'רים
        if os.path.exists("outputs/features.csv"):
            data['features'] = pd.read_csv("outputs/features.csv")

        # Dataset contract
        if os.path.exists("outputs/dataset_contract.json"):
            with open("outputs/dataset_contract.json", 'r', encoding='utf-8') as f:
                data['contract'] = json.load(f)

        # השוואת מודלים
        if os.path.exists("outputs/all_models_comparison.json"):
            with open("outputs/all_models_comparison.json", 'r', encoding='utf-8') as f:
                data['model_comparison'] = json.load(f)

        # מודל
        if os.path.exists("outputs/model.pkl"):
            # דיכוי אזהרות על גרסאות לא תואמות בעת טעינת המודל
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                try:
                    # ניסיון טעינה רגילה עם joblib
                    model_data = joblib.load("outputs/model.pkl")
                    
                    # בדיקה שהנתונים שנטענו הם dict
                    if isinstance(model_data, dict):
                        # בדיקה שהמודל מכיל את כל המפתחות הנדרשים
                        if 'model' in model_data and 'model_name' in model_data and 'metrics' in model_data:
                            data['model_data'] = model_data
                        else:
                            # אם חסרים מפתחות, נציג שגיאה
                            missing_keys = []
                            if 'model' not in model_data:
                                missing_keys.append('model')
                            if 'model_name' not in model_data:
                                missing_keys.append('model_name')
                            if 'metrics' not in model_data:
                                missing_keys.append('metrics')
                            st.error(f"⚠️ המודל נטען אבל חסרים מפתחות: {', '.join(missing_keys)}. נסה לאמן מחדש את המודל.")
                            data['model_data'] = None
                    else:
                        # אם זה לא dict, נציג שגיאה
                        st.error(f"⚠️ המודל נטען אבל בפורמט לא תקין (סוג: {type(model_data)}). נסה לאמן מחדש את המודל.")
                        data['model_data'] = None
                        
                except Exception as e:
                    # אם יש בעיה בטעינה, נציג שגיאה ברורה
                    import traceback
                    error_details = traceback.format_exc()
                    st.error(f"⚠️ בעיה בטעינת המודל: {str(e)}")
                    st.info("💡 **פתרון**: הרץ את הסקריפט הבא כדי לאמן מחדש את המודל:")
                    st.code("cd house-price-crewai\npython train_model_manually.py", language="bash")
                    # הצגת פרטי שגיאה בפיתוח
                    with st.expander("פרטי שגיאה (לפיתוח)"):
                        st.code(error_details, language="python")
                    data['model_data'] = None

        # תובנות
        if os.path.exists("outputs/insights.md"):
            with open("outputs/insights.md", 'r', encoding='utf-8') as f:
                data['insights'] = f.read()

        # דוח הערכה
        if os.path.exists("outputs/evaluation_report.md"):
            with open("outputs/evaluation_report.md", 'r', encoding='utf-8') as f:
                data['evaluation'] = f.read()

        # Model Card
        if os.path.exists("outputs/model_card.md"):
            with open("outputs/model_card.md", 'r', encoding='utf-8') as f:
                data['model_card'] = f.read()

        return data

    except Exception as e:
        st.error(f"שגיאה בטעינת הנתונים: {str(e)}")
        return {}


def home_page():
    """עמוד הבית"""
    st.markdown('<div class="main-header">🏠 חיזוי מחירי דירות בישראל</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">פרויקט CrewAI עם 6 סוכנים אוטונומיים</div>', unsafe_allow_html=True)

    # בדיקה אם הפרויקט רץ
    if not check_outputs_exist():
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.warning("⚠️ הפרויקט עדיין לא רץ!")
        st.write("אנא הרץ תחילה:")
        st.code("python run.py", language="bash")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # טעינת נתונים
    data = load_data()
    
    # בדיקה אם המודל לא נטען
    if 'model_data' not in data or data['model_data'] is None:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.warning("⚠️ המודל לא נטען או לא אומן!")
        st.write("**פתרון:** הרץ את הסקריפט הבא כדי לאמן את המודל:")
        st.code("cd house-price-crewai\npython train_model_manually.py", language="bash")
        st.markdown('</div>', unsafe_allow_html=True)
        # נמשיך להציג את שאר הנתונים גם אם המודל לא נטען

    # סטטיסטיקות כלליות
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📊 שורות נתונים",
            value=f"{len(data['clean_data']):,}" if 'clean_data' in data else "N/A"
        )

    with col2:
        st.metric(
            label="🔢 פיצ'רים",
            value=len(data['features'].columns) if 'features' in data else "N/A"
        )

    with col3:
        if 'model_data' in data and data['model_data'] is not None and isinstance(data['model_data'], dict) and 'metrics' in data['model_data']:
            try:
                st.metric(
                    label="🎯 R² Score",
                    value=f"{data['model_data']['metrics']['test_r2']:.3f}"
                )
            except (KeyError, TypeError, IndexError):
                st.metric(
                    label="🎯 R² Score",
                    value="N/A"
                )
        else:
            st.metric(
                label="🎯 R² Score",
                value="N/A"
            )

    with col4:
        if 'model_data' in data and data['model_data'] is not None and isinstance(data['model_data'], dict) and 'metrics' in data['model_data']:
            try:
                st.metric(
                    label="📉 RMSE",
                    value=f"{data['model_data']['metrics']['test_rmse']:.4f}"
                )
            except (KeyError, TypeError, IndexError):
                st.metric(
                    label="📉 RMSE",
                    value="N/A"
                )
        else:
            st.metric(
                label="📉 RMSE",
                value="N/A"
            )

    st.markdown("---")

    # סקירת הפרויקט
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 סקירת הפרויקט")
        st.write("""
        פרויקט זה משתמש ב-**CrewAI Flow** עם **שני צוותים** של סוכנים:

        **צוות 1: מנתחי נתונים** (3 סוכנים)
        - 🔍 Data Ingestion Agent - טוען נתונים
        - 🧹 Data Cleaning Agent - מנקה נתונים
        - 📊 EDA Agent - יוצר ויזואליזציות

        **צוות 2: מדעני נתונים** (3 סוכנים)
        - 🔧 Feature Engineer - יוצר פיצ'רים
        - 🤖 Model Trainer - מאמן מודלים
        - ✅ Model Evaluator - מעריך ומתעד
        """)

    with col2:
        st.subheader("🎯 תוצרים")
        if 'contract' in data:
            st.write(f"""
            ✅ **Dataset Contract**: {data['contract'].get('num_rows', 'N/A'):,} שורות
            ✅ **נתונים מנוקים**: outputs/clean_data.csv
            ✅ **פיצ'רים מהונדסים**: outputs/features.csv
            ✅ **מודל מאומן**: {data['model_data'].get('model_name', 'N/A') if 'model_data' in data and data['model_data'] is not None and isinstance(data['model_data'], dict) else 'N/A'}
            ✅ **דוחות**: insights, evaluation, model card
            ✅ **ויזואליזציות**: figures + evaluation_figures
            """)

    st.markdown("---")

    # גרפים מהירים
    if 'clean_data' in data:
        st.subheader("📈 התפלגות מחירי דירות")
        
        df = data['clean_data']
        # מציאת עמודת המחיר
        price_col = None
        if 'Price_Millions' in df.columns:
            price_col = 'Price_Millions'
            price_label = 'מחיר בית (במיליוני ש"ח)'
        elif 'MedHouseVal' in df.columns:
            price_col = 'MedHouseVal'
            price_label = 'מחיר בית (ב-$100k)'  # תמיכה לאחור
        else:
            # נסה למצוא עמודת מחיר
            possible_cols = [col for col in df.columns if 'price' in col.lower() or 'מחיר' in col.lower() or 'val' in col.lower()]
            if possible_cols:
                price_col = possible_cols[0]
                price_label = f'מחיר ({price_col})'
            else:
                st.warning("לא נמצאה עמודת מחיר בנתונים")
                return

        fig = px.histogram(
            df,
            x=price_col,
            nbins=50,
            title="התפלגות מחירי דירות",
            labels={price_col: price_label},
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})


def data_exploration_page():
    """עמוד חקר נתונים"""
    st.header("📊 חקר נתונים")

    data = load_data()

    if 'clean_data' not in data:
        st.warning("אין נתונים זמינים. הרץ את הפרויקט תחילה.")
        return

    df = data['clean_data']

    # סטטיסטיקות
    st.subheader("📋 סטטיסטיקות תיאוריות")
    st.dataframe(df.describe(), use_container_width=True)

    # ויזואליזציות
    st.subheader("📈 ויזואליזציות")

    viz_type = st.selectbox(
        "בחר סוג ויזואליזציה:",
        ["מפה גיאוגרפית", "מטריצת קורלציות", "התפלגויות", "Box Plots"]
    )

    if viz_type == "מפה גיאוגרפית":
        st.write("**מיקום דירות לפי מחיר**")
        # מציאת עמודות
        price_col = 'Price_Millions' if 'Price_Millions' in df.columns else ('MedHouseVal' if 'MedHouseVal' in df.columns else None)
        pop_col = 'Population' if 'Population' in df.columns else None
        hover_cols = []
        for col in ['Rooms', 'Size_sqm', 'AvgIncome', 'City', 'Floor', 'YearBuilt', 'Age', 'DistanceSea_km', 'DistanceCenter_km']:
            if col in df.columns:
                hover_cols.append(col)
        
        if price_col is None:
            st.warning("לא נמצאה עמודת מחיר בנתונים")
            return
        
        fig = px.scatter(
            df,
            x='Longitude',
            y='Latitude',
            color=price_col,
            size=pop_col if pop_col else None,
            hover_data=hover_cols if hover_cols else None,
            title='מיקום דירות בישראל',
            color_continuous_scale='Viridis',
            labels={price_col: 'מחיר (מיליוני ש"ח)' if price_col == 'Price_Millions' else 'מחיר ($100k)', 
                   pop_col: 'אוכלוסייה' if pop_col else None}
        )
        st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})

    elif viz_type == "מטריצת קורלציות":
        st.write("**קורלציות בין משתנים**")
        corr_matrix = df.corr()
        fig = px.imshow(
            corr_matrix,
            title='מטריצת קורלציות',
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})

    elif viz_type == "התפלגויות":
        st.write("**התפלגות משתנים**")
        column = st.selectbox("בחר משתנה:", df.columns)
        fig = px.histogram(df, x=column, nbins=50, title=f'התפלגות {column}')
        st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})

    elif viz_type == "Box Plots":
        st.write("**Box Plots - זיהוי outliers**")
        column = st.selectbox("בחר משתנה:", df.columns)
        fig = px.box(df, y=column, title=f'Box Plot - {column}')
        st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})

    # תובנות
    if 'insights' in data:
        st.subheader("💡 תובנות מהנתונים")
        st.markdown(data['insights'])


def model_performance_page():
    """עמוד ביצועי מודל"""
    st.header("🤖 ביצועי המודל")

    data = load_data()

    if 'model_data' not in data or data['model_data'] is None or not isinstance(data['model_data'], dict):
        st.warning("המודל עדיין לא אומן. הרץ את הפרויקט תחילה.")
        return

    # פרטי המודל
    st.subheader("ℹ️ פרטי המודל")
    col1, col2, col3 = st.columns(3)

    with col1:
        model_name = data['model_data'].get('model_name', 'N/A') if isinstance(data['model_data'], dict) else 'N/A'
        st.metric("שם המודל", model_name)

    with col2:
        if isinstance(data['model_data'], dict) and 'metrics' in data['model_data']:
            try:
                st.metric("Train RMSE", f"{data['model_data']['metrics'].get('train_rmse', 0):.4f}")
            except (KeyError, TypeError):
                st.metric("Train RMSE", "N/A")
        else:
            st.metric("Train RMSE", "N/A")

    with col3:
        if isinstance(data['model_data'], dict) and 'metrics' in data['model_data']:
            try:
                st.metric("Test RMSE", f"{data['model_data']['metrics'].get('test_rmse', 0):.4f}")
            except (KeyError, TypeError):
                st.metric("Test RMSE", "N/A")
        else:
            st.metric("Test RMSE", "N/A")

    # השוואת מודלים
    if 'model_comparison' in data and data['model_comparison'] is not None:
        try:
            st.subheader("📊 השוואת מודלים")

            # בדיקה שהנתונים הם list או dict
            if isinstance(data['model_comparison'], list) and len(data['model_comparison']) > 0:
                comparison_df = pd.DataFrame(data['model_comparison'])
                comparison_df = comparison_df.sort_values('test_rmse')
                
                # גרף השוואה
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    name='Train RMSE',
                    x=comparison_df['model_name'],
                    y=comparison_df['train_rmse'],
                    marker_color='lightblue'
                ))

                fig.add_trace(go.Bar(
                    name='Test RMSE',
                    x=comparison_df['model_name'],
                    y=comparison_df['test_rmse'],
                    marker_color='darkblue'
                ))

                fig.update_layout(
                    title='השוואת RMSE בין מודלים',
                    barmode='group',
                    xaxis_title='מודל',
                    yaxis_title='RMSE'
                )

                st.plotly_chart(fig, config={'displayModeBar': True, 'responsive': True})

                # טבלת השוואה
                st.dataframe(
                    comparison_df[['model_name', 'train_rmse', 'test_rmse', 'test_r2', 'training_time']],
                    use_container_width=True
                )
            else:
                st.warning("אין נתוני השוואה זמינים")
        except Exception as e:
            st.warning(f"בעיה בהצגת השוואת המודלים: {str(e)}")

    # דוח הערכה
    if 'evaluation' in data:
        st.subheader("📄 דוח הערכה מלא")
        st.markdown(data['evaluation'])

    # Model Card
    if 'model_card' in data:
        st.subheader("📋 Model Card")
        st.markdown(data['model_card'])


def prediction_page():
    """עמוד חיזויים"""
    st.header("🎯 חיזוי מחיר דירה")

    data = load_data()

    if 'model_data' not in data or data['model_data'] is None:
        st.warning("המודל עדיין לא אומן. הרץ את הפרויקט תחילה.")
        return

    st.write("הזן את מאפייני הדירה לחיזוי מחיר:")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("עיר", ["תל אביב", "ירושלים", "חיפה", "באר שבע", "רמת גן", "אשדוד", "נתניה", "בני ברק", "חולון", "רעננה"])
        size_sqm = st.slider("גודל (מ\"ר)", 40, 200, 100, 5)
        rooms = st.slider("מספר חדרים", 2, 6, 4, 1)
        floor = st.slider("קומה", 0, 15, 3, 1)
        year_built = st.slider("שנת בנייה", 1950, 2024, 2000, 1)

    with col2:
        distance_sea = st.slider("מרחק מהים (ק\"מ)", 0.0, 50.0, 5.0, 0.5)
        distance_center = st.slider("מרחק ממרכז העיר (ק\"מ)", 0.0, 20.0, 3.0, 0.5)
        population = st.slider("אוכלוסייה באזור (אלפים)", 10.0, 500.0, 100.0, 10.0)
        avg_income = st.slider("הכנסה ממוצעת באזור (אלפי ש\"ח)", 8.0, 30.0, 15.0, 0.5)

    if st.button("🔮 חזה מחיר", type="primary"):
        # בדיקה שהמודל קיים ותקין
        if data['model_data'] is None or 'model' not in data['model_data']:
            st.error("❌ המודל לא זמין. אנא אמן מחדש את המודל.")
            return
        
        # מיפוי ערים לקואורדינטות
        cities_coords = {
            'תל אביב': {'lat': 32.0853, 'lon': 34.7818},
            'ירושלים': {'lat': 31.7683, 'lon': 35.2137},
            'חיפה': {'lat': 32.7940, 'lon': 34.9896},
            'באר שבע': {'lat': 31.2530, 'lon': 34.7915},
            'רמת גן': {'lat': 32.0820, 'lon': 34.8138},
            'אשדוד': {'lat': 31.8044, 'lon': 34.6553},
            'נתניה': {'lat': 32.3333, 'lon': 34.8667},
            'בני ברק': {'lat': 32.0807, 'lon': 34.8338},
            'חולון': {'lat': 32.0100, 'lon': 34.7792},
            'רעננה': {'lat': 32.1844, 'lon': 34.8717},
        }
        
        city_coords = cities_coords.get(city, {'lat': 32.0, 'lon': 34.8})
        age = 2024 - year_built
        
        # יצירת DataFrame עם הקלט
        input_data = pd.DataFrame({
            'City': [city],
            'Latitude': [city_coords['lat']],
            'Longitude': [city_coords['lon']],
            'Size_sqm': [size_sqm],
            'Rooms': [rooms],
            'Floor': [floor],
            'YearBuilt': [year_built],
            'Age': [age],
            'DistanceSea_km': [distance_sea],
            'DistanceCenter_km': [distance_center],
            'Population': [population],
            'AvgIncome': [avg_income]
        })

        # הנדסת פיצ'רים (אותם פיצ'רים כמו באימון - מותאם לישראל)
        # הסרנו price_per_sqm - זה data leakage
        input_data['rooms_per_size'] = input_data['Rooms'] / (input_data['Size_sqm'] + 0.001)
        input_data['income_per_size'] = input_data['AvgIncome'] / (input_data['Size_sqm'] + 0.001)

        # מרכז ישראל
        center_lat, center_lon = 31.7683, 35.2137
        input_data['distance_to_center_israel'] = np.sqrt(
            (input_data['Latitude'] - center_lat)**2 +
            (input_data['Longitude'] - center_lon)**2
        )
        input_data['coastal_proximity'] = (input_data['DistanceSea_km'] < 10).astype(int)
        input_data['sea_proximity_score'] = 1 / (input_data['DistanceSea_km'] + 1)
        input_data['log_avg_income'] = np.log1p(input_data['AvgIncome'])

        # קטגוריית הכנסה
        if avg_income <= 10:
            income_cat = 0
        elif avg_income <= 15:
            income_cat = 1
        else:
            income_cat = 2
        input_data['income_category_encoded'] = income_cat

        # קטגוריית גיל
        if age <= 10:
            age_cat = 0
        elif age <= 30:
            age_cat = 1
        else:
            age_cat = 2
        input_data['age_category_encoded'] = age_cat

        input_data['income_per_room'] = input_data['AvgIncome'] * input_data['Rooms']
        input_data['size_income'] = input_data['Size_sqm'] * input_data['AvgIncome']
        # הסרנו location_price - זה data leakage, הוספנו location_score
        input_data['location_score'] = input_data['Latitude'] * input_data['Longitude']
        input_data['city_size_interaction'] = input_data['Size_sqm'] * input_data['Rooms']

        # המרת City ל-City_encoded (כמו באימון)
        # טעינת מיפוי הערים
        try:
            with open("outputs/city_mapping.json", 'r', encoding='utf-8') as f:
                city_mapping = json.load(f)
            input_data['City_encoded'] = city_mapping.get(city, 0)
        except:
            # אם אין מיפוי, נשתמש בקידוד פשוט
            cities_list = ["תל אביב", "ירושלים", "חיפה", "באר שבע", "רמת גן", "אשדוד", "נתניה", "בני ברק", "חולון", "רעננה"]
            input_data['City_encoded'] = cities_list.index(city) if city in cities_list else 0

        # הסרת עמודות לא מספריות (City) לפני החיזוי
        input_data_numeric = input_data.select_dtypes(include=[np.number])

        # חיזוי - צריך לוודא שהעמודות תואמות למודל
        # נטען את features.csv כדי לראות את המבנה
        try:
            features_df = pd.read_csv("outputs/features.csv")
            # נסיר את עמודת המחיר מהעמודות
            feature_columns = [col for col in features_df.columns if col != 'Price_Millions' and col != 'City']
            # נוודא שיש לנו את כל העמודות
            for col in feature_columns:
                if col not in input_data_numeric.columns:
                    # אם חסר, נוסיף ערך ברירת מחדל
                    input_data_numeric[col] = 0
            
            # נשתמש רק בעמודות שקיימות במודל
            input_for_prediction = input_data_numeric[feature_columns]
        except:
            # אם לא מצאנו features.csv, נשתמש בכל העמודות המספריות
            input_for_prediction = input_data_numeric
        
        # חיזוי
        # בדיקה ש-model_data הוא dict לפני שימוש ב-get()
        if not isinstance(data['model_data'], dict):
            st.error("❌ המודל לא זמין. אנא אמן מחדש את המודל.")
            return
        
        model = data['model_data'].get('model')
        scaler = data['model_data'].get('scaler')
        
        if model is None:
            st.error("❌ המודל לא זמין. אנא אמן מחדש את המודל.")
            return

        # דיכוי אזהרות בעת חיזוי
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                if scaler:
                    input_scaled = scaler.transform(input_for_prediction)
                    prediction = model.predict(input_scaled)[0]
                else:
                    prediction = model.predict(input_for_prediction)[0]
            except Exception as e:
                st.error(f"❌ שגיאה בחיזוי: {str(e)}")
                return

        # הצגת התוצאה
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.success(f"💰 המחיר החזוי: **{prediction:.2f} מיליון ש\"ח**")
        st.write(f"({prediction*1000000:,.0f} ש\"ח)")
        st.markdown('</div>', unsafe_allow_html=True)

        # הצגה על מפה
        st.subheader("📍 מיקום הדירה")
        map_df = pd.DataFrame({
            'lat': [city_coords['lat']],
            'lon': [city_coords['lon']],
            'price': [prediction]
        })
        st.map(map_df)


def main():
    """פונקציה ראשית"""

    # Sidebar
    st.sidebar.title("🧭 ניווט")
    page = st.sidebar.radio(
        "בחר עמוד:",
        ["🏠 עמוד הבית", "📊 חקר נתונים", "🤖 ביצועי מודל", "🎯 חיזוי מחיר"]
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("ℹ️ אודות")
    st.sidebar.info("""
    **פרויקט חיזוי מחירי דירות**

    טכנולוגיות:
    - CrewAI Flow
    - 6 Agents (2 Crews)
    - scikit-learn
    - Streamlit
    - Plotly

    נוצר על ידי: שוקי שועלי
    מייל: shuali.law1@gmail.com
    """)

    # הצגת העמוד הנבחר
    if page == "🏠 עמוד הבית":
        home_page()
    elif page == "📊 חקר נתונים":
        data_exploration_page()
    elif page == "🤖 ביצועי מודל":
        model_performance_page()
    elif page == "🎯 חיזוי מחיר":
        prediction_page()


if __name__ == "__main__":
    main()
