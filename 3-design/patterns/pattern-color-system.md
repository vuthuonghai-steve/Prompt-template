# Pattern: Color System (3-5 Colors Max)

## Problem
Too many colors → visual chaos, inconsistent brand, slow loading.

## Solution
Limit to EXACTLY 3-5 colors total: 1 primary + 2-3 neutrals + 1-2 accents.

**Core principles:**
- Maximum 5 colors without explicit permission
- 1 primary brand color
- 2-3 neutrals (white, grays, black variants)
- 1-2 accents
- NEVER use purple/violet unless asked

## Example

### ✅ Good: 5 Color System
```css
:root {
  /* 1. Primary brand */
  --primary: 220 90% 56%;        /* Blue */
  
  /* 2-4. Neutrals */
  --background: 0 0% 100%;       /* White */
  --foreground: 222 47% 11%;     /* Dark gray */
  --muted: 210 40% 96%;          /* Light gray */
  
  /* 5. Accent */
  --accent: 142 76% 36%;         /* Green */
}
```

### ❌ Bad: Too Many Colors
```css
:root {
  --primary: 220 90% 56%;
  --secondary: 280 80% 60%;
  --tertiary: 340 75% 55%;
  --accent-1: 142 76% 36%;
  --accent-2: 45 93% 47%;
  --accent-3: 10 80% 50%;
  /* 6+ colors = visual chaos */
}
```

## Gradient Rules

### ❌ Avoid Gradients
```css
/* DON'T use gradients unless explicitly asked */
background: linear-gradient(to right, blue, purple);
```

### ✅ If Necessary: Analogous Colors Only
```css
/* Use analogous colors (same temperature) */
--gradient-primary: linear-gradient(135deg, 
  hsl(220 90% 56%),  /* Blue */
  hsl(200 85% 60%)   /* Teal - same cool temperature */
);

/* NEVER mix opposing temperatures */
❌ pink → green
❌ orange → blue
❌ red → cyan
```

### Gradient Constraints
- Maximum 2-3 color stops
- Only as subtle accents
- Never for primary elements
- Analogous colors only

## Color Selection Guide

### Primary Color
```
Choose based on brand/purpose:
- Tech/Trust: Blue
- Nature/Health: Green
- Energy/Action: Orange
- Luxury: Gold/Black
- Creative: Teal/Coral
```

### Neutrals (2-3 required)
```
Always include:
- Background (white/off-white)
- Foreground (dark gray/black)
- Muted (light gray) - optional
```

### Accents (1-2 max)
```
Use for:
- Success states: Green
- Warnings: Amber
- Errors: Red
- Info: Blue
```

## Contrast Requirements

```css
/* If override background, MUST override text */
❌ Bad:
<div className="bg-primary">
  <p>Text</p> <!-- Invisible! -->
</div>

✅ Good:
<div className="bg-primary text-primary-foreground">
  <p>Text</p> <!-- Readable -->
</div>
```

## Decision Matrix

| Scenario | Colors Needed |
|----------|---------------|
| Simple landing page | 3 (primary + 2 neutrals) |
| Web app | 4 (primary + 2 neutrals + 1 accent) |
| E-commerce | 5 (primary + 2 neutrals + 2 accents) |
| Complex dashboard | 5 max (ask permission for more) |

## Anti-patterns
- ❌ More than 5 colors without permission
- ❌ Purple/violet as primary (unless asked)
- ❌ Opposing temperature gradients
- ❌ Complex gradients (4+ stops)
- ❌ Changing background without text color

## Checklist
- [ ] Total colors ≤ 5?
- [ ] 1 primary defined?
- [ ] 2-3 neutrals included?
- [ ] Accents ≤ 2?
- [ ] No purple (unless requested)?
- [ ] Gradients avoided or analogous only?
- [ ] Proper contrast for all combinations?

## Source
- v0 (Vercel) - "Color System: ALWAYS use exactly 3-5 colors total"
