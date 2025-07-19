#!/usr/bin/env python3
"""
Strategic Knowledge System for AGI Builder
Complex decision-making, licensing awareness, and real-time system health monitoring
"""

import json
import re
import os
import logging
import requests
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class LicenseType(Enum):
    """Software license types with compatibility information"""
    PUBLIC_DOMAIN = "public_domain"
    MIT = "mit"
    APACHE_2 = "apache_2.0"
    BSD_3_CLAUSE = "bsd_3_clause"
    GPL_V2 = "gpl_v2"
    GPL_V3 = "gpl_v3"
    LGPL = "lgpl"
    PROPRIETARY = "proprietary"
    UNKNOWN = "unknown"

@dataclass
class LicenseInfo:
    """Comprehensive license information"""
    license_type: LicenseType
    commercial_use: bool
    distribution: bool
    modification: bool
    private_use: bool
    patent_use: bool
    copyleft: bool
    requires_source: bool
    compatibility_risks: List[str]

@dataclass
class SystemHealth:
    """Real-time system health status"""
    service: str
    status: str
    response_time: float
    error_rate: float
    last_check: datetime
    metrics: Dict[str, Any]

class CopyrightLicensingEngine:
    """
    Advanced copyright and licensing awareness system
    Provides AGI with comprehensive understanding of intellectual property law
    """
    
    def __init__(self):
        self.license_database = self._initialize_license_database()
        self.license_patterns = self._initialize_license_patterns()
        self.usage_log = []
        
    def _initialize_license_database(self) -> Dict[LicenseType, LicenseInfo]:
        """Initialize comprehensive license compatibility database"""
        
        return {
            LicenseType.MIT: LicenseInfo(
                license_type=LicenseType.MIT,
                commercial_use=True,
                distribution=True,
                modification=True,
                private_use=True,
                patent_use=False,
                copyleft=False,
                requires_source=False,
                compatibility_risks=[]
            ),
            
            LicenseType.APACHE_2: LicenseInfo(
                license_type=LicenseType.APACHE_2,
                commercial_use=True,
                distribution=True,
                modification=True,
                private_use=True,
                patent_use=True,
                copyleft=False,
                requires_source=False,
                compatibility_risks=["GPL v2 incompatible"]
            ),
            
            LicenseType.GPL_V3: LicenseInfo(
                license_type=LicenseType.GPL_V3,
                commercial_use=True,
                distribution=True,
                modification=True,
                private_use=True,
                patent_use=True,
                copyleft=True,
                requires_source=True,
                compatibility_risks=[
                    "Requires derivative works to be GPL v3",
                    "Network copyleft - affects SaaS usage",
                    "Incompatible with proprietary software"
                ]
            ),
            
            LicenseType.BSD_3_CLAUSE: LicenseInfo(
                license_type=LicenseType.BSD_3_CLAUSE,
                commercial_use=True,
                distribution=True,
                modification=True,
                private_use=True,
                patent_use=False,
                copyleft=False,
                requires_source=False,
                compatibility_risks=[]
            ),
            
            LicenseType.PROPRIETARY: LicenseInfo(
                license_type=LicenseType.PROPRIETARY,
                commercial_use=False,
                distribution=False,
                modification=False,
                private_use=True,
                patent_use=False,
                copyleft=False,
                requires_source=False,
                compatibility_risks=[
                    "Cannot be redistributed",
                    "Usage restricted by license terms",
                    "May require payment or attribution"
                ]
            )
        }
    
    def _initialize_license_patterns(self) -> Dict[LicenseType, List[str]]:
        """Initialize regex patterns for license detection"""
        
        return {
            LicenseType.MIT: [
                r"MIT License",
                r"Permission is hereby granted, free of charge",
                r"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY"
            ],
            LicenseType.APACHE_2: [
                r"Apache License, Version 2\.0",
                r"Licensed under the Apache License",
                r"http://www\.apache\.org/licenses/LICENSE-2\.0"
            ],
            LicenseType.GPL_V3: [
                r"GNU GENERAL PUBLIC LICENSE\s+Version 3",
                r"This program is free software: you can redistribute it",
                r"GNU GPL v3"
            ],
            LicenseType.BSD_3_CLAUSE: [
                r"BSD 3-Clause License",
                r"Redistribution and use in source and binary forms",
                r"Neither the name of .* nor the names"
            ]
        }
    
    def detect_license(self, content: str, file_path: str = "") -> Tuple[LicenseType, float]:
        """Detect license type from file content with confidence score"""
        
        content_lower = content.lower()
        
        # Check for explicit license files
        if any(name in file_path.lower() for name in ['license', 'copying', 'copyright']):
            confidence_boost = 0.2
        else:
            confidence_boost = 0.0
        
        best_match = LicenseType.UNKNOWN
        best_confidence = 0.0
        
        for license_type, patterns in self.license_patterns.items():
            matches = 0
            total_patterns = len(patterns)
            
            for pattern in patterns:
                if re.search(pattern.lower(), content_lower):
                    matches += 1
            
            confidence = (matches / total_patterns) + confidence_boost
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = license_type
        
        return best_match, min(best_confidence, 1.0)
    
    def check_compatibility(self, primary_license: LicenseType, 
                          dependency_licenses: List[LicenseType]) -> Dict[str, Any]:
        """Check license compatibility for project dependencies"""
        
        primary_info = self.license_database.get(primary_license)
        if not primary_info:
            return {"compatible": False, "reason": "Unknown primary license"}
        
        compatibility_issues = []
        compatible_licenses = []
        
        for dep_license in dependency_licenses:
            dep_info = self.license_database.get(dep_license)
            if not dep_info:
                compatibility_issues.append(f"Unknown dependency license: {dep_license}")
                continue
            
            # Check copyleft compatibility
            if dep_info.copyleft and not primary_info.copyleft:
                if primary_license != LicenseType.GPL_V3:
                    compatibility_issues.append(
                        f"Copyleft license {dep_license} requires derivative work to be copyleft"
                    )
                    continue
            
            # Check proprietary compatibility
            if dep_license == LicenseType.PROPRIETARY:
                compatibility_issues.append(
                    f"Proprietary dependency may have usage restrictions"
                )
            
            compatible_licenses.append(dep_license)
        
        return {
            "compatible": len(compatibility_issues) == 0,
            "issues": compatibility_issues,
            "compatible_licenses": compatible_licenses,
            "recommendations": self._generate_license_recommendations(
                primary_license, dependency_licenses
            )
        }
    
    def _generate_license_recommendations(self, primary: LicenseType, 
                                        dependencies: List[LicenseType]) -> List[str]:
        """Generate recommendations for license compliance"""
        
        recommendations = []
        
        if primary == LicenseType.GPL_V3:
            recommendations.append("Ensure all dependencies are GPL v3 compatible")
            recommendations.append("Consider network copyleft implications for web services")
        
        if LicenseType.PROPRIETARY in dependencies:
            recommendations.append("Review proprietary license terms carefully")
            recommendations.append("Consider alternative open-source dependencies")
        
        if primary == LicenseType.MIT and LicenseType.GPL_V3 in dependencies:
            recommendations.append("Consider changing to GPL v3 to maintain compatibility")
        
        return recommendations
    
    def log_code_usage(self, source: str, license: LicenseType, 
                      file_path: str, modification_type: str = "copy"):
        """Log code usage for audit purposes"""
        
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "license": license.value,
            "file_path": file_path,
            "modification_type": modification_type,
            "compliance_checked": True
        }
        
        self.usage_log.append(usage_entry)
        
        # Save to persistent log file
        with open(".license_usage_log.json", "w") as f:
            json.dump(self.usage_log, f, indent=2)

class SystemHealthMonitor:
    """
    Real-time system health and observability engine
    Provides AGI with comprehensive understanding of system status and failure patterns
    """
    
    def __init__(self):
        self.failure_signatures = self._initialize_failure_signatures()
        self.metric_definitions = self._initialize_metric_definitions()
        self.health_history = []
        
    def _initialize_failure_signatures(self) -> Dict[str, Dict[str, Any]]:
        """Initialize library of common failure patterns"""
        
        return {
            "github_actions": {
                "build_timeout": {
                    "pattern": r"The operation was canceled",
                    "probable_cause": "Build exceeded time limit (6 hours for GitHub Actions)",
                    "solutions": [
                        "Optimize build steps for faster execution",
                        "Use build matrix to parallelize",
                        "Consider migrating to Google Cloud Build for longer timeouts",
                        "Cache dependencies to reduce build time"
                    ],
                    "severity": "high"
                },
                "dependency_conflict": {
                    "pattern": r"Could not find a version that satisfies",
                    "probable_cause": "Python package dependency conflict",
                    "solutions": [
                        "Update requirements.txt with compatible versions",
                        "Use virtual environment isolation",
                        "Check for conflicting transitive dependencies",
                        "Consider using poetry for dependency resolution"
                    ],
                    "severity": "medium"
                },
                "insufficient_permissions": {
                    "pattern": r"Permission denied|Forbidden",
                    "probable_cause": "GitHub token lacks required permissions",
                    "solutions": [
                        "Update GitHub token permissions",
                        "Check repository access rights",
                        "Verify workflow permissions in YAML",
                        "Use GITHUB_TOKEN with appropriate scopes"
                    ],
                    "severity": "high"
                }
            },
            
            "cloud_build": {
                "quota_exceeded": {
                    "pattern": r"Quota exceeded|Resource exhausted",
                    "probable_cause": "Google Cloud quota limits reached",
                    "solutions": [
                        "Request quota increase from Google Cloud",
                        "Optimize build resource usage",
                        "Implement build queuing and retry logic",
                        "Monitor quota usage proactively"
                    ],
                    "severity": "high"
                },
                "image_not_found": {
                    "pattern": r"Unable to pull image|Image not found",
                    "probable_cause": "Container image unavailable or misconfigured",
                    "solutions": [
                        "Verify image name and tag",
                        "Check container registry permissions",
                        "Use alternative builder image",
                        "Build custom image if needed"
                    ],
                    "severity": "medium"
                },
                "build_step_failure": {
                    "pattern": r"Step #\d+ - .* failed",
                    "probable_cause": "Individual build step encountered error",
                    "solutions": [
                        "Review step logs for specific error",
                        "Check command syntax and arguments",
                        "Verify file paths and permissions",
                        "Add error handling and retry logic"
                    ],
                    "severity": "medium"
                }
            },
            
            "deployment": {
                "connection_refused": {
                    "pattern": r"Connection refused|ECONNREFUSED",
                    "probable_cause": "Service not running or port not accessible",
                    "solutions": [
                        "Verify service is running and healthy",
                        "Check port binding (use 0.0.0.0 not localhost)",
                        "Verify firewall and network configuration",
                        "Check service startup logs"
                    ],
                    "severity": "high"
                },
                "memory_limit": {
                    "pattern": r"OOMKilled|Out of memory",
                    "probable_cause": "Application exceeded memory limits",
                    "solutions": [
                        "Increase memory allocation",
                        "Optimize application memory usage",
                        "Implement memory profiling",
                        "Use streaming for large data processing"
                    ],
                    "severity": "high"
                },
                "ssl_certificate": {
                    "pattern": r"SSL certificate|TLS handshake",
                    "probable_cause": "SSL/TLS certificate issue",
                    "solutions": [
                        "Verify certificate validity and expiration",
                        "Check certificate chain completeness",
                        "Update certificate authorities",
                        "Use proper certificate for domain"
                    ],
                    "severity": "medium"
                }
            }
        }
    
    def _initialize_metric_definitions(self) -> Dict[str, str]:
        """Initialize plain English explanations for system metrics"""
        
        return {
            "response_time": "Time taken for system to respond to request (lower is better)",
            "error_rate": "Percentage of requests that fail (lower is better)",
            "cpu_usage": "Processor utilization percentage (monitor for sustained high usage)",
            "memory_usage": "RAM utilization percentage (watch for memory leaks)",
            "disk_usage": "Storage space utilization (prevent disk full conditions)",
            "request_rate": "Number of requests per second (monitor for traffic spikes)",
            "build_duration": "Time taken to complete build process (optimize for efficiency)",
            "deployment_frequency": "How often code is deployed (higher indicates agility)",
            "mttr": "Mean Time To Recovery - average time to fix issues (lower is better)",
            "availability": "Percentage of time service is operational (target 99.9%+)"
        }
    
    def analyze_logs(self, log_content: str, service_type: str) -> Dict[str, Any]:
        """Analyze logs for failure patterns and provide diagnostic information"""
        
        service_signatures = self.failure_signatures.get(service_type, {})
        detected_issues = []
        
        for issue_name, signature in service_signatures.items():
            pattern = signature["pattern"]
            if re.search(pattern, log_content, re.IGNORECASE):
                detected_issues.append({
                    "issue": issue_name,
                    "severity": signature["severity"],
                    "probable_cause": signature["probable_cause"],
                    "solutions": signature["solutions"]
                })
        
        return {
            "issues_detected": len(detected_issues),
            "issues": detected_issues,
            "analysis_timestamp": datetime.now().isoformat(),
            "service_type": service_type,
            "recommendations": self._generate_proactive_recommendations(detected_issues)
        }
    
    def _generate_proactive_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate proactive recommendations based on detected issues"""
        
        recommendations = []
        
        if any(issue["severity"] == "high" for issue in issues):
            recommendations.append("Critical issues detected - prioritize immediate resolution")
        
        if len(issues) > 3:
            recommendations.append("Multiple issues detected - consider systematic review")
        
        # Pattern-based recommendations
        issue_types = [issue["issue"] for issue in issues]
        
        if "build_timeout" in issue_types:
            recommendations.append("Consider implementing build optimization strategy")
        
        if "quota_exceeded" in issue_types:
            recommendations.append("Implement resource monitoring and scaling automation")
        
        return recommendations
    
    def monitor_service_health(self, service_url: str, service_name: str) -> SystemHealth:
        """Monitor real-time health of a service"""
        
        start_time = datetime.now()
        
        try:
            response = requests.get(service_url, timeout=10)
            response_time = (datetime.now() - start_time).total_seconds()
            
            status = "healthy" if response.status_code == 200 else "degraded"
            error_rate = 0.0 if response.status_code == 200 else 1.0
            
        except requests.RequestException as e:
            response_time = (datetime.now() - start_time).total_seconds()
            status = "unhealthy"
            error_rate = 1.0
        
        health = SystemHealth(
            service=service_name,
            status=status,
            response_time=response_time,
            error_rate=error_rate,
            last_check=datetime.now(),
            metrics={
                "endpoint": service_url,
                "check_type": "http_get"
            }
        )
        
        self.health_history.append(health)
        return health

class ContextualDecisionEngine:
    """
    Advanced contextual decision-making system
    Provides AGI with nuanced understanding of trade-offs and tool selection
    """
    
    def __init__(self):
        self.decision_trees = self._initialize_decision_trees()
        self.feedback_history = []
        
    def _initialize_decision_trees(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive decision frameworks"""
        
        return {
            "ci_cd_platform_selection": {
                "factors": [
                    {
                        "name": "build_complexity",
                        "weight": 0.25,
                        "options": {
                            "simple": {"github_actions": 3, "cloud_build": 2},
                            "moderate": {"github_actions": 2, "cloud_build": 3},
                            "complex": {"github_actions": 1, "cloud_build": 3}
                        }
                    },
                    {
                        "name": "build_duration",
                        "weight": 0.25,
                        "options": {
                            "under_30min": {"github_actions": 3, "cloud_build": 2},
                            "30_60min": {"github_actions": 2, "cloud_build": 3},
                            "over_60min": {"github_actions": 0, "cloud_build": 3}
                        }
                    },
                    {
                        "name": "team_expertise",
                        "weight": 0.20,
                        "options": {
                            "github_native": {"github_actions": 3, "cloud_build": 1},
                            "cloud_native": {"github_actions": 1, "cloud_build": 3},
                            "platform_agnostic": {"github_actions": 2, "cloud_build": 2}
                        }
                    },
                    {
                        "name": "cost_sensitivity",
                        "weight": 0.15,
                        "options": {
                            "low": {"github_actions": 2, "cloud_build": 3},
                            "medium": {"github_actions": 3, "cloud_build": 2},
                            "high": {"github_actions": 3, "cloud_build": 1}
                        }
                    },
                    {
                        "name": "deployment_target",
                        "weight": 0.15,
                        "options": {
                            "github_ecosystem": {"github_actions": 3, "cloud_build": 1},
                            "google_cloud": {"github_actions": 1, "cloud_build": 3},
                            "multi_cloud": {"github_actions": 2, "cloud_build": 2}
                        }
                    }
                ]
            },
            
            "mobile_framework_selection": {
                "factors": [
                    {
                        "name": "developer_background",
                        "weight": 0.30,
                        "options": {
                            "python": {"kivy": 3, "flutter": 1, "react_native": 1},
                            "javascript": {"kivy": 1, "flutter": 1, "react_native": 3},
                            "dart": {"kivy": 1, "flutter": 3, "react_native": 1}
                        }
                    },
                    {
                        "name": "performance_requirements",
                        "weight": 0.25,
                        "options": {
                            "basic": {"kivy": 3, "flutter": 2, "react_native": 2},
                            "moderate": {"kivy": 2, "flutter": 3, "react_native": 2},
                            "high": {"kivy": 1, "flutter": 3, "react_native": 2}
                        }
                    },
                    {
                        "name": "development_speed",
                        "weight": 0.20,
                        "options": {
                            "prototype": {"kivy": 3, "flutter": 2, "react_native": 3},
                            "mvp": {"kivy": 2, "flutter": 3, "react_native": 3},
                            "production": {"kivy": 1, "flutter": 3, "react_native": 2}
                        }
                    },
                    {
                        "name": "platform_coverage",
                        "weight": 0.15,
                        "options": {
                            "android_only": {"kivy": 2, "flutter": 3, "react_native": 2},
                            "cross_platform": {"kivy": 2, "flutter": 3, "react_native": 3},
                            "web_integration": {"kivy": 1, "flutter": 2, "react_native": 3}
                        }
                    },
                    {
                        "name": "maintenance_burden",
                        "weight": 0.10,
                        "options": {
                            "minimal": {"kivy": 2, "flutter": 3, "react_native": 2},
                            "moderate": {"kivy": 2, "flutter": 2, "react_native": 2},
                            "acceptable": {"kivy": 3, "flutter": 3, "react_native": 3}
                        }
                    }
                ]
            }
        }
    
    def make_decision(self, decision_type: str, requirements: Dict[str, str]) -> Dict[str, Any]:
        """Make intelligent decision based on requirements and decision tree"""
        
        if decision_type not in self.decision_trees:
            return {"error": f"Unknown decision type: {decision_type}"}
        
        tree = self.decision_trees[decision_type]
        option_scores = {}
        
        # Calculate weighted scores for each option
        for factor in tree["factors"]:
            factor_name = factor["name"]
            weight = factor["weight"]
            requirement_value = requirements.get(factor_name, "moderate")
            
            if requirement_value in factor["options"]:
                scores = factor["options"][requirement_value]
                
                for option, score in scores.items():
                    if option not in option_scores:
                        option_scores[option] = 0
                    option_scores[option] += score * weight
        
        # Find best option
        if not option_scores:
            return {"error": "No scores calculated"}
        
        best_option = max(option_scores, key=option_scores.get)
        best_score = option_scores[best_option]
        
        # Calculate confidence based on score difference
        sorted_scores = sorted(option_scores.values(), reverse=True)
        confidence = (sorted_scores[0] - sorted_scores[1]) / sorted_scores[0] if len(sorted_scores) > 1 else 1.0
        
        return {
            "recommendation": best_option,
            "confidence": confidence,
            "all_scores": option_scores,
            "reasoning": self._generate_decision_reasoning(decision_type, requirements, best_option),
            "alternatives": [k for k, v in sorted(option_scores.items(), key=lambda x: x[1], reverse=True)[1:]]
        }
    
    def _generate_decision_reasoning(self, decision_type: str, requirements: Dict[str, str], 
                                   recommendation: str) -> str:
        """Generate human-readable reasoning for decision"""
        
        if decision_type == "ci_cd_platform_selection":
            if recommendation == "github_actions":
                return "GitHub Actions recommended for simpler builds with GitHub ecosystem integration"
            elif recommendation == "cloud_build":
                return "Google Cloud Build recommended for complex, long-running, or high-volume builds"
            else:
                return "Hybrid approach recommended for maximum flexibility and redundancy"
        
        elif decision_type == "mobile_framework_selection":
            if recommendation == "kivy":
                return "Kivy recommended for Python developers building prototypes or simple apps"
            elif recommendation == "flutter":
                return "Flutter recommended for high-performance cross-platform applications"
            elif recommendation == "react_native":
                return "React Native recommended for JavaScript developers needing rapid development"
        
        return f"Recommended {recommendation} based on requirement analysis"

def main():
    """Demonstrate strategic knowledge system"""
    
    print("🧠 Strategic Knowledge System for AGI Builder")
    print("=" * 60)
    
    # Test licensing engine
    print("Testing Copyright & Licensing Engine...")
    licensing = CopyrightLicensingEngine()
    
    # Test license detection
    mit_content = "MIT License\n\nPermission is hereby granted, free of charge..."
    license_type, confidence = licensing.detect_license(mit_content)
    print(f"Detected license: {license_type.value} (confidence: {confidence:.2f})")
    
    # Test compatibility check
    compatibility = licensing.check_compatibility(
        LicenseType.MIT, 
        [LicenseType.APACHE_2, LicenseType.BSD_3_CLAUSE]
    )
    print(f"License compatibility: {compatibility['compatible']}")
    
    # Test health monitoring
    print("\nTesting System Health Monitor...")
    health_monitor = SystemHealthMonitor()
    
    # Test log analysis
    error_log = "Step #3 - 'gcr.io/cloud-builders/python' failed: Could not find a version that satisfies"
    analysis = health_monitor.analyze_logs(error_log, "cloud_build")
    print(f"Issues detected: {analysis['issues_detected']}")
    
    # Test decision engine
    print("\nTesting Contextual Decision Engine...")
    decision_engine = ContextualDecisionEngine()
    
    requirements = {
        "build_complexity": "moderate",
        "build_duration": "30_60min",
        "team_expertise": "github_native",
        "cost_sensitivity": "medium",
        "deployment_target": "google_cloud"
    }
    
    decision = decision_engine.make_decision("ci_cd_platform_selection", requirements)
    print(f"Platform recommendation: {decision['recommendation']} (confidence: {decision['confidence']:.2f})")
    
    print("\n✅ Strategic Knowledge System operational!")

if __name__ == "__main__":
    main()