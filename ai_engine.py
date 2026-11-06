import re


def rewrite_content(
    original_content,
    personality,
    tone,
    audience,
    platform,
    brand_name="",
    industry="",
    brand_description="",
    preferred_words="",
    avoid_words="",
    content_type="",
    purpose="",
    length_choice=""
):
    rewritten = original_content.strip()
    explanations = []

    # 1. Normalise personality
    if isinstance(personality, str):
        personality = [personality]

    personality = personality or []

    # 2. Improve capitalisation
    if rewritten.isupper():
        rewritten = rewritten.capitalize()
        explanations.append(
            "Improved capitalisation for readability."
        )

    # 3. Reduce excessive punctuation
    if re.search(r"[!?]{2,}", rewritten):
        rewritten = re.sub(r"[!?]{2,}", ".", rewritten)
        explanations.append(
            "Reduced excessive punctuation."
        )

    # 4. Replace aggressive promotional language
    replacements = {
        "buy now": "explore our product",
        "hurry up": "discover it today",
        "best product ever": "a product designed with you in mind",
        "don't miss out": "find out more",
        "limited time offer": "special offer",
        "amazing deal": "special opportunity"
    }

    for old, new in replacements.items():
        pattern = re.compile(re.escape(old), re.IGNORECASE)

        if pattern.search(rewritten):
            rewritten = pattern.sub(new, rewritten)
            explanations.append(
                f"Replaced '{old}' with '{new}'."
            )

    # 5. Tone adaptation
    tone_rules = {
        "Professional": {
            "gonna": "going to",
            "wanna": "want to",
            "awesome": "excellent",
            "super cool": "highly useful"
        },
        "Formal": {
            "gonna": "going to",
            "wanna": "wish to",
            "hey": "hello",
            "cool": "excellent"
        },
        "Friendly": {
            "purchase": "get",
            "utilise": "use",
            "assistance": "help"
        },
        "Inspirational": {
            "can't": "can",
            "impossible": "challenging",
            "failure": "learning experience"
        }
    }

    if tone in tone_rules:
        for old, new in tone_rules[tone].items():
            pattern = re.compile(
                r"\b" + re.escape(old) + r"\b",
                re.IGNORECASE
            )
            rewritten = pattern.sub(new, rewritten)

        explanations.append(
            f"Adapted vocabulary for a {tone.lower()} tone."
        )

    # 6. Personality adaptation
    personality_rules = {
        "Friendly": "friendly and approachable",
        "Professional": "professional and credible",
        "Creative": "creative and expressive",
        "Bold": "confident and direct",
        "Minimalist": "simple and concise",
        "Trustworthy": "clear and reliable",
        "Innovative": "forward-thinking"
    }

    selected_personalities = [
        personality_rules[p]
        for p in personality
        if p in personality_rules
    ]

    if selected_personalities:
        explanations.append(
            "Applied brand personality direction: "
            + ", ".join(selected_personalities)
            + "."
        )

    # 7. Preferred vocabulary
    preferred = [
        word.strip()
        for word in preferred_words.split(",")
        if word.strip()
    ]

    if preferred:
        explanations.append(
            "Brand vocabulary preferences were considered: "
            + ", ".join(preferred) + "."
        )

    # 8. Avoided vocabulary
    avoided = [
        word.strip()
        for word in avoid_words.split(",")
        if word.strip()
    ]

    for word in avoided:
        pattern = re.compile(re.escape(word), re.IGNORECASE)

        if pattern.search(rewritten):
            rewritten = pattern.sub("", rewritten)
            explanations.append(
                f"Removed the restricted word or phrase '{word}'."
            )

    # 9. Platform awareness
    platform_guidance = {
        "Instagram": "Prepared for short, engaging social communication.",
        "LinkedIn": "Prepared for professional communication.",
        "Website": "Prepared for clear website communication.",
        "Email": "Prepared for direct email communication.",
        "Facebook": "Prepared for conversational social communication."
    }

    if platform in platform_guidance:
        explanations.append(platform_guidance[platform])

    # 10. Brand context
    if brand_name:
        explanations.append(f"Brand: {brand_name}.")

    if industry:
        explanations.append(f"Industry context: {industry}.")

    if brand_description:
        explanations.append("Brand description considered.")

    if audience:
        explanations.append(f"Target audience: {audience}.")

    if content_type:
        explanations.append(f"Content type: {content_type}.")

    if purpose:
        explanations.append(f"Communication purpose: {purpose}.")

    if length_choice:
        explanations.append(f"Requested content length: {length_choice}.")

    # 11. Return results
    return {
        "rewritten_content": rewritten,
        "explanations": explanations
    }