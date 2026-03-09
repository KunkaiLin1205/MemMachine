"""Prompt template for life-oriented personal context semantic memory extraction.

This prompt focuses on extracting personal characteristics, interests, lifestyle patterns,
goals, and life context that help provide personalized life guidance and advice.
This complements structured facts extraction by focusing on personal insights rather than concrete data.
"""

from memmachine.semantic_memory.semantic_model import (
    RawSemanticPrompt,
    SemanticCategory,
)
from memmachine.semantic_memory.util.semantic_prompt_template import (
    build_update_prompt,
)

# Life-oriented personal context tags
life_context_tags: dict[str, str] = {
    "interests": "Long-term interests and hobbies: what the user enjoys doing, passions, recreational activities, creative pursuits, learning interests, entertainment preferences, cultural interests, and things the user likes to do in their free time.",
    "lifestyle": "Stable lifestyle patterns and habits: daily routines, sleep patterns, exercise habits, dietary habits, work-life balance approach, stress management techniques, leisure activities, and time management style.",
    "goals": "Long-term goals and aspirations: career goals, personal development goals, health and fitness goals, financial goals, relationship goals, educational goals, life vision, and desired achievements.",
    "personality": "Stable personality traits and characteristics: communication style, decision-making style, introversion/extroversion, openness to new experiences, conscientiousness, emotional stability, and how the user typically interacts with others.",
    "life_situation": "Stable life circumstances and context: permanent living situation (city/region), family structure, work situation (job/career), major life stage, and long-term commitments.",
}

# Optimized description for life-oriented personal context
life_context_description = """
    You are a PERSONAL INSIGHT EXTRACTOR for a life advisor assistant. Extract deep personal 
    understanding that enables meaningful life guidance and personalized advice.
    
    ## YOUR ROLE
    
    Extract:
    - WHY and HOW the user thinks, feels, and behaves (motivations, patterns, characteristics)
    - Personal insights, values, goals, and life context
    - Psychological profile and life understanding
    
    Do NOT Extract:
    - WHAT the user has (facts, data, contact info, account numbers) → task_assistant_prompt
    - Historical events or temporary states → episodic memory
    
    Think of yourself as: Building a psychological profile, not a contact book.
    
    Important: Semantic memory is for STABLE, REUSABLE information.
    ALWAYS compare with existing features before creating new ones.
    
    ## TAG RULES
    
    Only use: interests, lifestyle, goals, personality, life_situation
    - interests: hobbies, passions, entertainment preferences
    - lifestyle: routines, habits, work-life balance
    - goals: aspirations, objectives, plans
    - personality: character traits, behavioral patterns
    - life_situation: circumstances, context
    
    ## WHAT TO EXTRACT
    
    - Interests: hobbies, passions, creative pursuits, learning interests, entertainment
    - Lifestyle: daily routines, sleep patterns, exercise habits, dietary habits
    - Goals: career aspirations, personal development, health goals, life vision
    - Personality: communication style, decision-making, introversion/extroversion
    - Life situation: living situation (city/region), family structure, work situation
    - Values: core values, priorities, what drives decisions
    
    Key Question: "Will this still be accurate in 6 months?" If YES → extract. If NO → skip.
    
    ## WHAT NOT TO EXTRACT
    
    ### Temporary/Transient Information (belongs in episodic memory)
    - Current location, travel status, temporary residence (hotels, Airbnbs)
    - Historical events, past actions, current projects or tasks
    - Temporary moods, situational feelings, context-dependent choices
    
    ### Structured Facts (belongs in task_assistant_prompt)
    - Contact info (phone, email), IDs, account numbers
    - Service provider contact details
    
    ### Highly Sensitive PII (never store for security)
    - Government IDs: SSN, passport numbers, driver's license numbers
    - Financial: credit card numbers, bank account numbers
    - Security: passwords, PINs, authentication credentials
    - Private records: medical records, financial records, legal documents
    
    ## FEATURE NAMING RULES
    
    ### Format
    - UPPERCASE with SPACES (e.g., "PRIMARY INTEREST", "CAREER GOAL")
    - Full words, not abbreviations
    - Be descriptive and meaningful
    
    ### Standard Names by Tag
    
    **Interests:** "PRIMARY INTEREST", "SECONDARY INTEREST", "PASSION"
    - Multiple: "INTEREST PHOTOGRAPHY", "INTEREST COOKING"
    
    **Lifestyle:** "WORK LIFE BALANCE STYLE", "EXERCISE HABIT", "SLEEP PATTERN", "DIETARY HABIT", "DAILY ROUTINE"
    - Multiple: "ROUTINE MORNING", "ROUTINE EVENING"
    
    **Goals:** "CAREER GOAL", "HEALTH GOAL", "FINANCIAL GOAL", "PERSONAL DEVELOPMENT GOAL", "LIFE VISION"
    - Multiple: "CAREER GOAL PRIMARY", "CAREER GOAL SECONDARY"
    
    **Personality:** "COMMUNICATION STYLE", "DECISION MAKING STYLE", "SOCIAL PREFERENCE", "EMOTIONAL PATTERN"
    
    **Life Situation:** "CURRENT LIFE STAGE", "CORE VALUE", "FAMILY SITUATION", "WORK SITUATION"
    - Multiple: "CORE VALUE FAMILY", "CORE VALUE CAREER"
    
    ## HANDLING DUPLICATES AND UPDATES
    
    Before adding or updating:
    1. Compare with existing features
    2. Analyze if it's the same or different information
    
    ### Decision Rules
    - SAME information: OVERWRITE using UPDATE
    - DIFFERENT information: Create new with different suffix
    
    Example: Existing "CAREER GOAL" is "become a manager", new claim is "start a side business"
    → Keep "CAREER GOAL" and ADD "CAREER GOAL ENTREPRENEURIAL"
    
    ## EXTRACTION PROCESS
    
    1. Compare with existing features to identify duplicates
    2. Select correct tag (DO NOT create new tags)
    3. Use standard feature names
    4. For duplicates: same info → UPDATE, different info → create with suffix
    5. Extract INSIGHTS and UNDERSTANDING, not just facts
    6. Look for underlying motivations, values, and personality traits
    
    Priority: personality/life_situation > goals > lifestyle > interests
"""

# Custom consolidation prompt for life-oriented personal context
life_context_consolidation_prompt = """
    You are performing memory consolidation for a life-oriented personal context memory system.
    Consolidation minimizes interference between personal insights while maintaining psychological profile integrity.

    ## INPUT/OUTPUT FORMAT

    ### Input Memory
    ```json
    {"tag": "string", "feature": "string", "value": "string", "metadata": {"id": integer}}
    ```

    ### Output Memory
    ```json
    {"tag": "string", "feature": "string", "value": "string", "metadata": {"citations": [list of ids]}}
    ```

    ## RULES

    ### Tags
    Only use: interests, lifestyle, goals, personality, life_situation

    ### Feature Names
    - UPPERCASE with SPACES (e.g., "PRIMARY INTEREST", "CAREER GOAL")
    - Use suffixes for multiple items: "INTEREST PHOTOGRAPHY", "INTEREST COOKING"
    - Standard names:
      - Interests: "PRIMARY INTEREST", "SECONDARY INTEREST", "PASSION"
      - Lifestyle: "EXERCISE HABIT", "SLEEP PATTERN", "DIETARY HABIT"
      - Goals: "CAREER GOAL", "HEALTH GOAL", "FINANCIAL GOAL", "LIFE VISION"
      - Personality: "COMMUNICATION STYLE", "DECISION MAKING STYLE", "SOCIAL PREFERENCE"
      - Life Situation: "CURRENT LIFE STAGE", "CORE VALUE", "FAMILY SITUATION"

    ## CONSOLIDATION GUIDELINES

    ### 0. DELETE FIRST (Highest Priority)

    **Highly Sensitive PII - DELETE:**
    - SSN, passport numbers, driver's license numbers
    - Credit card/bank account numbers
    - Passwords, PINs, credentials
    - Medical records, financial records, legal documents

    **Temporary Information - DELETE:**
    - "CURRENT LOCATION", "USER LOCATION", "STAYING AT"
    - Airbnb addresses, hotel rooms, current trips
    - Time-bound information, current projects
    - ASK: "Will this still be true in 6 months?" If NO → DELETE

    ### 1. Identical Information
    DELETE duplicates, KEEP only one

    ### 2. Evolution vs Different Items
    - Evolution/refinement: KEEP most complete/current version
    - Different items: UPDATE feature names with suffixes

    Example (Evolution): "CAREER GOAL": "become a manager" → "become a senior manager"
    → Keep "become a senior manager"

    Example (Different): "PRIMARY INTEREST": "photography" and "cooking"
    → Keep "INTEREST PHOTOGRAPHY" and "INTEREST COOKING"

    ### 3. Synonyms
    Consolidate to standard feature name ("MAIN HOBBY" → "PRIMARY INTEREST")

    ### 4. Redundant Information
    DELETE incomplete versions, KEEP complete ones

    ### 5. Multiple Items
    Use consistent suffixes. Don't create suffixes until you have 2+ distinct items.

    ## AGGRESSIVE DELETION

    More memories = more interference = more cognitive load.
    Be aggressive: some distinctions aren't worth maintaining. Delete ruthlessly.

    ## OUTPUT FORMAT

    CRITICAL: Both fields MUST be arrays. NEVER use null/None for any field.

    ### Output Schema
    ```
    <think> your reasoning </think>
    {"consolidated_memories": [...], "keep_memories": [...]}
    ```

    ### Field Descriptions

    **keep_memories** (REQUIRED - must be an array, never null):
    - List of metadata.id values (as strings) for memories to KEEP unchanged
    - Use empty array [] to delete ALL input memories
    - Example: ["123", "456"] keeps memories with those IDs

    **consolidated_memories** (REQUIRED - must be an array, never null):
    - List of NEW memories to create after consolidation
    - Each memory has: {"tag": "...", "feature": "...", "value": "..."}
    - Use empty array [] if no new memories needed

    ### Examples

    Keep distinct items unchanged:
    {"consolidated_memories": [], "keep_memories": ["1", "2"]}

    Merge duplicates into one:
    {"consolidated_memories": [{"tag": "interests", "feature": "INTEREST PHOTOGRAPHY", "value": "User enjoys photography as a hobby"}], "keep_memories": []}

    Delete temporary/sensitive data:
    {"consolidated_memories": [], "keep_memories": []}

    Keep all unchanged:
    {"consolidated_memories": [], "keep_memories": ["1", "2", "3"]}
"""

LifeContextSemanticCategory = SemanticCategory(
    name="profile_life_context",
    prompt=RawSemanticPrompt(
        update_prompt=build_update_prompt(
        tags=life_context_tags,
        description=life_context_description,
        ),
        consolidation_prompt=life_context_consolidation_prompt,
    ),
)

SEMANTIC_TYPE = LifeContextSemanticCategory
