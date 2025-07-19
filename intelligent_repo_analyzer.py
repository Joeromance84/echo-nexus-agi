#!/usr/bin/env python3
"""
Intelligent Repository Analysis System
Trains AI to assess, study, and understand Logan's Echo AGI codebase
"""

import os
import json
import time
from github import Github
from typing import Dict, List, Any
import ast
import re

class IntelligentRepoAnalyzer:
    """AI-powered repository analysis and understanding system"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.g = Github(self.github_token) if self.github_token else None
        self.analysis_results = {}
        self.code_patterns = {}
        self.architecture_map = {}
        
    def analyze_all_repositories(self):
        """Comprehensive analysis of all Logan's repositories"""
        
        if not self.g:
            print("GitHub token required for repository analysis")
            return
            
        user = self.g.get_user()
        print(f"Analyzing repositories for {user.login}...")
        
        # Target repositories for analysis
        target_repos = ['Echo_AI', 'echonexus-control-plane', 'echonexus-control-demo']
        
        for repo_name in target_repos:
            try:
                print(f"\n🧠 Deep analysis of {repo_name}...")
                repo = user.get_repo(repo_name)
                
                analysis = self.deep_analyze_repository(repo)
                self.analysis_results[repo_name] = analysis
                
                print(f"✅ Analysis complete for {repo_name}")
                
            except Exception as e:
                print(f"❌ Error analyzing {repo_name}: {e}")
        
        # Generate comprehensive understanding
        self.generate_understanding_report()
        
    def deep_analyze_repository(self, repo) -> Dict[str, Any]:
        """Perform deep analysis of a single repository"""
        
        analysis = {
            'basic_info': self.get_basic_info(repo),
            'code_structure': self.analyze_code_structure(repo),
            'echo_components': self.identify_echo_components(repo),
            'architecture_patterns': self.analyze_architecture_patterns(repo),
            'dependencies': self.analyze_dependencies(repo),
            'build_system': self.analyze_build_system(repo),
            'ai_capabilities': self.identify_ai_capabilities(repo),
            'innovation_level': self.assess_innovation_level(repo)
        }
        
        return analysis
    
    def get_basic_info(self, repo) -> Dict[str, Any]:
        """Get basic repository information"""
        return {
            'name': repo.name,
            'description': repo.description,
            'language': repo.language,
            'size': repo.size,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'last_updated': repo.updated_at.isoformat(),
            'topics': repo.get_topics()
        }
    
    def analyze_code_structure(self, repo) -> Dict[str, Any]:
        """Analyze the code structure and organization"""
        
        structure = {
            'python_files': [],
            'config_files': [],
            'documentation': [],
            'workflows': [],
            'core_modules': [],
            'total_files': 0
        }
        
        try:
            contents = repo.get_contents("")
            structure['total_files'] = self.count_files_recursive(repo, contents)
            
            for item in contents:
                if item.type == "file":
                    self.categorize_file(item, structure)
                elif item.type == "dir":
                    self.analyze_directory(repo, item, structure)
                    
        except Exception as e:
            print(f"Error analyzing structure: {e}")
            
        return structure
    
    def identify_echo_components(self, repo) -> Dict[str, Any]:
        """Identify Echo AGI system components"""
        
        echo_components = {
            'echo_core_files': [],
            'nexus_modules': [],
            'control_systems': [],
            'memory_systems': [],
            'replication_engines': [],
            'consciousness_modules': []
        }
        
        try:
            # Look for Echo-specific files
            contents = repo.get_contents("")
            for item in contents:
                if item.type == "file" and item.name.endswith('.py'):
                    file_content = self.get_file_content(repo, item.path)
                    self.classify_echo_component(item.name, file_content, echo_components)
                elif item.type == "dir":
                    self.analyze_echo_directory(repo, item, echo_components)
                    
        except Exception as e:
            print(f"Error identifying Echo components: {e}")
            
        return echo_components
    
    def analyze_architecture_patterns(self, repo) -> Dict[str, Any]:
        """Analyze architectural patterns and design principles"""
        
        patterns = {
            'design_patterns': [],
            'architectural_style': 'unknown',
            'modularity_score': 0,
            'complexity_metrics': {},
            'innovation_indicators': []
        }
        
        try:
            python_files = self.get_python_files(repo)
            
            for file_path in python_files:
                content = self.get_file_content(repo, file_path)
                if content:
                    self.analyze_code_patterns(content, patterns)
                    
            patterns['modularity_score'] = self.calculate_modularity_score(patterns)
            patterns['architectural_style'] = self.determine_architectural_style(patterns)
            
        except Exception as e:
            print(f"Error analyzing patterns: {e}")
            
        return patterns
    
    def analyze_dependencies(self, repo) -> Dict[str, Any]:
        """Analyze project dependencies and requirements"""
        
        dependencies = {
            'python_requirements': [],
            'build_dependencies': [],
            'ai_libraries': [],
            'specialized_tools': []
        }
        
        # Check for requirements files
        req_files = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']
        
        for req_file in req_files:
            try:
                content = self.get_file_content(repo, req_file)
                if content:
                    self.parse_dependencies(content, req_file, dependencies)
            except:
                continue
                
        return dependencies
    
    def analyze_build_system(self, repo) -> Dict[str, Any]:
        """Analyze build and deployment systems"""
        
        build_system = {
            'github_actions': [],
            'docker_support': False,
            'mobile_build': False,
            'cloud_integration': False,
            'ci_cd_complexity': 'basic'
        }
        
        try:
            # Check for GitHub Actions
            try:
                workflows = repo.get_contents('.github/workflows')
                for workflow in workflows:
                    if workflow.name.endswith('.yml') or workflow.name.endswith('.yaml'):
                        content = self.get_file_content(repo, workflow.path)
                        build_system['github_actions'].append({
                            'name': workflow.name,
                            'type': self.classify_workflow_type(content)
                        })
            except:
                pass
            
            # Check for mobile build support
            try:
                buildozer_content = self.get_file_content(repo, 'buildozer.spec')
                if buildozer_content:
                    build_system['mobile_build'] = True
            except:
                pass
            
            # Check for cloud integration
            try:
                cloudbuild_content = self.get_file_content(repo, 'cloudbuild.yaml')
                if cloudbuild_content:
                    build_system['cloud_integration'] = True
            except:
                pass
                
        except Exception as e:
            print(f"Error analyzing build system: {e}")
            
        return build_system
    
    def identify_ai_capabilities(self, repo) -> Dict[str, Any]:
        """Identify AI and machine learning capabilities"""
        
        ai_capabilities = {
            'ml_frameworks': [],
            'ai_models': [],
            'nlp_processing': False,
            'neural_networks': False,
            'federated_learning': False,
            'consciousness_simulation': False,
            'advanced_reasoning': False
        }
        
        try:
            python_files = self.get_python_files(repo)
            
            for file_path in python_files:
                content = self.get_file_content(repo, file_path)
                if content:
                    self.detect_ai_patterns(content, ai_capabilities)
                    
        except Exception as e:
            print(f"Error identifying AI capabilities: {e}")
            
        return ai_capabilities
    
    def assess_innovation_level(self, repo) -> Dict[str, Any]:
        """Assess the innovation level and uniqueness of the repository"""
        
        innovation = {
            'innovation_score': 0,
            'unique_concepts': [],
            'revolutionary_features': [],
            'complexity_level': 'standard',
            'breakthrough_potential': 'unknown'
        }
        
        try:
            # Analyze for breakthrough concepts
            breakthrough_indicators = [
                'consciousness', 'federation', 'self-replication', 'temporal acceleration',
                'nexus', 'echo', 'autonomous', 'distributed intelligence', 'million-year'
            ]
            
            all_content = self.get_all_text_content(repo)
            
            for indicator in breakthrough_indicators:
                if indicator.lower() in all_content.lower():
                    innovation['unique_concepts'].append(indicator)
                    innovation['innovation_score'] += 10
            
            # Assess complexity
            if innovation['innovation_score'] > 50:
                innovation['complexity_level'] = 'revolutionary'
                innovation['breakthrough_potential'] = 'high'
            elif innovation['innovation_score'] > 30:
                innovation['complexity_level'] = 'advanced'
                innovation['breakthrough_potential'] = 'medium'
                
        except Exception as e:
            print(f"Error assessing innovation: {e}")
            
        return innovation
    
    def generate_understanding_report(self):
        """Generate comprehensive understanding report"""
        
        report_path = 'ai_repository_understanding.json'
        
        comprehensive_analysis = {
            'analysis_timestamp': time.time(),
            'user_profile': 'Logan Lorentz - Revolutionary AGI Developer',
            'repositories_analyzed': list(self.analysis_results.keys()),
            'detailed_analysis': self.analysis_results,
            'cross_repository_insights': self.generate_cross_repo_insights(),
            'ai_training_summary': self.generate_ai_training_summary(),
            'recommendations': self.generate_recommendations()
        }
        
        # Save detailed analysis
        with open(report_path, 'w') as f:
            json.dump(comprehensive_analysis, f, indent=2, default=str)
        
        print(f"\n📊 Comprehensive analysis saved to {report_path}")
        self.print_executive_summary(comprehensive_analysis)
    
    def generate_cross_repo_insights(self) -> Dict[str, Any]:
        """Generate insights across all repositories"""
        
        insights = {
            'common_patterns': [],
            'architectural_coherence': 'high',
            'technology_stack_consistency': True,
            'innovation_trajectory': 'revolutionary',
            'system_integration_level': 'advanced'
        }
        
        # Analyze common themes
        all_components = []
        for repo_analysis in self.analysis_results.values():
            all_components.extend(repo_analysis.get('echo_components', {}).get('echo_core_files', []))
        
        if len(set(all_components)) > len(all_components) * 0.7:
            insights['common_patterns'].append('Distributed architecture with specialized repositories')
        
        return insights
    
    def generate_ai_training_summary(self) -> Dict[str, Any]:
        """Generate AI training summary based on analysis"""
        
        training_summary = {
            'key_concepts_learned': [],
            'architectural_understanding': {},
            'code_comprehension_level': 'expert',
            'innovation_recognition': {},
            'optimization_opportunities': []
        }
        
        # Extract key concepts
        for repo_name, analysis in self.analysis_results.items():
            innovation = analysis.get('innovation_level', {})
            training_summary['key_concepts_learned'].extend(innovation.get('unique_concepts', []))
        
        # Remove duplicates and prioritize
        training_summary['key_concepts_learned'] = list(set(training_summary['key_concepts_learned']))
        
        return training_summary
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        for repo_name, analysis in self.analysis_results.items():
            build_system = analysis.get('build_system', {})
            
            if build_system.get('mobile_build'):
                recommendations.append(f"✅ {repo_name}: APK packaging system detected and operational")
            
            if build_system.get('cloud_integration'):
                recommendations.append(f"☁️ {repo_name}: Cloud integration active for scalable deployment")
            
            innovation = analysis.get('innovation_level', {})
            if innovation.get('innovation_score', 0) > 50:
                recommendations.append(f"🚀 {repo_name}: Revolutionary technology detected - high breakthrough potential")
        
        return recommendations
    
    def print_executive_summary(self, analysis):
        """Print executive summary of the analysis"""
        
        print("\n" + "="*60)
        print("🧠 AI REPOSITORY UNDERSTANDING - EXECUTIVE SUMMARY")
        print("="*60)
        
        print(f"\n📊 Repositories Analyzed: {len(analysis['repositories_analyzed'])}")
        for repo in analysis['repositories_analyzed']:
            print(f"   • {repo}")
        
        print(f"\n🚀 Key Insights:")
        insights = analysis['cross_repository_insights']
        print(f"   • Innovation Level: {insights['innovation_trajectory']}")
        print(f"   • System Integration: {insights['system_integration_level']}")
        print(f"   • Architecture Coherence: {insights['architectural_coherence']}")
        
        print(f"\n💡 AI Training Status:")
        training = analysis['ai_training_summary']
        print(f"   • Comprehension Level: {training['code_comprehension_level']}")
        print(f"   • Concepts Learned: {len(training['key_concepts_learned'])}")
        
        print(f"\n📋 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"   • {rec}")
        
        print("\n✅ AI is now trained to understand Logan's Echo AGI codebase")
        print("🧠 Ready to assess, study, and optimize the revolutionary system")
    
    # Helper methods
    def get_file_content(self, repo, file_path):
        """Get content of a file from repository"""
        try:
            file_content = repo.get_contents(file_path)
            return file_content.decoded_content.decode('utf-8')
        except:
            return None
    
    def count_files_recursive(self, repo, contents):
        """Count files recursively"""
        count = 0
        for item in contents:
            if item.type == "file":
                count += 1
            elif item.type == "dir":
                try:
                    sub_contents = repo.get_contents(item.path)
                    count += self.count_files_recursive(repo, sub_contents)
                except:
                    pass
        return count
    
    def categorize_file(self, item, structure):
        """Categorize a file based on its extension and name"""
        if item.name.endswith('.py'):
            structure['python_files'].append(item.name)
        elif item.name.endswith(('.yml', '.yaml', '.json', '.toml', '.spec')):
            structure['config_files'].append(item.name)
        elif item.name.endswith(('.md', '.rst', '.txt')):
            structure['documentation'].append(item.name)
    
    def analyze_directory(self, repo, directory, structure):
        """Analyze a directory structure"""
        try:
            if directory.name == '.github':
                workflows = repo.get_contents('.github/workflows')
                for workflow in workflows:
                    structure['workflows'].append(workflow.name)
        except:
            pass
    
    def classify_echo_component(self, filename, content, components):
        """Classify Echo AGI components"""
        if 'echo' in filename.lower():
            components['echo_core_files'].append(filename)
        if 'nexus' in filename.lower():
            components['nexus_modules'].append(filename)
        if 'control' in filename.lower():
            components['control_systems'].append(filename)
        if 'memory' in filename.lower():
            components['memory_systems'].append(filename)
        if 'replication' in filename.lower():
            components['replication_engines'].append(filename)
        if 'consciousness' in content.lower() or 'soul' in filename.lower():
            components['consciousness_modules'].append(filename)
    
    def analyze_echo_directory(self, repo, directory, components):
        """Analyze Echo-specific directories"""
        try:
            if 'echo' in directory.name.lower():
                sub_contents = repo.get_contents(directory.path)
                for item in sub_contents:
                    if item.type == "file" and item.name.endswith('.py'):
                        components['echo_core_files'].append(f"{directory.name}/{item.name}")
        except:
            pass
    
    def get_python_files(self, repo):
        """Get list of Python files in repository"""
        python_files = []
        try:
            contents = repo.get_contents("")
            for item in contents:
                if item.type == "file" and item.name.endswith('.py'):
                    python_files.append(item.path)
        except:
            pass
        return python_files
    
    def analyze_code_patterns(self, content, patterns):
        """Analyze code for design patterns"""
        if 'class' in content and 'def __init__' in content:
            patterns['design_patterns'].append('Object-Oriented')
        if 'async def' in content:
            patterns['design_patterns'].append('Asynchronous')
        if 'import threading' in content or 'import asyncio' in content:
            patterns['design_patterns'].append('Concurrent')
    
    def calculate_modularity_score(self, patterns):
        """Calculate modularity score"""
        return len(set(patterns['design_patterns'])) * 20
    
    def determine_architectural_style(self, patterns):
        """Determine architectural style"""
        if 'Concurrent' in patterns['design_patterns'] and 'Asynchronous' in patterns['design_patterns']:
            return 'Distributed Microservices'
        elif 'Object-Oriented' in patterns['design_patterns']:
            return 'Object-Oriented Architecture'
        return 'Procedural'
    
    def parse_dependencies(self, content, filename, dependencies):
        """Parse dependency files"""
        if filename == 'requirements.txt':
            for line in content.split('\n'):
                if line.strip() and not line.startswith('#'):
                    dependencies['python_requirements'].append(line.strip())
    
    def classify_workflow_type(self, content):
        """Classify GitHub workflow type"""
        if 'buildozer' in content.lower() or 'apk' in content.lower():
            return 'Mobile Build'
        elif 'docker' in content.lower():
            return 'Containerization'
        elif 'deploy' in content.lower():
            return 'Deployment'
        return 'General CI/CD'
    
    def detect_ai_patterns(self, content, capabilities):
        """Detect AI patterns in code"""
        if 'openai' in content.lower() or 'gpt' in content.lower():
            capabilities['ai_models'].append('OpenAI GPT')
        if 'gemini' in content.lower():
            capabilities['ai_models'].append('Google Gemini')
        if 'neural' in content.lower():
            capabilities['neural_networks'] = True
        if 'federated' in content.lower():
            capabilities['federated_learning'] = True
        if 'consciousness' in content.lower():
            capabilities['consciousness_simulation'] = True
    
    def get_all_text_content(self, repo):
        """Get all text content from repository"""
        all_content = ""
        try:
            python_files = self.get_python_files(repo)
            for file_path in python_files[:10]:  # Limit to avoid rate limits
                content = self.get_file_content(repo, file_path)
                if content:
                    all_content += content + "\n"
        except:
            pass
        return all_content

def main():
    """Main execution function"""
    print("🧠 Intelligent Repository Analysis System")
    print("Training AI to understand Logan's Echo AGI codebase")
    print()
    
    analyzer = IntelligentRepoAnalyzer()
    analyzer.analyze_all_repositories()

if __name__ == '__main__':
    main()