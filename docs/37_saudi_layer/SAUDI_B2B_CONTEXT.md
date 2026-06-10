# Saudi B2B Business Context — سياق الأعمال السعودي

## Business Culture

### Decision-Making

Saudi B2B decision-making is **hierarchical** with these characteristics:

| Factor | Description |
|--------|-------------|
| **Key Decision-Maker** | Typically CEO / General Manager / Owner (especially in SMEs) |
| **Influencers** | Technical managers, trusted advisors, family members |
| **Decision Speed** | Slower than Western markets — relationship is required first |
| **Approval Process** | Multiple layers of approval possible, even in SMEs |
| **Trust Requirement** | Trust must be established before any transaction |
| **Reference Importance** | References and word-of-mouth are critical |
| **Price Sensitivity** | Moderate — quality and trust matter more than lowest price |

### Relationship Building Protocol

1. **Introduction**: Best through a mutual connection (وساطة/تزكية)
2. **First Meeting**: Build rapport, share tea/coffee, minimal business talk initially
3. **Trust Phase**: 1-3 meetings typically needed before serious business discussion
4. **Proposal**: Formal written proposal in Arabic (or bilingual)
5. **Negotiation**: Expected — leave room for negotiation in pricing
6. **Closing**: Face-to-face meeting for signature, not email
7. **Post-Sale**: Regular follow-up, maintain relationship

### Communication Preferences

| Channel | Appropriateness | Notes |
|---------|----------------|-------|
| **WhatsApp** | High for ongoing communication | Preferred channel after relationship established |
| **Phone Call** | High | Used for initial outreach if you have a referral |
| **Email** | Medium | Used for formal documents and proposals |
| **LinkedIn** | Medium-High | Growing especially in tech/consulting |
| **In-Person** | High | Essential for first serious meeting |
| **Video Call** | Medium | Increasingly accepted post-COVID |

### Business Seasons

| Season | Impact | Strategy |
|--------|--------|----------|
| **Ramadan** | Reduced hours, shorter work days | Morning only, reduced outreach |
| **Eid Al-Fitr** | 4-7 days holiday | Do not schedule meetings |
| **Eid Al-Adha** | 4-5 days holiday | Do not schedule meetings |
| **Summer (Jun-Aug)** | Reduced activity, many travel | Focus on preparation |
| **September** | New business year starts (post-summer) | High activity period |
| **Year-End (Nov-Dec)** | Budget planning, contract signing | Important sales period |
| **Saudi National Day (Sep 23)** | Holiday | Acknowledge/protional content only |
| **Founding Day (Feb 22)** | Holiday | Acknowledge/protional content only |
| **School Year Start (Sep)** | Parents/educational businesses busy | Keep communications brief |

### Business Hours

| Day | Government | Private Sector | Notes |
|-----|-----------|----------------|-------|
| Sunday-Thursday | 7:30-14:30 | 9:00-17:00 (varies) | Some private sector until 18:00 |
| Friday | Closed | Closed | Friday prayer 12:00-13:30 |
| Saturday | Closed | Some open (retail/service) | |

### Negotiation Style

| Aspect | Approach |
|--------|----------|
| **Opening Offer** | Expect a counter-offer, price 10-30% higher |
| **Relationship First** | Don't negotiate seriously before relationship is established |
| **Indirect Rejection** | "إن شاء الله" may mean "maybe" or "no" — look for context |
| **Saving Face** | Never put a Saudi counterpart in position of losing face |
| **Patience** | Rushing decisions is counterproductive |
| **Follow-up** | Follow up, but don't be pushy — there's a fine line |

### Wasta (واسطة) — Networking

Wasta (connections/influence) is real in Saudi business:
- A strong referral significantly accelerates trust-building
- Wasta is not corruption — it's relationship capital
- Leverage your network for introductions to decision-makers
- Offering Wasta before relationship is established can seem desperate

### Gender Dynamics

- Women entrepreneurs and executives are growing rapidly
- Many businesses now have mixed-gender workplaces
- For female decision-makers, use feminine forms appropriately
- Some conservative sectors (construction, heavy industry) remain male-dominated
- Fintech, e-commerce, consulting, and media are more gender-balanced

### Cultural Do's and Don'ts

| Do | Don't |
|----|-------|
| Greet with السلام عليكم | Don't rush to handshake with opposite gender |
| Address by title + first name | Don't use first name only until invited |
| Accept tea/coffee when offered | Don't refuse more than once |
| Use right hand for handshake | Don't use left hand for handshake or eating |
| Ask "كيف الحال؟" / "كيف الأمور؟" | Don't ask about family members (especially women) |
| Show respect for elders and seniority | Don't criticize government or religion |
| Show enthusiasm about Vision 2030 | Don't make political statements |
| Be patient | Don't show frustration at delays |

## Code Reference

- **Module**: `integrations/saudi_market.py` — Saudi calendar, Ramadan, prayer times
- **Module**: `auto_client_acquisition/saudi_layer/arabic_style.py` — formality, greetings, closings
- **Module**: `auto_client_acquisition/saudi_layer/whatsapp_boundary.py` — WhatsApp communication rules
