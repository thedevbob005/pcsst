## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-14 - Non-destructive Feedback for Interactive Elements
**Learning:** When implementing temporary UI feedback (like a 'Copied' state) that modifies an element's content or attributes, capturing the original state outside the event listener ensures that rapid, repeated interactions always restore the correct baseline rather than capturing a transient feedback state.
**Action:** Store `innerHTML` and `aria-label` during component initialization/registration and use `clearTimeout` to manage overlapping feedback cycles.

## 2025-05-14 - Contextual Accessibility Labels for Identical Actions
**Learning:** Multiple identical action buttons (like "Copy") on a single page need unique `aria-label` values that provide context (e.g., "Copy code to clipboard" vs "Copy commands to clipboard") to help screen-reader users distinguish between them.
**Action:** Use specific ARIA labels for repetitive interactive elements that indicate what they act upon.
