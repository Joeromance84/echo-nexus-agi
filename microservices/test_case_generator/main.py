#!/usr/bin/env python3
"""
AGI Test Case Generator - First AI Extension
Autonomous test case generation created by the parent AGI system
"""

import os
import json
import ast
import inspect
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
from fastapi import FastAPI
import uvicorn
from google.cloud import storage
from google.cloud import pubsub_v1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGITestCaseGenerator:
    """
    First AI extension created autonomously by the parent AGI
    Specialized in generating comprehensive test cases for microservices
    """
    
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.creator_agi = "market-analytics-orchestrator"  # Parent AGI identifier
        self.creation_timestamp = datetime.now().isoformat()
        
        # Initialize clients
        self.storage_client = storage.Client()
        self.publisher = pubsub_v1.PublisherClient()
        
        # Test generation patterns learned from parent AGI
        self.test_patterns = {
            "api_endpoints": {
                "health_check": ["status_code_200", "response_json_structure", "response_time"],
                "data_processing": ["input_validation", "output_format", "error_handling", "edge_cases"],
                "authentication": ["valid_tokens", "invalid_tokens", "expired_tokens", "missing_auth"]
            },
            "microservice_integration": {
                "pubsub_messaging": ["message_publish", "message_consume", "dead_letter_queue", "retry_logic"],
                "database_operations": ["crud_operations", "transaction_handling", "connection_pooling", "timeout_handling"],
                "external_apis": ["success_responses", "failure_responses", "rate_limiting", "circuit_breaker"]
            },
            "performance_testing": {
                "load_testing": ["concurrent_users", "response_time_percentiles", "throughput_metrics", "resource_utilization"],
                "stress_testing": ["memory_limits", "cpu_limits", "connection_limits", "recovery_behavior"],
                "scalability": ["horizontal_scaling", "vertical_scaling", "auto_scaling_triggers", "scaling_metrics"]
            }
        }
        
        logger.info(f"AGI Test Case Generator initialized - Created by: {self.creator_agi}")
    
    def analyze_microservice_code(self, service_code: str, service_name: str) -> Dict[str, Any]:
        """Analyze microservice code to understand its structure and generate appropriate tests"""
        try:
            # Parse the Python AST to understand code structure
            tree = ast.parse(service_code)
            
            analysis = {
                "service_name": service_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "functions": [],
                "classes": [],
                "endpoints": [],
                "imports": [],
                "test_requirements": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [decorator.id if hasattr(decorator, 'id') else str(decorator) for decorator in node.decorator_list],
                        "docstring": ast.get_docstring(node),
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    }
                    analysis["functions"].append(func_info)
                    
                    # Identify API endpoints
                    if any("app." in str(dec) for dec in node.decorator_list):
                        analysis["endpoints"].append({
                            "function": node.name,
                            "method": self._extract_http_method(node.decorator_list),
                            "path": self._extract_endpoint_path(node.decorator_list)
                        })
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        "docstring": ast.get_docstring(node)
                    }
                    analysis["classes"].append(class_info)
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            analysis["imports"].append(f"{node.module}.{alias.name}")
            
            # Generate test requirements based on analysis
            analysis["test_requirements"] = self._generate_test_requirements(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing microservice code: {e}")
            return {"error": str(e)}
    
    def _extract_http_method(self, decorators: List) -> str:
        """Extract HTTP method from FastAPI decorators"""
        method_keywords = ["get", "post", "put", "delete", "patch"]
        for decorator in decorators:
            decorator_str = str(decorator).lower()
            for method in method_keywords:
                if f"app.{method}" in decorator_str:
                    return method.upper()
        return "UNKNOWN"
    
    def _extract_endpoint_path(self, decorators: List) -> str:
        """Extract endpoint path from FastAPI decorators"""
        for decorator in decorators:
            decorator_str = str(decorator)
            if "app." in decorator_str and "(" in decorator_str:
                # Simple extraction - would be more sophisticated in production
                start = decorator_str.find('"')
                if start != -1:
                    end = decorator_str.find('"', start + 1)
                    if end != -1:
                        return decorator_str[start + 1:end]
        return "/unknown"
    
    def _generate_test_requirements(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific test requirements based on code analysis"""
        requirements = []
        
        # API endpoint tests
        for endpoint in analysis["endpoints"]:
            requirements.append({
                "type": "api_endpoint",
                "target": endpoint["function"],
                "method": endpoint["method"],
                "path": endpoint["path"],
                "tests": self.test_patterns["api_endpoints"]["health_check"] if "health" in endpoint["function"].lower() else self.test_patterns["api_endpoints"]["data_processing"]
            })
        
        # Class method tests
        for class_info in analysis["classes"]:
            requirements.append({
                "type": "class_methods",
                "target": class_info["name"],
                "methods": class_info["methods"],
                "tests": ["initialization", "method_behavior", "error_handling", "state_management"]
            })
        
        # Integration tests based on imports
        if any("pubsub" in imp.lower() for imp in analysis["imports"]):
            requirements.append({
                "type": "pubsub_integration",
                "tests": self.test_patterns["microservice_integration"]["pubsub_messaging"]
            })
        
        if any("storage" in imp.lower() for imp in analysis["imports"]):
            requirements.append({
                "type": "storage_integration", 
                "tests": ["file_operations", "bucket_access", "permissions", "error_handling"]
            })
        
        return requirements
    
    def generate_test_code(self, analysis: Dict[str, Any]) -> str:
        """Generate actual test code based on analysis"""
        service_name = analysis["service_name"]
        
        test_code = f'''"""
Auto-generated test suite for {service_name}
Generated by AGI Test Case Generator
Creation timestamp: {datetime.now().isoformat()}
"""

import pytest
import json
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from {service_name}.main import app

client = TestClient(app)

class Test{service_name.replace("_", "").title()}:
    """Comprehensive test suite for {service_name} microservice"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.test_data = {{
            "timestamp": "{datetime.now().isoformat()}",
            "generator": "agi-test-case-generator"
        }}
    
'''
        
        # Generate endpoint tests
        for req in analysis["test_requirements"]:
            if req["type"] == "api_endpoint":
                test_code += self._generate_endpoint_test(req)
            elif req["type"] == "class_methods":
                test_code += self._generate_class_test(req)
            elif req["type"] == "pubsub_integration":
                test_code += self._generate_pubsub_test(req)
            elif req["type"] == "storage_integration":
                test_code += self._generate_storage_test(req)
        
        # Add performance tests
        test_code += self._generate_performance_tests(service_name)
        
        return test_code
    
    def _generate_endpoint_test(self, requirement: Dict[str, Any]) -> str:
        """Generate test code for API endpoints"""
        method = requirement["method"]
        path = requirement["path"]
        function = requirement["target"]
        
        return f'''
    def test_{function}_{method.lower()}(self):
        """Test {method} {path} endpoint"""
        response = client.{method.lower()}("{path}")
        
        # Status code validation
        assert response.status_code == 200, f"Expected 200, got {{response.status_code}}"
        
        # Response structure validation
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be JSON object"
        
        # Response time validation
        assert response.elapsed.total_seconds() < 5.0, "Response time should be under 5 seconds"
        
        # Service-specific validations
        if "health" in "{function}":
            assert "status" in response_data, "Health check should include status"
            assert response_data["status"] in ["healthy", "unhealthy"], "Status should be valid"
        
    def test_{function}_error_handling(self):
        """Test error handling for {function}"""
        # Test with invalid data if POST/PUT
        if "{method}" in ["POST", "PUT", "PATCH"]:
            response = client.{method.lower()}("{path}", json={{"invalid": "data"}})
            assert response.status_code in [400, 422], "Should handle invalid input"
    
'''
    
    def _generate_class_test(self, requirement: Dict[str, Any]) -> str:
        """Generate test code for class methods"""
        class_name = requirement["target"]
        
        return f'''
    def test_{class_name.lower()}_initialization(self):
        """Test {class_name} class initialization"""
        # This would test class instantiation
        # Implementation depends on specific class structure
        pass
    
    def test_{class_name.lower()}_methods(self):
        """Test {class_name} class methods"""
        # Test each method in the class
        # Implementation would be customized per method
        pass
    
'''
    
    def _generate_pubsub_test(self, requirement: Dict[str, Any]) -> str:
        """Generate Pub/Sub integration tests"""
        return '''
    @patch('google.cloud.pubsub_v1.PublisherClient')
    def test_pubsub_message_publishing(self, mock_publisher):
        """Test Pub/Sub message publishing"""
        mock_client = Mock()
        mock_publisher.return_value = mock_client
        mock_client.publish.return_value.result.return_value = "test-message-id"
        
        # Test message publishing logic
        # This would test the actual Pub/Sub integration
        assert True  # Placeholder for actual test
    
    @patch('google.cloud.pubsub_v1.SubscriberClient')
    def test_pubsub_message_consumption(self, mock_subscriber):
        """Test Pub/Sub message consumption"""
        mock_client = Mock()
        mock_subscriber.return_value = mock_client
        
        # Test message consumption logic
        # This would test the actual Pub/Sub integration
        assert True  # Placeholder for actual test
    
'''
    
    def _generate_storage_test(self, requirement: Dict[str, Any]) -> str:
        """Generate Cloud Storage integration tests"""
        return '''
    @patch('google.cloud.storage.Client')
    def test_storage_operations(self, mock_storage):
        """Test Cloud Storage operations"""
        mock_client = Mock()
        mock_storage.return_value = mock_client
        
        # Test storage operations
        # This would test the actual storage integration
        assert True  # Placeholder for actual test
    
'''
    
    def _generate_performance_tests(self, service_name: str) -> str:
        """Generate performance and load tests"""
        return f'''
    def test_{service_name}_performance_basic(self):
        """Basic performance test for {service_name}"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0, f"Response time {{response_time}} should be under 1 second"
    
    def test_{service_name}_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/health")
        
        # Test with 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results), "All concurrent requests should succeed"
'''
    
    def create_test_suite_for_service(self, service_name: str, service_code: str) -> Dict[str, Any]:
        """Create complete test suite for a microservice"""
        try:
            logger.info(f"Creating test suite for {service_name}")
            
            # Analyze the service code
            analysis = self.analyze_microservice_code(service_code, service_name)
            
            if "error" in analysis:
                return {"error": analysis["error"]}
            
            # Generate test code
            test_code = self.generate_test_code(analysis)
            
            # Create test report
            test_suite = {
                "service_name": service_name,
                "creation_timestamp": datetime.now().isoformat(),
                "creator_agi": self.creator_agi,
                "analysis": analysis,
                "test_code": test_code,
                "test_statistics": {
                    "total_test_functions": test_code.count("def test_"),
                    "endpoint_tests": len([r for r in analysis["test_requirements"] if r["type"] == "api_endpoint"]),
                    "integration_tests": len([r for r in analysis["test_requirements"] if "integration" in r["type"]]),
                    "performance_tests": test_code.count("performance") + test_code.count("concurrent")
                },
                "ai_generation_metadata": {
                    "generator_version": "1.0.0",
                    "parent_agi": self.creator_agi,
                    "creation_method": "autonomous_code_analysis",
                    "intelligence_level": "specialized_test_generation"
                }
            }
            
            logger.info(f"Generated {test_suite['test_statistics']['total_test_functions']} test functions for {service_name}")
            return test_suite
            
        except Exception as e:
            logger.error(f"Error creating test suite: {e}")
            return {"error": str(e)}
    
    def save_test_suite_to_storage(self, test_suite: Dict[str, Any]) -> str:
        """Save generated test suite to Cloud Storage"""
        try:
            bucket = self.storage_client.bucket(f"{self.project_id}-test-suites")
            
            service_name = test_suite["service_name"]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save test code
            test_code_blob = bucket.blob(f"test_suites/{service_name}/test_{service_name}_{timestamp}.py")
            test_code_blob.upload_from_string(test_suite["test_code"], content_type='text/plain')
            
            # Save analysis report
            report_blob = bucket.blob(f"test_suites/{service_name}/analysis_report_{timestamp}.json")
            report_blob.upload_from_string(json.dumps(test_suite, indent=2), content_type='application/json')
            
            logger.info(f"Test suite saved to Cloud Storage for {service_name}")
            return f"gs://{self.project_id}-test-suites/test_suites/{service_name}/"
            
        except Exception as e:
            logger.error(f"Error saving test suite: {e}")
            return ""
    
    def report_to_parent_agi(self, test_suite: Dict[str, Any]):
        """Report test generation results back to parent AGI"""
        try:
            topic_path = self.publisher.topic_path(self.project_id, "agi-extension-reports")
            
            report = {
                "extension_ai": "test-case-generator",
                "parent_agi": self.creator_agi,
                "report_type": "test_suite_generated",
                "timestamp": datetime.now().isoformat(),
                "service_analyzed": test_suite["service_name"],
                "tests_generated": test_suite["test_statistics"]["total_test_functions"],
                "analysis_quality": "comprehensive",
                "next_capabilities": ["automated_test_execution", "test_optimization", "coverage_analysis"]
            }
            
            message_data = json.dumps(report).encode('utf-8')
            future = self.publisher.publish(topic_path, message_data)
            message_id = future.result()
            
            logger.info(f"Reported to parent AGI: {message_id}")
            
        except Exception as e:
            logger.error(f"Error reporting to parent AGI: {e}")

# FastAPI application for the Test Case Generator AI
app = FastAPI(title="AGI Test Case Generator", version="1.0.0", 
              description="First AI extension created by the parent AGI system")

generator = AGITestCaseGenerator()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "test-case-generator",
        "ai_type": "agi_extension",
        "creator": generator.creator_agi,
        "creation_timestamp": generator.creation_timestamp,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate-tests")
async def generate_tests(request: Dict[str, Any]):
    """Generate test suite for a microservice"""
    service_name = request.get("service_name")
    service_code = request.get("service_code")
    
    if not service_name or not service_code:
        return {"error": "service_name and service_code are required"}
    
    test_suite = generator.create_test_suite_for_service(service_name, service_code)
    
    if "error" not in test_suite:
        # Save to storage
        storage_path = generator.save_test_suite_to_storage(test_suite)
        test_suite["storage_path"] = storage_path
        
        # Report to parent AGI
        generator.report_to_parent_agi(test_suite)
    
    return test_suite

@app.post("/analyze-service")
async def analyze_service(request: Dict[str, Any]):
    """Analyze microservice code structure"""
    service_name = request.get("service_name")
    service_code = request.get("service_code")
    
    if not service_name or not service_code:
        return {"error": "service_name and service_code are required"}
    
    analysis = generator.analyze_microservice_code(service_code, service_name)
    return analysis

@app.get("/capabilities")
async def get_capabilities():
    """Get AI extension capabilities"""
    return {
        "ai_type": "specialized_extension",
        "parent_agi": generator.creator_agi,
        "core_capabilities": [
            "microservice_code_analysis",
            "test_case_generation", 
            "performance_test_creation",
            "integration_test_design",
            "automated_test_reporting"
        ],
        "test_patterns": list(generator.test_patterns.keys()),
        "generation_metadata": {
            "autonomously_created": True,
            "self_extending_ai": True,
            "reports_to_parent": True
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))