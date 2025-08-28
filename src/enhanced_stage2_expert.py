"""
Enhanced Stage 2: Expert-Level Evidence Hunting
Save as: src/enhanced_stage2_expert.py

Uses expert-persona prompts for maximum depth analysis that generates
the sophisticated technical debates real academics would have.
"""

import requests
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from expert_deep_prompts import ExpertDeepPrompts
from enhanced_analyzer import CoreUnderstanding


@dataclass 
class ExpertEvidence:
    """Evidence analyzed from multiple expert perspectives"""
    claim: str
    statistician_analysis: str
    methodologist_analysis: str
    domain_expert_analysis: str
    replication_expert_analysis: str
    evidence_strength_detailed: Dict[str, str]  # statistical, methodological, replication, domain
    specific_debate_points: Dict[str, List[str]]  # optimist vs skeptic with exact technical details


@dataclass
class FieldControversies:
    """Field-specific controversies and expert debate ammunition"""
    methodological_controversies: List[str]
    statistical_controversies: List[str] 
    domain_technical_disputes: List[str]
    generalizability_wars: List[str]
    reproducibility_ammunition: List[str]
    comparative_analysis: List[str]  # vs competing approaches


@dataclass
class ExpertDeepDive:
    """Maximum technical depth analysis"""
    algorithmic_specifications: List[str]
    experimental_precision: List[str]
    implementation_granularity: List[str]
    numerical_precision: List[str]
    methodological_choices: List[str]
    limitation_specifications: List[str]


@dataclass
class ComprehensiveExpertAnalysis:
    """Complete expert-level analysis with maximum depth"""
    expert_evidence_mappings: List[ExpertEvidence]
    field_controversies: FieldControversies
    expert_deep_dive: ExpertDeepDive
    comparative_field_analysis: List[str]
    expert_debate_scenarios: List[Dict[str, str]]  # Realistic expert debate conversations


class EnhancedStage2Expert:
    """Enhanced Stage 2 using expert-level deep analysis prompts"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.expert_prompts = ExpertDeepPrompts()
    
    def _call_ollama(self, prompt: str, max_length: int = 4000) -> str:
        """Enhanced Ollama call for complex expert analysis"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,  # Lower for more focused expert analysis
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=500)  # Longer for complex analysis
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Expert Analysis Error: {str(e)}]"
    
    def expert_evidence_analysis(self, core_understanding: CoreUnderstanding, 
                                full_text: str) -> List[ExpertEvidence]:
        """Analyze evidence using multiple expert perspectives"""
        
        print("🔬 Expert Evidence Analysis: Multi-expert perspective analysis...")
        
        # Get main claims
        main_claims = self._extract_key_claims(core_understanding)
        field = core_understanding.field_classification
        
        expert_evidence_list = []
        
        for claim in main_claims[:3]:  # Focus on top 3 claims for depth
            print(f"   🎯 Analyzing claim: {claim[:60]}...")
            
            # Find relevant evidence from full text
            evidence_text = self._find_evidence_for_claim(claim, full_text)
            
            if not evidence_text:
                continue
            
            # Generate multi-expert analysis prompt
            multi_expert_prompt = self.expert_prompts.generate_multi_expert_analysis_prompt(
                claim, evidence_text, field
            )
            
            # Get comprehensive expert analysis
            expert_response = self._call_ollama(multi_expert_prompt, max_length=5000)
            
            # Parse expert perspectives
            expert_evidence = self._parse_multi_expert_response(claim, expert_response)
            expert_evidence_list.append(expert_evidence)
            
            print(f"   ✅ Multi-expert analysis complete for claim")
        
        return expert_evidence_list
    
    def field_controversy_analysis(self, core_understanding: CoreUnderstanding,
                                 full_text: str) -> FieldControversies:
        """Find field-specific controversies that experts actually fight about"""
        
        print("⚔️ Field Controversy Analysis: Finding real academic battles...")
        
        field = core_understanding.field_classification
        
        # Generate field-specific controversy prompt
        controversy_prompt = self.expert_prompts.generate_field_specific_controversy_prompt(
            field, full_text[:5000]
        )
        
        # Get controversy analysis
        controversy_response = self._call_ollama(controversy_prompt, max_length=4000)
        
        # Parse controversies
        controversies = self._parse_field_controversies(controversy_response)
        
        print(f"   ✅ Found {sum(len(v) for v in [controversies.methodological_controversies, controversies.statistical_controversies, controversies.domain_technical_disputes, controversies.generalizability_wars, controversies.reproducibility_ammunition])} specific controversy points")
        
        return controversies
    
    def expert_technical_deep_dive(self, full_text: str, field: str) -> ExpertDeepDive:
        """Extract maximum technical depth using expert perspective"""
        
        print("🔬 Expert Technical Deep Dive: Maximum granularity extraction...")
        
        # Find technical sections
        technical_sections = self._extract_technical_sections(full_text)
        
        all_algorithmic = []
        all_experimental = []
        all_implementation = []
        all_numerical = []
        all_methodological = []
        all_limitations = []
        
        for section_name, section_content in technical_sections.items():
            print(f"   🔍 Deep diving into {section_name}...")
            
            # Generate technical deep dive prompt
            deep_dive_prompt = self.expert_prompts.generate_technical_deep_dive_prompt(
                section_content, field
            )
            
            # Get deep technical analysis
            technical_response = self._call_ollama(deep_dive_prompt, max_length=4000)
            
            # Parse technical details
            technical_details = self._parse_technical_deep_dive(technical_response)
            
            # Aggregate results
            all_algorithmic.extend(technical_details['algorithmic'])
            all_experimental.extend(technical_details['experimental'])
            all_implementation.extend(technical_details['implementation'])
            all_numerical.extend(technical_details['numerical'])
            all_methodological.extend(technical_details['methodological'])
            all_limitations.extend(technical_details['limitations'])
        
        return ExpertDeepDive(
            algorithmic_specifications=all_algorithmic,
            experimental_precision=all_experimental,
            implementation_granularity=all_implementation,
            numerical_precision=all_numerical,
            methodological_choices=all_methodological,
            limitation_specifications=all_limitations
        )
    
    def comparative_field_analysis(self, full_text: str, field: str) -> List[str]:
        """Compare to field standards and competing approaches"""
        
        print("📊 Comparative Field Analysis: Positioning against field standards...")
        
        # Generate comparative analysis prompt
        comparative_prompt = self.expert_prompts.generate_comparative_analysis_prompt(
            full_text[:5000], field
        )
        
        # Get comparative analysis
        comparative_response = self._call_ollama(comparative_prompt, max_length=3500)
        
        # Parse comparative analysis
        comparative_points = self._parse_comparative_analysis(comparative_response)
        
        print(f"   ✅ Generated {len(comparative_points)} comparative analysis points")
        
        return comparative_points
    
    def generate_expert_debate_scenarios(self, expert_evidence: List[ExpertEvidence],
                                       controversies: FieldControversies,
                                       technical_dive: ExpertDeepDive) -> List[Dict[str, str]]:
        """Generate realistic expert debate scenarios"""
        
        print("🎭 Generating Expert Debate Scenarios: Realistic academic arguments...")
        
        debate_scenarios = []
        
        # Scenario 1: Statistical vs Domain Expert Conflict
        if expert_evidence:
            stat_analysis = expert_evidence[0].statistician_analysis
            domain_analysis = expert_evidence[0].domain_expert_analysis
            
            scenario = {
                "title": "Statistical Rigor vs Domain Relevance Debate",
                "statistician_position": self._extract_key_points(stat_analysis, "critical"),
                "domain_expert_position": self._extract_key_points(domain_analysis, "supportive"),
                "core_disagreement": "Statistical adequacy vs practical significance",
                "technical_details": technical_dive.numerical_precision[:2] if technical_dive.numerical_precision else []
            }
            debate_scenarios.append(scenario)
        
        # Scenario 2: Methodology vs Replication Expert Conflict  
        if expert_evidence:
            method_analysis = expert_evidence[0].methodologist_analysis
            replication_analysis = expert_evidence[0].replication_expert_analysis
            
            scenario = {
                "title": "Methodological Innovation vs Reproducibility Debate",
                "methodologist_position": self._extract_key_points(method_analysis, "innovative"),
                "replication_expert_position": self._extract_key_points(replication_analysis, "conservative"),
                "core_disagreement": "Novel methods vs replicable methods",
                "technical_details": technical_dive.methodological_choices[:2] if technical_dive.methodological_choices else []
            }
            debate_scenarios.append(scenario)
        
        # Scenario 3: Field Standards Controversy
        if controversies.methodological_controversies:
            scenario = {
                "title": "Field Standards and Best Practices Debate",
                "optimist_position": "This represents methodological advancement",
                "skeptic_position": controversies.methodological_controversies[0] if controversies.methodological_controversies else "Deviates from established practices",
                "core_disagreement": "Innovation vs established practices",
                "technical_details": controversies.statistical_controversies[:2]
            }
            debate_scenarios.append(scenario)
        
        print(f"   ✅ Generated {len(debate_scenarios)} expert debate scenarios")
        
        return debate_scenarios
    
    def comprehensive_expert_analysis(self, core_understanding: CoreUnderstanding,
                                    full_text: str) -> ComprehensiveExpertAnalysis:
        """Complete expert-level analysis with maximum depth"""
        
        print("🚀 COMPREHENSIVE EXPERT-LEVEL ANALYSIS")
        print("=" * 60)
        
        field = core_understanding.field_classification
        
        # Expert evidence analysis
        expert_evidence = self.expert_evidence_analysis(core_understanding, full_text)
        
        # Field controversy analysis
        field_controversies = self.field_controversy_analysis(core_understanding, full_text)
        
        # Technical deep dive
        technical_deep_dive = self.expert_technical_deep_dive(full_text, field)
        
        # Comparative analysis
        comparative_analysis = self.comparative_field_analysis(full_text, field)
        
        # Generate debate scenarios
        debate_scenarios = self.generate_expert_debate_scenarios(
            expert_evidence, field_controversies, technical_deep_dive
        )
        
        return ComprehensiveExpertAnalysis(
            expert_evidence_mappings=expert_evidence,
            field_controversies=field_controversies,
            expert_deep_dive=technical_deep_dive,
            comparative_field_analysis=comparative_analysis,
            expert_debate_scenarios=debate_scenarios
        )
    
    def _extract_key_claims(self, core_understanding: CoreUnderstanding) -> List[str]:
        """Extract key claims for expert analysis"""
        claims = []
        
        story = core_understanding.research_story_arc
        for key, value in story.items():
            if any(claim_word in key for claim_word in ['finding', 'contribution', 'significance']) and len(value) > 50:
                claims.append(value)
        
        # Add debate points as potential claims
        for debate_point in core_understanding.debate_seed_points[:3]:
            if len(debate_point) > 50:
                claims.append(debate_point)
        
        return claims[:5]  # Top 5 claims
    
    def _find_evidence_for_claim(self, claim: str, full_text: str) -> str:
        """Find relevant evidence sections for a specific claim"""
        
        # Extract key terms from claim
        claim_terms = re.findall(r'\b[A-Za-z]{4,}\b', claim.lower())[:5]
        
        # Find paragraphs that contain multiple claim terms
        paragraphs = full_text.split('\n\n')
        relevant_paragraphs = []
        
        for paragraph in paragraphs:
            if len(paragraph) < 100:  # Skip very short paragraphs
                continue
                
            paragraph_lower = paragraph.lower()
            term_matches = sum(1 for term in claim_terms if term in paragraph_lower)
            
            if term_matches >= 2:  # Paragraph contains multiple relevant terms
                relevant_paragraphs.append(paragraph)
        
        # Return top relevant paragraphs
        evidence_text = '\n\n'.join(relevant_paragraphs[:3])
        return evidence_text[:3000]  # Limit length
    
    def _parse_multi_expert_response(self, claim: str, response: str) -> ExpertEvidence:
        """Parse multi-expert analysis response"""
        
        statistician_analysis = self._extract_section_content(response, "STATISTICIAN'S PERSPECTIVE", "METHODOLOGIST'S PERSPECTIVE")
        methodologist_analysis = self._extract_section_content(response, "METHODOLOGIST'S PERSPECTIVE", "DOMAIN EXPERT'S PERSPECTIVE")  
        domain_expert_analysis = self._extract_section_content(response, "DOMAIN EXPERT'S PERSPECTIVE", "REPLICATION EXPERT'S PERSPECTIVE")
        replication_expert_analysis = self._extract_section_content(response, "REPLICATION EXPERT'S PERSPECTIVE", "")
        
        # Parse evidence strengths
        evidence_strength = {
            "statistical": self._extract_evidence_grade(statistician_analysis),
            "methodological": self._extract_evidence_grade(methodologist_analysis),
            "domain": self._extract_evidence_grade(domain_expert_analysis),
            "replication": self._extract_evidence_grade(replication_expert_analysis)
        }
        
        # Extract debate points
        debate_points = {
            "optimist": self._extract_debate_points(response, "optimist"),
            "skeptic": self._extract_debate_points(response, "skeptic")
        }
        
        return ExpertEvidence(
            claim=claim,
            statistician_analysis=statistician_analysis,
            methodologist_analysis=methodologist_analysis,
            domain_expert_analysis=domain_expert_analysis,
            replication_expert_analysis=replication_expert_analysis,
            evidence_strength_detailed=evidence_strength,
            specific_debate_points=debate_points
        )
    
    def _parse_field_controversies(self, response: str) -> FieldControversies:
        """Parse field-specific controversies"""
        
        methodological = self._extract_bullet_points(response, "METHODOLOGICAL CONTROVERSIES")
        statistical = self._extract_bullet_points(response, "STATISTICAL")
        domain_technical = self._extract_bullet_points(response, "DOMAIN-SPECIFIC TECHNICAL")
        generalizability = self._extract_bullet_points(response, "GENERALIZABILITY")
        reproducibility = self._extract_bullet_points(response, "REPRODUCIBILITY")
        
        return FieldControversies(
            methodological_controversies=methodological,
            statistical_controversies=statistical,
            domain_technical_disputes=domain_technical,
            generalizability_wars=generalizability,
            reproducibility_ammunition=reproducibility,
            comparative_analysis=[]
        )
    
    def _parse_technical_deep_dive(self, response: str) -> Dict[str, List[str]]:
        """Parse technical deep dive response"""
        
        return {
            "algorithmic": self._extract_bullet_points(response, "ALGORITHMIC SPECIFICATIONS"),
            "experimental": self._extract_bullet_points(response, "EXPERIMENTAL PRECISION"),
            "implementation": self._extract_bullet_points(response, "IMPLEMENTATION GRANULARITY"),
            "numerical": self._extract_bullet_points(response, "NUMERICAL PRECISION"),
            "methodological": self._extract_bullet_points(response, "METHODOLOGICAL CHOICES"),
            "limitations": self._extract_bullet_points(response, "LIMITATION SPECIFICATIONS")
        }
    
    def _parse_comparative_analysis(self, response: str) -> List[str]:
        """Parse comparative analysis points"""
        
        points = []
        points.extend(self._extract_bullet_points(response, "COMPARISON TO FIELD STANDARDS"))
        points.extend(self._extract_bullet_points(response, "COMPETING APPROACHES"))
        points.extend(self._extract_bullet_points(response, "HISTORICAL CONTEXT"))
        points.extend(self._extract_bullet_points(response, "CURRENT CONTROVERSY"))
        
        return points
    
    def _extract_section_content(self, text: str, start_marker: str, end_marker: str) -> str:
        """Extract content between two markers"""
        
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return ""
        
        start_idx += len(start_marker)
        
        if end_marker:
            end_idx = text.find(end_marker, start_idx)
            if end_idx != -1:
                return text[start_idx:end_idx].strip()
        
        return text[start_idx:start_idx+1000].strip()  # Limit to 1000 chars
    
    def _extract_evidence_grade(self, text: str) -> str:
        """Extract evidence strength grade"""
        
        grades = ["VERY_STRONG", "STRONG", "MODERATE", "WEAK", "VERY_WEAK"]
        text_upper = text.upper()
        
        for grade in grades:
            if grade in text_upper:
                return grade.lower()
        
        return "unknown"
    
    def _extract_debate_points(self, text: str, side: str) -> List[str]:
        """Extract specific debate points for optimist/skeptic"""
        
        marker = f"{side.upper()} ARGUMENTS" if side in ["optimist", "skeptic"] else side.upper()
        
        section = self._extract_section_content(text, marker, "")
        points = self._extract_bullet_points(section, "")
        
        return points[:5]  # Top 5 points
    
    def _extract_bullet_points(self, text: str, section_marker: str) -> List[str]:
        """Extract bullet points from a section"""
        
        if section_marker:
            section_start = text.find(section_marker)
            if section_start != -1:
                text = text[section_start:]
        
        points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '•', '*', '[')) and len(line) > 20:
                # Clean up the point
                point = line.strip('- •*[]').strip()
                if point and len(point) > 15:
                    points.append(point)
        
        return points
    
    def _extract_technical_sections(self, full_text: str) -> Dict[str, str]:
        """Extract technical sections from full text"""
        
        sections = {}
        text_lower = full_text.lower()
        
        # Common technical section patterns
        section_patterns = {
            "methodology": [r"method", r"methodology", r"approach"],
            "results": [r"results", r"findings", r"outcomes"],
            "experiments": [r"experiment", r"evaluation", r"testing"],
            "implementation": [r"implementation", r"system", r"architecture"],
            "analysis": [r"analysis", r"statistical", r"data analysis"]
        }
        
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                # Find section content
                matches = list(re.finditer(rf'\b{pattern}\b', text_lower))
                if matches:
                    # Take first match and extract surrounding content
                    match_pos = matches[0].start()
                    # Extract 2000 characters around the match
                    start = max(0, match_pos - 500)
                    end = min(len(full_text), match_pos + 1500)
                    section_content = full_text[start:end]
                    
                    if len(section_content) > 200:
                        sections[section_name] = section_content
                        break
        
        return sections
    
    def _extract_key_points(self, text: str, tone: str) -> str:
        """Extract key points with specific tone"""
        
        # Simple extraction of first substantial sentence
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 30:
                return sentence
        
        return text[:100] if text else "No analysis available"
    
    def test_connection(self) -> bool:
        """Test Ollama connection"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 0 and "Error" not in test_response
        except:
            return False
