#!/usr/bin/env python3
"""
API Connection Validation Script
Tests connections to all external APIs required for Echo Nexus deployment
"""

import os
import sys
import json
import asyncio
import requests
from pathlib import Path
from datetime import datetime

# Import API connector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from echo_nexus_voice.api_connectors import get_api_connector

async def test_github_api() -> dict:
    """Test GitHub API connection"""
    
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return {
            "status": "error",
            "message": "GITHUB_TOKEN not found in environment",
            "authenticated": False
        }
    
    try:
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "status": "success",
                "message": f"Connected as {user_data.get('login', 'unknown')}",
                "authenticated": True,
                "user": user_data.get('login'),
                "rate_limit_remaining": response.headers.get('X-RateLimit-Remaining'),
                "rate_limit_reset": response.headers.get('X-RateLimit-Reset')
            }
        else:
            return {
                "status": "error",
                "message": f"GitHub API returned {response.status_code}: {response.text}",
                "authenticated": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"GitHub API connection failed: {str(e)}",
            "authenticated": False
        }

async def test_google_cloud_api() -> dict:
    """Test Google Cloud API connection"""
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return {
            "status": "error",
            "message": "GOOGLE_CLOUD_PROJECT not found in environment",
            "authenticated": False
        }
    
    try:
        # Try to run gcloud auth list
        import subprocess
        result = subprocess.run(
            ["gcloud", "auth", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            auth_data = json.loads(result.stdout)
            active_accounts = [acc for acc in auth_data if acc.get("status") == "ACTIVE"]
            
            if active_accounts:
                return {
                    "status": "success",
                    "message": f"Authenticated with {len(active_accounts)} account(s)",
                    "authenticated": True,
                    "project_id": project_id,
                    "active_accounts": [acc.get("account") for acc in active_accounts]
                }
            else:
                return {
                    "status": "warning",
                    "message": "gcloud available but no active authentication",
                    "authenticated": False
                }
        else:
            return {
                "status": "error",
                "message": f"gcloud command failed: {result.stderr}",
                "authenticated": False
            }
            
    except FileNotFoundError:
        return {
            "status": "warning",
            "message": "gcloud CLI not installed (optional for development)",
            "authenticated": False
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Google Cloud API check failed: {str(e)}",
            "authenticated": False
        }

async def test_ai_api_connections() -> dict:
    """Test AI API connections using the API connector"""
    
    try:
        connector = get_api_connector()
        
        # Test API connections
        validation_results = connector.validate_api_connections()
        
        # Get system status
        system_status = connector.get_system_status()
        
        ai_results = {
            "openai": {
                "status": "success" if validation_results.get("openai", False) else "error",
                "authenticated": validation_results.get("openai", False),
                "message": "Connected successfully" if validation_results.get("openai", False) else "Connection failed or API key missing"
            },
            "google": {
                "status": "success" if validation_results.get("google", False) else "error", 
                "authenticated": validation_results.get("google", False),
                "message": "Connected successfully" if validation_results.get("google", False) else "Connection failed or API key missing"
            }
        }
        
        # Add system information
        ai_results["system_info"] = {
            "available_providers": system_status.get("available_providers", []),
            "shadow_mode_enabled": system_status.get("shadow_mode_enabled", False),
            "total_interactions": system_status.get("total_interactions", 0)
        }
        
        return ai_results
        
    except Exception as e:
        return {
            "error": {
                "status": "error",
                "message": f"AI API connector failed: {str(e)}",
                "authenticated": False
            }
        }

async def test_replit_integration() -> dict:
    """Test Replit integration connectivity"""
    
    # Check if we're running in Replit environment
    replit_env = os.environ.get("REPLIT_DB_URL") is not None
    
    try:
        # Test localhost connectivity (typical for Replit)
        response = requests.get("http://localhost:5000/health", timeout=5)
        
        return {
            "status": "success",
            "message": "Replit integration accessible",
            "environment": "replit" if replit_env else "local",
            "health_check": response.status_code == 200
        }
        
    except requests.exceptions.RequestException:
        return {
            "status": "warning",
            "message": "Replit integration not currently running (normal during deployment)",
            "environment": "replit" if replit_env else "local",
            "health_check": False
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Replit integration test failed: {str(e)}",
            "environment": "replit" if replit_env else "local",
            "health_check": False
        }

async def generate_connection_report() -> dict:
    """Generate comprehensive API connection report"""
    
    print("Echo Nexus AGI - API Connection Validation")
    print("=" * 50)
    
    # Test all API connections
    print("Testing GitHub API...")
    github_result = await test_github_api()
    
    print("Testing Google Cloud API...")
    google_cloud_result = await test_google_cloud_api()
    
    print("Testing AI API connections...")
    ai_results = await test_ai_api_connections()
    
    print("Testing Replit integration...")
    replit_result = await test_replit_integration()
    
    # Compile report
    report = {
        "timestamp": datetime.now().isoformat(),
        "github": github_result,
        "google_cloud": google_cloud_result,
        "ai_apis": ai_results,
        "replit": replit_result
    }
    
    # Calculate overall status
    critical_services = [
        github_result.get("authenticated", False),
        any(ai_results.get(provider, {}).get("authenticated", False) for provider in ["openai", "google"])
    ]
    
    overall_status = "ready" if all(critical_services) else "partial" if any(critical_services) else "not_ready"
    report["overall_status"] = overall_status
    
    # Display results
    print(f"\nAPI Connection Results:")
    print(f"GitHub: {'✅' if github_result.get('authenticated') else '❌'} {github_result.get('message', '')}")
    print(f"Google Cloud: {'✅' if google_cloud_result.get('authenticated') else '⚠️'} {google_cloud_result.get('message', '')}")
    
    for provider, result in ai_results.items():
        if provider != "system_info":
            status_icon = "✅" if result.get("authenticated") else "❌"
            print(f"AI API ({provider}): {status_icon} {result.get('message', '')}")
    
    print(f"Replit: {'✅' if replit_result.get('status') == 'success' else '⚠️'} {replit_result.get('message', '')}")
    
    print(f"\nOverall Status: {overall_status.upper()}")
    
    # Save report
    Path("logs").mkdir(exist_ok=True)
    with open("logs/api_connection_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return report

async def main():
    """Main API connection test function"""
    try:
        report = await generate_connection_report()
        
        if report["overall_status"] == "ready":
            print("\n🚀 All critical API connections successful!")
            sys.exit(0)
        elif report["overall_status"] == "partial":
            print("\n⚠️  Some API connections failed. Deployment may have limited functionality.")
            sys.exit(0)  # Allow partial success
        else:
            print("\n❌ Critical API connections failed. Please check your credentials.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ API connection test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())