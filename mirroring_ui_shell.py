"""
Mirroring UI Shell - Interactive Interface for AGI Learning System
"""

import streamlit as st
from mirror_logger import MirrorLogger, GhostHandsMode
from mimic_engine import MimicEngine
from human_interface import HumanInteractionTracker, StyleProfile
from utils.github_helper import GitHubHelper
from echo_learning_system import EchoLearningSystem, AutonomousWorkflowManager
import json

def init_mirroring_system():
    """Initialize the complete mirroring system"""
    if 'mirror_logger' not in st.session_state:
        st.session_state.mirror_logger = MirrorLogger()
    
    if 'mimic_engine' not in st.session_state:
        st.session_state.mimic_engine = MimicEngine(st.session_state.mirror_logger)
    
    if 'human_interface' not in st.session_state:
        st.session_state.human_interface = HumanInteractionTracker(st.session_state.mirror_logger)
    
    if 'ghost_hands' not in st.session_state:
        st.session_state.ghost_hands = GhostHandsMode(st.session_state.mirror_logger)
    
    if 'github_helper' not in st.session_state:
        st.session_state.github_helper = GitHubHelper()
    
    if 'learning_system' not in st.session_state:
        st.session_state.learning_system = EchoLearningSystem()
    
    if 'autonomous_manager' not in st.session_state:
        st.session_state.autonomous_manager = AutonomousWorkflowManager(
            st.session_state.github_helper,
            st.session_state.learning_system
        )

def render_mirroring_dashboard():
    """Render the main mirroring system dashboard"""
    st.header("🔁 EchoNexus AGI Mirroring System")
    st.write("Comprehensive behavioral learning and mimicry interface")
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        observation_count = len(st.session_state.mirror_logger.history)
        st.metric("Observations", observation_count)
    
    with col2:
        pattern_count = len(st.session_state.mirror_logger.get_learning_patterns()['developer_behaviors'])
        st.metric("Learned Patterns", pattern_count)
    
    with col3:
        feedback_count = len(st.session_state.human_interface.feedback_history)
        st.metric("Human Feedback", feedback_count)
    
    with col4:
        suggestions = st.session_state.ghost_hands.get_suggestions()
        st.metric("Ghost Suggestions", len(suggestions))
    
    # Tabs for different functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Observation Logger", 
        "🎭 Mimicry Engine", 
        "👥 Human Interface", 
        "👻 Ghost Hands", 
        "🤖 Autonomous Execution"
    ])
    
    with tab1:
        render_observation_logger()
    
    with tab2:
        render_mimicry_engine()
    
    with tab3:
        render_human_interface()
    
    with tab4:
        render_ghost_hands()
    
    with tab5:
        render_autonomous_execution()

def render_observation_logger():
    """Render the observation logging interface"""
    st.subheader("📝 Observation Logger")
    st.write("Log developer actions and behaviors for AGI learning")
    
    # Manual observation entry
    with st.expander("➕ Add Manual Observation"):
        col1, col2 = st.columns(2)
        
        with col1:
            action = st.text_input("Developer Action", placeholder="e.g., fix_workflow_artifact_issue")
            thought = st.text_area("Thought Process", placeholder="What was the reasoning behind this action?")
        
        with col2:
            context = st.text_input("Context", placeholder="e.g., successful_build_no_artifacts")
            timing = st.number_input("Timing (seconds)", min_value=0.1, value=1.0, step=0.1)
        
        success = st.checkbox("Action was successful", value=True)
        
        if st.button("Log Observation"):
            obs_id = st.session_state.mirror_logger.observe_developer_action(
                action=action,
                thought_process=thought,
                context=context,
                timing=timing,
                success=success
            )
            st.success(f"Observation logged with ID: {obs_id}")
    
    # Recent observations
    st.subheader("📊 Recent Observations")
    recent_obs = st.session_state.mirror_logger.history[-5:]
    
    for i, obs in enumerate(reversed(recent_obs), 1):
        with st.expander(f"Observation {i}: {obs.get('input', 'Unknown')[:50]}..."):
            st.write(f"**Timestamp:** {obs.get('timestamp', 'Unknown')}")
            st.write(f"**Input:** {obs.get('input', 'Unknown')}")
            st.write(f"**Response:** {obs.get('response', 'Unknown')}")
            st.write(f"**Outcome:** {obs.get('outcome', 'Unknown')}")
            
            if obs.get('context'):
                st.json(obs['context'])
    
    # Search observations
    st.subheader("🔍 Search Observations")
    search_keywords = st.text_input("Search keywords (comma-separated)")
    
    if search_keywords:
        keywords = [kw.strip() for kw in search_keywords.split(',')]
        similar_obs = st.session_state.mirror_logger.get_similar_observations(keywords, limit=10)
        
        st.write(f"Found {len(similar_obs)} matching observations:")
        for obs in similar_obs:
            relevance = obs.get('relevance_score', 0)
            st.write(f"**Relevance: {relevance:.2f}** - {obs.get('input', 'Unknown')[:100]}...")

def render_mimicry_engine():
    """Render the mimicry engine interface"""
    st.subheader("🎭 Mimicry Engine")
    st.write("Analyze and mimic code styles and patterns")
    
    # Code analysis section
    st.subheader("📊 Code Analysis")
    example_code = st.text_area(
        "Example Code to Analyze",
        placeholder="Paste code here to analyze its style and structure...",
        height=200
    )
    
    if example_code and st.button("Analyze Code"):
        features = st.session_state.mimic_engine.analyze_code_features(example_code)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Structure")
            st.json(features['structure'])
            
            st.subheader("Patterns")
            st.json(features['patterns'])
        
        with col2:
            st.subheader("Style")
            st.json(features['style'])
            
            st.subheader("Complexity")
            st.json(features['complexity'])
    
    # Mimicry generation
    st.subheader("🎨 Generate Mimicked Code")
    col1, col2 = st.columns(2)
    
    with col1:
        mimic_goal = st.text_input("Goal for new code", placeholder="e.g., data processing function")
    
    with col2:
        if example_code and mimic_goal and st.button("Generate Mimicked Code"):
            mimicked = st.session_state.mimic_engine.mimic_style(example_code, mimic_goal)
            
            st.subheader("Generated Code")
            st.code(mimicked, language='python')
            
            # Self-evaluation
            if st.button("Evaluate Mimicry"):
                evaluation = st.session_state.mimic_engine.self_evaluate(example_code, mimicked)
                
                st.subheader("Mimicry Evaluation")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Similarity", f"{evaluation['overall_similarity']:.2f}")
                
                with col2:
                    st.metric("Structure Match", f"{evaluation['structure_similarity']:.2f}")
                
                with col3:
                    st.metric("Style Match", f"{evaluation['style_similarity']:.2f}")
                
                if evaluation['recommendations']:
                    st.subheader("Recommendations")
                    for rec in evaluation['recommendations']:
                        st.write(f"• {rec}")

def render_human_interface():
    """Render the human interaction interface"""
    st.subheader("👥 Human Learning Interface")
    st.write("Learn from human feedback and corrections")
    
    # User profile selection
    user_id = st.selectbox(
        "Select User Profile",
        options=list(st.session_state.human_interface.user_profiles.keys()) + ["Create New"],
        index=0 if st.session_state.human_interface.user_profiles else 0
    )
    
    if user_id == "Create New":
        new_user_id = st.text_input("New User ID")
        if new_user_id:
            user_id = new_user_id
    
    if user_id and user_id != "Create New":
        user_profile = st.session_state.human_interface.get_user_profile(user_id)
        
        # User preferences
        with st.expander("⚙️ User Preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                coding_style = st.selectbox("Coding Style", ["adaptive", "explicit", "concise"], 
                                          index=["adaptive", "explicit", "concise"].index(user_profile.preferences.get('coding_style', 'adaptive')))
                indentation = st.selectbox("Indentation", ["spaces", "tabs"],
                                         index=["spaces", "tabs"].index(user_profile.preferences.get('indentation', 'spaces')))
                comment_density = st.selectbox("Comment Density", ["low", "moderate", "high"],
                                             index=["low", "moderate", "high"].index(user_profile.preferences.get('comment_density', 'moderate')))
            
            with col2:
                line_length = st.number_input("Max Line Length", min_value=60, max_value=120, 
                                            value=user_profile.preferences.get('line_length', 80))
                type_hints = st.checkbox("Use Type Hints", value=user_profile.preferences.get('type_hints', True))
                error_handling = st.selectbox("Error Handling", ["explicit", "minimal"],
                                            index=["explicit", "minimal"].index(user_profile.preferences.get('error_handling', 'explicit')))
            
            if st.button("Update Preferences"):
                user_profile.preferences.update({
                    'coding_style': coding_style,
                    'indentation': indentation,
                    'comment_density': comment_density,
                    'line_length': line_length,
                    'type_hints': type_hints,
                    'error_handling': error_handling
                })
                st.session_state.human_interface.save_interaction_history()
                st.success("Preferences updated!")
        
        # Feedback logging
        st.subheader("📝 Log Feedback")
        col1, col2 = st.columns(2)
        
        with col1:
            original_code = st.text_area("Original Code", height=150)
            feedback_type = st.selectbox("Feedback Type", ["correction", "improvement", "style_change"])
        
        with col2:
            corrected_code = st.text_area("Corrected Code", height=150)
            
            if original_code and corrected_code and st.button("Log Feedback"):
                feedback_id = st.session_state.human_interface.log_feedback(
                    original_code, corrected_code, feedback_type, user_id
                )
                st.success(f"Feedback logged with ID: {feedback_id}")
        
        # User insights
        st.subheader("📊 User Insights")
        recommendations = st.session_state.human_interface.get_personalized_recommendations(user_id, "general")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Style Recommendations:**")
            style_recs = recommendations['style_preferences']
            for key, value in style_recs.items():
                st.write(f"• {key}: {value}")
        
        with col2:
            st.write(f"**Confidence Level:** {recommendations['confidence']:.2f}")
            st.write(f"**Learned Patterns:** {len(recommendations['learned_patterns'])}")

def render_ghost_hands():
    """Render the ghost hands mode interface"""
    st.subheader("👻 Ghost Hands Mode")
    st.write("Stealth observation and confidence-based suggestions")
    
    # Current suggestions
    suggestions = st.session_state.ghost_hands.get_suggestions()
    
    if suggestions:
        st.subheader("💡 Ready Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            with st.expander(f"Suggestion {i}: {suggestion['action']}"):
                st.write(f"**Confidence:** {suggestion['confidence']:.2f}")
                st.write(f"**Context:** {suggestion['context']}")
                st.write(f"**Learned From:** {suggestion['learned_from']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Accept Suggestion {i}"):
                        st.success("Suggestion accepted! Logging positive feedback...")
                        st.session_state.human_interface.log_approval(suggestion['action'])
                
                with col2:
                    if st.button(f"Reject Suggestion {i}"):
                        rejection_reason = st.text_input(f"Rejection reason for suggestion {i}")
                        if rejection_reason:
                            st.session_state.human_interface.log_rejection(suggestion['action'], rejection_reason)
                            st.warning("Suggestion rejected. Learning from feedback...")
    else:
        st.info("No suggestions ready. Ghost Hands is observing silently...")
    
    # Shadow activity logging
    st.subheader("👤 Shadow Activity")
    col1, col2 = st.columns(2)
    
    with col1:
        shadow_action = st.text_input("Action to Shadow")
        shadow_context = st.text_input("Shadow Context")
    
    with col2:
        if shadow_action and shadow_context and st.button("Log Shadow Activity"):
            observation = st.session_state.ghost_hands.shadow_activity(shadow_action, shadow_context)
            st.success(f"Shadow activity logged with confidence: {observation['confidence']:.2f}")
    
    # Configuration
    st.subheader("⚙️ Ghost Hands Configuration")
    current_threshold = st.session_state.ghost_hands.confidence_threshold
    new_threshold = st.slider("Confidence Threshold", 0.0, 1.0, current_threshold, 0.1)
    
    if new_threshold != current_threshold:
        st.session_state.ghost_hands.confidence_threshold = new_threshold
        st.info(f"Confidence threshold updated to {new_threshold:.1f}")

def render_autonomous_execution():
    """Render the autonomous execution interface"""
    st.subheader("🤖 Autonomous AGI Execution")
    st.write("Watch the AGI execute tasks autonomously with learning")
    
    # Repository input
    repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/username/repo")
    
    if repo_url:
        # Parse repository
        if "/github.com/" in repo_url:
            parts = repo_url.split("/")[-2:]
            owner, repo = parts[0], parts[1]
            
            st.write(f"**Target:** {owner}/{repo}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Run Autonomous Diagnostic"):
                    with st.spinner("AGI performing autonomous diagnostic..."):
                        diagnostic = st.session_state.autonomous_manager.execute_autonomous_workflow_management(owner, repo)
                        
                        st.subheader("🤖 AGI Execution Report")
                        st.write(f"**Success:** {diagnostic.get('success', False)}")
                        
                        if diagnostic.get('actions_taken'):
                            st.write("**Actions Taken:**")
                            for i, action in enumerate(diagnostic['actions_taken'], 1):
                                st.write(f"{i}. {action}")
                        
                        if diagnostic.get('error'):
                            st.error(f"Error: {diagnostic['error']}")
            
            with col2:
                if st.button("📊 View Learning Patterns"):
                    patterns = st.session_state.mirror_logger.get_learning_patterns()
                    
                    st.subheader("📈 Learning Summary")
                    st.write(f"**Developer Behaviors:** {len(patterns['developer_behaviors'])}")
                    st.write(f"**Successful Sequences:** {len(patterns['successful_sequences'])}")
                    st.write(f"**Code Corrections:** {len(patterns['code_corrections'])}")
                    
                    if patterns['developer_behaviors']:
                        st.subheader("Recent Developer Behaviors")
                        for behavior in patterns['developer_behaviors'][-3:]:
                            st.write(f"• {behavior['action']}: {behavior['thought']}")
    
    # Learning statistics
    st.subheader("📊 Learning Statistics")
    
    # Get correction insights
    insights = st.session_state.human_interface.get_correction_insights()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Frequent Corrections:**")
        for correction_type, count in insights['frequent_corrections']:
            st.write(f"• {correction_type}: {count} times")
    
    with col2:
        st.write("**User Trends:**")
        for user_id, trends in insights['user_trends'].items():
            st.write(f"• {user_id}: {trends['total_corrections']} corrections")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="EchoNexus Mirroring System",
        page_icon="🔁",
        layout="wide"
    )
    
    # Initialize systems
    init_mirroring_system()
    
    # Render main interface
    render_mirroring_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown("🧠 **EchoNexus AGI Mirroring System** - Learning from developer behavior patterns")

if __name__ == "__main__":
    main()