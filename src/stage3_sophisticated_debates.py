"""
Stage 3: Sophisticated Evidence-Based Debate Generator
Save as: src/stage3_sophisticated_debates.py

Generates expert-level academic debates using comprehensive evidence from Stage 1 + Stage 2.
Creates realistic discussions with specific paper references, evidence citations, and technical depth.
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
class DebateTurn:
    """Single turn in sophisticated debate"""
    speaker: str
    speaker_role: str
    content: str
    evidence_cited: List[str]
    technical_depth: str  # "basic", "intermediate", "expert"
    argument_type: str  # "supporting", "counter", "questioning", "clarifying"
    turn_number: int


@dataclass
class SophisticatedDebate:
    """Complete evidence-based debate"""
    paper_title: str
    field: str
    debate_topics: List[str]
    turns: List[DebateTurn]
    evidence_citations: List[str]
    technical_concepts_discussed: List[str]
    total_turns: int
    sophistication_score: int


@dataclass
class ExpertPersonality:
    """Enhanced personality with field-specific expertise"""
    name: str
    role: str
    field_expertise: List[str]
    debate_style: str
    evidence_preference: str  # "strong_evidence", "methodology_focus", "application_focus"
    technical_depth: str


class Stage3SophisticatedDebates:
    """Generate expert-level academic debates using comprehensive evidence"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        
        # Define field-adaptive personalities
        self.expert_personalities = self._define_expert_personalities()
    
    def _call_ollama(self, prompt: str, max_length: int = 800) -> str:
        """Enhanced API call for sophisticated debate generation"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,  # Balanced for natural but focused debates
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Debate Generation Error: {str(e)}]"
    
    def _define_expert_personalities(self) -> Dict[str, ExpertPersonality]:
        """Define field-adaptive expert personalities"""
        
        return {
            "optimist": ExpertPersonality(
                name="Dr. Ava D.",
                role="The Innovation Advocate",
                field_expertise=[],  # Will be set dynamically based on paper field
                debate_style="Enthusiastic, evidence-citing, application-focused, sees potential",
                evidence_preference="strong_evidence",
                technical_depth="expert"
            ),
            "skeptic": ExpertPersonality(
                name="Prof. Marcus Webb", 
                role="The Critical Methodologist",
                field_expertise=[],  # Will be set dynamically based on paper field
                debate_style="Rigorous, methodology-focused, limitation-aware, demands proof",
                evidence_preference="methodology_focus",
                technical_depth="expert"
            )
        }
    
    def adapt_personalities_to_field(self, field: str) -> Dict[str, ExpertPersonality]:
        """Adapt personalities based on paper's field"""
        
        field_lower = field.lower()
        
        # Computer Science / ML / AI
        if any(term in field_lower for term in ['computer science', 'machine learning', 'artificial intelligence', 'algorithm']):
            optimist_expertise = ["Algorithm Design", "Performance Optimization", "Scalability Analysis", "Real-world Applications"]
            skeptic_expertise = ["Computational Complexity", "Experimental Validation", "Baseline Comparisons", "Reproducibility"]
        
        # Biology / Medical / Life Sciences
        elif any(term in field_lower for term in ['biology', 'medical', 'clinical', 'biomedical', 'life science']):
            optimist_expertise = ["Translational Research", "Clinical Applications", "Therapeutic Potential", "Novel Mechanisms"]
            skeptic_expertise = ["Statistical Power", "Sample Representativeness", "Confounding Variables", "Clinical Significance"]
        
        # Psychology / Social Sciences  
        elif any(term in field_lower for term in ['psychology', 'social', 'behavioral', 'cognitive']):
            optimist_expertise = ["Behavioral Applications", "Social Impact", "Individual Differences", "Practical Interventions"]
            skeptic_expertise = ["Measurement Validity", "Population Generalizability", "Cultural Bias", "Effect Size Interpretation"]
        
        # Physics / Engineering / Mathematical
        elif any(term in field_lower for term in ['physics', 'engineering', 'mathematical', 'theoretical']):
            optimist_expertise = ["Theoretical Elegance", "Mathematical Innovation", "Engineering Applications", "Predictive Power"]
            skeptic_expertise = ["Mathematical Rigor", "Assumption Validity", "Experimental Verification", "Model Limitations"]
        
        # General/Other fields
        else:
            optimist_expertise = ["Innovation Potential", "Practical Applications", "Methodological Advances", "Cross-disciplinary Impact"]
            skeptic_expertise = ["Methodological Rigor", "Evidence Quality", "Reproducibility Concerns", "Limitation Analysis"]
        
        # Update personalities
        adapted_personalities = {}
        for key, personality in self.expert_personalities.items():
            adapted = ExpertPersonality(
                name=personality.name,
                role=personality.role,
                field_expertise=optimist_expertise if key == "optimist" else skeptic_expertise,
                debate_style=personality.debate_style,
                evidence_preference=personality.evidence_preference,
                technical_depth=personality.technical_depth
            )
            adapted_personalities[key] = adapted
        
        return adapted_personalities
    
    def generate_sophisticated_debate(self, complete_analysis: CompleteAnalysis, 
                                    max_topics: int = 3, 
                                    exchanges_per_topic: int = 4) -> SophisticatedDebate:
        """Generate sophisticated evidence-based debate"""
        
        print("🎭 Stage 3: Generating sophisticated evidence-based debates...")
        
        # Adapt personalities to field
        field = complete_analysis.core_understanding.field_classification
        personalities = self.adapt_personalities_to_field(field)
        
        print(f"🎯 Field-adapted personalities for: {field}")
        print(f"   😊 Dr. Ava D. expertise: {personalities['optimist'].field_expertise}")
        print(f"   🤨 Prof. Marcus Webb expertise: {personalities['skeptic'].field_expertise}")
        
        # Generate evidence-rich debate topics
        debate_topics = self._generate_evidence_based_topics(complete_analysis, max_topics)
        
        # Generate sophisticated debate turns
        turns = []
        turn_number = 1
        evidence_citations = []
        technical_concepts = []
        
        for topic_idx, topic in enumerate(debate_topics):
            print(f"\n🎯 Generating sophisticated exchanges for topic {topic_idx + 1}...")
            
            topic_turns, topic_evidence, topic_concepts = self._generate_topic_debate(
                topic, complete_analysis, personalities, exchanges_per_topic, turn_number
            )
            
            turns.extend(topic_turns)
            evidence_citations.extend(topic_evidence)
            technical_concepts.extend(topic_concepts)
            turn_number += len(topic_turns)
        
        # Calculate sophistication score
        sophistication_score = self._calculate_sophistication_score(turns, evidence_citations, technical_concepts)
        
        # Extract paper title from analysis
        story = complete_analysis.core_understanding.research_story_arc
        paper_title = story.get('main_topic', 'Research Paper')
        
        debate = SophisticatedDebate(
            paper_title=paper_title,
            field=field,
            debate_topics=[topic['question'] for topic in debate_topics],
            turns=turns,
            evidence_citations=evidence_citations,
            technical_concepts_discussed=technical_concepts,
            total_turns=len(turns),
            sophistication_score=sophistication_score
        )
        
        print(f"✅ Sophisticated debate generated!")
        print(f"   🎭 Total turns: {len(turns)}")
        print(f"   📚 Evidence citations: {len(evidence_citations)}")
        print(f"   🔬 Technical concepts: {len(technical_concepts)}")
        print(f"   🏆 Sophistication score: {sophistication_score}/100")
        
        return debate
    
    def _generate_evidence_based_topics(self, complete_analysis: CompleteAnalysis, max_topics: int) -> List[Dict[str, any]]:
        """Generate debate topics using evidence mappings"""
        
        print("📋 Generating evidence-based debate topics...")
        
        # Use Stage 1 debate points + Stage 2 evidence
        stage1_debates = complete_analysis.core_understanding.debate_seed_points
        evidence_mappings = complete_analysis.comprehensive_evidence.evidence_mappings
        gaps = complete_analysis.comprehensive_evidence.claim_evidence_gaps
        
        topics = []
        
        for i, debate_point in enumerate(stage1_debates[:max_topics]):
            # Find relevant evidence for this debate point
            relevant_evidence = []
            relevant_gaps = []
            
            # Match evidence mappings to debate point
            for mapping in evidence_mappings:
                if self._topics_match(debate_point, mapping.claim):
                    relevant_evidence.append(mapping)
            
            # Match gaps to debate point  
            for gap in gaps:
                if any(word in gap.lower() for word in debate_point.lower().split()[:4]):
                    relevant_gaps.append(gap)
            
            topic = {
                "question": debate_point,
                "evidence_mappings": relevant_evidence,
                "evidence_gaps": relevant_gaps,
                "topic_id": i + 1
            }
            
            topics.append(topic)
            print(f"   🎯 Topic {i+1}: {len(relevant_evidence)} evidence mappings, {len(relevant_gaps)} gaps")
        
        return topics
    
    def _topics_match(self, debate_point: str, claim: str) -> bool:
        """Check if debate point matches claim"""
        debate_words = set(debate_point.lower().split())
        claim_words = set(claim.lower().split())
        
        # Check for word overlap
        overlap = len(debate_words.intersection(claim_words))
        return overlap >= 2  # At least 2 words in common
    
    def _generate_topic_debate(self, topic: Dict, complete_analysis: CompleteAnalysis, 
                             personalities: Dict[str, ExpertPersonality], 
                             exchanges: int, start_turn: int) -> Tuple[List[DebateTurn], List[str], List[str]]:
        """Generate sophisticated exchanges for one topic"""
        
        turns = []
        evidence_cited = []
        technical_concepts = []
        
        # Prepare context for debate
        debate_context = self._prepare_debate_context(topic, complete_analysis)
        
        # Generate opening statements
        optimist_opening = self._generate_expert_statement(
            personalities["optimist"], topic, debate_context, "opening", None
        )
        
        skeptic_opening = self._generate_expert_statement(
            personalities["skeptic"], topic, debate_context, "counter", optimist_opening
        )
        
        # Add opening turns
        turns.append(DebateTurn(
            speaker=personalities["optimist"].name,
            speaker_role=personalities["optimist"].role,
            content=optimist_opening,
            evidence_cited=self._extract_citations(optimist_opening),
            technical_depth="expert",
            argument_type="supporting",
            turn_number=start_turn
        ))
        
        turns.append(DebateTurn(
            speaker=personalities["skeptic"].name,
            speaker_role=personalities["skeptic"].role,
            content=skeptic_opening,
            evidence_cited=self._extract_citations(skeptic_opening),
            technical_depth="expert",
            argument_type="counter",
            turn_number=start_turn + 1
        ))
        
        # Generate follow-up exchanges
        current_speaker = "optimist"
        last_statement = skeptic_opening
        
        for exchange in range(2, exchanges):
            personality = personalities[current_speaker]
            
            # Determine argument type
            if exchange % 2 == 0:
                arg_type = "supporting" if current_speaker == "optimist" else "questioning"
            else:
                arg_type = "counter" if current_speaker == "skeptic" else "clarifying"
            
            statement = self._generate_expert_statement(
                personality, topic, debate_context, arg_type, last_statement
            )
            
            turns.append(DebateTurn(
                speaker=personality.name,
                speaker_role=personality.role,
                content=statement,
                evidence_cited=self._extract_citations(statement),
                technical_depth="expert",
                argument_type=arg_type,
                turn_number=start_turn + exchange
            ))
            
            last_statement = statement
            current_speaker = "skeptic" if current_speaker == "optimist" else "optimist"
        
        # Collect evidence and concepts from all turns
        for turn in turns:
            evidence_cited.extend(turn.evidence_cited)
            technical_concepts.extend(self._extract_technical_concepts(turn.content))
        
        return turns, evidence_cited, technical_concepts
    
    def _prepare_debate_context(self, topic: Dict, complete_analysis: CompleteAnalysis) -> str:
        """Prepare rich context for evidence-based debate"""
        
        context = []
        
        # Paper field and title
        field = complete_analysis.core_understanding.field_classification
        story = complete_analysis.core_understanding.research_story_arc
        
        context.append(f"RESEARCH FIELD: {field}")
        context.append(f"PAPER TOPIC: {story.get('main_topic', 'Research paper')}")
        
        # Evidence mappings for this topic
        if topic.get('evidence_mappings'):
            context.append(f"\nRELEVANT EVIDENCE:")
            for mapping in topic['evidence_mappings'][:3]:
                context.append(f"CLAIM: {mapping.claim}")
                context.append(f"EVIDENCE STRENGTH: {mapping.evidence_strength}")
                if mapping.supporting_evidence:
                    context.append(f"SUPPORTING: {'; '.join(mapping.supporting_evidence[:2])}")
                if mapping.contradictory_evidence:
                    context.append(f"CONTRADICTORY: {'; '.join(mapping.contradictory_evidence[:2])}")
        
        # Technical details
        tech = complete_analysis.comprehensive_evidence.technical_deep_dive
        if tech.algorithms_detailed or tech.performance_metrics:
            context.append(f"\nTECHNICAL DETAILS:")
            context.extend(tech.algorithms_detailed[:2])
            context.extend(tech.performance_metrics[:2])
        
        # Evidence gaps for skeptical arguments
        if topic.get('evidence_gaps'):
            context.append(f"\nEVIDENCE GAPS:")
            context.extend(topic['evidence_gaps'][:2])
        
        return "\n".join(context)
    
    def _generate_expert_statement(self, personality: ExpertPersonality, topic: Dict, 
                                 context: str, argument_type: str, previous_statement: Optional[str]) -> str:
        """Generate expert-level statement with evidence citations"""
        
        # Build sophisticated prompt
        prompt = f"""You are {personality.name}, {personality.role}, an expert in {', '.join(personality.field_expertise[:3])}.

DEBATE CONTEXT:
{context}

DEBATE TOPIC: {topic['question']}

YOUR EXPERTISE: {', '.join(personality.field_expertise)}
YOUR STYLE: {personality.debate_style}
ARGUMENT TYPE: {argument_type}

{f"PREVIOUS STATEMENT TO RESPOND TO: {previous_statement}" if previous_statement else ""}

INSTRUCTIONS:
- Provide a sophisticated academic response (2-3 sentences)
- Reference specific evidence, data, or methodological details from the context
- Use field-appropriate technical terminology  
- Cite specific findings, numbers, or technical approaches when available
- Maintain your expertise focus: {personality.evidence_preference}
- Sound like a real expert in {personality.field_expertise[0] if personality.field_expertise else 'research methodology'}

{personality.name}'s expert response:"""
        
        return self._call_ollama(prompt, max_length=600)
    
    def _extract_citations(self, statement: str) -> List[str]:
        """Extract evidence citations from statement"""
        
        citations = []
        
        # Look for citation patterns
        citation_patterns = [
            r'Table \d+',
            r'Figure \d+',
            r'Section \d+',
            r'\d+%',
            r'p\s*[<>=]\s*0\.\d+',
            r'confidence interval',
            r'effect size',
            r'sample size',
            r'baseline',
            r'control group'
        ]
        
        import re
        for pattern in citation_patterns:
            matches = re.findall(pattern, statement, re.IGNORECASE)
            citations.extend(matches)
        
        return citations
    
    def _extract_technical_concepts(self, statement: str) -> List[str]:
        """Extract technical concepts from statement"""
        
        # Common technical terms to identify
        technical_terms = [
            'algorithm', 'methodology', 'statistical', 'experimental', 'validation',
            'reproducibility', 'generalizability', 'significance', 'correlation',
            'regression', 'optimization', 'implementation', 'performance', 'accuracy',
            'precision', 'recall', 'baseline', 'benchmark', 'evaluation', 'metric'
        ]
        
        concepts = []
        statement_lower = statement.lower()
        
        for term in technical_terms:
            if term in statement_lower:
                concepts.append(term)
        
        return concepts
    
    def _calculate_sophistication_score(self, turns: List[DebateTurn], 
                                      evidence_citations: List[str], 
                                      technical_concepts: List[str]) -> int:
        """Calculate debate sophistication score (0-100)"""
        
        score = 0
        
        # Evidence citation density (max 30 points)
        citation_density = len(evidence_citations) / len(turns) if turns else 0
        score += min(30, int(citation_density * 10))
        
        # Technical concept diversity (max 25 points)
        unique_concepts = len(set(technical_concepts))
        score += min(25, unique_concepts * 2)
        
        # Turn depth and length (max 25 points)
        avg_turn_length = sum(len(turn.content) for turn in turns) / len(turns) if turns else 0
        if avg_turn_length > 200:
            score += 25
        elif avg_turn_length > 150:
            score += 20
        elif avg_turn_length > 100:
            score += 15
        
        # Expert-level language (max 20 points)
        expert_indicators = ['methodology', 'statistical', 'significant', 'evidence', 'analysis', 'validation']
        expert_count = sum(1 for turn in turns for indicator in expert_indicators if indicator in turn.content.lower())
        score += min(20, expert_count * 2)
        
        return min(100, score)
    
    def format_sophisticated_debate(self, debate: SophisticatedDebate) -> str:
        """Format sophisticated debate for display"""
        
        output = []
        output.append("🎭 SOPHISTICATED EVIDENCE-BASED DEBATE")
        output.append("=" * 60)
        output.append(f"📄 Paper: {debate.paper_title}")
        output.append(f"🎯 Field: {debate.field}")
        output.append(f"🏆 Sophistication Score: {debate.sophistication_score}/100")
        output.append(f"📚 Evidence Citations: {len(debate.evidence_citations)}")
        output.append(f"🔬 Technical Concepts: {len(debate.technical_concepts_discussed)}")
        
        output.append(f"\n🎯 DEBATE TOPICS:")
        for i, topic in enumerate(debate.debate_topics, 1):
            output.append(f"   {i}. {topic}")
        
        output.append(f"\n💬 SOPHISTICATED EXCHANGES ({debate.total_turns} turns):")
        output.append("-" * 50)
        
        current_topic_idx = 0
        turns_per_topic = debate.total_turns // len(debate.debate_topics)
        
        for i, turn in enumerate(debate.turns):
            # Add topic separator
            if i % turns_per_topic == 0 and i > 0:
                current_topic_idx += 1
                output.append(f"\n🎯 TOPIC {current_topic_idx + 1}: {debate.debate_topics[current_topic_idx]}")
                output.append("-" * 30)
            elif i == 0:
                output.append(f"\n🎯 TOPIC 1: {debate.debate_topics[0]}")
                output.append("-" * 30)
            
            # Format turn
            speaker_emoji = "😊" if "Ava" in turn.speaker else "🤨"
            output.append(f"\n{speaker_emoji} **{turn.speaker}** ({turn.argument_type}):")
            output.append(f"{turn.content}")
            
            if turn.evidence_cited:
                output.append(f"   📚 Citations: {', '.join(turn.evidence_cited[:3])}")
        
        # Show sophistication breakdown
        output.append(f"\n📊 SOPHISTICATION ANALYSIS:")
        citation_density = len(debate.evidence_citations) / debate.total_turns if debate.total_turns else 0
        output.append(f"   📚 Citation density: {citation_density:.1f} per turn")
        output.append(f"   🔬 Unique technical concepts: {len(set(debate.technical_concepts_discussed))}")
        avg_turn_length = sum(len(turn.content) for turn in debate.turns) / len(debate.turns) if debate.turns else 0
        output.append(f"   📝 Average turn length: {avg_turn_length:.0f} characters")
        
        return "\n".join(output)
    
    def test_connection(self) -> bool:
        """Test Ollama connection"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 0 and "Error" not in test_response
        except:
            return False
