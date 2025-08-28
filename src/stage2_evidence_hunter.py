"""
Stage 2: Evidence Hunting - Intelligent Full Paper Analysis
Save as: src/stage2_evidence_hunter.py

Uses Stage 1 core understanding to hunt for evidence throughout the full paper.
Maps claims to supporting/contradictory evidence for sophisticated debates.
"""

import requests
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Import Stage 1 results
from enhanced_analyzer import CoreUnderstanding


@dataclass
class EvidenceMapping:
    """Maps claims to their supporting evidence"""
    claim: str
    supporting_evidence: List[str]
    contradictory_evidence: List[str]
    evidence_strength: str  # "strong", "moderate", "weak", "absent"
    evidence_location: List[str]  # Which sections contain evidence


@dataclass
class TechnicalDeepDive:
    """Detailed technical analysis from full paper"""
    algorithms_detailed: List[str]
    experimental_design: List[str]
    statistical_results: List[str]
    performance_metrics: List[str]
    implementation_details: List[str]
    comparison_results: List[str]
    limitations_detailed: List[str]


@dataclass
class MethodologyAnalysis:
    """Detailed methodology analysis"""
    data_collection: List[str]
    sample_characteristics: List[str]
    control_measures: List[str]
    validation_approaches: List[str]
    statistical_methods: List[str]
    potential_biases: List[str]


@dataclass
class ComprehensiveEvidence:
    """Complete Stage 2 evidence analysis"""
    evidence_mappings: List[EvidenceMapping]
    technical_deep_dive: TechnicalDeepDive
    methodology_analysis: MethodologyAnalysis
    claim_evidence_gaps: List[str]
    overclaim_detection: List[str]
    expert_debate_ammunition: Dict[str, List[str]]  # "optimist" and "skeptic" ammunition


class Stage2EvidenceHunter:
    """Stage 2: Hunt for evidence using Stage 1 understanding"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def _call_ollama(self, prompt: str, max_length: int = 3000) -> str:
        """Enhanced Ollama API call for evidence analysis"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.5,  # Lower for more focused evidence extraction
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=400)  # Longer timeout for full paper
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Evidence Analysis Error: {str(e)}]"
    
    def intelligent_section_search(self, full_text: str, core_understanding: CoreUnderstanding) -> Dict[str, str]:
        """Intelligently find relevant sections based on Stage 1 understanding"""
        
        print("🔍 Stage 2: Intelligent section search based on core understanding...")
        
        # Use field classification to guide section detection
        field = core_understanding.field_classification.lower()
        
        # Adaptive section patterns based on field
        if any(word in field for word in ['computer science', 'machine learning', 'algorithm']):
            section_priorities = ['methods', 'methodology', 'algorithm', 'implementation', 'experiments', 'evaluation', 'results', 'performance']
        elif any(word in field for word in ['biology', 'medical', 'clinical']):
            section_priorities = ['methods', 'materials', 'subjects', 'procedure', 'analysis', 'results', 'findings']
        elif any(word in field for word in ['psychology', 'social', 'behavioral']):
            section_priorities = ['participants', 'procedure', 'measures', 'analysis', 'results', 'discussion']
        else:
            section_priorities = ['methods', 'methodology', 'analysis', 'results', 'experiments', 'evaluation']
        
        # Smart section extraction
        sections = {}
        text_lower = full_text.lower()
        
        # Find key sections using adaptive patterns
        for priority in section_priorities:
            section_content = self._extract_priority_section(full_text, text_lower, priority)
            if section_content:
                sections[priority] = section_content
                print(f"✅ Found {priority}: {len(section_content)} characters")
        
        # Extract results/findings sections (critical for evidence)
        results_content = self._extract_results_sections(full_text, text_lower)
        if results_content:
            sections['results_detailed'] = results_content
            print(f"✅ Found detailed results: {len(results_content)} characters")
        
        # Extract discussion section (for claims analysis)
        discussion_content = self._extract_discussion_section(full_text, text_lower)
        if discussion_content:
            sections['discussion'] = discussion_content
            print(f"✅ Found discussion: {len(discussion_content)} characters")
        
        return sections
    
    def _extract_priority_section(self, text: str, text_lower: str, section_name: str) -> Optional[str]:
        """Extract a priority section using multiple patterns"""
        
        patterns = [
            rf'\b{section_name}\b[:\s]*(.*?)(?=\s*(?:\d+\.|\b(?:results?|discussion|conclusion|references?)\b))',
            rf'\b{section_name}\b[:\s]*\n(.*?)(?=\n\s*(?:\d+\.|\b(?:results?|discussion)\b))',
            rf'\d+\.?\s*{section_name}[:\s]*(.*?)(?=\s*(?:\d+\.|\b(?:results?|discussion)\b))'
        ]
        
        for pattern in patterns:
            matches = list(re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE))
            if matches:
                match = matches[0]
                if len(match.groups()) > 0:
                    start = match.start(1)
                    end = match.end(1)
                    extracted = text[start:end].strip()
                    if len(extracted) > 100:
                        return extracted
        
        return None
    
    def _extract_results_sections(self, text: str, text_lower: str) -> Optional[str]:
        """Extract all results-related content"""
        
        results_patterns = [
            r'\b(?:results?|findings?|outcomes?)\b[:\s]*(.*?)(?=\s*(?:discussion|conclusion|references?))',
            r'\d+\.?\s*(?:results?|findings?)[:\s]*(.*?)(?=\s*(?:\d+\.|\bdiscussion\b))'
        ]
        
        all_results = []
        for pattern in results_patterns:
            matches = list(re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE))
            for match in matches:
                if len(match.groups()) > 0:
                    start = match.start(1) 
                    end = match.end(1)
                    results_content = text[start:end].strip()
                    if len(results_content) > 100:
                        all_results.append(results_content)
        
        return '\n\n'.join(all_results) if all_results else None
    
    def _extract_discussion_section(self, text: str, text_lower: str) -> Optional[str]:
        """Extract discussion section for claims analysis"""
        
        discussion_patterns = [
            r'\bdiscussion\b[:\s]*(.*?)(?=\s*(?:conclusion|references?|acknowledgments?))',
            r'\d+\.?\s*discussion[:\s]*(.*?)(?=\s*(?:\d+\.|\bconclusion\b))'
        ]
        
        for pattern in discussion_patterns:
            matches = list(re.finditer(pattern, text_lower, re.DOTALL | re.IGNORECASE))
            if matches:
                match = matches[0]
                if len(match.groups()) > 0:
                    start = match.start(1)
                    end = match.end(1)
                    extracted = text[start:end].strip()
                    if len(extracted) > 200:
                        return extracted
        
        return None
    
    def evidence_claim_mapping(self, core_understanding: CoreUnderstanding, 
                             full_sections: Dict[str, str]) -> List[EvidenceMapping]:
        """Map claims from Stage 1 to evidence in full paper"""
        
        print("🔍 Stage 2: Mapping claims to evidence...")
        
        # Extract main claims from core understanding
        main_claims = []
        
        # Claims from research story
        story = core_understanding.research_story_arc
        if 'key_findings' in story:
            main_claims.append(story['key_findings'])
        if 'claimed_significance' in story:
            main_claims.append(story['claimed_significance'])
        if 'primary_findings' in story:
            main_claims.append(story['primary_findings'])
        
        # Additional claims from confidence assessment
        confidence = core_understanding.confidence_assessment
        for key, value in confidence.items():
            if 'claim' in key and len(value) > 50:
                main_claims.append(value)
        
        print(f"📋 Found {len(main_claims)} main claims to verify")
        
        evidence_mappings = []
        
        for claim in main_claims:
            if len(claim) < 30:  # Skip very short claims
                continue
                
            # Create evidence mapping prompt
            evidence_prompt = f"""You are an expert peer reviewer conducting evidence analysis. 

SPECIFIC CLAIM TO VERIFY:
"{claim}"

FULL PAPER SECTIONS FOR EVIDENCE:
{self._prepare_evidence_context(full_sections)}

TASK: Analyze whether this specific claim is supported by evidence in the paper sections.

REQUIRED ANALYSIS:

**SUPPORTING EVIDENCE:**
- [List specific evidence that supports this claim]
- [Quote exact numbers, results, or findings that back up the claim]
- [Identify which sections contain supporting evidence]

**CONTRADICTORY EVIDENCE:**
- [List any evidence that contradicts or weakens this claim]  
- [Note any results that don't align with the claim]
- [Identify conflicting information]

**EVIDENCE STRENGTH:**
- [Rate as: STRONG, MODERATE, WEAK, or ABSENT]
- [Explain why - what makes the evidence strong or weak?]

**EVIDENCE LOCATION:**
- [List which paper sections contain relevant evidence]
- [Note specific tables, figures, or paragraphs if mentioned]

Be specific and quote exact evidence. Focus only on this specific claim."""

            evidence_response = self._call_ollama(evidence_prompt, max_length=2000)
            
            # Parse the evidence mapping
            mapping = self._parse_evidence_mapping(claim, evidence_response, full_sections)
            evidence_mappings.append(mapping)
            print(f"  ✅ Mapped evidence for: {claim[:50]}... (Strength: {mapping.evidence_strength})")
        
        return evidence_mappings
    
    def _prepare_evidence_context(self, sections: Dict[str, str], max_length: int = 4000) -> str:
        """Prepare relevant sections for evidence analysis"""
        
        # Prioritize sections most likely to contain evidence
        priority_order = ['results_detailed', 'results', 'methodology', 'methods', 'discussion', 'experiments', 'evaluation']
        
        context = ""
        for section_name in priority_order:
            if section_name in sections and len(context) < max_length:
                remaining_space = max_length - len(context)
                section_content = sections[section_name][:remaining_space]
                context += f"\n\n{section_name.upper()}:\n{section_content}"
        
        # Add any remaining sections if space available
        for section_name, content in sections.items():
            if section_name not in priority_order and len(context) < max_length:
                remaining_space = max_length - len(context)
                section_content = content[:remaining_space]
                context += f"\n\n{section_name.upper()}:\n{section_content}"
        
        return context
    
    def _parse_evidence_mapping(self, claim: str, response: str, sections: Dict[str, str]) -> EvidenceMapping:
        """Parse evidence mapping response"""
        
        supporting_evidence = []
        contradictory_evidence = []
        evidence_strength = "unknown"
        evidence_location = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_upper = line.upper()
            
            # Detect sections
            if 'SUPPORTING EVIDENCE' in line_upper:
                current_section = 'supporting'
                continue
            elif 'CONTRADICTORY EVIDENCE' in line_upper:
                current_section = 'contradictory'
                continue
            elif 'EVIDENCE STRENGTH' in line_upper:
                current_section = 'strength'
                continue
            elif 'EVIDENCE LOCATION' in line_upper:
                current_section = 'location'
                continue
            
            # Parse content
            if current_section == 'supporting' and line.startswith(('-', '•', '*')):
                evidence = line.strip('- •*').strip()
                if len(evidence) > 20:
                    supporting_evidence.append(evidence)
            
            elif current_section == 'contradictory' and line.startswith(('-', '•', '*')):
                evidence = line.strip('- •*').strip()
                if len(evidence) > 20:
                    contradictory_evidence.append(evidence)
            
            elif current_section == 'strength':
                if any(strength in line.upper() for strength in ['STRONG', 'MODERATE', 'WEAK', 'ABSENT']):
                    if 'STRONG' in line.upper():
                        evidence_strength = 'strong'
                    elif 'MODERATE' in line.upper():
                        evidence_strength = 'moderate'
                    elif 'WEAK' in line.upper():
                        evidence_strength = 'weak'
                    elif 'ABSENT' in line.upper():
                        evidence_strength = 'absent'
            
            elif current_section == 'location' and line.startswith(('-', '•', '*')):
                location = line.strip('- •*').strip()
                if len(location) > 5:
                    evidence_location.append(location)
        
        return EvidenceMapping(
            claim=claim,
            supporting_evidence=supporting_evidence,
            contradictory_evidence=contradictory_evidence,
            evidence_strength=evidence_strength,
            evidence_location=evidence_location
        )
    
    def comprehensive_stage2_analysis(self, core_understanding: CoreUnderstanding, 
                                    full_text: str) -> ComprehensiveEvidence:
        """Complete Stage 2 analysis: Evidence hunting + technical deep dive"""
        
        print("🚀 Stage 2: COMPREHENSIVE Evidence Hunting Analysis")
        print("=" * 60)
        
        # Step 1: Intelligent section search
        full_sections = self.intelligent_section_search(full_text, core_understanding)
        
        # Step 2: Evidence-claim mapping
        evidence_mappings = self.evidence_claim_mapping(core_understanding, full_sections)
        
        # Step 3: Technical deep dive
        technical_analysis = self._technical_deep_dive(full_sections, core_understanding)
        
        # Step 4: Methodology analysis  
        methodology_analysis = self._methodology_analysis(full_sections, core_understanding)
        
        # Step 5: Gap and overclaim detection
        gaps, overclaims = self._detect_gaps_and_overclaims(evidence_mappings, core_understanding)
        
        # Step 6: Generate expert debate ammunition
        debate_ammunition = self._generate_debate_ammunition(evidence_mappings, technical_analysis, methodology_analysis)
        
        return ComprehensiveEvidence(
            evidence_mappings=evidence_mappings,
            technical_deep_dive=technical_analysis,
            methodology_analysis=methodology_analysis,
            claim_evidence_gaps=gaps,
            overclaim_detection=overclaims,
            expert_debate_ammunition=debate_ammunition
        )
    
    def _technical_deep_dive(self, sections: Dict[str, str], core_understanding: CoreUnderstanding) -> TechnicalDeepDive:
        """Extract detailed technical information for expert debates"""
        
        print("🔬 Technical deep dive analysis...")
        
        # Create comprehensive technical analysis prompt
        technical_prompt = f"""You are a technical expert analyzing this research paper for detailed implementation and performance information.

RESEARCH FIELD: {core_understanding.field_classification}

FULL PAPER SECTIONS:
{self._prepare_evidence_context(sections, max_length=5000)}

EXTRACT DETAILED TECHNICAL INFORMATION:

**ALGORITHMS DETAILED:**
- [Specific algorithm names, mathematical formulations, pseudocode]
- [Implementation choices and parameters]
- [Computational complexity analysis]

**EXPERIMENTAL DESIGN:**
- [Specific experimental setup and procedures]
- [Control groups and variables]
- [Randomization and blinding procedures]

**STATISTICAL RESULTS:**
- [Exact statistical tests used]
- [P-values, confidence intervals, effect sizes]
- [Sample sizes and power analysis]

**PERFORMANCE METRICS:**
- [Specific measurement approaches]
- [Baseline comparisons and benchmarks]
- [Quantitative results with exact numbers]

**IMPLEMENTATION DETAILS:**
- [Software, hardware, and computational requirements]
- [Parameter settings and hyperparameters]
- [Code availability and reproducibility information]

**COMPARISON RESULTS:**
- [How their method compares to alternatives]
- [Statistical significance of comparisons]
- [Fairness of comparison methodology]

**LIMITATIONS DETAILED:**
- [Specific technical limitations acknowledged]
- [Scope and generalizability constraints]
- [Known failure modes or edge cases]

Extract specific, technical details that domain experts would need for evaluation."""
        
        technical_response = self._call_ollama(technical_prompt, max_length=3000)
        
        return self._parse_technical_deep_dive(technical_response)
    
    def _methodology_analysis(self, sections: Dict[str, str], core_understanding: CoreUnderstanding) -> MethodologyAnalysis:
        """Analyze methodology for potential issues and strengths"""
        
        print("📐 Methodology analysis...")
        
        methodology_prompt = f"""You are a methodology expert reviewing this research for experimental rigor and potential biases.

RESEARCH FIELD: {core_understanding.field_classification}

PAPER SECTIONS:
{self._prepare_evidence_context(sections, max_length=4000)}

ANALYZE METHODOLOGY RIGOR:

**DATA COLLECTION:**
- [How was data collected and from what sources?]
- [Sampling methodology and selection criteria]
- [Data quality and validation procedures]

**SAMPLE CHARACTERISTICS:**
- [Sample size justification and power analysis]
- [Demographics and representativeness]
- [Inclusion/exclusion criteria]

**CONTROL MEASURES:**
- [Control groups and control variables]
- [Randomization procedures]
- [Blinding and bias prevention]

**VALIDATION APPROACHES:**
- [Cross-validation, holdout sets, or validation procedures]
- [Replication and reproducibility measures]
- [Independent validation or peer review]

**STATISTICAL METHODS:**
- [Appropriateness of statistical tests]
- [Multiple comparison corrections]
- [Assumption checking and model validation]

**POTENTIAL BIASES:**
- [Selection bias, confirmation bias, or other systematic errors]
- [Confounding variables not controlled for]
- [Measurement bias or instrumentation issues]

Focus on methodological strengths and weaknesses that experts would debate."""
        
        methodology_response = self._call_ollama(methodology_prompt, max_length=2500)
        
        return self._parse_methodology_analysis(methodology_response)
    
    def _detect_gaps_and_overclaims(self, evidence_mappings: List[EvidenceMapping], 
                                  core_understanding: CoreUnderstanding) -> Tuple[List[str], List[str]]:
        """Detect gaps between claims and evidence, and potential overclaims"""
        
        gaps = []
        overclaims = []
        
        # Analyze evidence strength vs claim strength
        for mapping in evidence_mappings:
            claim = mapping.claim
            strength = mapping.evidence_strength
            
            # Check for gaps (weak/absent evidence for strong claims)
            if strength in ['weak', 'absent']:
                if any(strong_word in claim.lower() for strong_word in ['significant', 'substantial', 'breakthrough', 'revolutionary', 'superior']):
                    gaps.append(f"Strong claim '{claim[:60]}...' has {strength} evidence")
            
            # Check for overclaims (stronger claims than evidence supports)
            if strength == 'moderate' and any(very_strong in claim.lower() for very_strong in ['revolutionary', 'breakthrough', 'unprecedented']):
                overclaims.append(f"Claim uses strong language '{claim[:60]}...' but evidence is only moderate")
            
            # Check for contradictory evidence
            if mapping.contradictory_evidence:
                gaps.append(f"Contradictory evidence found for claim '{claim[:60]}...': {len(mapping.contradictory_evidence)} counter-points")
        
        return gaps, overclaims
    
    def _generate_debate_ammunition(self, evidence_mappings: List[EvidenceMapping],
                                  technical_analysis: TechnicalDeepDive,
                                  methodology_analysis: MethodologyAnalysis) -> Dict[str, List[str]]:
        """Generate specific ammunition for optimist vs skeptic debates"""
        
        optimist_ammunition = []
        skeptic_ammunition = []
        
        # From evidence mappings
        for mapping in evidence_mappings:
            if mapping.evidence_strength == 'strong' and mapping.supporting_evidence:
                optimist_ammunition.extend([f"Strong evidence: {evidence}" for evidence in mapping.supporting_evidence[:2]])
            
            if mapping.evidence_strength in ['weak', 'absent'] or mapping.contradictory_evidence:
                skeptic_ammunition.append(f"Weak evidence for key claim: {mapping.claim[:60]}...")
                skeptic_ammunition.extend([f"Contradictory finding: {evidence}" for evidence in mapping.contradictory_evidence[:2]])
        
        # From technical analysis
        if technical_analysis.performance_metrics:
            optimist_ammunition.extend([f"Impressive performance: {metric}" for metric in technical_analysis.performance_metrics[:2]])
        
        if technical_analysis.limitations_detailed:
            skeptic_ammunition.extend([f"Significant limitation: {limit}" for limit in technical_analysis.limitations_detailed[:2]])
        
        # From methodology analysis  
        if methodology_analysis.validation_approaches:
            optimist_ammunition.extend([f"Rigorous validation: {approach}" for approach in methodology_analysis.validation_approaches[:2]])
        
        if methodology_analysis.potential_biases:
            skeptic_ammunition.extend([f"Potential bias: {bias}" for bias in methodology_analysis.potential_biases[:2]])
        
        return {
            "optimist": optimist_ammunition[:8],  # Limit to most important points
            "skeptic": skeptic_ammunition[:8]
        }
    
    def _parse_technical_deep_dive(self, response: str) -> TechnicalDeepDive:
        """Parse technical deep dive response"""
        
        algorithms = []
        experimental = []
        statistical = []
        performance = []
        implementation = []
        comparison = []
        limitations = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_upper = line.upper()
            
            # Section detection
            if 'ALGORITHMS DETAILED' in line_upper:
                current_section = 'algorithms'
            elif 'EXPERIMENTAL DESIGN' in line_upper:
                current_section = 'experimental'
            elif 'STATISTICAL RESULTS' in line_upper:
                current_section = 'statistical'
            elif 'PERFORMANCE METRICS' in line_upper:
                current_section = 'performance'
            elif 'IMPLEMENTATION DETAILS' in line_upper:
                current_section = 'implementation'
            elif 'COMPARISON RESULTS' in line_upper:
                current_section = 'comparison'
            elif 'LIMITATIONS DETAILED' in line_upper:
                current_section = 'limitations'
            elif line.startswith(('-', '•', '*')) and len(line) > 20:
                # Extract content based on current section
                content = line.strip('- •*').strip()
                if current_section == 'algorithms':
                    algorithms.append(content)
                elif current_section == 'experimental':
                    experimental.append(content)
                elif current_section == 'statistical':
                    statistical.append(content)
                elif current_section == 'performance':
                    performance.append(content)
                elif current_section == 'implementation':
                    implementation.append(content)
                elif current_section == 'comparison':
                    comparison.append(content)
                elif current_section == 'limitations':
                    limitations.append(content)
        
        return TechnicalDeepDive(
            algorithms_detailed=algorithms,
            experimental_design=experimental,
            statistical_results=statistical,
            performance_metrics=performance,
            implementation_details=implementation,
            comparison_results=comparison,
            limitations_detailed=limitations
        )
    
    def _parse_methodology_analysis(self, response: str) -> MethodologyAnalysis:
        """Parse methodology analysis response"""
        
        data_collection = []
        sample_characteristics = []
        control_measures = []
        validation_approaches = []
        statistical_methods = []
        potential_biases = []
        
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_upper = line.upper()
            
            # Section detection
            if 'DATA COLLECTION' in line_upper:
                current_section = 'data'
            elif 'SAMPLE CHARACTERISTICS' in line_upper:
                current_section = 'sample'
            elif 'CONTROL MEASURES' in line_upper:
                current_section = 'control'
            elif 'VALIDATION APPROACHES' in line_upper:
                current_section = 'validation'
            elif 'STATISTICAL METHODS' in line_upper:
                current_section = 'statistical'
            elif 'POTENTIAL BIASES' in line_upper:
                current_section = 'biases'
            elif line.startswith(('-', '•', '*')) and len(line) > 20:
                # Extract content
                content = line.strip('- •*').strip()
                if current_section == 'data':
                    data_collection.append(content)
                elif current_section == 'sample':
                    sample_characteristics.append(content)
                elif current_section == 'control':
                    control_measures.append(content)
                elif current_section == 'validation':
                    validation_approaches.append(content)
                elif current_section == 'statistical':
                    statistical_methods.append(content)
                elif current_section == 'biases':
                    potential_biases.append(content)
        
        return MethodologyAnalysis(
            data_collection=data_collection,
            sample_characteristics=sample_characteristics,
            control_measures=control_measures,
            validation_approaches=validation_approaches,
            statistical_methods=statistical_methods,
            potential_biases=potential_biases
        )
    
    def test_connection(self) -> bool:
        """Test Ollama connection"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 0 and "Error" not in test_response
        except:
            return False
