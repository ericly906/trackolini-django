from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

def bar_graph_constructor(artist, tracks, feature, label):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tracks, y=feature, marker_color="rgb(40, 15, 107)"))
    fig.update_layout(
        title=label + " of " + artist + " Tracks",
        xaxis_title="Tracks",
        yaxis_title=label,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_showticklabels=False
    )
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

def line_plot_constructor(time, feature, label):
    fig = px.line(x=time, y=feature)
    fig.update_layout(
        title_text=label,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        xaxis_title="Timestamp (Seconds)",
        yaxis_title=label,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")


def line_subplot_constructor(time, y1, y2, name1, name2):
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Scatter(x=time, y=y1, name=name1),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=time, y=y2, name=name2),
        row=1, col=2
    )

    fig.update_layout(
        title_text=name1,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="White"
        ),
        xaxis_title="Timestamp (Seconds)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis2 = dict(range=[0, 1]),
    )
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
