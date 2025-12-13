"""
בדיקת חיזוי המודל - בדיקה מהירה
"""
import pandas as pd
import numpy as np
import joblib
import json

# טעינת המודל
model_data = joblib.load("outputs/model.pkl")
model = model_data['model']
scaler = model_data.get('scaler')

print("="*60)
print("בדיקת חיזויי המודל")
print("="*60)
print(f"מודל: {model_data['model_name']}")
print(f"Test R²: {model_data['metrics']['test_r2']:.4f}")
print(f"Test RMSE: {model_data['metrics']['test_rmse']:.4f}")
print()

# טעינת נתוני האימון
features_df = pd.read_csv("outputs/features.csv")
feature_columns = [col for col in features_df.columns if col != 'Price_Millions']

print(f"עמודות פיצ'רים: {len(feature_columns)}")
print()

# דוגמאות לבדיקה
test_cases = [
    {
        "name": "דירה בתל אביב - 4 חדרים, 100 מ\"ר, חדשה",
        "City": "תל אביב",
        "Latitude": 32.0853,
        "Longitude": 34.7818,
        "Size_sqm": 100,
        "Rooms": 4,
        "Floor": 3,
        "YearBuilt": 2020,
        "Age": 4,
        "DistanceSea_km": 2.0,
        "DistanceCenter_km": 1.0,
        "Population": 200,
        "AvgIncome": 20.0
    },
    {
        "name": "דירה בירושלים - 3 חדרים, 80 מ\"ר, ישנה",
        "City": "ירושלים",
        "Latitude": 31.7683,
        "Longitude": 35.2137,
        "Size_sqm": 80,
        "Rooms": 3,
        "Floor": 2,
        "YearBuilt": 1980,
        "Age": 44,
        "DistanceSea_km": 50.0,
        "DistanceCenter_km": 2.0,
        "Population": 150,
        "AvgIncome": 15.0
    },
    {
        "name": "דירה בבאר שבע - 3 חדרים, 90 מ\"ר, בינונית",
        "City": "באר שבע",
        "Latitude": 31.2530,
        "Longitude": 34.7915,
        "Size_sqm": 90,
        "Rooms": 3,
        "Floor": 1,
        "YearBuilt": 2010,
        "Age": 14,
        "DistanceSea_km": 45.0,
        "DistanceCenter_km": 5.0,
        "Population": 100,
        "AvgIncome": 12.0
    }
]

# טעינת מיפוי ערים
with open("outputs/city_mapping.json", 'r', encoding='utf-8') as f:
    city_mapping = json.load(f)

for test_case in test_cases:
    print("-"*60)
    print(f"📍 {test_case['name']}")
    print("-"*60)

    # יצירת DataFrame
    input_data = pd.DataFrame([test_case])

    # הנדסת פיצ'רים (בדיוק כמו באימון)
    input_data['City_encoded'] = city_mapping.get(test_case['City'], 0)
    input_data['rooms_per_size'] = input_data['Rooms'] / (input_data['Size_sqm'] + 0.001)
    input_data['income_per_size'] = input_data['AvgIncome'] / (input_data['Size_sqm'] + 0.001)

    center_lat, center_lon = 31.7683, 35.2137
    input_data['distance_to_center_israel'] = np.sqrt(
        (input_data['Latitude'] - center_lat)**2 +
        (input_data['Longitude'] - center_lon)**2
    )
    input_data['coastal_proximity'] = (input_data['DistanceSea_km'] < 10).astype(int)
    input_data['sea_proximity_score'] = 1 / (input_data['DistanceSea_km'] + 1)
    input_data['log_avg_income'] = np.log1p(input_data['AvgIncome'])

    # קטגוריות
    if test_case['AvgIncome'] <= 10:
        income_cat = 0
    elif test_case['AvgIncome'] <= 15:
        income_cat = 1
    else:
        income_cat = 2
    input_data['income_category_encoded'] = income_cat

    if test_case['Age'] <= 10:
        age_cat = 0
    elif test_case['Age'] <= 30:
        age_cat = 1
    else:
        age_cat = 2
    input_data['age_category_encoded'] = age_cat

    input_data['income_per_room'] = input_data['AvgIncome'] * input_data['Rooms']
    input_data['size_income'] = input_data['Size_sqm'] * input_data['AvgIncome']
    input_data['location_score'] = input_data['Latitude'] * input_data['Longitude']
    input_data['city_size_interaction'] = input_data['Size_sqm'] * input_data['Rooms']

    # הסרת City והמרה למספרים
    input_data = input_data.drop('City', axis=1)
    input_data_numeric = input_data.select_dtypes(include=[np.number])

    # וידוא שכל העמודות קיימות
    for col in feature_columns:
        if col not in input_data_numeric.columns:
            input_data_numeric[col] = 0

    # שימוש רק בעמודות הנכונות בסדר הנכון
    input_for_prediction = input_data_numeric[feature_columns]

    # חיזוי
    if scaler:
        input_scaled = scaler.transform(input_for_prediction)
        prediction = model.predict(input_scaled)[0]
    else:
        prediction = model.predict(input_for_prediction)[0]

    print(f"💰 מחיר חזוי: {prediction:.2f} מיליון ש\"ח")
    print(f"   ({prediction*1000000:,.0f} ש\"ח)")

    # השוואה למחיר ממוצע בעיר
    city_data = features_df[features_df['City_encoded'] == city_mapping.get(test_case['City'], 0)]
    if len(city_data) > 0:
        avg_price = city_data['Price_Millions'].mean()
        print(f"   מחיר ממוצע ב{test_case['City']}: {avg_price:.2f} מיליון ש\"ח")
        diff = ((prediction - avg_price) / avg_price) * 100
        if diff > 0:
            print(f"   ההפרש: +{diff:.1f}% מהממוצע")
        else:
            print(f"   ההפרש: {diff:.1f}% מהממוצע")
    print()

print("="*60)
print("בדיקה הושלמה!")
print("="*60)
