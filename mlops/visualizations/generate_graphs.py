import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import json
import numpy as np
from pathlib import Path

class MLOpsVisualizer:
    def __init__(self):
        """Initialize the MLOps visualizer."""
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        self.graphs_dir = Path('mlops/visualizations/graphs')
        self.graphs_dir.mkdir(parents=True, exist_ok=True)
        
    def get_metric_data(self, metric_type, hours=24):
        """Fetch metric data from Cloud Monitoring."""
        now = datetime.utcnow()
        seconds = int(now.timestamp())
        nanos = int(now.microsecond * 1000)
        interval = monitoring_v3.TimeInterval({
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": int((now - timedelta(hours=hours)).timestamp())}
        })
        
        results = self.client.list_time_series(
            request={
                "name": self.project_name,
                "filter": f'metric.type = "{metric_type}"',
                "interval": interval,
            }
        )
        
        return results

    def create_latency_graph(self):
        """Create latency trend graph with box plot."""
        results = self.get_metric_data("aiplatform.googleapis.com/endpoint/prediction_latency")
        
        df = pd.DataFrame({
            'timestamp': [],
            'latency': []
        })
        
        for result in results:
            for point in result.points:
                df = pd.concat([df, pd.DataFrame({
                    'timestamp': [datetime.fromtimestamp(point.interval.end_time.seconds)],
                    'latency': [point.value.double_value]
                })])
        
        # Create time series plot
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['latency'],
            mode='lines+markers',
            name='Latency'
        ))
        
        fig_ts.update_layout(
            title='Model Latency Over Time',
            xaxis_title='Time',
            yaxis_title='Latency (ms)',
            template='plotly_dark'
        )
        
        # Create box plot
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df['latency'],
            name='Latency Distribution'
        ))
        
        fig_box.update_layout(
            title='Latency Distribution',
            yaxis_title='Latency (ms)',
            template='plotly_dark'
        )
        
        return fig_ts, fig_box

    def create_error_rate_graph(self):
        """Create error rate trend graph with heatmap."""
        results = self.get_metric_data("aiplatform.googleapis.com/endpoint/error_count")
        
        df = pd.DataFrame({
            'timestamp': [],
            'error_count': []
        })
        
        for result in results:
            for point in result.points:
                df = pd.concat([df, pd.DataFrame({
                    'timestamp': [datetime.fromtimestamp(point.interval.end_time.seconds)],
                    'error_count': [point.value.double_value]
                })])
        
        # Create time series plot
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['error_count'],
            mode='lines+markers',
            name='Error Count'
        ))
        
        fig_ts.update_layout(
            title='Error Rate Over Time',
            xaxis_title='Time',
            yaxis_title='Error Count',
            template='plotly_dark'
        )
        
        # Create heatmap
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day_name()
        pivot_table = df.pivot_table(
            values='error_count',
            index='day',
            columns='hour',
            aggfunc='mean'
        )
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='Reds'
        ))
        
        fig_heat.update_layout(
            title='Error Rate Heatmap by Hour and Day',
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            template='plotly_dark'
        )
        
        return fig_ts, fig_heat

    def create_token_usage_graph(self):
        """Create token usage trend graph with histogram."""
        results = self.get_metric_data("aiplatform.googleapis.com/endpoint/token_count")
        
        df = pd.DataFrame({
            'timestamp': [],
            'token_count': []
        })
        
        for result in results:
            for point in result.points:
                df = pd.concat([df, pd.DataFrame({
                    'timestamp': [datetime.fromtimestamp(point.interval.end_time.seconds)],
                    'token_count': [point.value.double_value]
                })])
        
        # Create time series plot
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['token_count'],
            mode='lines+markers',
            name='Token Usage'
        ))
        
        fig_ts.update_layout(
            title='Token Usage Over Time',
            xaxis_title='Time',
            yaxis_title='Token Count',
            template='plotly_dark'
        )
        
        # Create histogram
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df['token_count'],
            name='Token Usage Distribution',
            nbinsx=50
        ))
        
        fig_hist.update_layout(
            title='Token Usage Distribution',
            xaxis_title='Token Count',
            yaxis_title='Frequency',
            template='plotly_dark'
        )
        
        return fig_ts, fig_hist

    def create_cost_graph(self):
        """Create cost trend graph with pie chart."""
        results = self.get_metric_data("aiplatform.googleapis.com/endpoint/cost")
        
        df = pd.DataFrame({
            'timestamp': [],
            'cost': []
        })
        
        for result in results:
            for point in result.points:
                df = pd.concat([df, pd.DataFrame({
                    'timestamp': [datetime.fromtimestamp(point.interval.end_time.seconds)],
                    'cost': [point.value.double_value]
                })])
        
        # Create time series plot
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['cost'],
            mode='lines+markers',
            name='Cost'
        ))
        
        fig_ts.update_layout(
            title='Cost Over Time',
            xaxis_title='Time',
            yaxis_title='Cost (USD)',
            template='plotly_dark'
        )
        
        # Create pie chart for cost distribution by day
        df['day'] = df['timestamp'].dt.day_name()
        daily_costs = df.groupby('day')['cost'].sum()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=daily_costs.index,
            values=daily_costs.values,
            hole=.3
        )])
        
        fig_pie.update_layout(
            title='Cost Distribution by Day',
            template='plotly_dark'
        )
        
        return fig_ts, fig_pie

    def save_graphs(self):
        """Save all graphs dynamically."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate and save all graphs
        graphs = {
            'latency': self.create_latency_graph(),
            'error_rate': self.create_error_rate_graph(),
            'token_usage': self.create_token_usage_graph(),
            'cost': self.create_cost_graph()
        }
        
        for metric, (fig_ts, fig_alt) in graphs.items():
            # Save time series plots
            fig_ts.write_html(self.graphs_dir / f'{metric}_ts_{timestamp}.html')
            fig_ts.write_image(self.graphs_dir / f'{metric}_ts_{timestamp}.png')
            
            # Save alternative visualizations
            fig_alt.write_html(self.graphs_dir / f'{metric}_alt_{timestamp}.html')
            fig_alt.write_image(self.graphs_dir / f'{metric}_alt_{timestamp}.png')
            
            # Save data as CSV
            df = pd.DataFrame({
                'timestamp': fig_ts.data[0].x,
                'value': fig_ts.data[0].y
            })
            df.to_csv(self.graphs_dir / f'{metric}_data_{timestamp}.csv', index=False)

def create_dashboard():
    """Create an interactive dashboard with MLOps metrics."""
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    visualizer = MLOpsVisualizer()
    
    app.layout = dbc.Container([
        html.H1("AiDemy MLOps Dashboard", className="text-center my-4"),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='latency-ts-graph')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='latency-box-graph')
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='error-ts-graph')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='error-heat-graph')
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='token-ts-graph')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='token-hist-graph')
            ], width=6)
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='cost-ts-graph')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='cost-pie-graph')
            ], width=6)
        ]),
        
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000,  # update every 5 minutes
            n_intervals=0
        )
    ])
    
    @app.callback(
        [Output('latency-ts-graph', 'figure'),
         Output('latency-box-graph', 'figure'),
         Output('error-ts-graph', 'figure'),
         Output('error-heat-graph', 'figure'),
         Output('token-ts-graph', 'figure'),
         Output('token-hist-graph', 'figure'),
         Output('cost-ts-graph', 'figure'),
         Output('cost-pie-graph', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_graphs(n):
        latency_ts, latency_box = visualizer.create_latency_graph()
        error_ts, error_heat = visualizer.create_error_rate_graph()
        token_ts, token_hist = visualizer.create_token_usage_graph()
        cost_ts, cost_pie = visualizer.create_cost_graph()
        
        # Save graphs on each update
        visualizer.save_graphs()
        
        return (
            latency_ts, latency_box,
            error_ts, error_heat,
            token_ts, token_hist,
            cost_ts, cost_pie
        )
    
    return app

def main():
    """Main function to generate and display MLOps visualizations."""
    print("📊 Generating MLOps visualizations...")
    
    try:
        # Create and run dashboard
        app = create_dashboard()
        print("\n🚀 Starting interactive dashboard...")
        print("Access the dashboard at: http://localhost:8050")
        print(f"Graphs will be saved to: {Path('mlops/visualizations/graphs').absolute()}")
        app.run_server(debug=True)
        
    except Exception as e:
        print(f"❌ Error generating visualizations: {str(e)}")
        raise

if __name__ == "__main__":
    main() 