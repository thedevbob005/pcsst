## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-06-22 - Non-Destructive Feedback Patterns
**Learning:** Temporary UI feedback (like 'Copied' states) should use a non-destructive pattern that captures and restores both `innerHTML` and accessibility attributes (e.g., `aria-label`). This ensures that icons or complex button content are not lost. Additionally, managing feedback timeouts with `clearTimeout` is critical to prevent race conditions during rapid user interactions.
**Action:** Always store the initial state (content and ARIA) outside the click listener's closure and clear existing timeouts before starting new feedback cycles.
