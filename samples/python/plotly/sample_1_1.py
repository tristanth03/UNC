import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Initial parameters
x_min = 0
x_max = 10
frequency = 1.0
amplitude = 1.0
phase = 0

def create_sine_plot(x_min, x_max, frequency, amplitude, phase):
    """Generate sine wave data"""
    x = np.linspace(x_min, x_max, 1000)
    y = amplitude * np.sin(2 * np.pi * frequency * x + phase)
    return x, y

# Create initial data
x, y = create_sine_plot(x_min, x_max, frequency, amplitude, phase)

# Create figure with buttons and sliders
fig = go.Figure()

# Add initial trace
fig.add_trace(go.Scatter(
    x=x, 
    y=y,
    mode='lines',
    name='sin(x)',
    line=dict(color='#1f77b4', width=3),
    hovertemplate='x: %{x:.2f}<br>y: %{y:.3f}<extra></extra>'
))

# Add buttons for quick adjustments
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(
                    args=[{"visible": [True]},
                          {"title": "Sine Wave Visualization"}],
                    label="Reset",
                    method="update"
                ),
                dict(
                    args=[{"xaxis.range": [0, 2*np.pi]}],
                    label="One Period",
                    method="relayout"
                ),
                dict(
                    args=[{"xaxis.range": [0, 6*np.pi]}],
                    label="Three Periods",
                    method="relayout"
                ),
            ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ]
)

# Add sliders for parameter control
fig.update_layout(
    sliders=[
        # Amplitude slider
        dict(
            active=0,
            yanchor="top",
            y=-0.15,
            xanchor="left",
            currentvalue=dict(
                prefix="Amplitude: ",
                visible=True,
                xanchor="center",
                font=dict(size=14)
            ),
            transition=dict(duration=300),
            pad=dict(b=10, t=50),
            len=0.9,
            x=0.05,
            steps=[
                dict(
                    args=[[f"Amplitude={amp:.1f}"]],
                    label=f"{amp:.1f}",
                    method="skip"
                )
                for amp in np.arange(0.1, 3.1, 0.1)
            ]
        ),
        # Frequency slider
        dict(
            active=0,
            yanchor="top",
            y=-0.25,
            xanchor="left",
            currentvalue=dict(
                prefix="Frequency: ",
                visible=True,
                xanchor="center",
                font=dict(size=14)
            ),
            transition=dict(duration=300),
            pad=dict(b=10, t=50),
            len=0.9,
            x=0.05,
            steps=[
                dict(
                    args=[[f"Frequency={freq:.1f}"]],
                    label=f"{freq:.1f}",
                    method="skip"
                )
                for freq in np.arange(0.5, 3.1, 0.1)
            ]
        ),
        # Phase slider
        dict(
            active=0,
            yanchor="top",
            y=-0.35,
            xanchor="left",
            currentvalue=dict(
                prefix="Phase (radians): ",
                visible=True,
                xanchor="center",
                font=dict(size=14)
            ),
            transition=dict(duration=300),
            pad=dict(b=10, t=50),
            len=0.9,
            x=0.05,
            steps=[
                dict(
                    args=[[f"Phase={phase:.2f}"]],
                    label=f"{phase:.2f}",
                    method="skip"
                )
                for phase in np.arange(0, 2*np.pi, 0.2)
            ]
        ),
    ]
)

# Update layout
fig.update_layout(
    title="Interactive Sine Wave Visualization",
    xaxis_title="x",
    yaxis_title="y = A·sin(2πfx + φ)",
    hovermode='x unified',
    plot_bgcolor='rgba(245, 245, 245, 0.5)',
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
    ),
    height=700,
    margin=dict(b=250),
    font=dict(size=12)
)

# Show the plot
fig.show()