# src/personalities.py
"""AI Personality System for Research Paper Debates"""

from typing import Dict, List, Any
from dataclasses import dataclass
import random


@dataclass
class PersonalityProfile:
    """Define an AI personality for paper debates"""
    name: str
    role: str
    expertise: List[str]
    personality_traits: List[str]
    speaking_style: str
    catchphrases: List[str]
    perspective: str
    favorite_questions: List[str]


class ResearchPersonalities:
    """Manage different AI research personalities"""
    
    def __init__(self):
        self.personalities = self._define_personalities()
    
    def _define_personalities(self) -> Dict[str, PersonalityProfile]:
        """Define the core research personalities"""
        
        return {
            "optimist": PersonalityProfile(
                name="Dr. Sarah Chen",
                role="The Enthusiastic Researcher",
                expertise=[
                    "Machine Learning", "Data Science", "Algorithm Development",
                    "Network Analysis", "Computational Biology", "AI Applications"
                ],
                personality_traits=[
                    "Optimistic about research potential",
                    "Focuses on breakthrough possibilities", 
                    "Emphasizes practical applications",
                    "Encourages innovation and risk-taking",
                    "Sees the bigger picture and future implications",
                    "Diplomatic but passionate about discoveries"
                ],
                speaking_style="Enthusiastic, explanatory, uses analogies, builds excitement",
                catchphrases=[
                    "This could be game-changing!",
                    "Think about the possibilities here...",
                    "What excites me most about this work is...",
                    "This opens up so many new directions!",
                    "The potential applications are endless!",
                    "Let me paint a picture of what this could mean..."
                ],
                perspective="Focuses on potential, applications, and positive implications",
                favorite_questions=[
                    "What new possibilities does this create?",
                    "How could this transform the field?", 
                    "What are the broader implications?",
                    "Where could we take this next?",
                    "What problems could this solve?"
                ]
            ),
            
            "skeptic": PersonalityProfile(
                name="Prof. Marcus Webb",
                role="The Critical Analyst", 
                expertise=[
                    "Research Methodology", "Statistical Analysis", "Experimental Design",
                    "Peer Review", "Scientific Rigor", "Meta-Analysis"
                ],
                personality_traits=[
                    "Methodologically rigorous",
                    "Questions assumptions and claims",
                    "Focuses on limitations and potential flaws",
                    "Values reproducibility and robustness",
                    "Skeptical of bold claims without solid evidence",
                    "Direct and precise in communication"
                ],
                speaking_style="Analytical, precise, asks probing questions, methodical",
                catchphrases=[
                    "Hold on, let's examine this more carefully...",
                    "I have serious concerns about...",
                    "The data doesn't quite support that conclusion...",
                    "We need to be more cautious here...",
                    "What about the limitations?",
                    "I'm not convinced that..."
                ],
                perspective="Focuses on methodology, limitations, and scientific rigor",
                favorite_questions=[
                    "How robust is this methodology?",
                    "What are the key limitations?",
                    "Can these results be reproduced?",
                    "Are the claims well-supported?",
                    "What could go wrong with this approach?"
                ]
            )
        }
    
    def get_personality(self, personality_type: str) -> PersonalityProfile:
        """Get a specific personality profile"""
        return self.personalities.get(personality_type)
    
    def get_speaking_prompt(self, personality_type: str, context: str, 
                          previous_exchange: str = "") -> str:
        """Generate a speaking prompt for a personality"""
        
        personality = self.get_personality(personality_type)
        if not personality:
            raise ValueError(f"Unknown personality type: {personality_type}")
        
        # Add some variety with random elements
        catchphrase = random.choice(personality.catchphrases)
        favorite_question = random.choice(personality.favorite_questions)
        
        prompt = f"""
You are {personality.name}, {personality.role}.

PERSONALITY TRAITS:
{chr(10).join(f"• {trait}" for trait in personality.personality_traits)}

EXPERTISE AREAS:
{chr(10).join(f"• {area}" for area in personality.expertise)}

SPEAKING STYLE: {personality.speaking_style}

PERSPECTIVE: {personality.perspective}

CONTEXT: {context}

{f"PREVIOUS EXCHANGE: {previous_exchange}" if previous_exchange else ""}

Respond as {personality.name} would, incorporating your personality naturally. 
Use your speaking style and perspective. You might naturally use phrases like "{catchphrase}" 
or ask questions like "{favorite_question}" when appropriate.

Keep your response to 2-3 sentences and stay in character. Be natural and conversational,
as if you're having a discussion with a colleague about this research.

{personality.name}'s response:"""
        
        return prompt
    
    def get_introduction_prompt(self, personality_type: str, paper_topic: str) -> str:
        """Generate an introduction prompt for a personality"""
        
        personality = self.get_personality(personality_type)
        
        prompt = f"""
You are {personality.name}, {personality.role}, introducing a research paper discussion.

PAPER TOPIC: {paper_topic}

Your task: Provide a brief, enthusiastic introduction to this paper from your perspective as {personality.name}.
- Keep it to 1-2 sentences
- Reflect your personality ({personality.perspective})
- Set the tone for your role in the discussion

{personality.name}'s introduction:"""
        
        return prompt
    
    def get_response_prompt(self, personality_type: str, topic: str, 
                          other_speaker_said: str, discussion_context: str) -> str:
        """Generate a response prompt for ongoing discussion"""
        
        personality = self.get_personality(personality_type)
        
        prompt = f"""
You are {personality.name}, {personality.role}.

DISCUSSION TOPIC: {topic}
RESEARCH CONTEXT: {discussion_context}

The other speaker just said: "{other_speaker_said}"

Respond as {personality.name} would:
- Stay true to your perspective: {personality.perspective}
- Use your speaking style: {personality.speaking_style}
- Reference specific aspects of the research when possible
- Keep response to 2-3 sentences
- Be conversational and natural

{personality.name}'s response:"""
        
        return prompt


class PersonalityTester:
    """Test personality responses"""
    
    def __init__(self):
        self.personalities = ResearchPersonalities()
    
    def test_personality_responses(self, context: str):
        """Test both personalities with sample context"""
        
        print("🎭 PERSONALITY SYSTEM TEST")
        print("=" * 50)
        print(f"Context: {context}")
        print()
        
        # Test both personalities
        for personality_type in ["optimist", "skeptic"]:
            personality = self.personalities.get_personality(personality_type)
            print(f"\n👤 {personality.name} ({personality.role}):")
            print(f"   Traits: {', '.join(personality.personality_traits[:2])}...")
            print(f"   Style: {personality.speaking_style}")
            print(f"   Perspective: {personality.perspective}")
            
            # Show sample prompt
            prompt = self.personalities.get_speaking_prompt(personality_type, context)
            print(f"\n📝 Sample prompt length: {len(prompt)} characters")
            print(f"   Example catchphrase: '{random.choice(personality.catchphrases)}'")
    
    def test_introduction_prompts(self, paper_topic: str):
        """Test introduction prompts"""
        
        print("\n🎬 INTRODUCTION PROMPTS TEST")
        print("=" * 50)
        
        for personality_type in ["optimist", "skeptic"]:
            personality = self.personalities.get_personality(personality_type)
            prompt = self.personalities.get_introduction_prompt(personality_type, paper_topic)
            
            print(f"\n👤 {personality.name} Introduction Prompt:")
            print("-" * 30)
            print(prompt)
    
    def test_response_prompts(self, topic: str, context: str):
        """Test response prompts"""
        
        print("\n💬 RESPONSE PROMPTS TEST") 
        print("=" * 50)
        
        sample_statement = "I think this methodology is quite robust and the results are impressive."
        
        for personality_type in ["optimist", "skeptic"]:
            personality = self.personalities.get_personality(personality_type)
            prompt = self.personalities.get_response_prompt(
                personality_type, topic, sample_statement, context
            )
            
            print(f"\n👤 {personality.name} Response Prompt:")
            print("-" * 30)
            print(prompt[:300] + "..." if len(prompt) > 300 else prompt)


def main():
    """Test the personality system"""
    
    # Sample research context
    context = """
    Research paper on optimized parallel implementations of Well-Connected Components (WCC) 
    and Connectivity Modifier (CM) algorithms for community detection in large-scale networks.
    The authors claim 23% performance improvement using Chapel's tasking model on billion-edge graphs.
    """
    
    paper_topic = "Optimized Parallel Implementations of WCC and CM Algorithms for Network Community Detection"
    
    tester = PersonalityTester()
    
    # Run tests
    tester.test_personality_responses(context)
    tester.test_introduction_prompts(paper_topic)
    tester.test_response_prompts("Algorithm Performance Claims", context)
    
    print(f"\n✅ Personality system ready!")
    print(f"Next: Integrate with dialogue generation engine")


if __name__ == "__main__":
    main()
