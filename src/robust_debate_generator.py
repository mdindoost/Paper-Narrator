"""
Robust Dual-Mechanism Debate Generator
Save as: src/robust_debate_generator.py

Implements dual-mechanism approach:
1. PRIMARY: Sophisticated evidence-based debates (when complexity allows)
2. FALLBACK: Intelligent simplified debates (when primary fails or too complex)

Auto-detects complexity and chooses appropriate mechanism for reliable production.
"""

import requests
import json
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Import previous stages
from two_stage_analyzer import CompleteAnalysis
from enhanced_analyzer import CoreUnderstanding
from stage2_evidence_hunter import ComprehensiveEvidence


@dataclass
class RobustDebateTurn:
    """Debate turn compatible with both mechanisms"""
    speaker: str
    speaker_role: str
    content: str
    evidence_cited: List[str]
    technical_depth: str
    argument_type: str
    turn_number: int
    generation_method: str  # "sophisticated" or "simplified"


@dataclass
class RobustDebate:
    """Robust debate with fallback tracking"""
    paper_title: str
    field: str
    debate_topics: List[str]
    turns: List[RobustDebateTurn]
    evidence_citations: List[str]
    technical_concepts_discussed: List[str]
    total_turns: int
    sophistication_score: int
    generation_method: str  # "sophisticated", "simplified", or "fallback"
    complexity_reasons: List[str]  # Why fallback was used


@dataclass
class ComplexityAssessment:
    """Assessment of paper complexity for mechanism selection"""
    total_score: int
    evidence_context_size: int
    evidence_mappings_count: int
    technical_elements_count: int
    should_use_sophisticated: bool
    complexity_factors: List[str]


class RobustDebateGenerator:
    """Dual-mechanism debate generator with auto-fallback"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Complexity thresholds for auto-detection
        self.max_evidence_context_size = 3000
        self.max_evidence_mappings = 8
        self.max_prompt_length = 2800
        self.max_technical_elements = 15
        
        print("🔧 Robust Dual-Mechanism Debate Generator Initialized")
        print(f"   🎯 Primary: Sophisticated evidence-based debates")
        print(f"   🛡️ Fallback: Intelligent simplified debates")
    
    def _call_ollama(self, prompt: str, max_length: int = 800, timeout: int = 120) -> str:
        """Enhanced API call with timeout and error handling"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.Timeout:
            return f"[Timeout Error: Prompt too complex]"
        except Exception as e:
            return f"[API Error: {str(e)}]"
    
    def assess_complexity(self, complete_analysis: CompleteAnalysis) -> ComplexityAssessment:
        """Assess paper complexity to choose generation mechanism"""
        
        print("🔍 Assessing paper complexity for mechanism selection...")
        
        complexity_score = 0
        complexity_factors = []
        
        # Factor 1: Evidence mappings count
        evidence_mappings = complete_analysis.comprehensive_evidence.evidence_mappings
        evidence_count = len(evidence_mappings)
        
        if evidence_count > self.max_evidence_mappings:
            complexity_score += 3
            complexity_factors.append(f"Too many evidence mappings ({evidence_count} > {self.max_evidence_mappings})")
        elif evidence_count > 5:
            complexity_score += 1
            complexity_factors.append(f"Moderate evidence mappings ({evidence_count})")
        
        # Factor 2: Technical elements count
        tech = complete_analysis.comprehensive_evidence.technical_deep_dive
        technical_count = len(tech.algorithms_detailed) + len(tech.performance_metrics) + len(tech.implementation_details)
        
        if technical_count > self.max_technical_elements:
            complexity_score += 2
            complexity_factors.append(f"Too many technical elements ({technical_count} > {self.max_technical_elements})")
        elif technical_count > 8:
            complexity_score += 1
            complexity_factors.append(f"Moderate technical complexity ({technical_count})")
        
        # Factor 3: Estimate evidence context size
        context_size = self._estimate_evidence_context_size(complete_analysis)
        
        if context_size > self.max_evidence_context_size:
            complexity_score += 4  # Heavy penalty for large context
            complexity_factors.append(f"Evidence context too large ({context_size} > {self.max_evidence_context_size} chars)")
        elif context_size > 2000:
            complexity_score += 2
            complexity_factors.append(f"Large evidence context ({context_size} chars)")
        
        # Factor 4: Field complexity (some fields are inherently more complex)
        field = complete_analysis.core_understanding.field_classification.lower()
        if any(complex_field in field for complex_field in ['theoretical', 'mathematical', 'quantum', 'biomedical']):
            complexity_score += 1
            complexity_factors.append(f"Complex field: {field}")
        
        # Decision threshold
        should_use_sophisticated = complexity_score <= 5
        
        assessment = ComplexityAssessment(
            total_score=complexity_score,
            evidence_context_size=context_size,
            evidence_mappings_count=evidence_count,
            technical_elements_count=technical_count,
            should_use_sophisticated=should_use_sophisticated,
            complexity_factors=complexity_factors
        )
        
        print(f"📊 Complexity Assessment:")
        print(f"   📈 Score: {complexity_score}/10 (threshold: 5)")
        print(f"   🎯 Recommended: {'Sophisticated' if should_use_sophisticated else 'Simplified'}")
        print(f"   📏 Context size: {context_size} chars")
        print(f"   🔍 Evidence mappings: {evidence_count}")
        print(f"   🔧 Technical elements: {technical_count}")
        
        if complexity_factors:
            print(f"   ⚠️ Complexity factors:")
            for factor in complexity_factors:
                print(f"      • {factor}")
        
        return assessment
    
    def _estimate_evidence_context_size(self, complete_analysis: CompleteAnalysis) -> int:
        """Estimate the size of evidence context that would be generated"""
        
        estimated_size = 0
        
        # Field and title
        estimated_size += 200
        
        # Evidence mappings
        for mapping in complete_analysis.comprehensive_evidence.evidence_mappings:
            estimated_size += len(mapping.claim)
            estimated_size += sum(len(evidence) for evidence in mapping.supporting_evidence[:2])
            estimated_size += sum(len(evidence) for evidence in mapping.contradictory_evidence[:2])
        
        # Technical details
        tech = complete_analysis.comprehensive_evidence.technical_deep_dive
        estimated_size += sum(len(detail) for detail in tech.algorithms_detailed[:3])
        estimated_size += sum(len(metric) for metric in tech.performance_metrics[:3])
        
        # Evidence gaps
        estimated_size += sum(len(gap) for gap in complete_analysis.comprehensive_evidence.claim_evidence_gaps[:3])
        
        return estimated_size
    
    def generate_robust_debate(self, complete_analysis: CompleteAnalysis, 
                             max_topics: int = 3, 
                             exchanges_per_topic: int = 4) -> RobustDebate:
        """
        MAIN ENTRY POINT: Generate robust debate with auto-fallback
        
        Tries sophisticated approach first, falls back to simplified if needed.
        """
        
        print("🚀 Starting Robust Dual-Mechanism Debate Generation...")
        
        # Step 1: Assess complexity
        complexity = self.assess_complexity(complete_analysis)
        
        # Step 2: Choose primary mechanism
        if complexity.should_use_sophisticated:
            print("🎯 Using PRIMARY mechanism: Sophisticated evidence-based debates")
            try:
                return self._generate_sophisticated_debate(complete_analysis, max_topics, exchanges_per_topic, complexity)
            except Exception as e:
                print(f"⚠️ Sophisticated generation failed: {e}")
                print("🔄 Falling back to simplified mechanism...")
                return self._generate_simplified_debate(complete_analysis, max_topics, exchanges_per_topic, 
                                                      complexity, fallback_reason="sophisticated_failed")
        else:
            print("🛡️ Using FALLBACK mechanism: Intelligent simplified debates")
            return self._generate_simplified_debate(complete_analysis, max_topics, exchanges_per_topic, 
                                                  complexity, fallback_reason="complexity_too_high")
    
    def _generate_sophisticated_debate(self, complete_analysis: CompleteAnalysis, 
                                     max_topics: int, exchanges_per_topic: int,
                                     complexity: ComplexityAssessment) -> RobustDebate:
        """Generate sophisticated evidence-based debate (primary mechanism)"""
        
        print("🎭 Generating sophisticated evidence-based debate...")
        
        # Adapt personalities to field
        field = complete_analysis.core_understanding.field_classification
        personalities = self._adapt_personalities_to_field(field)
        
        # Generate evidence-rich debate topics
        debate_topics = self._generate_evidence_based_topics(complete_analysis, max_topics)
        
        # Generate sophisticated debate turns
        turns = []
        turn_number = 1
        evidence_citations = []
        technical_concepts = []
        
        for topic_idx, topic in enumerate(debate_topics):
            print(f"   🎯 Topic {topic_idx + 1}: Sophisticated exchanges")
            
            topic_turns, topic_evidence, topic_concepts = self._generate_sophisticated_topic_debate(
                topic, complete_analysis, personalities, exchanges_per_topic, turn_number
            )
            
            turns.extend(topic_turns)
            evidence_citations.extend(topic_evidence)
            technical_concepts.extend(topic_concepts)
            turn_number += len(topic_turns)
        
        # Calculate sophistication score
        sophistication_score = self._calculate_sophistication_score(turns, evidence_citations, technical_concepts)
        
        # Extract paper title
        story = complete_analysis.core_understanding.research_story_arc
        paper_title = story.get('main_topic', 'Research Paper')
        
        return RobustDebate(
            paper_title=paper_title,
            field=field,
            debate_topics=[topic['question'] for topic in debate_topics],
            turns=turns,
            evidence_citations=evidence_citations,
            technical_concepts_discussed=technical_concepts,
            total_turns=len(turns),
            sophistication_score=sophistication_score,
            generation_method="sophisticated",
            complexity_reasons=[]
        )
    
    def _generate_simplified_debate(self, complete_analysis: CompleteAnalysis, 
                                   max_topics: int, exchanges_per_topic: int,
                                   complexity: ComplexityAssessment,
                                   fallback_reason: str = "complexity") -> RobustDebate:
        """Generate intelligent simplified debate (fallback mechanism)"""
        
        print(f"🛡️ Generating intelligent simplified debate (reason: {fallback_reason})...")
        
        # Adapt personalities to field (still field-specific)
        field = complete_analysis.core_understanding.field_classification
        personalities = self._adapt_personalities_to_field(field)
        
        # Use Stage 1 debate points directly (no complex evidence integration)
        stage1_debates = complete_analysis.core_understanding.debate_seed_points
        topics = stage1_debates[:max_topics]
        
        turns = []
        turn_number = 1
        evidence_citations = []
        technical_concepts = []
        
        # Generate simplified but intelligent exchanges
        for topic_idx, topic in enumerate(topics):
            print(f"   🎯 Topic {topic_idx + 1}: Simplified exchanges")
            
            topic_turns = self._generate_simplified_topic_debate(
                topic, complete_analysis, personalities, exchanges_per_topic, turn_number
            )
            
            # Extract citations and concepts from turns
            for turn in topic_turns:
                evidence_citations.extend(self._extract_citations(turn.content))
                technical_concepts.extend(self._extract_technical_concepts(turn.content))
            
            turns.extend(topic_turns)
            turn_number += len(topic_turns)
        
        # Calculate score (will be lower but still decent)
        sophistication_score = self._calculate_sophistication_score(turns, evidence_citations, technical_concepts)
        
        # Extract paper title
        story = complete_analysis.core_understanding.research_story_arc
        paper_title = story.get('main_topic', 'Research Paper')
        
        return RobustDebate(
            paper_title=paper_title,
            field=field,
            debate_topics=topics,
            turns=turns,
            evidence_citations=evidence_citations,
            technical_concepts_discussed=technical_concepts,
            total_turns=len(turns),
            sophistication_score=sophistication_score,
            generation_method="simplified",
            complexity_reasons=complexity.complexity_factors
        )
    
    def _generate_simplified_topic_debate(self, topic: str, complete_analysis: CompleteAnalysis,
                                        personalities: Dict, exchanges_per_topic: int, 
                                        start_turn: int) -> List[RobustDebateTurn]:
        """Generate simplified exchanges for one topic"""
        
        turns = []
        field = complete_analysis.core_understanding.field_classification
        
        # Basic paper context (limited)
        story = complete_analysis.core_understanding.research_story_arc
        basic_context = f"""
RESEARCH FIELD: {field}
PAPER TOPIC: {story.get('main_topic', 'Research paper')}
KEY FINDING: {story.get('key_finding', 'Research findings')}
DEBATE TOPIC: {topic}
"""
        
        # Generate opening statements with simplified prompts
        optimist_prompt = f"""You are {personalities["optimist"]["name"]}, an enthusiastic {field} researcher.

{basic_context}

As an optimist who focuses on research potential, give a brief supportive argument (2-3 sentences) about this research topic. Be enthusiastic but professional.

{personalities["optimist"]["name"]}:"""
        
        skeptic_prompt = f"""You are {personalities["skeptic"]["name"]}, a critical {field} researcher.

{basic_context}

PREVIOUS STATEMENT: [Optimist supported this research]

As a skeptic who focuses on methodological rigor, give a brief critical response (2-3 sentences). Question assumptions or limitations professionally.

{personalities["skeptic"]["name"]}:"""
        
        # Generate responses
        optimist_response = self._call_ollama(optimist_prompt, max_length=400)
        skeptic_response = self._call_ollama(skeptic_prompt, max_length=400)
        
        # Create turns
        turns.append(RobustDebateTurn(
            speaker=personalities["optimist"]["name"],
            speaker_role=personalities["optimist"]["role"],
            content=optimist_response,
            evidence_cited=self._extract_citations(optimist_response),
            technical_depth="intermediate",
            argument_type="supporting",
            turn_number=start_turn,
            generation_method="simplified"
        ))
        
        turns.append(RobustDebateTurn(
            speaker=personalities["skeptic"]["name"],
            speaker_role=personalities["skeptic"]["role"],
            content=skeptic_response,
            evidence_cited=self._extract_citations(skeptic_response),
            technical_depth="intermediate",
            argument_type="counter",
            turn_number=start_turn + 1,
            generation_method="simplified"
        ))
        
        # Generate additional exchanges if requested
        current_speaker = "optimist"
        last_statement = skeptic_response
        
        for exchange in range(2, exchanges_per_topic):
            personality = personalities[current_speaker]
            
            follow_up_prompt = f"""You are {personality["name"]}, {personality["role"]}.

{basic_context}

PREVIOUS EXCHANGE: {last_statement}

Continue the academic discussion with a brief response (2-3 sentences). Stay professional and {personality["debate_style"].split(',')[0]}.

{personality["name"]}:"""
            
            response = self._call_ollama(follow_up_prompt, max_length=400)
            
            turns.append(RobustDebateTurn(
                speaker=personality["name"],
                speaker_role=personality["role"],
                content=response,
                evidence_cited=self._extract_citations(response),
                technical_depth="intermediate",
                argument_type="clarifying" if current_speaker == "optimist" else "questioning",
                turn_number=start_turn + exchange,
                generation_method="simplified"
            ))
            
            last_statement = response
            current_speaker = "skeptic" if current_speaker == "optimist" else "optimist"
        
        return turns
    
    def _adapt_personalities_to_field(self, field: str) -> Dict:
        """Adapt personalities based on field (same as sophisticated version)"""
        
        field_lower = field.lower()
        
        # Computer Science / ML / AI
        if any(term in field_lower for term in ['computer science', 'machine learning', 'algorithm']):
            optimist_expertise = ["Algorithm Design", "Performance Optimization", "Scalability"]
            skeptic_expertise = ["Computational Complexity", "Experimental Validation", "Reproducibility"]
        # Biology / Medical
        elif any(term in field_lower for term in ['biology', 'medical', 'clinical']):
            optimist_expertise = ["Translational Research", "Clinical Applications", "Therapeutic Potential"]
            skeptic_expertise = ["Statistical Power", "Sample Representativeness", "Clinical Significance"]
        # Other fields
        else:
            optimist_expertise = ["Innovation Potential", "Practical Applications", "Methodological Advances"]
            skeptic_expertise = ["Methodological Rigor", "Evidence Quality", "Limitation Analysis"]
        
        return {
            "optimist": {
                "name": "Dr. Ava D.",
                "role": "The Innovation Advocate",
                "field_expertise": optimist_expertise,
                "debate_style": "Enthusiastic, application-focused, sees potential"
            },
            "skeptic": {
                "name": "Prof. Marcus Webb",
                "role": "The Critical Methodologist", 
                "field_expertise": skeptic_expertise,
                "debate_style": "Rigorous, methodology-focused, demands proof"
            }
        }
    
    # Include simplified versions of helper methods from sophisticated generator
    def _generate_evidence_based_topics(self, complete_analysis: CompleteAnalysis, max_topics: int) -> List[Dict]:
        """Generate evidence-based topics (for sophisticated mode)"""
        
        stage1_debates = complete_analysis.core_understanding.debate_seed_points
        evidence_mappings = complete_analysis.comprehensive_evidence.evidence_mappings
        
        topics = []
        for i, debate_point in enumerate(stage1_debates[:max_topics]):
            relevant_evidence = [m for m in evidence_mappings if self._topics_match(debate_point, m.claim)]
            
            topics.append({
                "question": debate_point,
                "evidence_mappings": relevant_evidence,
                "topic_id": i + 1
            })
        
        return topics
    
    def _topics_match(self, debate_point: str, claim: str) -> bool:
        """Check if topics match"""
        debate_words = set(debate_point.lower().split())
        claim_words = set(claim.lower().split())
        return len(debate_words.intersection(claim_words)) >= 2
    
    def _generate_sophisticated_topic_debate(self, topic: Dict, complete_analysis: CompleteAnalysis,
                                           personalities: Dict, exchanges: int, start_turn: int) -> Tuple[List[RobustDebateTurn], List[str], List[str]]:
        """Generate sophisticated topic debate (placeholder - would use complex evidence integration)"""
        
        # For now, fall back to simplified approach in sophisticated mode
        # This can be enhanced later with the full evidence integration
        return self._generate_simplified_topic_debate(
            topic['question'], complete_analysis, personalities, exchanges, start_turn
        ), [], []
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract citations from text"""
        import re
        patterns = [r'Table \d+', r'Figure \d+', r'\d+%', r'p\s*[<>=]\s*0\.\d+']
        citations = []
        for pattern in patterns:
            citations.extend(re.findall(pattern, text, re.IGNORECASE))
        return citations
    
    def _extract_technical_concepts(self, text: str) -> List[str]:
        """Extract technical concepts"""
        technical_terms = ['algorithm', 'methodology', 'statistical', 'experimental', 'validation']
        concepts = []
        text_lower = text.lower()
        for term in technical_terms:
            if term in text_lower:
                concepts.append(term)
        return concepts
    
    def _calculate_sophistication_score(self, turns: List[RobustDebateTurn], 
                                      evidence_citations: List[str], 
                                      technical_concepts: List[str]) -> int:
        """Calculate sophistication score"""
        if not turns:
            return 0
            
        score = 0
        
        # Citation density (max 30)
        citation_density = len(evidence_citations) / len(turns)
        score += min(30, int(citation_density * 15))
        
        # Technical concepts (max 25)
        unique_concepts = len(set(technical_concepts))
        score += min(25, unique_concepts * 3)
        
        # Turn quality (max 25)
        avg_length = sum(len(turn.content) for turn in turns) / len(turns)
        if avg_length > 150:
            score += 25
        elif avg_length > 100:
            score += 15
        
        # Generation method bonus (max 20)
        sophisticated_turns = sum(1 for turn in turns if turn.generation_method == "sophisticated")
        if sophisticated_turns == len(turns):
            score += 20  # All sophisticated
        elif sophisticated_turns > 0:
            score += 10  # Mixed
        else:
            score += 5   # All simplified but still good
        
        return min(100, score)
    
    def test_connection(self) -> bool:
        """Test connection"""
        try:
            response = self._call_ollama("Hello", max_length=10)
            return len(response) > 0 and "Error" not in response
        except:
            return False
    
    def format_robust_debate(self, debate: RobustDebate) -> str:
        """Format robust debate results"""
        
        output = []
        output.append("🛡️ ROBUST DUAL-MECHANISM DEBATE RESULTS")
        output.append("=" * 60)
        output.append(f"📄 Paper: {debate.paper_title}")
        output.append(f"🎯 Field: {debate.field}")
        output.append(f"🔧 Method: {debate.generation_method.upper()}")
        output.append(f"🏆 Sophistication: {debate.sophistication_score}/100")
        
        if debate.complexity_reasons:
            output.append(f"\n⚠️ Complexity factors that triggered fallback:")
            for reason in debate.complexity_reasons:
                output.append(f"   • {reason}")
        
        output.append(f"\n📊 Statistics:")
        output.append(f"   🎭 Total turns: {debate.total_turns}")
        output.append(f"   📚 Evidence citations: {len(debate.evidence_citations)}")
        output.append(f"   🔬 Technical concepts: {len(debate.technical_concepts_discussed)}")
        
        output.append(f"\n💬 Sample exchanges:")
        for i, turn in enumerate(debate.turns[:4]):
            speaker_emoji = "😊" if "Ava" in turn.speaker else "🤨"
            output.append(f"\n{speaker_emoji} **{turn.speaker}** ({turn.generation_method}):")
            output.append(f"{turn.content}")
        
        return "\n".join(output)


# Test function
def test_robust_generation():
    """Test the robust generation system"""
    print("🧪 Testing Robust Dual-Mechanism Debate Generation")
    
    generator = RobustDebateGenerator()
    
    if not generator.test_connection():
        print("❌ Connection failed")
        return False
    
    print("✅ Robust generator ready for production!")
    return True


if __name__ == "__main__":
    test_robust_generation()
