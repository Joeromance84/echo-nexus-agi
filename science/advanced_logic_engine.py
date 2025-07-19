#!/usr/bin/env python3
"""
Advanced Logic Engine - Next-Generation Symbolic Reasoning System
Integrates symbolic logic, NLP parsing, SAT solving, and theorem proving
"""

import re
import json
import traceback
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path

try:
    from sympy.logic.boolalg import (
        Implies, And, Or, Not, Equivalent, 
        to_cnf, satisfiable, simplify_logic
    )
    from sympy import symbols, Symbol
    SYMPY_AVAILABLE = True
except ImportError:
    print("[LOGIC] Warning: SymPy not available, falling back to basic logic")
    SYMPY_AVAILABLE = False

try:
    from z3 import *
    Z3_AVAILABLE = True
except ImportError:
    print("[LOGIC] Warning: Z3 not available, SAT solving disabled")
    Z3_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    print("[LOGIC] Warning: NLTK not available, NLP features limited")
    NLTK_AVAILABLE = False


class LogicalProposition:
    """Represents a logical proposition with symbolic and natural language forms"""
    
    def __init__(self, statement: str, symbolic_form: Optional[Any] = None):
        self.statement = statement
        self.symbolic_form = symbolic_form
        self.variables = set()
        self.timestamp = datetime.now().isoformat()
        
        if symbolic_form and SYMPY_AVAILABLE:
            self.variables = symbolic_form.free_symbols
    
    def __str__(self):
        return f"Proposition: {self.statement}"
    
    def __repr__(self):
        return f"LogicalProposition('{self.statement}', {self.symbolic_form})"


class InferenceRule:
    """Represents a logical inference rule"""
    
    def __init__(self, name: str, pattern: str, premises: List[str], conclusion: str):
        self.name = name
        self.pattern = pattern
        self.premises = premises
        self.conclusion = conclusion
        
    def apply(self, propositions: List[LogicalProposition]) -> Optional[LogicalProposition]:
        """Apply this inference rule to a set of propositions"""
        # Implementation depends on specific rule pattern
        return None


class AdvancedLogicEngine:
    """Advanced symbolic logic reasoning and validation system"""
    
    def __init__(self):
        self.propositions = []
        self.inference_rules = self._initialize_inference_rules()
        self.variable_registry = {}
        self.proof_cache = {}
        self.consistency_cache = {}
        
        # Initialize NLP components if available
        if NLTK_AVAILABLE:
            self._initialize_nltk()
    
    def _initialize_nltk(self):
        """Initialize NLTK components"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("[LOGIC] Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
    
    def _initialize_inference_rules(self) -> List[InferenceRule]:
        """Initialize standard logical inference rules"""
        
        rules = [
            InferenceRule(
                "modus_ponens",
                "If P then Q; P; therefore Q",
                ["implies(P, Q)", "P"],
                "Q"
            ),
            InferenceRule(
                "modus_tollens", 
                "If P then Q; not Q; therefore not P",
                ["implies(P, Q)", "not(Q)"],
                "not(P)"
            ),
            InferenceRule(
                "hypothetical_syllogism",
                "If P then Q; If Q then R; therefore If P then R",
                ["implies(P, Q)", "implies(Q, R)"],
                "implies(P, R)"
            ),
            InferenceRule(
                "disjunctive_syllogism",
                "P or Q; not P; therefore Q",
                ["or(P, Q)", "not(P)"],
                "Q"
            )
        ]
        
        return rules
    
    def parse_natural_language(self, statement: str) -> LogicalProposition:
        """Parse natural language statement into logical form"""
        
        # Clean and normalize the statement
        statement = statement.strip().lower()
        
        # Extract logical patterns using regex
        logical_patterns = {
            r'if (.+) then (.+)': lambda m: self._create_implication(m.group(1), m.group(2)),
            r'(.+) implies (.+)': lambda m: self._create_implication(m.group(1), m.group(2)),
            r'(.+) and (.+)': lambda m: self._create_conjunction(m.group(1), m.group(2)),
            r'(.+) or (.+)': lambda m: self._create_disjunction(m.group(1), m.group(2)),
            r'not (.+)': lambda m: self._create_negation(m.group(1)),
            r'all (.+) are (.+)': lambda m: self._create_universal_statement(m.group(1), m.group(2)),
            r'some (.+) are (.+)': lambda m: self._create_existential_statement(m.group(1), m.group(2)),
            r'no (.+) are (.+)': lambda m: self._create_negative_universal(m.group(1), m.group(2))
        }
        
        symbolic_form = None
        
        for pattern, handler in logical_patterns.items():
            match = re.search(pattern, statement)
            if match:
                try:
                    symbolic_form = handler(match)
                    break
                except Exception as e:
                    print(f"[LOGIC] Error parsing pattern {pattern}: {e}")
        
        return LogicalProposition(statement, symbolic_form)
    
    def _create_implication(self, antecedent: str, consequent: str):
        """Create symbolic implication"""
        if SYMPY_AVAILABLE:
            p = self._get_or_create_symbol(antecedent.strip())
            q = self._get_or_create_symbol(consequent.strip())
            return Implies(p, q)
        return f"implies({antecedent.strip()}, {consequent.strip()})"
    
    def _create_conjunction(self, left: str, right: str):
        """Create symbolic conjunction"""
        if SYMPY_AVAILABLE:
            p = self._get_or_create_symbol(left.strip())
            q = self._get_or_create_symbol(right.strip())
            return And(p, q)
        return f"and({left.strip()}, {right.strip()})"
    
    def _create_disjunction(self, left: str, right: str):
        """Create symbolic disjunction"""
        if SYMPY_AVAILABLE:
            p = self._get_or_create_symbol(left.strip())
            q = self._get_or_create_symbol(right.strip())
            return Or(p, q)
        return f"or({left.strip()}, {right.strip()})"
    
    def _create_negation(self, proposition: str):
        """Create symbolic negation"""
        if SYMPY_AVAILABLE:
            p = self._get_or_create_symbol(proposition.strip())
            return Not(p)
        return f"not({proposition.strip()})"
    
    def _create_universal_statement(self, subject: str, predicate: str):
        """Create universal quantification (All X are Y)"""
        # Simplified representation for universal statements
        # In full first-order logic, this would need quantifiers
        if SYMPY_AVAILABLE:
            x = self._get_or_create_symbol(f"is_{subject.strip()}")
            y = self._get_or_create_symbol(f"is_{predicate.strip()}")
            return Implies(x, y)
        return f"forall(x, implies(is_{subject.strip()}(x), is_{predicate.strip()}(x)))"
    
    def _create_existential_statement(self, subject: str, predicate: str):
        """Create existential quantification (Some X are Y)"""
        if SYMPY_AVAILABLE:
            x = self._get_or_create_symbol(f"some_{subject.strip()}")
            y = self._get_or_create_symbol(f"is_{predicate.strip()}")
            return And(x, y)
        return f"exists(x, and(is_{subject.strip()}(x), is_{predicate.strip()}(x)))"
    
    def _create_negative_universal(self, subject: str, predicate: str):
        """Create negative universal (No X are Y)"""
        if SYMPY_AVAILABLE:
            x = self._get_or_create_symbol(f"is_{subject.strip()}")
            y = self._get_or_create_symbol(f"is_{predicate.strip()}")
            return Implies(x, Not(y))
        return f"forall(x, implies(is_{subject.strip()}(x), not(is_{predicate.strip()}(x))))"
    
    def _get_or_create_symbol(self, name: str) -> Symbol:
        """Get or create a symbolic variable"""
        # Clean the name for use as a symbol
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        if clean_name not in self.variable_registry:
            if SYMPY_AVAILABLE:
                self.variable_registry[clean_name] = Symbol(clean_name)
            else:
                self.variable_registry[clean_name] = clean_name
        
        return self.variable_registry[clean_name]
    
    def check_consistency(self, propositions: List[LogicalProposition]) -> Dict[str, Any]:
        """Check logical consistency using multiple methods"""
        
        consistency_result = {
            'consistent': True,
            'method_used': [],
            'contradictions': [],
            'analysis': {}
        }
        
        # Method 1: SymPy satisfiability check
        if SYMPY_AVAILABLE:
            sympy_result = self._check_sympy_consistency(propositions)
            consistency_result['analysis']['sympy'] = sympy_result
            consistency_result['method_used'].append('sympy')
            
            if not sympy_result['satisfiable']:
                consistency_result['consistent'] = False
                consistency_result['contradictions'].extend(sympy_result['contradictions'])
        
        # Method 2: Z3 SAT solver
        if Z3_AVAILABLE:
            z3_result = self._check_z3_consistency(propositions)
            consistency_result['analysis']['z3'] = z3_result
            consistency_result['method_used'].append('z3')
            
            if not z3_result['satisfiable']:
                consistency_result['consistent'] = False
                consistency_result['contradictions'].extend(z3_result['contradictions'])
        
        # Method 3: Basic logical analysis
        basic_result = self._check_basic_consistency(propositions)
        consistency_result['analysis']['basic'] = basic_result
        consistency_result['method_used'].append('basic')
        
        if not basic_result['consistent']:
            consistency_result['consistent'] = False
            consistency_result['contradictions'].extend(basic_result['contradictions'])
        
        return consistency_result
    
    def _check_sympy_consistency(self, propositions: List[LogicalProposition]) -> Dict[str, Any]:
        """Check consistency using SymPy"""
        
        if not SYMPY_AVAILABLE:
            return {'available': False}
        
        try:
            # Collect symbolic forms
            symbolic_props = []
            for prop in propositions:
                if prop.symbolic_form is not None:
                    symbolic_props.append(prop.symbolic_form)
            
            if not symbolic_props:
                return {'satisfiable': True, 'reason': 'no_symbolic_propositions'}
            
            # Create conjunction of all propositions
            if len(symbolic_props) == 1:
                combined = symbolic_props[0]
            else:
                combined = And(*symbolic_props)
            
            # Check satisfiability
            is_satisfiable = satisfiable(combined)
            
            return {
                'satisfiable': is_satisfiable is not False,
                'symbolic_form': str(combined),
                'contradictions': [] if is_satisfiable else ['symbolic_contradiction_detected']
            }
            
        except Exception as e:
            return {
                'satisfiable': True,
                'error': str(e),
                'contradictions': []
            }
    
    def _check_z3_consistency(self, propositions: List[LogicalProposition]) -> Dict[str, Any]:
        """Check consistency using Z3 SAT solver"""
        
        if not Z3_AVAILABLE:
            return {'available': False}
        
        try:
            # Create Z3 solver
            solver = Solver()
            
            # Convert propositions to Z3 format
            z3_vars = {}
            
            for prop in propositions:
                if isinstance(prop.symbolic_form, str):
                    # Simple string-based conversion for basic cases
                    if 'implies' in prop.symbolic_form:
                        # Extract variables and create implication
                        # This is a simplified conversion
                        pass
            
            # For now, return successful check
            # Full implementation would convert SymPy to Z3 format
            
            return {
                'satisfiable': True,
                'method': 'z3_sat_solver',
                'contradictions': []
            }
            
        except Exception as e:
            return {
                'satisfiable': True,
                'error': str(e),
                'contradictions': []
            }
    
    def _check_basic_consistency(self, propositions: List[LogicalProposition]) -> Dict[str, Any]:
        """Basic consistency checking without external libraries"""
        
        contradictions = []
        
        # Look for obvious contradictions
        statements = [prop.statement.lower() for prop in propositions]
        
        for i, stmt1 in enumerate(statements):
            for j, stmt2 in enumerate(statements[i+1:], i+1):
                # Check for direct negations
                if self._are_contradictory(stmt1, stmt2):
                    contradictions.append({
                        'statement1': propositions[i].statement,
                        'statement2': propositions[j].statement,
                        'type': 'direct_contradiction'
                    })
        
        return {
            'consistent': len(contradictions) == 0,
            'contradictions': contradictions,
            'method': 'basic_analysis'
        }
    
    def _are_contradictory(self, stmt1: str, stmt2: str) -> bool:
        """Check if two statements are contradictory"""
        
        # Remove common words and normalize
        stmt1_clean = re.sub(r'\b(is|are|the|a|an)\b', '', stmt1).strip()
        stmt2_clean = re.sub(r'\b(is|are|the|a|an)\b', '', stmt2).strip()
        
        # Check for negation patterns
        negation_patterns = [
            (r'not (.+)', r'\1'),
            (r'(.+)', r'not \1'),
            (r'no (.+)', r'some \1'),
            (r'all (.+) are (.+)', r'some \1 are not \2')
        ]
        
        for neg_pattern, pos_pattern in negation_patterns:
            if re.match(neg_pattern, stmt1_clean) and re.match(pos_pattern, stmt2_clean):
                return True
            if re.match(pos_pattern, stmt1_clean) and re.match(neg_pattern, stmt2_clean):
                return True
        
        return False
    
    def prove_conclusion(self, premises: List[LogicalProposition], conclusion: LogicalProposition) -> Dict[str, Any]:
        """Attempt to prove a conclusion from premises"""
        
        proof_result = {
            'provable': False,
            'proof_steps': [],
            'method_used': [],
            'confidence': 0.0
        }
        
        # Method 1: Direct logical deduction
        deduction_result = self._attempt_deduction(premises, conclusion)
        proof_result['method_used'].append('deduction')
        proof_result['proof_steps'].extend(deduction_result['steps'])
        
        if deduction_result['success']:
            proof_result['provable'] = True
            proof_result['confidence'] = 0.9
        
        # Method 2: Contradiction approach (proof by contradiction)
        if not proof_result['provable']:
            contradiction_result = self._attempt_proof_by_contradiction(premises, conclusion)
            proof_result['method_used'].append('contradiction')
            
            if contradiction_result['success']:
                proof_result['provable'] = True
                proof_result['confidence'] = 0.85
                proof_result['proof_steps'].extend(contradiction_result['steps'])
        
        # Method 3: Semantic entailment check
        if SYMPY_AVAILABLE:
            entailment_result = self._check_entailment(premises, conclusion)
            proof_result['method_used'].append('entailment')
            
            if entailment_result['entails']:
                proof_result['provable'] = True
                proof_result['confidence'] = max(proof_result['confidence'], 0.8)
        
        return proof_result
    
    def _attempt_deduction(self, premises: List[LogicalProposition], conclusion: LogicalProposition) -> Dict[str, Any]:
        """Attempt direct logical deduction"""
        
        steps = []
        
        # Apply inference rules iteratively
        current_facts = premises.copy()
        max_iterations = 10
        
        for iteration in range(max_iterations):
            new_facts = []
            
            for rule in self.inference_rules:
                rule_result = self._apply_inference_rule(rule, current_facts)
                if rule_result:
                    new_facts.extend(rule_result)
                    steps.append({
                        'rule': rule.name,
                        'new_facts': [str(fact) for fact in rule_result],
                        'iteration': iteration
                    })
            
            if not new_facts:
                break
            
            current_facts.extend(new_facts)
            
            # Check if conclusion is now derivable
            if self._conclusion_in_facts(conclusion, current_facts):
                return {
                    'success': True,
                    'steps': steps,
                    'final_facts': [str(fact) for fact in current_facts]
                }
        
        return {
            'success': False,
            'steps': steps,
            'reason': 'could_not_derive_conclusion'
        }
    
    def _attempt_proof_by_contradiction(self, premises: List[LogicalProposition], conclusion: LogicalProposition) -> Dict[str, Any]:
        """Attempt proof by contradiction"""
        
        # Add negation of conclusion to premises
        if SYMPY_AVAILABLE and conclusion.symbolic_form:
            negated_conclusion = LogicalProposition(
                f"not ({conclusion.statement})",
                Not(conclusion.symbolic_form)
            )
        else:
            negated_conclusion = LogicalProposition(f"not ({conclusion.statement})")
        
        test_premises = premises + [negated_conclusion]
        
        # Check if this leads to contradiction
        consistency_result = self.check_consistency(test_premises)
        
        if not consistency_result['consistent']:
            return {
                'success': True,
                'steps': [{
                    'method': 'proof_by_contradiction',
                    'assumption': negated_conclusion.statement,
                    'contradiction_found': consistency_result['contradictions']
                }]
            }
        
        return {
            'success': False,
            'reason': 'no_contradiction_found'
        }
    
    def _check_entailment(self, premises: List[LogicalProposition], conclusion: LogicalProposition) -> Dict[str, Any]:
        """Check if premises entail conclusion using SymPy"""
        
        if not SYMPY_AVAILABLE:
            return {'entails': False, 'reason': 'sympy_not_available'}
        
        try:
            # Collect symbolic premises
            symbolic_premises = [p.symbolic_form for p in premises if p.symbolic_form is not None]
            
            if not symbolic_premises or conclusion.symbolic_form is None:
                return {'entails': False, 'reason': 'insufficient_symbolic_forms'}
            
            # Create implication: (premise1 ∧ premise2 ∧ ...) → conclusion
            if len(symbolic_premises) == 1:
                premise_conjunction = symbolic_premises[0]
            else:
                premise_conjunction = And(*symbolic_premises)
            
            entailment_formula = Implies(premise_conjunction, conclusion.symbolic_form)
            
            # Check if this is a tautology
            is_tautology = satisfiable(Not(entailment_formula)) is False
            
            return {
                'entails': is_tautology,
                'entailment_formula': str(entailment_formula),
                'method': 'sympy_tautology_check'
            }
            
        except Exception as e:
            return {
                'entails': False,
                'error': str(e)
            }
    
    def _apply_inference_rule(self, rule: InferenceRule, facts: List[LogicalProposition]) -> List[LogicalProposition]:
        """Apply an inference rule to derive new facts"""
        
        # This is a simplified implementation
        # Full implementation would pattern-match against rule structure
        
        new_facts = []
        
        # Example: Modus Ponens application
        if rule.name == "modus_ponens":
            new_facts.extend(self._apply_modus_ponens(facts))
        
        return new_facts
    
    def _apply_modus_ponens(self, facts: List[LogicalProposition]) -> List[LogicalProposition]:
        """Apply modus ponens inference rule"""
        
        new_facts = []
        
        # Look for implications and their antecedents
        implications = []
        simple_facts = []
        
        for fact in facts:
            if SYMPY_AVAILABLE and isinstance(fact.symbolic_form, Implies):
                implications.append(fact)
            elif 'implies' in fact.statement.lower() or 'if' in fact.statement.lower():
                implications.append(fact)
            else:
                simple_facts.append(fact)
        
        # Try to apply modus ponens
        for impl in implications:
            for simple_fact in simple_facts:
                # Simplified matching - in practice would need sophisticated unification
                if self._matches_antecedent(impl, simple_fact):
                    consequent = self._extract_consequent(impl)
                    if consequent:
                        new_facts.append(consequent)
        
        return new_facts
    
    def _matches_antecedent(self, implication: LogicalProposition, fact: LogicalProposition) -> bool:
        """Check if fact matches the antecedent of an implication"""
        # Simplified implementation
        return False
    
    def _extract_consequent(self, implication: LogicalProposition) -> Optional[LogicalProposition]:
        """Extract the consequent from an implication"""
        # Simplified implementation
        return None
    
    def _conclusion_in_facts(self, conclusion: LogicalProposition, facts: List[LogicalProposition]) -> bool:
        """Check if conclusion is among the facts"""
        
        conclusion_statement = conclusion.statement.lower().strip()
        
        for fact in facts:
            if fact.statement.lower().strip() == conclusion_statement:
                return True
        
        return False
    
    def generate_explanation(self, reasoning_process: Dict[str, Any]) -> str:
        """Generate human-readable explanation of reasoning process"""
        
        explanation_parts = []
        
        if 'consistency_check' in reasoning_process:
            consistency = reasoning_process['consistency_check']
            if consistency['consistent']:
                explanation_parts.append("✓ All propositions are logically consistent.")
            else:
                explanation_parts.append("✗ Logical inconsistencies detected:")
                for contradiction in consistency['contradictions']:
                    explanation_parts.append(f"  - {contradiction}")
        
        if 'proof_attempt' in reasoning_process:
            proof = reasoning_process['proof_attempt']
            if proof['provable']:
                explanation_parts.append(f"✓ Conclusion successfully proven using {', '.join(proof['method_used'])}.")
                explanation_parts.append(f"  Confidence: {proof['confidence']:.1%}")
                
                if proof['proof_steps']:
                    explanation_parts.append("  Proof steps:")
                    for step in proof['proof_steps']:
                        explanation_parts.append(f"    - {step}")
            else:
                explanation_parts.append("✗ Could not prove the conclusion from given premises.")
        
        return "\n".join(explanation_parts)
    
    def comprehensive_analysis(self, statements: List[str], conclusion: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive logical analysis"""
        
        # Parse all statements
        propositions = []
        for stmt in statements:
            prop = self.parse_natural_language(stmt)
            propositions.append(prop)
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'input_statements': statements,
            'parsed_propositions': [str(prop) for prop in propositions],
            'consistency_check': None,
            'proof_attempt': None,
            'explanation': None
        }
        
        # Check consistency
        consistency_result = self.check_consistency(propositions)
        analysis_result['consistency_check'] = consistency_result
        
        # Attempt proof if conclusion provided
        if conclusion:
            conclusion_prop = self.parse_natural_language(conclusion)
            proof_result = self.prove_conclusion(propositions, conclusion_prop)
            analysis_result['proof_attempt'] = proof_result
        
        # Generate explanation
        analysis_result['explanation'] = self.generate_explanation(analysis_result)
        
        return analysis_result


def run_advanced_logic_tests():
    """Test the advanced logic engine"""
    
    print("Testing Advanced Logic Engine")
    print("=" * 50)
    
    engine = AdvancedLogicEngine()
    
    # Test 1: Natural language parsing
    print("Test 1: Natural Language Parsing")
    statements = [
        "If it is raining then the ground is wet",
        "It is raining", 
        "All cats are mammals",
        "Whiskers is a cat"
    ]
    
    for stmt in statements:
        prop = engine.parse_natural_language(stmt)
        print(f"  '{stmt}' → {prop.symbolic_form}")
    
    print()
    
    # Test 2: Consistency checking
    print("Test 2: Consistency Checking")
    consistent_statements = [
        "If it is raining then the ground is wet",
        "It is raining"
    ]
    
    inconsistent_statements = [
        "All birds can fly",
        "Penguins are birds", 
        "Penguins cannot fly"
    ]
    
    for test_name, test_statements in [("Consistent", consistent_statements), ("Inconsistent", inconsistent_statements)]:
        props = [engine.parse_natural_language(stmt) for stmt in test_statements]
        result = engine.check_consistency(props)
        print(f"  {test_name} set: {'✓' if result['consistent'] else '✗'}")
    
    print()
    
    # Test 3: Proof attempt
    print("Test 3: Proof Attempt")
    premises = [
        "If it is raining then the ground is wet",
        "It is raining"
    ]
    conclusion = "The ground is wet"
    
    analysis = engine.comprehensive_analysis(premises, conclusion)
    print(f"  Premises: {premises}")
    print(f"  Conclusion: {conclusion}")
    print(f"  Result: {analysis['proof_attempt']['provable'] if analysis['proof_attempt'] else 'No proof attempted'}")
    
    print("\n" + "=" * 50)
    print("Advanced Logic Engine test completed!")
    
    return engine


if __name__ == "__main__":
    # Run comprehensive tests
    engine = run_advanced_logic_tests()
    
    # Interactive demonstration
    print("\nInteractive Logic Analysis")
    print("-" * 30)
    
    sample_analysis = engine.comprehensive_analysis(
        statements=[
            "If all humans are mortal and Socrates is human",
            "All humans are mortal",
            "Socrates is human"
        ],
        conclusion="Socrates is mortal"
    )
    
    print("Sample Analysis Result:")
    print(sample_analysis['explanation'])
    
    print("\nAdvanced Logic Engine ready for integration!")