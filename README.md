# 🏠 Israel Housing Price Prediction - CrewAI Project

A complete machine learning project using **CrewAI Flow** with **6 autonomous agents** organized in 2 crews, implementing a full ML pipeline from data ingestion to model deployment.

**[עברית](README_HEBREW.md)** | [Quick Start Guide](START_GUIDE.md) | [Fixes Summary](FIXES_SUMMARY.md)

## 🎯 Project Overview

This project predicts Israeli housing prices using a multi-agent system powered by CrewAI. It demonstrates:

- ✅ **CrewAI Flow** orchestration with validation between crews
- ✅ **6 Autonomous Agents** (2 crews of 3 agents each)
- ✅ **Dataset Contract** for data governance
- ✅ **Multiple Model Variants** (3 different ML models)
- ✅ **Professional Documentation** (Model Card, Evaluation Reports)
- ✅ **Interactive Dashboard** (Streamlit)
- ✅ **Reproducible Pipeline**

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      HousePricePredictionFlow                   │
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

## 🤖 The 6 Agents

### Crew 1: Data Analysts
1. **Data Ingestion Agent** - Loads Israeli Housing dataset
2. **Data Cleaning Agent** - Handles missing values and outliers
3. **EDA Agent** - Creates visualizations and insights

### Crew 2: Data Scientists
4. **Feature Engineer** - Creates new meaningful features
5. **Model Trainer** - Trains 3 different models (Linear, RF, GB)
6. **Model Evaluator** - Evaluates and documents the best model

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or extract the project
cd house-price-crewai

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Pipeline

```bash
python run.py
```

This will:
- ✓ Load and clean the data
- ✓ Perform EDA
- ✓ Engineer features
- ✓ Train 3 models
- ✓ Evaluate and select the best model
- ✓ Generate comprehensive reports

**Expected runtime**: 2-5 minutes

### 3. Launch Dashboard

```bash
streamlit run app/streamlit_app.py
```

Opens in browser at: `http://localhost:8501`

## 📁 Project Structure

```
house-price-crewai/
├── crews/                          # Agent crews
│   ├── data_analyst_crew/
│   │   ├── __init__.py
│   │   ├── agents.py              # 3 data analyst agents
│   │   ├── tasks.py               # Their tasks
│   │   ├── tools.py               # Their tools
│   │   └── crew.py                # Crew orchestration
│   └── data_scientist_crew/
│       ├── __init__.py
│       ├── agents.py              # 3 data scientist agents
│       ├── tasks.py               # Their tasks
│       ├── tools.py               # Their tools
│       └── crew.py                # Crew orchestration
├── flow/
│   ├── __init__.py
│   └── housing_flow.py            # Main flow with validation
├── app/
│   ├── __init__.py
│   └── streamlit_app.py           # Interactive dashboard
├── outputs/                        # Generated artifacts
│   ├── raw_data.csv
│   ├── clean_data.csv
│   ├── features.csv
│   ├── dataset_contract.json      # Dataset contract
│   ├── insights.md                # EDA insights
│   ├── feature_engineering_report.md
│   ├── model.pkl                  # Best model
│   ├── all_models_comparison.json
│   ├── evaluation_report.md
│   ├── model_card.md              # Professional model card
│   ├── figures/                   # EDA visualizations
│   └── evaluation_figures/        # Model evaluation plots
├── run.py                         # Main execution script
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## 📈 Outputs

### Data Files
- `raw_data.csv` - Original dataset
- `clean_data.csv` - Cleaned dataset
- `features.csv` - Dataset with engineered features

### Documentation
- `dataset_contract.json` - Data governance contract
- `insights.md` - Key insights from EDA
- `feature_engineering_report.md` - Feature creation details
- `evaluation_report.md` - Model performance analysis
- `model_card.md` - Professional model documentation

### Models
- `model.pkl` - Best performing model
- `all_models_comparison.json` - Comparison of all 3 models

### Visualizations
- `figures/` - EDA visualizations (distributions, correlations, geographic)
- `evaluation_figures/` - Model evaluation plots (predicted vs actual, residuals)

## 🎓 Project Requirements Compliance

This project fulfills all course requirements:

| Requirement | Implementation | Status |
|------------|----------------|--------|
| CrewAI Flow | HousePricePredictionFlow with validation | ✅ |
| Multiple Crews | 2 crews (Analysts + Scientists) | ✅ |
| 6+ Agents | 3 + 3 agents | ✅ |
| Dataset Contract | JSON contract with metadata | ✅ |
| Model Variants | 3 models: Linear, RF, Gradient Boosting | ✅ |
| Model Card | Professional documentation | ✅ |
| Evaluation Report | Comprehensive performance analysis | ✅ |
| Dashboard | Streamlit with 4 pages | ✅ |
| Reproducibility | Automated pipeline with run.py | ✅ |

## 🔧 Customization

### Modify Agents

Edit agents in `crews/*/agents.py`:
```python
def your_custom_agent(self) -> Agent:
    return Agent(
        role="Your Role",
        goal="Your Goal",
        backstory="Your Backstory",
        tools=[YourCustomTool()],
        verbose=True
    )
```

### Add New Tools

Create tools in `crews/*/tools.py`:
```python
class YourCustomTool(BaseTool):
    name: str = "Your Tool Name"
    description: str = "What it does"

    def _run(self, **kwargs) -> str:
        # Your implementation
        return "Result"
```

### Modify the Flow

Edit `flow/housing_flow.py` to:
- Add validation steps
- Change crew execution order
- Add new crews

## 📊 Dashboard Features

The Streamlit dashboard includes:

1. **🏠 Home Page**
   - Project overview
   - Key metrics
   - Quick visualizations

2. **📊 Data Exploration**
   - Interactive visualizations
   - Geographic analysis
   - Correlation matrices
   - Distribution plots

3. **🤖 Model Performance**
   - Model comparison
   - Performance metrics
   - Full evaluation report
   - Model Card

4. **🎯 Price Prediction**
   - Interactive prediction form
   - Real-time price estimation
   - Location visualization

## 🛠️ Technologies Used

- **CrewAI 0.86.0** - Multi-agent orchestration
- **Python 3.8+** - Programming language
- **scikit-learn** - Machine learning
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Streamlit** - Dashboard framework
- **Matplotlib/Seaborn** - Static visualizations

## 📝 Model Performance

The system trains and compares 3 models:

1. **Linear Regression** - Baseline model
2. **Random Forest** - Ensemble tree-based model
3. **Gradient Boosting** - Advanced boosting model

The best model is automatically selected based on test RMSE.

**Typical Performance:**
- RMSE: ~0.5-0.7 (in units of $100k)
- R² Score: ~0.6-0.8
- MAE: ~0.4-0.6

## 🤝 Contributing

To extend this project:

1. Add new agents in `crews/`
2. Create new tools for agents
3. Enhance the dashboard
4. Add more ML models
5. Improve feature engineering

## 📄 License

This project is for educational purposes.

## 👥 Authors

שוקי שועלי - AI Course Final Project

## 🙏 Acknowledgments

- **CrewAI** for the amazing multi-agent framework
- **scikit-learn** for the California Housing dataset
- **Streamlit** for the easy-to-use dashboard framework

---

**Need Help?**

1. Check the outputs in `outputs/` folder
2. Read the generated markdown reports
3. Review the dashboard at `http://localhost:8501`
4. Check agent logs for debugging

**Happy Predicting! 🏠📊🤖**
