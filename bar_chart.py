import plotly.graph_objects as go
import numpy as np
import datetime

# 1. Generate years & data
current_year = datetime.datetime.now().year
years = np.arange(1960, current_year + 1)

# Simulate population growth (in millions)
base_male = np.linspace(1500, 4000, len(years))
base_female = np.linspace(1400, 3900, len(years))

male_population = base_male + np.random.randint(-100, 100, len(years))
female_population = base_female + np.random.randint(-100, 100, len(years))

# 2. Create stacked bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=years,
    y=male_population,
    name='Male Population',
    marker_color='#4A90E2'
))

fig.add_trace(go.Bar(
    x=years,
    y=female_population,
    name='Female Population',
    marker_color='#FF69B4'
))

# 3. Customize layout
fig.update_layout(
    barmode='stack',
    title=f"Population Distribution (1960 - {current_year})",
    xaxis=dict(
        title="Year",
        rangeslider=dict(visible=True),  # Adds draggable slider at bottom
        range=[years[-10], years[-1]]   # Show last 10 years initially
    ),
    yaxis=dict(title="Population (in millions)"),
    legend=dict(title="Gender"),
    template='plotly_white',
    height=500
)

# 4. Show figure
fig.show()
