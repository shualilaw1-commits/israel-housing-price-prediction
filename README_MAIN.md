# 🏠 Israel Housing Price Prediction using CrewAI

**A Professional ML Project with Multi-Agent AI System**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.80%2B-green)](https://www.crewai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Educational-yellow)](LICENSE)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Author](#-author)

---

## 🎯 Project Overview

This project implements an end-to-end machine learning pipeline for predicting housing prices in Israel using **CrewAI's multi-agent framework**. Six autonomous agents work collaboratively in two specialized crews to handle data processing, analysis, model training, and evaluation.

### Why This Project Matters

- **Multi-Agent AI**: Demonstrates cutting-edge AI orchestration using CrewAI Flow
- **Production-Ready**: Includes data contracts, model cards, and comprehensive documentation
- **Israeli Market**: Adapted for Israeli housing market with local features (cities, distances, prices in ILS)
- **Interactive**: Full-featured Streamlit dashboard for exploration and predictions
- **Reproducible**: Automated pipeline from raw data to deployed model

---

## ✨ Key Features

### 🤖 Multi-Agent System
- **6 Autonomous Agents** organized in 2 specialized crews
- **CrewAI Flow** orchestration with validation between stages
- Collaborative problem-solving and task execution

### 📊 Complete ML Pipeline
- **Data Ingestion** with contract validation
- **Automated Cleaning** and preprocessing
- **Feature Engineering** with domain-specific features
- **Model Training** with 3 different algorithms
- **Comprehensive Evaluation** and documentation

### 🎨 Interactive Dashboard
- **Streamlit-based** web application
- **4 Main Pages**: Home, Data Exploration, Model Performance, Price Prediction
- **Real-time Predictions** with user inputs
- **Rich Visualizations** using Plotly

### 📝 Professional Documentation
- **Dataset Contract**: Data governance and validation
- **Model Card**: Model details, metrics, and limitations
- **Evaluation Report**: Comprehensive performance analysis
- **User Guides**: In Hebrew and English

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  HousePricePredictionFlow                       │
│                     (CrewAI Flow)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐    │
│  │  Data Analyst Crew   │   ──>   │ Data Scientist Crew  │    │
│  │  (3 Agents)          │         │ (3 Agents)           │    │
│  └──────────────────────┘         └──────────────────────┘    │
│           │                                  │                  │
│           ▼                                  ▼                  │
│  ┌─────────────────┐              ┌─────────────────┐         │
│  │ 1. Data Ingest  │              │ 4. Feature Eng  │         │
│  │ 2. Data Clean   │              │ 5. Model Train  │         │
│  │ 3. EDA          │              │ 6. Evaluation   │         │
│  └─────────────────┘              └─────────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The 6 Agents

#### Crew 1: Data Analysts 📊
1. **Data Ingestion Agent**
   - Loads Israeli housing dataset
   - Creates dataset contract
   - Validates data quality

2. **Data Cleaning Agent**
   - Handles missing values
   - Removes outliers
   - Preprocesses features

3. **EDA Agent**
   - Creates visualizations
   - Generates insights
   - Analyzes correlations

#### Crew 2: Data Scientists 🔬
4. **Feature Engineer**
   - Creates new features
   - Applies domain knowledge
   - Documents feature engineering

5. **Model Trainer**
   - Trains 3 ML models:
     - Linear Regression
     - Random Forest
     - Gradient Boosting
   - Performs hyperparameter tuning
   - Selects best model

6. **Model Evaluator**
   - Evaluates model performance
   - Creates model card
   - Generates evaluation report
   - Produces visualizations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) OpenAI API key for full CrewAI features

### Installation

```bash
# Clone the repository
git clone https://github.com/[YOUR-USERNAME]/israel-housing-price-prediction.git
cd israel-housing-price-prediction

# Install dependencies
pip install -r requirements.txt

# (Optional) Set up environment variables
# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### Running the Project

#### Option 1: Interactive Dashboard (Recommended)

**Windows:**
```bash
# Double-click on:
1_RUN_DASHBOARD.bat
```

**Manual:**
```bash
streamlit run app/streamlit_app.py
```

Opens at: `http://localhost:8501`

#### Option 2: Train Models

**Windows:**
```bash
# Double-click on:
2_TRAIN_MODEL.bat
```

**Manual:**
```bash
python train_model_manually.py
```

Time: ~6-7 minutes

#### Option 3: Full CrewAI Pipeline

**Windows:**
```bash
# Double-click on:
3_RUN_FULL_PROJECT.bat
```

**Manual:**
```bash
python run.py
```

Requires: OpenAI API key in `.env`

#### Option 4: System Check

**Windows:**
```bash
# Double-click on:
0_CHECK_SYSTEM.bat
```

Verifies: Python, packages, files, outputs

---

## 📚 Documentation

### Quick Links

- **[English Documentation](README.md)** - Full project documentation
- **[Hebrew Documentation](README_HEBREW.md)** - תיעוד מלא בעברית
- **[Quick Start Guide](START_GUIDE.md)** - Get started in 3 minutes
- **[GitHub Upload Guide](GITHUB_UPLOAD.md)** - How to upload to GitHub
- **[Project Summary](PROJECT_SUMMARY.md)** - High-level overview
- **[Setup Guide](SETUP.md)** - Detailed installation instructions

### Generated Documentation

After running the project, you'll find:

- `outputs/dataset_contract.json` - Data governance document
- `outputs/insights.md` - Data analysis insights
- `outputs/feature_engineering_report.md` - Feature documentation
- `outputs/evaluation_report.md` - Model evaluation
- `outputs/model_card.md` - Model documentation

---

## 📁 Project Structure

```
israel-housing-price-prediction/
│
├── 📁 crews/                       # CrewAI Agents and Crews
│   ├── data_analyst_crew/          # Crew 1 - Data Analysts
│   │   ├── agents.py               # 3 data analysis agents
│   │   ├── tasks.py                # Analysis tasks
│   │   ├── tools.py                # Data processing tools
│   │   └── crew.py                 # Crew orchestration
│   │
│   └── data_scientist_crew/        # Crew 2 - Data Scientists
│       ├── agents.py               # 3 ML agents
│       ├── tasks.py                # ML tasks
│       ├── tools.py                # ML tools
│       └── crew.py                 # Crew orchestration
│
├── 📁 flow/                        # CrewAI Flow
│   └── housing_flow.py             # Main flow logic
│
├── 📁 app/                         # Streamlit Dashboard
│   └── streamlit_app.py            # Web application
│
├── 📁 outputs/                     # Generated Files
│   ├── clean_data.csv              # Processed data
│   ├── features.csv                # Engineered features
│   ├── model.pkl                   # Trained model
│   ├── dataset_contract.json       # Data contract
│   ├── model_card.md               # Model documentation
│   └── evaluation_report.md        # Performance report
│
├── 📄 run.py                       # Main entry point
├── 📄 train_model_manually.py      # Standalone training
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
│
├── 🪟 0_CHECK_SYSTEM.bat           # System verification
├── 🪟 1_RUN_DASHBOARD.bat          # Launch dashboard
├── 🪟 2_TRAIN_MODEL.bat            # Train models
├── 🪟 3_RUN_FULL_PROJECT.bat       # Run full pipeline
└── 🪟 4_UPLOAD_TO_GITHUB.bat       # Upload to GitHub
```

---

## 🛠️ Technologies

### Core Frameworks
- **CrewAI 0.80+** - Multi-agent orchestration
- **Python 3.8+** - Programming language
- **Streamlit 1.28+** - Web dashboard

### Data Science Stack
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning

### Visualization
- **plotly** - Interactive charts
- **matplotlib** - Static plots
- **seaborn** - Statistical visualizations

### LLM Integration
- **OpenAI API** - Agent intelligence
- **langchain** - LLM tooling

---

## 📊 Expected Performance

Based on Israeli housing market data:

- **RMSE**: 0.5-0.7 (500k-700k ILS error)
- **R² Score**: 0.6-0.8 (60-80% variance explained)
- **MAE**: 0.4-0.6 (400k-600k ILS average error)

### Features Adapted for Israel

- Cities: Tel Aviv, Jerusalem, Haifa, Beer Sheva, etc.
- Distances: From sea, from city center (km)
- Income: Average income in thousands of ILS
- Prices: Housing prices in millions of ILS
- Geographic: Israeli coordinates (latitude/longitude)

---

## 👨‍💻 Author

**Shuki Shoali**
- Email: shuali.law1@gmail.com
- Project: Final Project - AI/ML Course

---

## 📄 License

This is an educational project - Free to use for learning purposes.

---

## 🙏 Acknowledgments

- **CrewAI** - For the amazing multi-agent framework
- **scikit-learn** - For ML tools and sample data structure
- **Streamlit** - For the dashboard framework
- **OpenAI** - For LLM capabilities

---

## 📞 Support

For questions or issues:

1. Check the [Hebrew Documentation](README_HEBREW.md)
2. Review the [Start Guide](START_GUIDE.md)
3. Email: shuali.law1@gmail.com

---

<div align="center">

**Creating Collaborative AI Agents - The Future of ML! 🤖🏠📊**

Made with ❤️ using CrewAI

</div>
