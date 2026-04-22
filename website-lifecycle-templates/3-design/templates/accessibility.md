# Accessibility Template

## WCAG 2.1 AA Compliance

**Goal**: Ensure all users can access and use the website

---

## Semantic HTML

### Use Proper Elements
```tsx
// ✅ CORRECT
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content</p>
  </article>
</main>

<footer>
  <p>Footer content</p>
</footer>

// ❌ WRONG
<div className="header">
  <div className="nav">
    <div className="link">Home</div>
  </div>
</div>
```

### Semantic Elements
- `<header>`: Site/section header
- `<nav>`: Navigation links
- `<main>`: Main content (one per page)
- `<article>`: Self-contained content
- `<section>`: Thematic grouping
- `<aside>`: Sidebar/related content
- `<footer>`: Site/section footer

---

## ARIA Attributes

### When to Use ARIA
- **First**: Use semantic HTML
- **Second**: Add ARIA when semantic HTML insufficient
- **Never**: Use ARIA to override semantic HTML

### Common ARIA Patterns

#### Buttons
```tsx
// Icon button
<button aria-label="Close dialog">
  <X className="h-4 w-4" />
</button>

// Toggle button
<button 
  aria-pressed={isActive}
  aria-label="Toggle notifications"
>
  {isActive ? 'On' : 'Off'}
</button>
```

#### Dialogs/Modals
```tsx
<div
  role="dialog"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
  aria-modal="true"
>
  <h2 id="dialog-title">Dialog Title</h2>
  <p id="dialog-description">Dialog description</p>
</div>
```

#### Tabs
```tsx
<div role="tablist" aria-label="Settings tabs">
  <button
    role="tab"
    aria-selected={activeTab === 'profile'}
    aria-controls="profile-panel"
  >
    Profile
  </button>
</div>

<div
  role="tabpanel"
  id="profile-panel"
  aria-labelledby="profile-tab"
>
  Panel content
</div>
```

#### Live Regions
```tsx
// Announcements
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent alerts
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

---

## Color Contrast

### WCAG AA Requirements
- **Normal text**: 4.5:1 contrast ratio
- **Large text** (18pt+): 3:1 contrast ratio
- **UI components**: 3:1 contrast ratio

### Testing
```tsx
// ✅ GOOD CONTRAST
<div className="bg-background text-foreground">
  {/* foreground on background: 7:1 ratio */}
</div>

// ❌ POOR CONTRAST
<div className="bg-gray-200 text-gray-300">
  {/* Only 1.5:1 ratio - fails WCAG */}
</div>
```

### Tools
- Chrome DevTools: Lighthouse audit
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Contrast Ratio](https://contrast-ratio.com/)

---

## Keyboard Navigation

### Focus Management
```tsx
// Visible focus indicator
<button className="
  focus:outline-none 
  focus:ring-2 
  focus:ring-ring 
  focus:ring-offset-2
">
  Button
</button>

// Skip to main content
<a 
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4"
>
  Skip to main content
</a>

<main id="main-content">
  {/* Main content */}
</main>
```

### Keyboard Shortcuts
- **Tab**: Move focus forward
- **Shift + Tab**: Move focus backward
- **Enter/Space**: Activate button/link
- **Escape**: Close dialog/menu
- **Arrow keys**: Navigate lists/menus

### Focus Trap (Modals)
```tsx
import { useEffect, useRef } from 'react'

function Modal({ isOpen, onClose }) {
  const modalRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => {
    if (!isOpen) return
    
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    
    const firstElement = focusableElements?.[0] as HTMLElement
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement
    
    firstElement?.focus()
    
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault()
        lastElement?.focus()
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault()
        firstElement?.focus()
      }
    }
    
    document.addEventListener('keydown', handleTab)
    return () => document.removeEventListener('keydown', handleTab)
  }, [isOpen])
  
  return (
    <div ref={modalRef} role="dialog" aria-modal="true">
      {/* Modal content */}
    </div>
  )
}
```

---

## Screen Reader Support

### Hidden Content
```tsx
// Visually hidden, screen reader accessible
<span className="sr-only">
  Additional context for screen readers
</span>

// Hidden from everyone
<div aria-hidden="true">
  Decorative content
</div>
```

### Image Alt Text
```tsx
// ✅ CORRECT
<img src="/logo.png" alt="Company name logo" />

// Decorative image
<img src="/decoration.png" alt="" aria-hidden="true" />

// ❌ WRONG
<img src="/logo.png" alt="image" />
<img src="/logo.png" />  // Missing alt
```

### Form Labels
```tsx
// ✅ CORRECT
<label htmlFor="email">Email address</label>
<input id="email" type="email" />

// Alternative with aria-label
<input 
  type="email" 
  aria-label="Email address"
  placeholder="Enter email"
/>

// ❌ WRONG
<input type="email" placeholder="Email" />  // No label
```

---

## Touch Targets

### Minimum Size
```tsx
// ✅ CORRECT - 44px minimum
<button className="min-h-[44px] min-w-[44px] px-4 py-2">
  Button
</button>

// ❌ WRONG - Too small
<button className="p-1 text-xs">
  Tiny button
</button>
```

### Spacing
```tsx
// Adequate spacing between touch targets
<div className="flex gap-4">
  <button className="min-h-[44px]">Button 1</button>
  <button className="min-h-[44px]">Button 2</button>
</div>
```

---

## Forms Accessibility

### Complete Form Example
```tsx
<form onSubmit={handleSubmit}>
  <fieldset>
    <legend>Personal Information</legend>
    
    {/* Text input */}
    <div>
      <label htmlFor="name">Full Name</label>
      <input
        id="name"
        type="text"
        required
        aria-required="true"
        aria-describedby="name-error"
      />
      <span id="name-error" role="alert" className="text-destructive">
        {errors.name}
      </span>
    </div>
    
    {/* Radio group */}
    <fieldset>
      <legend>Gender</legend>
      <div>
        <input type="radio" id="male" name="gender" value="male" />
        <label htmlFor="male">Male</label>
      </div>
      <div>
        <input type="radio" id="female" name="gender" value="female" />
        <label htmlFor="female">Female</label>
      </div>
    </fieldset>
    
    {/* Checkbox */}
    <div>
      <input 
        type="checkbox" 
        id="terms" 
        required
        aria-required="true"
      />
      <label htmlFor="terms">
        I agree to the terms and conditions
      </label>
    </div>
    
    <button type="submit">Submit</button>
  </fieldset>
</form>
```

---

## Testing Checklist

### Automated Testing
- [ ] Run Lighthouse accessibility audit
- [ ] Use axe DevTools browser extension
- [ ] Check WAVE accessibility tool

### Manual Testing
- [ ] Navigate entire site with keyboard only
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Verify color contrast ratios
- [ ] Check focus indicators visible
- [ ] Test form validation messages
- [ ] Verify all images have alt text
- [ ] Check heading hierarchy (h1 → h2 → h3)

### Screen Reader Testing
- **Windows**: NVDA (free), JAWS
- **Mac**: VoiceOver (built-in)
- **Mobile**: TalkBack (Android), VoiceOver (iOS)

---

## Common Patterns

### Accessible Button
```tsx
<button
  type="button"
  aria-label="Close dialog"
  className="
    min-h-[44px] min-w-[44px]
    focus:outline-none focus:ring-2 focus:ring-ring
  "
  onClick={handleClose}
>
  <X className="h-4 w-4" aria-hidden="true" />
</button>
```

### Accessible Link
```tsx
<a
  href="/about"
  className="
    text-primary underline
    focus:outline-none focus:ring-2 focus:ring-ring
  "
>
  Learn more about our company
</a>
```

### Accessible Card
```tsx
<article className="border rounded-lg p-4">
  <h2 className="text-xl font-semibold">Card Title</h2>
  <p className="text-muted-foreground">Card description</p>
  <a 
    href="/details"
    className="text-primary"
    aria-label="Read more about Card Title"
  >
    Read more
  </a>
</article>
```

---

**Sources**: v0 accessibility guidelines, WCAG 2.1 AA standards
