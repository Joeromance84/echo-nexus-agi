#!/usr/bin/env python3
"""
Docker Self-Packer: Containerized Deployment System
Echo's capability for autonomous Docker containerization and deployment
"""

import os
import subprocess
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

class DockerSelfPacker:
    """
    Advanced autonomous Docker containerization system
    Enables Echo to package herself into portable container deployments
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.container_config = self._load_container_config()
        self.docker_available = self._check_docker_availability()
        
    def _load_container_config(self) -> Dict[str, Any]:
        """Load Docker containerization configuration"""
        config_path = self.project_root / "echo_config" / "docker_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        
        return {
            "base_image": "python:3.11-slim",
            "container_name": "echo-nexus-agi",
            "image_name": "logan/echo-nexus",
            "version": "latest",
            "exposed_ports": ["5000", "8080"],
            "environment_variables": {
                "ECHO_MODE": "container",
                "PYTHONPATH": "/app",
                "STREAMLIT_SERVER_PORT": "5000"
            },
            "volume_mounts": ["/app/data", "/app/logs"],
            "python_requirements": [
                "streamlit",
                "openai",
                "requests", 
                "pygithub",
                "pyyaml"
            ]
        }
    
    def _check_docker_availability(self) -> bool:
        """Check if Docker is available and accessible"""
        try:
            result = subprocess.run(
                ["docker", "--version"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def create_dockerfile(self) -> bool:
        """
        Create optimized Dockerfile for Echo Nexus deployment
        """
        dockerfile_content = f'''# Echo Nexus AGI - Autonomous Intelligence Container
FROM {self.container_config['base_image']}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs uploads knowledge_core echo_runtime

# Set permissions
RUN chmod +x scripts/*.sh || true

# Expose ports
EXPOSE {' '.join(self.container_config['exposed_ports'])}

# Environment variables
{chr(10).join(f'ENV {k}="{v}"' for k, v in self.container_config['environment_variables'].items())}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
'''
        
        dockerfile_path = self.project_root / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        print("✅ Dockerfile created successfully")
        return True
    
    def create_requirements_txt(self) -> bool:
        """
        Generate requirements.txt for container dependencies
        """
        requirements_content = "\n".join([
            "# Echo Nexus AGI Dependencies",
            "# Core framework",
            "streamlit>=1.28.0",
            "kivy>=2.2.0",
            "",
            "# AI and API integration", 
            "openai>=1.0.0",
            "google-generativeai>=0.3.0",
            "",
            "# Web and networking",
            "requests>=2.31.0",
            "pygithub>=1.59.0",
            "",
            "# Data handling",
            "pyyaml>=6.0",
            "pydantic>=2.0.0",
            "pandas>=2.1.0",
            "",
            "# Additional utilities",
            "python-dotenv>=1.0.0",
            "psutil>=5.9.0",
            "",
            "# Development and debugging",
            "pytest>=7.4.0",
            "black>=23.0.0"
        ] + self.container_config['python_requirements'])
        
        requirements_path = self.project_root / "requirements.txt"
        requirements_path.write_text(requirements_content)
        print("✅ requirements.txt generated")
        return True
    
    def create_docker_compose(self) -> bool:
        """
        Create docker-compose.yml for complete deployment orchestration
        """
        compose_content = f'''version: '3.8'

services:
  echo-nexus:
    build: .
    image: {self.container_config['image_name']}:{self.container_config['version']}
    container_name: {self.container_config['container_name']}
    ports:
      - "5000:5000"
      - "8080:8080"
    environment:
      - ECHO_MODE=container
      - PYTHONPATH=/app
      - STREAMLIT_SERVER_PORT=5000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  echo-database:
    image: postgres:15-alpine
    container_name: echo-postgres
    environment:
      POSTGRES_DB: echo_nexus
      POSTGRES_USER: echo
      POSTGRES_PASSWORD: nexus_secure_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  echo-redis:
    image: redis:7-alpine
    container_name: echo-redis
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: echo-nexus-network
'''
        
        compose_path = self.project_root / "docker-compose.yml"
        compose_path.write_text(compose_content)
        print("✅ docker-compose.yml created")
        return True
    
    def create_dockerignore(self) -> bool:
        """
        Create .dockerignore to exclude unnecessary files
        """
        dockerignore_content = '''# Echo Nexus Docker Ignore
# Virtual environments
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo

# Git and version control
.git/
.gitignore

# Logs and temporary files
*.log
logs/
tmp/
temp/

# Build artifacts
build/
dist/
*.egg-info/

# OS-specific files
.DS_Store
Thumbs.db

# Development files
.env
.env.local
docker-compose.override.yml

# Large data files
*.zip
*.tar.gz
*.apk

# Cache directories
.cache/
.pytest_cache/
'''
        
        dockerignore_path = self.project_root / ".dockerignore"
        dockerignore_path.write_text(dockerignore_content)
        print("✅ .dockerignore created")
        return True
    
    def build_image(self, tag: Optional[str] = None) -> Dict[str, Any]:
        """
        Build Docker image for Echo Nexus
        """
        if not self.docker_available:
            return {
                "success": False,
                "error": "Docker not available on system"
            }
        
        # Prepare build context
        self.create_dockerfile()
        self.create_requirements_txt()
        self.create_dockerignore()
        
        # Determine image tag
        if not tag:
            tag = f"{self.container_config['image_name']}:{self.container_config['version']}"
        
        print(f"🏗️ Building Docker image: {tag}")
        
        try:
            # Build command
            build_cmd = [
                "docker", "build",
                "-t", tag,
                ".",
                "--progress=plain"
            ]
            
            result = subprocess.run(
                build_cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                # Get image information
                image_info = self._get_image_info(tag)
                
                return {
                    "success": True,
                    "image_tag": tag,
                    "image_id": image_info.get("Id", "unknown")[:12],
                    "size": image_info.get("Size", "unknown"),
                    "created": image_info.get("Created", "unknown"),
                    "build_output": result.stdout[-1000:],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Docker build failed",
                    "build_output": result.stderr[-1000:],
                    "return_code": result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Build timeout (30 minutes exceeded)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Build exception: {str(e)}"
            }
    
    def _get_image_info(self, tag: str) -> Dict[str, Any]:
        """Get Docker image information"""
        try:
            result = subprocess.run(
                ["docker", "image", "inspect", tag],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                image_data = json.loads(result.stdout)
                return image_data[0] if image_data else {}
            
        except Exception:
            pass
        
        return {}
    
    def run_container(self, 
                     image_tag: Optional[str] = None,
                     detached: bool = True,
                     port_mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run Echo Nexus container
        """
        if not self.docker_available:
            return {
                "success": False,
                "error": "Docker not available on system"
            }
        
        if not image_tag:
            image_tag = f"{self.container_config['image_name']}:{self.container_config['version']}"
        
        # Default port mapping
        if not port_mapping:
            port_mapping = {
                "5000": "5000",  # Streamlit
                "8080": "8080"   # Additional services
            }
        
        try:
            # Run command
            run_cmd = ["docker", "run"]
            
            if detached:
                run_cmd.append("-d")
            
            # Port mappings
            for host_port, container_port in port_mapping.items():
                run_cmd.extend(["-p", f"{host_port}:{container_port}"])
            
            # Container name
            run_cmd.extend(["--name", self.container_config['container_name']])
            
            # Volume mounts
            run_cmd.extend(["-v", f"{self.project_root}/data:/app/data"])
            run_cmd.extend(["-v", f"{self.project_root}/logs:/app/logs"])
            
            # Environment variables
            for env_var, value in self.container_config['environment_variables'].items():
                run_cmd.extend(["-e", f"{env_var}={value}"])
            
            # Image
            run_cmd.append(image_tag)
            
            print(f"🚀 Running container: {' '.join(run_cmd)}")
            
            result = subprocess.run(run_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                
                return {
                    "success": True,
                    "container_id": container_id,
                    "container_name": self.container_config['container_name'],
                    "image_tag": image_tag,
                    "ports": port_mapping,
                    "detached": detached,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Container run failed",
                    "output": result.stderr,
                    "return_code": result.returncode
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Container run exception: {str(e)}"
            }
    
    def deploy_with_compose(self) -> Dict[str, Any]:
        """
        Deploy complete Echo Nexus stack using Docker Compose
        """
        if not self.docker_available:
            return {
                "success": False,
                "error": "Docker not available on system"
            }
        
        # Create compose file
        self.create_docker_compose()
        
        try:
            # Deploy with compose
            deploy_cmd = ["docker-compose", "up", "-d", "--build"]
            
            print("🚀 Deploying Echo Nexus stack with Docker Compose...")
            
            result = subprocess.run(
                deploy_cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                # Get running services
                services = self._get_compose_services()
                
                return {
                    "success": True,
                    "deployment_method": "docker-compose",
                    "services": services,
                    "compose_output": result.stdout[-1000:],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": "Docker Compose deployment failed",
                    "compose_output": result.stderr[-1000:],
                    "return_code": result.returncode
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Deployment timeout (30 minutes exceeded)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Deployment exception: {str(e)}"
            }
    
    def _get_compose_services(self) -> List[Dict[str, str]]:
        """Get information about running compose services"""
        try:
            result = subprocess.run(
                ["docker-compose", "ps", "--format", "json"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            
        except Exception:
            pass
        
        return []
    
    def get_container_status(self) -> Dict[str, Any]:
        """Get current container deployment status"""
        if not self.docker_available:
            return {"docker_available": False}
        
        status = {
            "docker_available": True,
            "dockerfile_exists": (self.project_root / "Dockerfile").exists(),
            "compose_file_exists": (self.project_root / "docker-compose.yml").exists(),
            "requirements_exists": (self.project_root / "requirements.txt").exists(),
            "containers": [],
            "images": []
        }
        
        # Check for existing containers
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        container_info = json.loads(line)
                        if self.container_config['container_name'] in container_info.get('Names', ''):
                            status['containers'].append(container_info)
        
        except Exception:
            pass
        
        # Check for existing images
        try:
            result = subprocess.run(
                ["docker", "images", "--format", "json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        image_info = json.loads(line)
                        if self.container_config['image_name'] in image_info.get('Repository', ''):
                            status['images'].append(image_info)
        
        except Exception:
            pass
        
        return status

def main():
    """Standalone Docker packer execution"""
    print("🚀 Echo Nexus Docker Self-Packer")
    
    packer = DockerSelfPacker()
    
    print("📊 Container environment status:")
    status = packer.get_container_status()
    for key, value in status.items():
        if key not in ['containers', 'images']:
            print(f"   {key}: {value}")
    
    if status['docker_available']:
        # Build image
        print("\n🏗️ Building Docker image...")
        build_result = packer.build_image()
        
        if build_result["success"]:
            print(f"✅ Build successful!")
            print(f"   Image: {build_result['image_tag']}")
            print(f"   ID: {build_result['image_id']}")
            
            # Run container
            print("\n🚀 Starting container...")
            run_result = packer.run_container()
            
            if run_result["success"]:
                print(f"✅ Container started!")
                print(f"   Container ID: {run_result['container_id']}")
                print(f"   Access: http://localhost:5000")
            else:
                print(f"❌ Container start failed: {run_result['error']}")
        else:
            print(f"❌ Build failed: {build_result['error']}")
    else:
        print("❌ Docker not available on this system")

if __name__ == "__main__":
    main()