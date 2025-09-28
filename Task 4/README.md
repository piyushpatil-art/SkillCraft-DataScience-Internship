🚦 Task 4 – US Traffic Accident Analysis (EDA & Visualization)

## 📌 Overview
This task focuses on analyzing the **US Accidents Dataset (March 2023)** using Python.  
The dataset is large (~7.7M records), so we perform **data cleaning, exploratory data analysis (EDA), and visualization** to uncover key accident trends and insights.  

---

## 📊 Dataset
- **Source**: [US Accidents (2016–2023) Dataset on Kaggle](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)  
- **File Used**: `US_Accidents_March23.csv` (download from Kaggle)  
- **Sample File Included**: `task4_sampled_cleaned.csv` (cleaned & reduced version for testing and visualization)  

---

## ⚙️ Steps Performed
1. **Data Loading**  
   - Loaded dataset (`US_Accidents_March23.csv`)  
   - Selected important columns (`ID, Severity, Start_Time, End_Time, Start_Lat, Start_Lng, Weather_Condition, Visibility(mi), Precipitation(in), Crossing, Traffic_Signal`)  

2. **Data Cleaning**  
   - Converted `Start_Time` to datetime  
   - Extracted **Hour** and **Day of Week** features  
   - Filled missing values (`Weather_Condition`, `Visibility`, `Precipitation`)  
   - Reduced dataset size by sampling 100,000 rows for efficiency  

3. **Exploratory Data Analysis (EDA)**  
   - Accidents by **Hour of the Day**  
   - Accidents by **Day of the Week**  
   - Top **Weather Conditions** during accidents  
   - Impact of **Road Features** (Crossing, Traffic Signal)  
   - Accident Hotspots (KDE plot of Lat & Lng)  

4. **Visualization**  
   - Used **Matplotlib & Seaborn** for graphs  
   - Saved all plots as `.png` files  

---

## 📌 Insights
- 🚗 Most accidents occur during **rush hours (7–9 AM, 4–7 PM)**  
- 📅 Weekdays show **higher accident frequency** compared to weekends  
- 🌧️ **Rain & fog** significantly increase accident likelihood  
- 🚦 Many accidents happen near **traffic signals and crossings**  
- 🏙️ Hotspot analysis reveals **urban areas are more prone** to accidents  

---

## 🤝 Connect with Me
If you found this project helpful or interesting, feel free to connect with me:  

🔗- **LinkedIn:** [www.linkedin.com/in/piyushpatil06](https://www.linkedin.com/in/piyushpatil06)
💻- **GitHub:** [https://github.com/piyushpatil-art](https://github.com/piyushpatil-art)

---

