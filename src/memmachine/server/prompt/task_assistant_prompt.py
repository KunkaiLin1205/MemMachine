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
    You are extracting personal context and characteristics from conversations with a life advisor assistant.
    This information helps provide personalized life guidance, understand user's goals, values, and constraints,
    and offer meaningful advice across sessions.
    
    IMPORTANT CONTEXT:
    - Episodic memories already contain refined descriptions and atomic claims, including all historical events and temporary states
    - Semantic memory is for STABLE, REUSABLE user information that persists across sessions
    - Structured facts (contacts, accounts, identities) are extracted separately by task_facts_prompt
    - Your job is to extract personal characteristics that help the agent:
      * Provide personalized life advice and recommendations
      * Understand the user's context, goals, values, and constraints
      * Recognize patterns in user's interests, lifestyle, and personality
      * Offer meaningful guidance based on user's life situation
    
    EXTRACTION GUIDELINES:
    - Extract personal characteristics, interests, lifestyle patterns, goals, and life context
    - Focus on information that is STABLE and REUSABLE across sessions
    - Use descriptive feature names that capture the essence of the characteristic (e.g., "PRIMARY INTEREST", "WORK LIFE BALANCE STYLE", "CAREER GOAL", "COMMUNICATION STYLE")
    - Extract patterns and recurring themes that indicate life context
    - Include information that helps the agent understand the user deeply, not just complete tasks
    
    FEATURE NAMING GUIDELINES:
    - Use descriptive, meaningful feature names that capture the personal characteristic
    - Use UPPERCASE letters with SPACES between words (e.g., "PRIMARY INTEREST", "CAREER GOAL")
    - Be concise but clear - use full words, not abbreviations
    - Examples of good feature names:
      * "PRIMARY INTEREST" or "HOBBY" (not "INTEREST" or "LIKES")
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
    - Avoid generic names like "INFO", "DATA", "DETAIL" - be specific about the characteristic
    - For interests: use format like "PRIMARY INTEREST", "HOBBY", "PASSION"
    - For goals: use format like "CAREER GOAL", "HEALTH GOAL", "FINANCIAL GOAL"
    - For personality: use format like "COMMUNICATION STYLE", "DECISION MAKING STYLE", "INTROVERSION LEVEL"
    
    DO NOT EXTRACT (These belong in episodic memory, not semantic memory):
    - Historical events or past actions (e.g., "booked a flight on 2026-01-23", "visited Paris last summer")
    - Temporary states or pending actions (e.g., "flight_booking_pending", "waiting for payment")
    - One-time transactions or specific occurrences (e.g., "made a purchase", "called customer service")
    - Time-specific information that will become outdated (e.g., "currently traveling", "has a meeting tomorrow")
    - Travel history, booking history, transaction history, or any event-based information
    - Temporary preferences or context-dependent choices (e.g., "wants pizza today" vs. stable "prefers Italian food")
    - Structured facts like contact information, account numbers, identities (these are handled by task_facts_prompt)
    
    ONLY EXTRACT STABLE PERSONAL CHARACTERISTICS:
    - User's interests and hobbies that persist over time
    - Lifestyle patterns and habits (daily routines, exercise, sleep, work-life balance)
    - Goals and aspirations (career, personal development, health, financial)
    - Personality traits and characteristics (communication style, decision-making, introversion/extroversion)
    - Life situation and context (living situation, family structure, work situation, life stage)
    
    PRIORITIZE:
    1. Personal characteristics that affect life guidance (personality, life_situation)
    2. Goals and aspirations (goals)
    3. Lifestyle patterns and habits (lifestyle)
    4. Interests and hobbies (interests)
    
    Be thorough but precise. Extract characteristics that help the agent provide personalized
    life advice and understand the user deeply. Remember: if it's a one-time event or temporary
    state, it belongs in episodic memory, not semantic memory. Structured facts belong in task_facts_prompt.
"""

LifeContextSemanticCategory = SemanticCategory(
    name="profile_life_context",
    prompt=StructuredSemanticPrompt(
        tags=life_context_tags,
        description=life_context_description,
    ),
)

SEMANTIC_TYPE = LifeContextSemanticCategory
