# -*- coding: utf-8 -*-
"""Check what's in the model.pkl file"""
import os
import sys
import joblib
import pickle
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("Checking model.pkl file")
print("="*60)

if not os.path.exists("outputs/model.pkl"):
    print("ERROR: model.pkl not found")
    sys.exit(1)

print("\n1. Trying joblib.load...")
try:
    data = joblib.load("outputs/model.pkl")
    print(f"   Type: {type(data)}")
    print(f"   Is dict: {isinstance(data, dict)}")
    if isinstance(data, dict):
        print(f"   Keys: {list(data.keys())}")
        if 'model' in data:
            print(f"   Model type: {type(data['model'])}")
        if 'model_name' in data:
            print(f"   Model name: {data['model_name']}")
    else:
        print(f"   Shape (if array): {data.shape if hasattr(data, 'shape') else 'N/A'}")
        print(f"   First few elements: {data[:3] if hasattr(data, '__getitem__') else 'N/A'}")
except Exception as e:
    print(f"   ERROR: {str(e)}")
    print(f"   Exception type: {type(e).__name__}")

print("\n2. Trying pickle directly...")
try:
    with open("outputs/model.pkl", 'rb') as f:
        data = pickle.load(f)
        print(f"   Type: {type(data)}")
        print(f"   Is dict: {isinstance(data, dict)}")
        if isinstance(data, dict):
            print(f"   Keys: {list(data.keys())}")
except Exception as e:
    print(f"   ERROR: {str(e)}")

print("\n" + "="*60)

