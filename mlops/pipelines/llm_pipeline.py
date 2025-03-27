from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs
import yaml
import os
from datetime import datetime

class LLMPipeline:
    def __init__(self, config_path):
        """Initialize the LLM pipeline with configuration."""
        self.config = self._load_config(config_path)
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        self.region = self.config['monitoring']['region']
        
        # Initialize Vertex AI
        aiplatform.init(
            project=self.project_id,
            location=self.region
        )

    def _load_config(self, config_path):
        """Load pipeline configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def create_endpoints(self):
        """Create or update Vertex AI endpoints for LLM models."""
        for model in self.config['models']:
            endpoint = aiplatform.Endpoint.create(
                display_name=model['endpoint'],
                project=self.project_id,
                location=self.region
            )
            print(f"Created endpoint: {endpoint.display_name}")

    def deploy_models(self):
        """Deploy models to their respective endpoints."""
        for model in self.config['models']:
            endpoint = aiplatform.Endpoint.list(
                filter=f"display_name={model['endpoint']}",
                project=self.project_id,
                location=self.region
            )[0]
            
            # Deploy model with monitoring
            endpoint.deploy_all(
                model=model['name'],
                deployed_model_display_name=f"{model['name']}-{datetime.now().strftime('%Y%m%d')}",
                machine_type="n1-standard-4",
                accelerator_type="NVIDIA_TESLA_T4",
                accelerator_count=1,
                min_replica_count=self.config['deployment']['min_instances'],
                max_replica_count=self.config['deployment']['max_instances'],
                traffic_split={"0": 100},
                service_account=self.config['security']['authentication']['service_account'],
                enable_request_response_logging=True,
                request_response_logging_sampling_rate=1.0,
                enable_access_logging=True,
                enable_container_logging=True
            )
            print(f"Deployed model {model['name']} to endpoint {endpoint.display_name}")

    def setup_monitoring(self):
        """Set up monitoring for deployed models."""
        for model in self.config['models']:
            endpoint = aiplatform.Endpoint.list(
                filter=f"display_name={model['endpoint']}",
                project=self.project_id,
                location=self.region
            )[0]
            
            # Configure monitoring
            endpoint.set_monitoring_config(
                metrics=self.config['monitoring']['metrics'],
                alerts=self.config['monitoring']['alerts'],
                logging_config=self.config['logging']
            )
            print(f"Set up monitoring for endpoint {endpoint.display_name}")

    def setup_cost_management(self):
        """Set up cost management and budgeting."""
        from google.cloud import billing_v1
        
        client = billing_v1.CloudBillingClient()
        project_name = f"projects/{self.project_id}"
        
        # Get billing account
        project_billing_info = client.get_project_billing_info(name=project_name)
        billing_account = project_billing_info.billing_account_name
        
        # Set up budget
        budget = {
            "display_name": "AiDemy LLM Budget",
            "budget_filter": {
                "projects": [f"projects/{self.project_id}"]
            },
            "amount": {
                "specified_amount": {
                    "currency_code": "USD",
                    "units": str(self.config['cost_management']['budget'])
                }
            },
            "threshold_rules": [
                {
                    "threshold_percent": alert['threshold'] * 100,
                    "spend_basis": "CURRENT_SPEND"
                }
                for alert in self.config['cost_management']['alerts']
            ]
        }
        
        client.create_budget(
            parent=billing_account,
            budget=budget
        )
        print("Set up cost management and budgeting")

    def run_pipeline(self):
        """Run the complete pipeline."""
        print("Starting LLM pipeline...")
        
        # Create endpoints
        self.create_endpoints()
        
        # Deploy models
        self.deploy_models()
        
        # Set up monitoring
        self.setup_monitoring()
        
        # Set up cost management
        self.setup_cost_management()
        
        print("Pipeline completed successfully!")

def main():
    """Main function to run the pipeline."""
    config_path = "mlops/config/vertex_pipeline_config.yaml"
    pipeline = LLMPipeline(config_path)
    pipeline.run_pipeline()

if __name__ == "__main__":
    main() 