"""
Expert-Level Deep Analysis Prompts
Save as: src/expert_deep_prompts.py

Specialized prompts that make AI think like actual domain experts
for generating sophisticated, technical debates with maximum depth.
"""

from typing import Dict, List, Any
import re


class ExpertDeepPrompts:
    """Generate expert-level prompts for deep technical analysis"""
    
    def __init__(self):
        # Expert personas for different types of analysis
        self.expert_personas = {
            "statistician": "You are a senior biostatistician with 15+ years experience reviewing papers for top-tier journals. You focus obsessively on statistical rigor, sample sizes, power analysis, multiple comparisons, and statistical assumptions.",
            
            "methodologist": "You are a research methodology expert who has written textbooks on experimental design. You scrutinize every aspect of how studies are conducted, looking for confounders, selection bias, measurement error, and threats to validity.",
            
            "domain_expert": "You are a world-renowned expert in this specific research domain with 200+ publications. You know the field's history, competing approaches, current controversies, and exactly what constitutes meaningful progress vs incremental work.",
            
            "replication_expert": "You are a specialist in research reproducibility who has attempted to replicate hundreds of studies. You focus on whether others could actually reproduce these results and what critical details are missing.",
            
            "critic": "You are a notoriously tough peer reviewer known for identifying fatal flaws in papers. You approach every claim with deep skepticism and look for any possible way the conclusions could be wrong.",
            
            "theorist": "You are a theoretical expert who understands the mathematical foundations and theoretical assumptions underlying the methods. You focus on whether the theory actually supports the practical application."
        }
    
    def generate_field_specific_controversy_prompt(self, field: str, paper_content: str) -> str:
        """Generate prompts to find field-specific controversies that experts actually fight about"""
        
        field_controversies = {
            "machine learning": [
                "generalization vs memorization debates",
                "statistical significance vs practical significance in ML metrics", 
                "benchmark dataset bias and evaluation methodology disputes",
                "interpretability vs performance tradeoff arguments",
                "reproducibility crisis in ML experiments"
            ],
            "psychology": [
                "replication crisis and statistical power issues",
                "WEIRD population generalizability problems", 
                "p-hacking and multiple comparisons scandals",
                "effect size vs statistical significance debates",
                "measurement validity and construct disputes"
            ],
            "medicine": [
                "clinical significance vs statistical significance",
                "randomized controlled trial design controversies",
                "endpoint selection and composite outcome disputes",
                "subgroup analysis and post-hoc testing issues",
                "real-world evidence vs controlled trial debates"
            ],
            "computer science": [
                "theoretical complexity vs practical performance gaps",
                "algorithmic fairness vs optimization accuracy tradeoffs",
                "scalability claims vs limited experimental validation",
                "novelty vs incremental improvement distinctions",
                "reproducible systems research challenges"
            ]
        }
        
        # Determine most relevant controversies for this field
        relevant_controversies = []
        for field_key, controversies in field_controversies.items():
            if field_key in field.lower():
                relevant_controversies = controversies
                break
        
        if not relevant_controversies:
            relevant_controversies = field_controversies["computer science"]  # Default
        
        prompt = f"""You are a senior academic expert in {field} with deep knowledge of the field's most contentious debates and methodological controversies.

PAPER CONTENT:
{paper_content[:4000]}

FIELD-SPECIFIC CONTROVERSIES TO INVESTIGATE:
{chr(10).join(f"• {controversy}" for controversy in relevant_controversies)}

TASK: Identify which of these field-specific controversies this paper touches on, and find EXACT TECHNICAL DETAILS that experts would fiercely debate.

REQUIRED DEEP ANALYSIS:

**METHODOLOGICAL CONTROVERSIES:**
- [What specific methodological choices would experts in {field} strongly disagree about?]
- [Quote exact sentences where authors make controversial methodological decisions]
- [What alternative approaches would critics argue are superior and why?]

**STATISTICAL/EVIDENCE CONTROVERSIES:**
- [What specific statistical decisions would statisticians criticize?]
- [Quote exact numbers, sample sizes, significance levels that are problematic]
- [What statistical assumptions might be violated or questionable?]

**DOMAIN-SPECIFIC TECHNICAL DISPUTES:**
- [What technical claims would domain experts challenge based on field knowledge?]
- [What competing theories or methods in {field} would critics prefer?]
- [Quote specific technical details that contradict established practices]

**GENERALIZABILITY WARS:**
- [What population/setting limitations would experts exploit to attack generalizability?]
- [Quote exact experimental conditions that limit broader applicability]
- [What real-world contexts would this approach fail in?]

**REPRODUCIBILITY AMMUNITION:**
- [What critical implementation details are missing for replication?]
- [What computational/experimental details would make reproduction difficult?]
- [Quote specific places where methods are vague or underspecified]

For each controversy, provide:
1. EXACT QUOTE from paper
2. SPECIFIC technical criticism experts would make
3. ALTERNATIVE approaches critics would advocate
4. PRECISE numbers/details that support the criticism

Be brutally specific and technical. Think like an expert who lives and breathes this field."""
        
        return prompt
    
    def generate_multi_expert_analysis_prompt(self, claim: str, evidence_text: str, field: str) -> str:
        """Generate prompt simulating multiple expert perspectives on same evidence"""
        
        prompt = f"""You are conducting a multi-expert panel review of a specific research claim. Analyze this claim from FOUR different expert perspectives simultaneously.

SPECIFIC CLAIM TO ANALYZE:
"{claim}"

EVIDENCE FROM PAPER:
{evidence_text[:3000]}

RESEARCH FIELD: {field}

MULTI-EXPERT ANALYSIS REQUIRED:

**THE STATISTICIAN'S PERSPECTIVE:**
{self.expert_personas["statistician"]}

Statistical Analysis:
- [Exact statistical issues with this claim - quote specific numbers]
- [What statistical tests/procedures are missing or inadequate?]
- [Specific power analysis, effect size, or significance problems]
- [Exact alternative statistical approaches that should have been used]

**THE METHODOLOGIST'S PERSPECTIVE:**
{self.expert_personas["methodologist"]}

Methodological Analysis:
- [Specific experimental design flaws that undermine this claim]
- [What confounding variables or biases are not controlled for?]
- [Exact procedural choices that introduce systematic error]
- [Alternative experimental designs that would be more rigorous]

**THE DOMAIN EXPERT'S PERSPECTIVE:**
{self.expert_personas["domain_expert"]}

Field-Specific Analysis:
- [How does this claim compare to established knowledge in {field}?]
- [What competing theories or prior work contradicts this claim?]
- [Specific technical aspects that domain experts would question]
- [Exact precedents in the field that support or refute this approach]

**THE REPLICATION EXPERT'S PERSPECTIVE:**
{self.expert_personas["replication_expert"]}

Reproducibility Analysis:
- [What specific details are missing for replication of this claim?]
- [Exact experimental parameters that need clarification]
- [What computational/technical barriers would prevent reproduction?]
- [Specific ways this claim could fail when others attempt replication]

For each expert perspective, provide:
1. EXACT QUOTES from the evidence that support their concerns
2. SPECIFIC technical objections with precise details
3. QUANTITATIVE criticism (exact numbers, measurements, parameters)
4. CONCRETE alternative approaches they would recommend

Make each expert perspective distinctly technical and adversarial - these experts should find different types of flaws and have heated disagreements."""
        
        return prompt
    
    def generate_technical_deep_dive_prompt(self, section_content: str, field: str) -> str:
        """Generate prompt for extracting maximum technical depth"""
        
        prompt = f"""You are a technical expert in {field} conducting the most detailed possible analysis of methodology and implementation.

PAPER SECTION CONTENT:
{section_content[:4000]}

EXTRACT MAXIMUM TECHNICAL DEPTH:

**ALGORITHMIC SPECIFICATIONS:**
- [Exact algorithm names, mathematical formulations, pseudocode mentioned]
- [Specific parameter values, hyperparameters, configuration details]
- [Precise computational complexity analysis or performance characteristics]
- [Exact optimization procedures, convergence criteria, stopping conditions]

**EXPERIMENTAL PRECISION:**
- [Exact sample sizes, group assignments, randomization procedures]
- [Specific measurement instruments, scales, validation procedures used]
- [Precise data collection protocols, timing, environmental controls]
- [Exact statistical analysis procedures with all parameter settings]

**IMPLEMENTATION GRANULARITY:**
- [Specific software versions, hardware specifications, computational environments]
- [Exact preprocessing steps, data cleaning procedures, transformation methods]
- [Precise evaluation metrics with exact mathematical definitions]
- [Specific baseline implementations and comparison procedures]

**NUMERICAL PRECISION:**
- [All exact numbers: means, standard deviations, confidence intervals]
- [Specific p-values, effect sizes, statistical test results]
- [Precise performance measurements with error bars and significance tests]
- [Exact sample characteristics: demographics, inclusion criteria, attrition rates]

**METHODOLOGICAL CHOICES:**
- [Specific justifications for methodological decisions made]
- [Alternative approaches that were considered and rejected (with reasons)]
- [Exact control variables, covariates, matching procedures used]
- [Precise randomization, blinding, or control group procedures]

**LIMITATION SPECIFICATIONS:**
- [Exact scope limitations with specific population/context restrictions]
- [Precise technical limitations with specific failure modes or edge cases]
- [Specific generalizability constraints with exact boundary conditions]
- [Exact computational or practical constraints that limit applicability]

For each technical detail, extract:
1. EXACT NUMBERS and precise specifications
2. SPECIFIC methodological choices with their justifications
3. PRECISE comparison points and evaluation criteria
4. EXACT limitations and scope restrictions

Be obsessively detailed. Extract every single number, specification, and technical choice that an expert would need to evaluate or reproduce this work."""
        
        return prompt
    
    def generate_evidence_strength_assessment_prompt(self, claim: str, supporting_evidence: List[str], 
                                                   contradictory_evidence: List[str], field: str) -> str:
        """Generate prompt for rigorous evidence strength assessment"""
        
        prompt = f"""You are a senior peer reviewer for a top-tier {field} journal conducting the most rigorous possible evidence evaluation.

CLAIM TO EVALUATE:
"{claim}"

SUPPORTING EVIDENCE:
{chr(10).join(f"• {evidence}" for evidence in supporting_evidence[:5])}

CONTRADICTORY EVIDENCE:
{chr(10).join(f"• {evidence}" for evidence in contradictory_evidence[:5])}

RIGOROUS EVIDENCE STRENGTH ASSESSMENT:

**STATISTICAL EVIDENCE STRENGTH:**
- [Exact statistical power and effect size analysis]
- [Specific sample size adequacy for the claimed effect]
- [Precise confidence interval interpretation and practical significance]
- [Exact multiple comparisons and statistical assumption violations]
Grade: [VERY_STRONG/STRONG/MODERATE/WEAK/VERY_WEAK] with quantitative justification

**METHODOLOGICAL EVIDENCE STRENGTH:**
- [Specific experimental design adequacy for causal claims]
- [Exact control group appropriateness and confounding variable control]
- [Precise measurement validity and reliability assessment]
- [Specific randomization and blinding adequacy]
Grade: [VERY_STRONG/STRONG/MODERATE/WEAK/VERY_WEAK] with methodological justification

**REPLICATION EVIDENCE STRENGTH:**
- [Exact reproducibility likelihood based on methodological detail]
- [Specific missing details that would prevent replication]
- [Precise generalizability assessment across populations/settings]
- [Exact robustness to alternative analytical approaches]
Grade: [VERY_STRONG/STRONG/MODERATE/WEAK/VERY_WEAK] with reproducibility justification

**DOMAIN-SPECIFIC EVIDENCE STRENGTH:**
- [How this evidence compares to field standards and established knowledge]
- [Specific precedents that support or contradict this evidence pattern]
- [Exact theoretical consistency with established {field} principles]
- [Specific practical implications and real-world validation potential]
Grade: [VERY_STRONG/STRONG/MODERATE/WEAK/VERY_WEAK] with domain-specific justification

**OVERALL EVIDENCE INTEGRATION:**
- [Exact evidence convergence analysis - do multiple lines of evidence align?]
- [Specific evidence gaps that weaken the overall case]
- [Precise weighing of supporting vs contradictory evidence strength]
- [Exact alternative explanations that could account for the evidence pattern]

FINAL EVIDENCE STRENGTH: [VERY_STRONG/STRONG/MODERATE/WEAK/VERY_WEAK]

SPECIFIC DEBATE POINTS FOR EXPERTS:
Optimist Arguments: [3 specific, technical points an optimist could make with exact evidence]
Skeptic Arguments: [3 specific, technical points a skeptic could make with exact counter-evidence]
Unresolved Technical Questions: [3 specific questions that would require additional research]

Provide exact numerical reasoning and technical specifications for all assessments."""
        
        return prompt
    
    def generate_comparative_analysis_prompt(self, paper_content: str, field: str) -> str:
        """Generate prompt for comparing to field standards and competing approaches"""
        
        prompt = f"""You are a world expert in {field} with encyclopedic knowledge of the field's methods, standards, and competing approaches.

PAPER CONTENT:
{paper_content[:4000]}

COMPARATIVE FIELD ANALYSIS:

**COMPARISON TO FIELD STANDARDS:**
- [How does this methodology compare to gold-standard approaches in {field}?]
- [What are the established benchmarks/baselines in this area and how does this compare?]
- [Specific ways this approach deviates from accepted best practices]
- [Exact performance metrics compared to field-standard evaluation criteria]

**COMPETING APPROACHES ANALYSIS:**
- [What are the 3-5 main competing methods/theories in this specific area?]
- [Exactly how would each competing approach handle this problem differently?]
- [Specific advantages/disadvantages of this approach vs each major alternative]
- [Precise performance comparisons where available in the literature]

**HISTORICAL CONTEXT:**
- [What previous landmark papers in {field} does this build upon or contradict?]
- [Specific evolution of methods in this area - where does this fit?]
- [Exact ways this represents genuine novelty vs incremental improvement]
- [Particular failed approaches from field history that this resembles]

**CURRENT CONTROVERSY POSITIONING:**
- [What ongoing debates in {field} does this paper take sides on?]
- [Specific controversial positions this paper implicitly or explicitly adopts]
- [Exact ways this approach would be criticized by different schools of thought]
- [Particular methodological camps that would strongly oppose this approach]

**PRACTICAL IMPLEMENTATION COMPARISON:**
- [How does the computational/practical complexity compare to alternatives?]
- [Specific scalability advantages/disadvantages vs competing approaches]
- [Exact resource requirements (data, computation, expertise) vs alternatives]
- [Particular real-world deployment challenges vs established methods]

For each comparison, provide:
1. EXACT technical specifications of how approaches differ
2. SPECIFIC performance/outcome differences with numbers where possible
3. PRECISE advantages/disadvantages for each approach
4. CONCRETE examples of where each approach succeeds/fails

Generate ammunition for debates between proponents of different approaches."""
        
        return prompt
    
    def get_expert_persona_prompt(self, expert_type: str) -> str:
        """Get specific expert persona prompt"""
        return self.expert_personas.get(expert_type, self.expert_personas["domain_expert"])


# Example usage and testing
def test_expert_prompts():
    """Test the expert-level prompt generation"""
    
    prompts = ExpertDeepPrompts()
    
    # Test field-specific controversy prompt
    sample_field = "Machine Learning - Computer Vision"
    sample_content = "We propose a novel deep learning architecture that achieves 95% accuracy on ImageNet classification..."
    
    controversy_prompt = prompts.generate_field_specific_controversy_prompt(sample_field, sample_content)
    
    print("🔬 FIELD-SPECIFIC CONTROVERSY PROMPT:")
    print("=" * 60)
    print(controversy_prompt[:1000] + "...")
    
    # Test multi-expert analysis
    sample_claim = "Our method achieves 95% accuracy with statistical significance p<0.001"
    sample_evidence = "We tested on 1000 samples with cross-validation showing mean accuracy 95.2% ± 2.1%"
    
    multi_expert_prompt = prompts.generate_multi_expert_analysis_prompt(sample_claim, sample_evidence, sample_field)
    
    print("\n👥 MULTI-EXPERT ANALYSIS PROMPT:")
    print("=" * 60) 
    print(multi_expert_prompt[:1000] + "...")


if __name__ == "__main__":
    test_expert_prompts()
