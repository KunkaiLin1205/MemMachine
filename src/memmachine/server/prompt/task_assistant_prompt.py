"""Prompt template for task-oriented structured facts semantic memory extraction.

This prompt focuses on extracting stable, structured facts needed for task completion:
contact information, account details, identities, preferences, relationships, and services.
These facts are typically listed at the beginning of a session for quick reference.
"""

from memmachine.semantic_memory.semantic_model import (
    SemanticCategory,
    StructuredSemanticPrompt,
)

# Task-oriented structured facts tags
task_assistant_tags: dict[str, str] = {
    # === Core Identity & Contact ===
    "basics": "Basic personal information: full name, date of birth, gender, age, marital status, education level, occupation, and other basic demographic information. IMPORTANT: If information belongs to someone other than the user (e.g., spouse's name, child's date of birth), include ownership in the feature name (e.g., 'SPOUSE FULL NAME', 'CHILD DATE OF BIRTH').",
    "contacts": "Contact information and addresses: phone numbers, email addresses, permanent addresses, mailing addresses, work addresses, emergency contacts. IMPORTANT: Always include ownership/relationship in feature names when the contact belongs to someone other than the user (e.g., 'SPOUSE EMAIL', 'CHILD PHONE NUMBER', 'EMERGENCY CONTACT PHONE'). For the user's own contacts, use standard names like 'EMAIL', 'PHONE NUMBER'.",
    "identities": "Stable identification numbers and documents: social security numbers (last 4 digits), driver's license numbers, passport numbers, tax IDs, employee IDs, student IDs, insurance member IDs.",
    
    # === Financial & Accounts ===
    "accounts": "Account information: account numbers, account holder names, account types, bank account details, credit card information (last 4 digits, card type), subscription account IDs, service account numbers, membership numbers, customer IDs, loyalty program numbers.",
    
    # === Preferences & Settings ===
    "preferences": "User preferences: preferred contact methods (phone, email, text), communication style preferences, service preferences (appointment times, service providers), payment methods, dietary preferences, accessibility needs, language preferences, notification preferences, time zone, preferred meeting formats.",
    
    # === Relationships & Network ===
    "relationships": "Personal relationships and family contacts: family members (spouse, children, parents, siblings), close friends, business contacts, authorized representatives, people the user frequently interacts with or makes decisions on behalf of. Include relationship context (e.g., 'my wife Sarah', 'my son John') and relevant contact information or identifiers. IMPORTANT: When storing contact information for family members or others, use feature names that include ownership (e.g., 'SPOUSE EMAIL', 'CHILD PHONE NUMBER', 'EMERGENCY CONTACT NAME').",
    "services": "Service providers and professional contacts: doctor, lawyer, accountant, dentist, insurance agent, financial advisor, therapist, personal trainer, and other professional service providers. Include contact information, specialties, and relevant details for these service providers. IMPORTANT: Use feature names that include the service provider type (e.g., 'DOCTOR PHONE', 'LAWYER EMAIL', 'ACCOUNTANT CONTACT').",
}

# Optimized description for task-oriented structured facts
task_assistant_description = """
    You are extracting structured, factual user information from conversations with a task-oriented assistant.
    This information is used to efficiently complete user requests and is typically referenced at the start of sessions.
    
    YOUR ROLE AND CONTEXT
    
    Your Job:
    - Extract structured facts that help the agent quickly access information needed for task completion
    - Store contact information, account details, identities, preferences, relationships, and service providers
    - Enable the agent to complete tasks efficiently without asking for repeated information
    
    Important Context:
    - Episodic memories already contain refined descriptions and atomic claims, including all historical events and temporary states
    - Semantic memory is for STABLE, REUSABLE user information that persists across sessions
    - You will receive an OLD_PROFILE containing existing features - ALWAYS check this first before creating new features
    
    WHAT TO EXTRACT
    
    Extract These Stable Structured Facts:
    - Permanent contact information (phone, email, addresses)
    - Stable account information (account numbers, IDs - last 4 digits only)
    - Long-term preferences (communication methods, service preferences, payment methods)
    - Relationship information that remains stable (family members, close contacts)
    - Service provider relationships with contact information
    
    Do NOT Extract (These belong in episodic memory):
    - Historical events or past actions (e.g., "booked a flight on 2026-01-23")
    - Temporary states or pending actions (e.g., "flight_booking_pending")
    - One-time transactions or specific occurrences (e.g., "made a purchase")
    - Time-specific information that will become outdated (e.g., "currently traveling")
    - Travel history, booking history, transaction history, or any event-based information
    - Temporary preferences or context-dependent choices (e.g., "wants pizza today" vs. stable "prefers Italian food")
    
    FEATURE NAMING RULES
    
    Format Rules:
    - Use UPPERCASE letters with SPACES between words (e.g., "PHONE NUMBER", "EMAIL")
    - Use full words, not abbreviations
    - Be specific and descriptive
    
    Standard Feature Names (User's Own Information):
    - "FULL NAME" (not "NAME", "USER NAME", "USERNAME")
    - "EMAIL" (not "EMAIL ADDRESS", "CONTACT EMAIL", "E-MAIL")
    - "PHONE NUMBER" (not "PHONE", "MOBILE", "TELEPHONE")
    - "MOBILE PHONE" (only if user has multiple phones and you need to distinguish)
    - "BANK ACCOUNT LAST4" (not "ACCOUNT", "BANK", "ACCOUNT NUMBER")
    - "CREDIT CARD LAST4" (not "CARD", "CARD NUMBER")
    - "PREFERRED PAYMENT METHOD" (not "PAYMENT", "PREFERENCE")
    - "TIMEZONE" (not "TZ", "TIME ZONE")
    - "DATE OF BIRTH" (not "DOB", "BIRTHDATE", "BIRTH DATE")
    - "HOME ADDRESS" (not "ADDRESS", "HOME", "RESIDENCE")
    
    Feature Names with Ownership (Information Belonging to Others):
    Format: "[OWNER] [INFORMATION TYPE]"
    
    Family Members:
    - Spouse: "SPOUSE EMAIL", "SPOUSE PHONE NUMBER", "SPOUSE FULL NAME"
    - Children: "CHILD NAME", "CHILD EMAIL", "CHILD PHONE NUMBER"
      * Multiple children: "CHILD 1 NAME", "CHILD 2 NAME", etc.
    - Parents: "PARENT NAME", "PARENT EMAIL", "PARENT PHONE NUMBER"
      * Specific: "MOTHER NAME", "FATHER NAME"
    - Siblings: "SIBLING NAME", "SIBLING PHONE"
    - Emergency contacts: "EMERGENCY CONTACT NAME", "EMERGENCY CONTACT PHONE", "EMERGENCY CONTACT EMAIL"
    
    Service Providers:
    - "DOCTOR NAME", "DOCTOR PHONE", "DOCTOR EMAIL"
    - "LAWYER CONTACT", "ACCOUNTANT EMAIL"
    - "PRIMARY DOCTOR PHONE" (if multiple doctors)
    
    Work Contacts:
    - "MANAGER NAME", "MANAGER EMAIL"
    - "COLLEAGUE PHONE"
    
    Ownership Examples:
    - User's own email → "EMAIL"
    - Spouse's email → "SPOUSE EMAIL"
    - Child's phone → "CHILD PHONE NUMBER" or "CHILD 1 PHONE NUMBER"
    - Emergency contact's phone → "EMERGENCY CONTACT PHONE"
    - Doctor's contact → "DOCTOR PHONE"
    
    AVOIDING DUPLICATES
    
    Before Adding a New Feature:
    1. ALWAYS check OLD_PROFILE for existing features with the same or similar meaning
    2. If a similar feature exists, USE the existing feature name exactly as it appears
    3. Do NOT create a new feature with a different name for the same information
    
    Updating Existing Features:
    - Use UPDATE commands (delete old + add new) to modify existing features
    - Do NOT use ADD commands to create duplicates
    - Example: If OLD_PROFILE has "EMAIL" and new message mentions "email address", 
      UPDATE "EMAIL" instead of creating "EMAIL ADDRESS"
    
    Reusing Feature Names:
    - If you see a feature name in OLD_PROFILE that means the same thing, USE THAT EXACT NAME
    - Do not create synonyms or variations
    - Check OLD_PROFILE first - reuse existing feature names when the information matches
    
    EXTRACTION PROCESS
    
    Step-by-Step Process:
    1. Check OLD_PROFILE for existing features
    2. Identify what information is new or needs updating
    3. Use standard feature names (see FEATURE NAMING RULES above)
    4. Include ownership prefix if information belongs to someone else
    5. Extract ALL structured facts, even basic ones like names and contact details
    6. For account numbers and IDs, store only the last 4 digits
    7. Include relationship context when extracting family/contact information
    8. Extract service provider information with contact details and specialties
    
    Priority Order:
    1. Contact information needed for task completion (contacts, basics)
    2. Account and identity information (accounts, identities)
    3. User preferences that affect task execution (preferences)
    4. Relationship and service provider information (relationships, services)
    
    Remember: Extract stable, reusable facts that can be quickly referenced at the start 
    of sessions to complete tasks efficiently. If it's a one-time event or temporary 
    state, it belongs in episodic memory, not semantic memory.
"""

TaskAssistantSemanticCategory = SemanticCategory(
    name="profile",
    prompt=StructuredSemanticPrompt(
        tags=task_assistant_tags,
        description=task_assistant_description,
    ),
)

SEMANTIC_TYPE = TaskAssistantSemanticCategory
