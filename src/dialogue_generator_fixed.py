# src/dialogue_generator_fixed.py
"""FIXED Dialogue Generator that actually uses Phase 1 analysis results"""

import requests
import json
from typing import Dict, List, Tuple, Any
from personalities import ResearchPersonalities, PersonalityProfile
from dataclasses import dataclass


@dataclass
class ConversationTurn:
    """Represents one turn in the conversation"""
    speaker: str
    speaker_role: str
    content: str
    topic: str
    turn_number: int


@dataclass
class ConversationScript:
    """Complete conversation script"""
    title: str
    paper_topic: str
    introduction: str
    turns: List[ConversationTurn]
    conclusion: str
    total_turns: int
    duration_estimate: str


class FixedDialogueEngine:
    """FIXED dialogue generator that uses Phase 1 results"""
    
    def __init__(self, model_name: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        self.personalities = ResearchPersonalities()
        
    def _call_ollama(self, prompt: str, max_length: int = 300) -> str:
        """Call Ollama API for dialogue generation"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": max_length
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            return f"[Error generating response: {str(e)}]"
    
    def generate_introduction(self, paper_summary: Dict[str, Any]) -> str:
        """Generate paper-specific introduction"""
        
        main_topic = paper_summary.get('main_topic', 'Research paper').strip()
        key_finding = paper_summary.get('key_finding', 'Novel research findings').strip()
        
        intro_prompt = f"""
Generate a brief, engaging podcast introduction for THIS SPECIFIC research paper discussion.

SPECIFIC PAPER DETAILS:
Topic: {main_topic}
Key Finding: {key_finding}

Create a 2-3 sentence introduction that:
- Welcomes listeners to "Research Rundown"
- Mentions the SPECIFIC paper topic (community detection, WCC, CM algorithms, Chapel, etc.)
- Sets up debate between optimistic and skeptical researchers
- Sounds natural and engaging
- Uses the ACTUAL paper content, not generic research terms

Introduction:"""

        return self._call_ollama(intro_prompt, max_length=200)
    
    def generate_conversation_starter(self, topic: Dict[str, str], 
                                    paper_context: str) -> Tuple[str, str]:
        """Generate opening statements using ACTUAL paper content"""
        
        question = topic.get('question', 'Research methodology')
        optimist_view = topic.get('optimist_view', '')
        skeptic_view = topic.get('skeptic_view', '')
        
        # FORCE the AI to use specific paper content
        optimist_prompt = f"""
You are Dr. Sarah Chen, the enthusiastic researcher, discussing THIS SPECIFIC RESEARCH PAPER.

PAPER CONTEXT: {paper_context}
DISCUSSION TOPIC: {question}
YOUR PERSPECTIVE: {optimist_view}

CRITICAL: You must discuss the ACTUAL paper content - mention specific details like:
- WCC (Well-Connected Components) and CM (Connectivity Modifier) algorithms  
- Chapel programming language
- Community detection in large-scale networks
- Performance improvements on billion-edge graphs
- Real datasets (Bitcoin, OpenAlex, CEN)

Do NOT talk about generic topics like "machine learning" or "computational biology" - stick to THIS paper's content.

Respond as Dr. Sarah Chen with enthusiasm about THIS specific research (2-3 sentences):
"""
        
        optimist_opening = self._call_ollama(optimist_prompt, max_length=250)
        
        # Generate skeptic response to the optimist's specific opening
        skeptic_prompt = f"""
You are Prof. Marcus Webb, the critical analyst, responding to Dr. Sarah Chen's statement.

PAPER CONTEXT: {paper_context}
DISCUSSION TOPIC: {question}
DR. CHEN JUST SAID: "{optimist_opening}"
YOUR PERSPECTIVE: {skeptic_view}

Respond with skeptical analysis of the SPECIFIC points Dr. Chen raised. Focus on:
- Methodological concerns about WCC/CM algorithms
- Questions about Chapel language choice
- Limitations of testing on only 3 datasets (Bitcoin, OpenAlex, CEN)
- Skepticism about performance claims

Stay focused on THIS paper's content, not generic research issues.

Prof. Marcus Webb's response (2-3 sentences):
"""
        
        skeptic_response = self._call_ollama(skeptic_prompt, max_length=250)
        
        return optimist_opening, skeptic_response
    
    def generate_follow_up_exchange(self, topic: str, previous_exchange: List[ConversationTurn],
                                  paper_context: str, current_speaker: str) -> str:
        """Generate follow-up using ACTUAL paper details"""
        
        # Get recent context
        recent_context = ""
        if previous_exchange:
            last_turns = previous_exchange[-2:]
            for turn in last_turns:
                recent_context += f"{turn.speaker}: {turn.content}\n"
        
        last_statement = previous_exchange[-1].content if previous_exchange else ""
        
        # FORCE use of specific paper content
        response_prompt = f"""
You are {"Dr. Sarah Chen (optimistic)" if current_speaker == "optimist" else "Prof. Marcus Webb (skeptical)"}.

PAPER CONTEXT: {paper_context}
TOPIC: {topic}
PREVIOUS STATEMENT: "{last_statement}"

CRITICAL: Respond to the previous statement about THIS SPECIFIC PAPER. You must mention:
- WCC and CM algorithms specifically
- Chapel programming language 
- Community detection in networks
- Performance results on billion-edge graphs
- Specific datasets (Bitcoin, OpenAlex, CEN)

Do NOT use generic research terms. Reference the ACTUAL paper content.

{"Dr. Sarah Chen" if current_speaker == "optimist" else "Prof. Marcus Webb"}'s response (2-3 sentences):
"""
        
        return self._call_ollama(response_prompt, max_length=250)
    
    def create_full_conversation(self, analysis_results: Dict[str, Any], 
                               max_topics: int = 3, 
                               exchanges_per_topic: int = 3) -> ConversationScript:
        """Generate conversation using ACTUAL Phase 1 analysis results"""
        
        print("🎬 Generating conversation using ACTUAL paper analysis...")
        
        # Extract SPECIFIC data from Phase 1 analysis
        paper_summary = analysis_results.get('summary', {})
        discussion_topics = analysis_results.get('detailed_discussion_topics', [])
        
        # Validate we have the right data
        main_topic = paper_summary.get('main_topic', '')
        print(f"📋 Using paper topic: {main_topic}")
        
        if 'community detection' not in main_topic.lower() and 'WCC' not in str(discussion_topics):
            print("⚠️  WARNING: Phase 1 data doesn't seem paper-specific!")
        
        # Use actual paper discussion topics
        topics_to_discuss = discussion_topics[:max_topics]
        print(f"🎯 Will discuss {len(topics_to_discuss)} paper-specific topics")
        
        # Create detailed paper context with SPECIFIC content
        paper_context = f"""
        SPECIFIC PAPER DETAILS:
        Topic: {paper_summary.get('main_topic', 'Community detection research')}
        Key Finding: {paper_summary.get('key_finding', 'Novel WCC/CM algorithms')}
        Method: {paper_summary.get('method', 'Chapel programming language implementation')}
        
        IMPORTANT: This paper is about WCC and CM algorithms for community detection, 
        implemented in Chapel programming language, tested on Bitcoin/OpenAlex/CEN datasets.
        NOT about machine learning, computational biology, or disease diagnosis.
        """
        
        # Generate paper-specific introduction
        print("📝 Generating paper-specific introduction...")
        introduction = self.generate_introduction(paper_summary)
        
        # Generate conversation turns
        turns = []
        turn_number = 1
        
        for topic_idx, topic in enumerate(topics_to_discuss):
            print(f"💬 Topic {topic_idx + 1}: {topic['question'][:50]}...")
            
            # Generate opening exchange using ACTUAL paper content
            optimist_opening, skeptic_response = self.generate_conversation_starter(
                topic, paper_context
            )
            
            # Add optimist opening
            optimist_personality = self.personalities.get_personality("optimist")
            turns.append(ConversationTurn(
                speaker=optimist_personality.name,
                speaker_role=optimist_personality.role,
                content=optimist_opening,
                topic=topic['question'],
                turn_number=turn_number
            ))
            turn_number += 1
            
            # Add skeptic response
            skeptic_personality = self.personalities.get_personality("skeptic")
            turns.append(ConversationTurn(
                speaker=skeptic_personality.name,
                speaker_role=skeptic_personality.role,
                content=skeptic_response,
                topic=topic['question'],
                turn_number=turn_number
            ))
            turn_number += 1
            
            # Generate follow-up exchanges using paper content
            current_speaker = "optimist"
            
            for exchange in range(exchanges_per_topic - 1):
                follow_up = self.generate_follow_up_exchange(
                    topic['question'], turns, paper_context, current_speaker
                )
                
                personality = self.personalities.get_personality(current_speaker)
                turns.append(ConversationTurn(
                    speaker=personality.name,
                    speaker_role=personality.role,
                    content=follow_up,
                    topic=topic['question'],
                    turn_number=turn_number
                ))
                turn_number += 1
                
                current_speaker = "skeptic" if current_speaker == "optimist" else "optimist"
        
        # Generate paper-specific conclusion
        print("🏁 Generating paper-specific conclusion...")
        conclusion_prompt = f"""
Generate a brief conclusion for a podcast discussion about THIS SPECIFIC PAPER:

Paper: {paper_summary.get('main_topic', 'Community detection research')}
Topics discussed: WCC algorithms, CM algorithms, Chapel programming, community detection

Create a 2-3 sentence conclusion that:
- Summarizes the debate about WCC/CM algorithms and Chapel implementation
- Thanks listeners
- Mentions the specific research area (community detection, not generic topics)

Conclusion:
"""
        
        conclusion = self._call_ollama(conclusion_prompt, max_length=200)
        
        # Calculate duration
        total_words = sum(len(turn.content.split()) for turn in turns)
        total_words += len(introduction.split()) + len(conclusion.split())
        duration_minutes = max(1, total_words // 150)
        
        # Use ACTUAL paper topic for title
        actual_topic = paper_summary.get('main_topic', 'Community Detection Research')
        
        script = ConversationScript(
            title=f"Research Rundown: {actual_topic[:60]}",
            paper_topic=actual_topic,
            introduction=introduction,
            turns=turns,
            conclusion=conclusion,
            total_turns=len(turns),
            duration_estimate=f"~{duration_minutes} minutes"
        )
        
        print(f"✅ Generated {len(turns)} turns about ACTUAL paper content")
        return script
    
    def format_script_for_display(self, script: ConversationScript) -> str:
        """Format the conversation script for readable display"""
        
        output = []
        output.append("🎙️  " + "=" * 60)
        output.append(f"📻 {script.title}")
        output.append(f"⏱️  Estimated Duration: {script.duration_estimate}")
        output.append("🎙️  " + "=" * 60)
        
        # Introduction
        output.append(f"\n🎬 INTRODUCTION:")
        output.append(f"{script.introduction}")
        
        # Conversation turns
        output.append(f"\n💬 CONVERSATION:")
        output.append("-" * 50)
        
        current_topic = ""
        for turn in script.turns:
            if turn.topic != current_topic:
                current_topic = turn.topic
                output.append(f"\n🎯 Topic: {current_topic}")
                output.append("-" * 30)
            
            speaker_emoji = "😊" if "Sarah" in turn.speaker else "🤨"
            output.append(f"\n{speaker_emoji} **{turn.speaker}**: {turn.content}")
        
        # Conclusion
        output.append(f"\n\n🏁 CONCLUSION:")
        output.append(f"{script.conclusion}")
        
        output.append(f"\n📊 STATISTICS:")
        output.append(f"   • Total turns: {script.total_turns}")
        output.append(f"   • Estimated duration: {script.duration_estimate}")
        
        return "\n".join(output)
    
    def test_connection(self) -> bool:
        """Test if Ollama is available"""
        try:
            test_response = self._call_ollama("Hello", max_length=10)
            return len(test_response) > 5 and "Error" not in test_response
        except:
            return False
