"""
Two-Stage Analyzer Integration Module
Save as: src/two_stage_analyzer.py

Integrates Stage 1 (Core Understanding) + Stage 2 (Evidence Hunting)
for comprehensive academic paper analysis ready for sophisticated debates.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass

# Import both stages
from enhanced_analyzer import EnhancedPaperAnalyzer, CoreUnderstanding
from stage2_evidence_hunter import Stage2EvidenceHunter, ComprehensiveEvidence


@dataclass
class CompleteAnalysis:
    """Complete two-stage analysis results"""
    core_understanding: CoreUnderstanding
    comprehensive_evidence: ComprehensiveEvidence
    analysis_quality_score: int
    ready_for_debates: bool


class TwoStageAnalyzer:
    """Complete two-stage paper analyzer for sophisticated AI debates"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.stage1_analyzer = EnhancedPaperAnalyzer(model_name, base_url)
        self.stage2_hunter = Stage2EvidenceHunter(model_name, base_url)
    
    def analyze_paper_complete(self, raw_text: str) -> CompleteAnalysis:
        """
        Complete two-stage analysis of research paper
        
        Args:
            raw_text: Full paper text from PDF extraction
            
        Returns:
            CompleteAnalysis with both stages + quality assessment
        """
        
        print("🚀 Starting Complete Two-Stage Analysis...")
        
        # Stage 1: Core Understanding
        print("\n📖 Stage 1: Core Understanding Analysis...")
        core_sections = self.stage1_analyzer.enhanced_section_detection(raw_text)
        
        if not core_sections:
            raise ValueError("No core sections found - cannot analyze paper")
        
        core_understanding = self.stage1_analyzer.stage1_core_understanding_analysis(core_sections)
        
        # Stage 2: Evidence Hunting
        print("\n🔍 Stage 2: Evidence Hunting Analysis...")
        comprehensive_evidence = self.stage2_hunter.comprehensive_stage2_analysis(
            core_understanding, raw_text
        )
        
        # Quality assessment
        quality_score = self._assess_analysis_quality(core_understanding, comprehensive_evidence)
        ready_for_debates = quality_score >= 12  # High threshold for debate readiness
        
        print(f"\n✅ Two-Stage Analysis Complete! Quality Score: {quality_score}/20")
        
        return CompleteAnalysis(
            core_understanding=core_understanding,
            comprehensive_evidence=comprehensive_evidence,
            analysis_quality_score=quality_score,
            ready_for_debates=ready_for_debates
        )
    
    def _assess_analysis_quality(self, core_understanding: CoreUnderstanding, 
                               comprehensive_evidence: ComprehensiveEvidence) -> int:
        """Assess overall analysis quality for debate readiness"""
        
        score = 0
        
        # Stage 1 quality (max 10 points)
        if core_understanding.field_classification != "General Research":
            score += 2
        
        if len(core_understanding.debate_seed_points) >= 8:
            score += 3
        elif len(core_understanding.debate_seed_points) >= 5:
            score += 2
        
        if len(core_understanding.research_story_arc) >= 5:
            score += 2
        elif len(core_understanding.research_story_arc) >= 3:
            score += 1
        
        if len(core_understanding.key_technical_elements) >= 6:
            score += 2
        elif len(core_understanding.key_technical_elements) >= 3:
            score += 1
        
        if len(core_understanding.confidence_assessment) >= 4:
            score += 1
        
        # Stage 2 quality (max 10 points)
        if len(comprehensive_evidence.evidence_mappings) >= 3:
            score += 2
        
        strong_evidence = sum(1 for m in comprehensive_evidence.evidence_mappings if m.evidence_strength == 'strong')
        if strong_evidence >= 2:
            score += 2
        elif strong_evidence >= 1:
            score += 1
        
        tech = comprehensive_evidence.technical_deep_dive
        if len(tech.algorithms_detailed) + len(tech.performance_metrics) >= 4:
            score += 2
        
        method = comprehensive_evidence.methodology_analysis
        if len(method.potential_biases) + len(comprehensive_evidence.claim_evidence_gaps) >= 3:
            score += 2
        
        ammunition = comprehensive_evidence.expert_debate_ammunition
        if len(ammunition.get('optimist', [])) >= 3 and len(ammunition.get('skeptic', [])) >= 3:
            score += 2
        
        return score
    
    def get_debate_ammunition(self, analysis: CompleteAnalysis) -> Dict[str, List[str]]:
        """Extract ready-to-use debate ammunition for AI personalities"""
        
        return analysis.comprehensive_evidence.expert_debate_ammunition
    
    def get_technical_details(self, analysis: CompleteAnalysis) -> Dict[str, List[str]]:
        """Extract technical details for expert-level discussions"""
        
        tech = analysis.comprehensive_evidence.technical_deep_dive
        
        return {
            "algorithms": tech.algorithms_detailed,
            "performance": tech.performance_metrics,
            "experimental_design": tech.experimental_design,
            "statistical_results": tech.statistical_results,
            "implementation": tech.implementation_details,
            "limitations": tech.limitations_detailed
        }
    
    def get_evidence_gaps(self, analysis: CompleteAnalysis) -> List[str]:
        """Extract evidence gaps for skeptical arguments"""
        
        return (analysis.comprehensive_evidence.claim_evidence_gaps + 
                analysis.comprehensive_evidence.overclaim_detection)
    
    def test_connection(self) -> bool:
        """Test if both analysis stages are ready"""
        return (self.stage1_analyzer.test_connection() and 
                self.stage2_hunter.test_connection())
    
    def generate_debate_topics(self, analysis: CompleteAnalysis) -> List[Dict[str, str]]:
        """Generate sophisticated debate topics using both stages"""
        
        topics = []
        
        # Use Stage 1 debate points as base
        stage1_debates = analysis.core_understanding.debate_seed_points
        
        # Enhance with Stage 2 evidence
        evidence_mappings = analysis.comprehensive_evidence.evidence_mappings
        gaps = analysis.comprehensive_evidence.claim_evidence_gaps
        
        # Combine for sophisticated topics
        for i, debate_point in enumerate(stage1_debates[:5]):
            topic = {
                "question": debate_point,
                "optimist_evidence": [],
                "skeptic_evidence": []
            }
            
            # Find relevant evidence mappings
            for mapping in evidence_mappings:
                if any(word in mapping.claim.lower() for word in debate_point.lower().split()[:3]):
                    if mapping.supporting_evidence:
                        topic["optimist_evidence"].extend(mapping.supporting_evidence[:2])
                    if mapping.contradictory_evidence:
                        topic["skeptic_evidence"].extend(mapping.contradictory_evidence[:2])
            
            # Add gaps as skeptic evidence
            relevant_gaps = [gap for gap in gaps if any(word in gap.lower() for word in debate_point.lower().split()[:3])]
            topic["skeptic_evidence"].extend(relevant_gaps[:2])
            
            topics.append(topic)
        
        return topics
    
    def format_analysis_summary(self, analysis: CompleteAnalysis) -> str:
        """Format complete analysis for display"""
        
        output = []
        output.append("📊 COMPLETE TWO-STAGE ANALYSIS SUMMARY")
        output.append("=" * 50)
        
        # Stage 1 summary
        core = analysis.core_understanding
        output.append(f"\n🎯 FIELD: {core.field_classification}")
        output.append(f"📖 Research Story Elements: {len(core.research_story_arc)}")
        output.append(f"⚔️ Debate Points: {len(core.debate_seed_points)}")
        output.append(f"🔧 Technical Elements: {len(core.key_technical_elements)}")
        
        # Stage 2 summary
        evidence = analysis.comprehensive_evidence
        output.append(f"\n🔍 Evidence Mappings: {len(evidence.evidence_mappings)}")
        
        strong_evidence = sum(1 for m in evidence.evidence_mappings if m.evidence_strength == 'strong')
        output.append(f"💪 Strong Evidence Claims: {strong_evidence}")
        
        tech = evidence.technical_deep_dive
        output.append(f"🔬 Technical Details: {len(tech.algorithms_detailed) + len(tech.performance_metrics)}")
        
        ammunition = evidence.expert_debate_ammunition
        output.append(f"⚔️ Debate Ammunition: {len(ammunition.get('optimist', []))} vs {len(ammunition.get('skeptic', []))}")
        
        # Quality assessment
        output.append(f"\n🏆 Quality Score: {analysis.analysis_quality_score}/20")
        output.append(f"🎬 Debate Ready: {'✅ YES' if analysis.ready_for_debates else '❌ Needs improvement'}")
        
        return "\n".join(output)


# Example usage function
def quick_analysis_example():
    """Example of how to use the two-stage analyzer"""
    
    # Initialize analyzer
    analyzer = TwoStageAnalyzer()
    
    # Check connection
    if not analyzer.test_connection():
        print("❌ Connection failed")
        return
    
    # Example: analyze a paper (you would get raw_text from PDF processor)
    raw_text = "Your extracted PDF text here..."
    
    try:
        # Run complete analysis
        analysis = analyzer.analyze_paper_complete(raw_text)
        
        # Display summary
        print(analyzer.format_analysis_summary(analysis))
        
        # Get debate materials
        if analysis.ready_for_debates:
            ammunition = analyzer.get_debate_ammunition(analysis)
            technical_details = analyzer.get_technical_details(analysis)
            evidence_gaps = analyzer.get_evidence_gaps(analysis)
            
            print("\n🎭 Ready for sophisticated AI debates!")
            print(f"😊 Optimist ammunition: {len(ammunition.get('optimist', []))} points")
            print(f"🤨 Skeptic ammunition: {len(ammunition.get('skeptic', []))} points")
            print(f"🔬 Technical details: {sum(len(v) for v in technical_details.values())} elements")
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


if __name__ == "__main__":
    print("📚 Two-Stage Analyzer Integration Module")
    print("Use this module to integrate Stage 1 + Stage 2 analysis")
    print("\nExample usage:")
    print("  from two_stage_analyzer import TwoStageAnalyzer")
    print("  analyzer = TwoStageAnalyzer()")
    print("  analysis = analyzer.analyze_paper_complete(raw_text)")
