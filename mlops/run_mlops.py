import os
from datetime import datetime
from pipelines.llm_pipeline import LLMPipeline
from google.cloud import monitoring_v3
from google.cloud import logging
import json

def setup_environment():
    """Set up environment variables and authentication."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verify required environment variables
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def create_monitoring_client():
    """Create a monitoring client for metrics."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
    return client, project_name

def create_logging_client():
    """Create a logging client for structured logging."""
    client = logging.Client()
    return client

def log_metrics(client, project_name, metrics):
    """Log custom metrics to Cloud Monitoring."""
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/aidemy/metrics"
    
    # Add metric labels
    series.metric.labels["service"] = "aidemy"
    series.metric.labels["environment"] = os.getenv('ENVIRONMENT', 'development')
    
    # Create time series data
    point = monitoring_v3.Point()
    point.value.double_value = metrics['value']
    
    # Set timestamp
    now = datetime.utcnow()
    seconds = int(now.timestamp())
    nanos = int(now.microsecond * 1000)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point.interval = interval
    
    series.points = [point]
    
    # Write time series
    client.create_time_series(
        request={"name": project_name, "time_series": [series]}
    )

def main():
    """Main function to demonstrate MLOps functionality."""
    print("🚀 Starting AiDemy MLOps Demo...")
    
    try:
        # Set up environment
        setup_environment()
        print("✅ Environment setup complete")
        
        # Initialize monitoring
        monitoring_client, project_name = create_monitoring_client()
        print("✅ Monitoring client initialized")
        
        # Initialize logging
        logging_client = create_logging_client()
        logger = logging_client.logger('aidemy-mlops')
        print("✅ Logging client initialized")
        
        # Load and run pipeline
        config_path = "mlops/config/vertex_pipeline_config.yaml"
        pipeline = LLMPipeline(config_path)
        
        # Log pipeline start
        logger.info("Starting LLM pipeline", extra={
            "pipeline_name": pipeline.config['pipeline']['name'],
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Run pipeline steps
        print("\n📊 Running Pipeline Steps:")
        
        # 1. Create endpoints
        print("\n1️⃣ Creating endpoints...")
        pipeline.create_endpoints()
        log_metrics(monitoring_client, project_name, {
            "value": 1,
            "metric": "endpoints_created"
        })
        
        # 2. Deploy models
        print("\n2️⃣ Deploying models...")
        pipeline.deploy_models()
        log_metrics(monitoring_client, project_name, {
            "value": len(pipeline.config['models']),
            "metric": "models_deployed"
        })
        
        # 3. Set up monitoring
        print("\n3️⃣ Setting up monitoring...")
        pipeline.setup_monitoring()
        log_metrics(monitoring_client, project_name, {
            "value": 1,
            "metric": "monitoring_configured"
        })
        
        # 4. Set up cost management
        print("\n4️⃣ Setting up cost management...")
        pipeline.setup_cost_management()
        log_metrics(monitoring_client, project_name, {
            "value": pipeline.config['cost_management']['budget'],
            "metric": "budget_configured"
        })
        
        # Log pipeline completion
        logger.info("Pipeline completed successfully", extra={
            "pipeline_name": pipeline.config['pipeline']['name'],
            "timestamp": datetime.utcnow().isoformat(),
            "models_deployed": len(pipeline.config['models'])
        })
        
        print("\n✅ Pipeline completed successfully!")
        
        # Display monitoring dashboard URL
        print("\n📈 Monitoring Dashboard:")
        print(f"https://console.cloud.google.com/monitoring/dashboards/custom/aidemy-llm-dashboard?project={os.getenv('GOOGLE_CLOUD_PROJECT')}")
        
    except Exception as e:
        # Log error
        logger.error(f"Pipeline failed: {str(e)}", extra={
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
        raise

if __name__ == "__main__":
    main() 