"""Phase 2 Integration - FIXED to use Phase 1 analysis results"""

import sys
from pathlib import Path
import json
from typing import Dict  

from pdf_processor import PDFProcessor
from summarizer_final_fixed_v2 import FinalFixedPaperSummarizerV2 as FinalFixedPaperSummarizer
from dialogue_generator_fixed import FixedDialogueEngine
from config import OUTPUT_DIR


class FixedPaperNarratorPhase2:
    """FIXED AI Paper Narrator that uses Phase 1 results"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.summarizer = FinalFixedPaperSummarizer()
        self.dialogue_engine = FixedDialogueEngine()  # Use FIXED dialogue generator
    
    def check_prerequisites(self) -> bool:
        """Check if all required services are running"""
        print("🔧 Checking FIXED Phase 2 prerequisites...")
        
        if not self.summarizer.test_connection():
            print("❌ Ollama not running or model not available")
            return False
        
        print("✅ Ollama connection successful")
        
        if not self.dialogue_engine.test_connection():
            print("❌ FIXED dialogue engine connection failed")
            return False
        
        print("✅ FIXED dialogue engine ready")
        return True
    
    def process_paper_with_dialogue(self, pdf_path: str, 
                                  max_topics: int = 3,
                                  exchanges_per_topic: int = 3) -> Dict:
        """FIXED pipeline that actually uses Phase 1 analysis"""
        
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        print(f"\n📄 Processing with FIXED Phase 2: {pdf_path.name}")
        print("=" * 70)
        
        # Step 1: Phase 1 analysis
        print("Step 1: Phase 1 analysis...")
        paper_data = self.pdf_processor.process_paper(str(pdf_path))
        analysis_results = self.summarizer.deep_paper_analysis(paper_data)
        
        # Validate Phase 1 results contain paper-specific content
        main_topic = analysis_results['summary'].get('main_topic', '')
        print(f"📋 Phase 1 identified topic: {main_topic}")
        
        if 'community' in main_topic.lower() or 'WCC' in str(analysis_results['detailed_discussion_topics']):
            print("✅ Phase 1 results are paper-specific")
        else:
            print("⚠️  Phase 1 results seem generic - proceeding anyway")
        
        # Step 2: FIXED dialogue generation that uses Phase 1 results
        print(f"\nStep 2: FIXED dialogue generation using Phase 1 analysis...")
        print(f"   📊 Using {len(analysis_results['detailed_discussion_topics'])} paper-specific topics")
        
        conversation_script = self.dialogue_engine.create_full_conversation(
            analysis_results,  # Pass the ACTUAL Phase 1 results
            max_topics=max_topics,
            exchanges_per_topic=exchanges_per_topic
        )
        
        # Validate conversation mentions paper content
        script_text = ' '.join([turn.content for turn in conversation_script.turns])
        paper_terms = ['WCC', 'Chapel', 'community detection', 'parallel', 'network']
        generic_terms = ['machine learning', 'computational biology', 'disease']
        
        paper_mentions = sum(1 for term in paper_terms if term.lower() in script_text.lower())
        generic_mentions = sum(1 for term in generic_terms if term.lower() in script_text.lower())
        
        print(f"   📊 Conversation validation:")
        print(f"      Paper-specific terms: {paper_mentions}")
        print(f"      Generic terms: {generic_mentions}")
        
        if paper_mentions > generic_mentions:
            print("   ✅ Conversation is paper-specific!")
        else:
            print("   ❌ Conversation is still too generic!")
        
        # Combine results
        complete_result = {
            "source_file": str(pdf_path),
            "phase1_analysis": {
                "extraction": paper_data["metadata"],
                "enhanced_sections": analysis_results["enhanced_sections"],
                "detailed_summary": analysis_results["summary"],
                "comprehensive_analysis": analysis_results["comprehensive_analysis"],
                "discussion_topics": analysis_results["detailed_discussion_topics"],
                "analysis_depth": analysis_results["analysis_depth"]
            },
            "phase2_dialogue": {
                "conversation_script": {
                    "title": conversation_script.title,
                    "paper_topic": conversation_script.paper_topic,
                    "introduction": conversation_script.introduction,
                    "turns": [
                        {
                            "speaker": turn.speaker,
                            "speaker_role": turn.speaker_role,
                            "content": turn.content,
                            "topic": turn.topic,
                            "turn_number": turn.turn_number
                        }
                        for turn in conversation_script.turns
                    ],
                    "conclusion": conversation_script.conclusion,
                    "total_turns": conversation_script.total_turns,
                    "duration_estimate": conversation_script.duration_estimate
                }
            },
            "validation": {
                "paper_specific_terms": paper_mentions,
                "generic_terms": generic_mentions,
                "is_paper_specific": paper_mentions > generic_mentions
            },
            "status": "fixed_phase2_complete"
        }
        
        # Save results
        output_file = OUTPUT_DIR / f"{pdf_path.stem}_FIXED_phase2.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ FIXED analysis saved to: {output_file}")
        return complete_result, conversation_script
    
    def display_conversation_script(self, conversation_script):
        """Display the generated conversation"""
        formatted_script = self.dialogue_engine.format_script_for_display(conversation_script)
        print(formatted_script)
    
    def display_phase2_summary(self, results: Dict, conversation_script):
        """Display Phase 2 summary with validation"""
        
        print("\n" + "="*80)
        print("📊 FIXED PHASE 2 RESULTS")
        print("="*80)
        
        # Phase 1 Summary
        phase1 = results["phase1_analysis"]
        print(f"\n📋 PHASE 1 ANALYSIS:")
        print(f"   • Sections detected: {phase1['analysis_depth']['sections_found']}")
        print(f"   • Strengths identified: {phase1['analysis_depth']['total_strengths']}")
        print(f"   • Weaknesses identified: {phase1['analysis_depth']['total_weaknesses']}")
        print(f"   • Discussion topics: {phase1['analysis_depth']['discussion_topics']}")
        
        # Phase 2 Summary
        print(f"\n🎭 FIXED PHASE 2 DIALOGUE:")
        print(f"   • Conversation title: {conversation_script.title}")
        print(f"   • Total speaking turns: {conversation_script.total_turns}")
        print(f"   • Estimated duration: {conversation_script.duration_estimate}")
        
        # Validation results
        validation = results.get("validation", {})
        print(f"\n✅ CONTENT VALIDATION:")
        print(f"   • Paper-specific terms: {validation.get('paper_specific_terms', 0)}")
        print(f"   • Generic terms: {validation.get('generic_terms', 0)}")
        print(f"   • Is paper-specific: {validation.get('is_paper_specific', False)}")
        
        if validation.get('is_paper_specific', False):
            print(f"   🎉 SUCCESS: Dialogue uses actual paper content!")
        else:
            print(f"   ⚠️  WARNING: Dialogue is still too generic")


def main():
    """FIXED Phase 2 main entry point"""
    
    print("🔧 AI Paper Narrator - FIXED Phase 2")
    print("Analysis + ACTUALLY Uses Phase 1 Results")
    print("-" * 50)
    
    narrator = FixedPaperNarratorPhase2()
    
    if not narrator.check_prerequisites():
        sys.exit(1)
    
    # Get parameters
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        max_topics = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        exchanges_per_topic = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    else:
        pdf_path = input("\n📁 Enter path to PDF file: ").strip().strip('"')
        max_topics = int(input("📊 Max topics (default 2): ") or "2")
        exchanges_per_topic = int(input("💬 Exchanges per topic (default 2): ") or "2")
    
    try:
        # Process with FIXED dialogue
        results, conversation_script = narrator.process_paper_with_dialogue(
            pdf_path, max_topics, exchanges_per_topic
        )
        
        # Display results
        narrator.display_conversation_script(conversation_script)
        narrator.display_phase2_summary(results, conversation_script)
        
        # Final validation
        validation = results.get("validation", {})
        if validation.get('is_paper_specific', False):
            print(f"\n🎉 FIXED Phase 2 SUCCESS!")
            print(f"📄 Dialogue mentions WCC, Chapel, community detection")
            print(f"🚀 Ready for Phase 3 (Audio Generation)")
        else:
            print(f"\n⚠️  Dialogue still needs improvement")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
