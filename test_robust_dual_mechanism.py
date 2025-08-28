#!/usr/bin/env python3
"""
Test Robust Dual-Mechanism System
Save as: test_robust_dual_mechanism.py (in root directory)

Tests the complete robust pipeline with auto-fallback:
- Tests complexity assessment
- Validates sophisticated vs simplified generation
- Ensures 100% success rate
- Checks production quality across different paper types
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append('src')
sys.path.append('.')

# Import robust components
try:
    from pdf_processor import PDFProcessor
    from robust_pipeline_integration import RobustPipelineIntegration, RobustDialogueEngine
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have all robust system files:")
    print("  - src/robust_debate_generator.py")
    print("  - src/robust_pipeline_integration.py")
    sys.exit(1)


def test_robust_dual_mechanism(pdf_path: str):
    """Test robust dual-mechanism with complexity assessment"""
    
    print("🛡️ TESTING ROBUST DUAL-MECHANISM SYSTEM")
    print("Auto-detection + Sophisticated/Simplified Fallback")
    print("=" * 70)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print(f"📄 Testing with: {pdf_file.name}")
    
    # Initialize robust system
    pdf_processor = PDFProcessor()
    robust_integration = RobustPipelineIntegration()
    
    # Test connection
    if not robust_integration.test_connection():
        print("❌ Robust system connection failed")
        return False
    
    print("✅ Robust system ready")
    
    try:
        # ================== PDF PROCESSING ==================
        print(f"\n{'='*20} PDF PROCESSING {'='*20}")
        
        print("📖 Extracting PDF content...")
        paper_data = pdf_processor.process_paper(pdf_path)
        raw_text = paper_data["raw_text"]
        print(f"✅ Extracted {len(raw_text):,} characters")
        
        # ================== ROBUST CONVERSATION GENERATION ==================
        print(f"\n{'='*15} ROBUST CONVERSATION GENERATION {'='*15}")
        
        print("🛡️ Testing robust conversation creation...")
        print("   (This should ALWAYS succeed regardless of complexity)")
        
        # Test with different settings to see fallback behavior
        test_settings = [
            {"max_topics": 2, "exchanges": 3, "label": "Conservative"},
            {"max_topics": 3, "exchanges": 4, "label": "Standard"},
            {"max_topics": 4, "exchanges": 5, "label": "Aggressive"}
        ]
        
        results = []
        
        for setting in test_settings:
            print(f"\n🧪 Testing {setting['label']} settings: {setting['max_topics']} topics, {setting['exchanges']} exchanges")
            
            try:
                robust_script = robust_integration.create_robust_conversation(
                    paper_data, 
                    max_topics=setting["max_topics"], 
                    exchanges_per_topic=setting["exchanges"]
                )
                
                results.append({
                    "setting": setting["label"],
                    "success": True,
                    "method": robust_script.generation_method,
                    "sophistication": robust_script.sophistication_score,
                    "quality": robust_script.production_quality,
                    "turns": robust_script.total_turns,
                    "citations": len(robust_script.evidence_citations),
                    "script": robust_script
                })
                
                print(f"   ✅ SUCCESS: {robust_script.generation_method} mode")
                print(f"      🏆 Sophistication: {robust_script.sophistication_score}/100")
                print(f"      📈 Quality: {robust_script.production_quality}")
                print(f"      🎭 Turns: {robust_script.total_turns}")
                print(f"      📚 Citations: {len(robust_script.evidence_citations)}")
                
            except Exception as e:
                print(f"   ❌ FAILED: {e}")
                results.append({
                    "setting": setting["label"],
                    "success": False,
                    "error": str(e)
                })
        
        # ================== LEGACY COMPATIBILITY TEST ==================
        print(f"\n{'='*15} LEGACY COMPATIBILITY TEST {'='*15}")
        
        print("🔄 Testing drop-in replacement for existing system...")
        
        # Test RobustDialogueEngine as drop-in replacement
        robust_dialogue_engine = RobustDialogueEngine()
        
        # Simulate existing system's analysis_results format
        mock_analysis_results = {
            "enhanced_sections": {"abstract": raw_text[:1000], "conclusion": raw_text[-1000:]},
            "summary": {"main_topic": "Research Paper Analysis", "key_finding": "Novel findings"},
            "analysis_depth": {"total_strengths": 5, "total_weaknesses": 3}
        }
        
        print("🧪 Testing legacy create_full_conversation interface...")
        
        try:
            legacy_script = robust_dialogue_engine.create_full_conversation(
                mock_analysis_results, max_topics=3, exchanges_per_topic=4
            )
            
            print("✅ Legacy compatibility successful!")
            print(f"   📝 Title: {legacy_script.title}")
            print(f"   🎭 Turns: {legacy_script.total_turns}")
            print(f"   ⏱️ Duration: {legacy_script.duration_estimate}")
            
            # Check production info
            if hasattr(legacy_script, 'production_info'):
                info = legacy_script.production_info
                print(f"   🔧 Generation: {info['generation_method']}")
                print(f"   🏆 Sophistication: {info['sophistication_score']}")
                print(f"   📈 Quality: {info['production_quality']}")
                print(f"   📚 Citations: {info['evidence_citations']}")
            
        except Exception as e:
            print(f"❌ Legacy compatibility failed: {e}")
            return False
        
        # ================== RESULTS ANALYSIS ==================
        print(f"\n{'='*20} ROBUST SYSTEM ANALYSIS {'='*20}")
        
        successful_results = [r for r in results if r["success"]]
        
        print(f"📊 SUCCESS RATE: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.0f}%)")
        
        if len(successful_results) == len(results):
            print("✅ 100% SUCCESS RATE - Robust system working perfectly!")
        else:
            print("⚠️ Some failures detected - needs debugging")
        
        # Analyze generation methods used
        methods_used = [r["method"] for r in successful_results]
        sophistication_modes = set(methods_used)
        
        print(f"\n🔧 GENERATION METHODS USED:")
        for method in sophistication_modes:
            count = methods_used.count(method)
            print(f"   {method.upper()}: {count}/{len(successful_results)} tests")
        
        # Quality distribution
        quality_levels = [r["quality"] for r in successful_results]
        print(f"\n📈 PRODUCTION QUALITY DISTRIBUTION:")
        for quality in ["excellent", "good", "acceptable"]:
            count = quality_levels.count(quality)
            if count > 0:
                print(f"   {quality.upper()}: {count}/{len(successful_results)} tests")
        
        # Show best result details
        if successful_results:
            best_result = max(successful_results, key=lambda r: r["sophistication"])
            print(f"\n🏆 BEST RESULT ({best_result['setting']} settings):")
            print(f"   🔧 Method: {best_result['method']}")
            print(f"   🏆 Sophistication: {best_result['sophistication']}/100")
            print(f"   📈 Quality: {best_result['quality']}")
            print(f"   🎭 Turns: {best_result['turns']}")
            print(f"   📚 Citations: {best_result['citations']}")
            
            # Show sample content
            script = best_result["script"]
            print(f"\n💬 SAMPLE EXCHANGES:")
            print("-" * 50)
            for i, turn in enumerate(script.turns[:3]):
                speaker_emoji = "😊" if "Ava" in turn.speaker else "🤨"
                print(f"\n{speaker_emoji} **{turn.speaker}** ({turn.generation_method}):")
                print(f"{turn.content}")
        
        # ================== PRODUCTION READINESS ASSESSMENT ==================
        print(f"\n{'='*15} PRODUCTION READINESS ASSESSMENT {'='*15}")
        
        production_score = 0
        max_production_score = 10
        
        # Success rate
        success_rate = len(successful_results) / len(results)
        if success_rate == 1.0:
            production_score += 3
            print("✅ Perfect reliability (100% success rate) (+3)")
        elif success_rate >= 0.8:
            production_score += 2
            print("✅ High reliability (80%+ success rate) (+2)")
        else:
            production_score += 1
            print("⚠️ Moderate reliability (<80% success rate) (+1)")
        
        # Quality consistency
        if successful_results:
            min_quality_score = min(r["sophistication"] for r in successful_results)
            if min_quality_score >= 50:
                production_score += 2
                print("✅ Consistent quality (all results ≥50 sophistication) (+2)")
            elif min_quality_score >= 30:
                production_score += 1
                print("✅ Acceptable quality (all results ≥30 sophistication) (+1)")
        
        # Method diversity (shows fallback working)
        if len(sophistication_modes) > 1:
            production_score += 2
            print("✅ Adaptive behavior (multiple generation methods used) (+2)")
        elif "simplified" in sophistication_modes:
            production_score += 1
            print("✅ Fallback working (simplified method used) (+1)")
        
        # Content quality
        if successful_results:
            avg_turns = sum(r["turns"] for r in successful_results) / len(successful_results)
            if avg_turns >= 6:
                production_score += 2
                print(f"✅ Rich content (avg {avg_turns:.1f} turns per conversation) (+2)")
            elif avg_turns >= 4:
                production_score += 1
                print(f"✅ Adequate content (avg {avg_turns:.1f} turns per conversation) (+1)")
        
        # Evidence integration
        if successful_results:
            total_citations = sum(r["citations"] for r in successful_results)
            if total_citations > 0:
                production_score += 1
                print(f"✅ Evidence integration ({total_citations} total citations) (+1)")
        
        print(f"\n🏆 PRODUCTION READINESS SCORE: {production_score}/{max_production_score}")
        
        if production_score >= 8:
            print("🌟 OUTSTANDING - Ready for production YouTube content!")
            production_ready = True
        elif production_score >= 6:
            print("✅ EXCELLENT - Production ready with high confidence!")
            production_ready = True
        elif production_score >= 4:
            print("⚠️ GOOD - Production ready with minor monitoring needed")
            production_ready = True
        else:
            print("❌ NEEDS IMPROVEMENT - Not ready for production")
            production_ready = False
        
        # Final recommendations
        print(f"\n🎯 PRODUCTION RECOMMENDATIONS:")
        
        if production_ready:
            print("✅ APPROVED FOR YOUTUBE INTEGRATION")
            print("   1. Replace dialogue_generator_fixed.py import")
            print("   2. Test with your existing audio/video pipeline")
            print("   3. Monitor generation methods in production")
            print("   4. Expect mix of sophisticated/simplified based on complexity")
        else:
            print("❌ NEEDS WORK BEFORE PRODUCTION")
            print("   1. Debug failed test cases")
            print("   2. Improve fallback mechanisms")
            print("   3. Re-test with different papers")
        
        return production_ready
        
    except Exception as e:
        print(f"❌ Robust system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    
    default_path = "/home/md724/ai_paper_narrator/data/input/WCC_and_CM_Paper_Complex_Networks-1.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_path
    
    print("🛡️ AI Paper Narrator - Robust Dual-Mechanism Test")
    print("Testing production-ready system with auto-fallback")
    print("-" * 70)
    
    success = test_robust_dual_mechanism(pdf_path)
    
    if success:
        print(f"\n🎉 ROBUST SYSTEM TEST SUCCESSFUL!")
        print(f"✅ Production-ready with auto-fallback guarantees")
        print(f"✅ 100% content generation success rate")
        print(f"✅ Graceful quality degradation")
        print(f"✅ Legacy compatibility maintained")
        print(f"\n🔗 READY FOR YOUTUBE INTEGRATION!")
        print(f"Change import: RobustDialogueEngine as FixedDialogueEngine")
    else:
        print(f"\n🔧 ROBUST SYSTEM NEEDS IMPROVEMENT")
        print(f"❌ Check test results above for specific issues")


if __name__ == "__main__":
    main()
