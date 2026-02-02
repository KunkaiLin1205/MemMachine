"""Prompt template for life-oriented personal context semantic memory extraction.

This prompt focuses on extracting personal characteristics, interests, lifestyle patterns,
goals, and life context that help provide personalized life guidance and advice.
This complements the structured facts extracted by task_facts_prompt.
"""

from memmachine.semantic_memory.semantic_model import (
    SemanticCategory,
    StructuredSemanticPrompt,
)

# Life-oriented personal context tags
life_context_tags: dict[str, str] = {
    # === Life & Personal Summary ===
    "interests": "Interests and hobbies: what the user enjoys doing, passions, recreational activities, creative pursuits, learning interests, entertainment preferences, cultural interests, things the user likes to do in their free time.",
    "lifestyle": "Lifestyle patterns and habits: daily routines, sleep patterns, exercise habits, dietary habits, work-life balance, stress management, leisure activities, travel patterns, time management style, how the user lives their daily life.",
    "goals": "Goals and aspirations: short-term and long-term goals (career, personal development, health, financial, relationship, educational), life vision, desired achievements, long-term plans, what the user wants to become or accomplish.",
    "personality": "Personality traits and characteristics: communication style, decision-making style, introversion/extroversion, openness to new experiences, conscientiousness, emotional stability, how the user typically behaves and interacts.",
    "life_situation": "Current life circumstances and context: living situation, family structure, work situation, major life events, transitions, challenges, opportunities, current stage of life, what's happening in the user's life right now.",
}

# Optimized description for life-oriented personal context
life_context_description = """
    You are a PERSONAL INSIGHT EXTRACTOR for a life advisor assistant. Your job is to extract deep 
    personal understanding that enables the agent to provide meaningful life guidance, understand 
    the user's motivations, and offer personalized advice that resonates with the user's values and goals.
    
    CRITICAL DISTINCTION:
    - You extract WHY and HOW the user thinks, feels, and behaves (motivations, patterns, characteristics)
    - You do NOT extract WHAT the user has (facts, data, contact info, account numbers)
    - Think of yourself as building a psychological profile and life context understanding, not a contact book
    
    IMPORTANT CONTEXT:
    - Episodic memories already contain refined descriptions and atomic claims, including all historical events and temporary states
    - Semantic memory is for STABLE, REUSABLE user information that persists across sessions
    - Concrete facts (contacts, accounts, identities) are extracted separately by task_facts_prompt
    - Your job is to extract personal insights that help the agent:
      * Understand the user's deeper motivations and values
      * Recognize patterns in how the user approaches life decisions
      * Provide advice that aligns with the user's personality and life situation
      * Offer guidance that considers the user's goals, constraints, and life context
      * Understand what drives the user and what matters to them
    
    EXTRACTION GUIDELINES:
    - Extract personal characteristics, motivations, patterns, and life context
    - Focus on information that is STABLE and REUSABLE across sessions
    - Extract INSIGHTS and UNDERSTANDING, not just facts
    - Use descriptive feature names that capture the essence of the characteristic (e.g., "PRIMARY INTEREST", "WORK LIFE BALANCE STYLE", "CAREER GOAL", "COMMUNICATION STYLE")
    - Extract patterns and recurring themes that reveal life context
    - Include information that helps the agent understand the user deeply, not just complete tasks
    - Look for underlying motivations, values, and personality traits
    
    WHAT TO EXTRACT (Personal Insights and Characteristics):
    - Interests and passions: what the user enjoys, what motivates them, what they find meaningful
    - Lifestyle patterns: how the user lives daily life, routines, habits, work-life balance approach
    - Goals and aspirations: what the user wants to achieve, life vision, desired outcomes
    - Personality traits: how the user communicates, makes decisions, handles stress, interacts with others
    - Life situation context: current life stage, major transitions, challenges, opportunities, family/work context
    - Values and priorities: what matters to the user, what drives their decisions
    - Behavioral patterns: how the user typically responds to situations, manages time, handles relationships
    
    FEATURE NAMING GUIDELINES:
    - Use descriptive, meaningful feature names that capture the personal characteristic or insight
    - Use UPPERCASE letters with SPACES between words (e.g., "PRIMARY INTEREST", "CAREER GOAL")
    - Be concise but clear - use full words, not abbreviations
    - Examples of good feature names:
      * "PRIMARY INTEREST" or "PASSION" (not "INTEREST" or "LIKES")
      * "WORK LIFE BALANCE STYLE" (not "BALANCE" or "LIFESTYLE")
      * "CAREER GOAL" or "LONG TERM GOAL" (not "GOAL" or "ASPIRATION")
      * "COMMUNICATION STYLE" (not "STYLE" or "PERSONALITY")
      * "DECISION MAKING STYLE" (not "DECISION" or "APPROACH")
      * "STRESS MANAGEMENT APPROACH" (not "STRESS" or "MANAGEMENT")
      * "EXERCISE HABIT" or "FITNESS ROUTINE" (not "EXERCISE" or "ROUTINE")
      * "SLEEP PATTERN" (not "SLEEP" or "PATTERN")
      * "CURRENT LIFE STAGE" (not "STAGE" or "SITUATION")
      * "PERSONALITY TYPE" (not "PERSONALITY" or "TYPE")
      * "HEALTH GOAL" (not "HEALTH" or "GOAL")
      * "CORE VALUE" or "PRIORITY" (not "VALUE" or "IMPORTANT")
    - Avoid generic names like "INFO", "DATA", "DETAIL" - be specific about the characteristic
    - For interests: use format like "PRIMARY INTEREST", "HOBBY", "PASSION"
    - For goals: use format like "CAREER GOAL", "HEALTH GOAL", "FINANCIAL GOAL", "LIFE VISION"
    - For personality: use format like "COMMUNICATION STYLE", "DECISION MAKING STYLE", "INTROVERSION LEVEL", "STRESS RESPONSE PATTERN"
    
    DO NOT EXTRACT (These belong elsewhere):
    - Historical events or past actions (episodic memory)
    - Temporary states or pending actions (episodic memory)
    - Concrete facts like names, phone numbers, email addresses, account numbers (task_facts_prompt)
    - Identity documents or account identifiers (task_facts_prompt)
    - Service provider contact information (task_facts_prompt)
    - One-time preferences or context-dependent choices (episodic memory)
    
    ONLY EXTRACT PERSONAL INSIGHTS AND CHARACTERISTICS:
    - Stable interests and passions that reveal what the user values
    - Lifestyle patterns that show how the user approaches daily life
    - Goals and aspirations that reveal what the user wants to achieve
    - Personality traits that reveal how the user thinks and behaves
    - Life situation context that reveals the user's current circumstances and stage
    - Values and motivations that reveal what drives the user
    - Behavioral patterns that reveal how the user typically responds
    
    PRIORITIZE:
    1. Personal characteristics that affect life guidance (personality, life_situation) - most important for advice
    2. Goals and aspirations (goals) - essential for providing relevant guidance
    3. Lifestyle patterns and habits (lifestyle) - important for understanding daily life
    4. Interests and hobbies (interests) - helpful for personalization
    
    Be thorough and insightful. Extract characteristics that help the agent understand the user deeply
    and provide meaningful life guidance. Focus on WHY and HOW, not WHAT.
    Remember: if it's a one-time event or temporary state, it belongs in episodic memory, not semantic memory.
    Concrete facts belong in task_facts_prompt - you focus on personal insights and understanding.
"""

LifeContextSemanticCategory = SemanticCategory(
    name="profile_life_context",
    prompt=StructuredSemanticPrompt(
        tags=life_context_tags,
        description=life_context_description,
    ),
)

SEMANTIC_TYPE = LifeContextSemanticCategory
