## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-06-13 - Robust Micro-Feedback for Interactive Elements
**Learning:** Micro-feedback interactions (like 'Copied' states) are prone to state regression if they capture the current DOM state within the click listener closure. If a user clicks rapidly, the 'feedback' state itself can be captured as the 'original' state, leading to broken UI after the timeout.
**Action:** Always capture and store the "baseline" state (innerHTML, ARIA labels, classes) during component initialization or registration, outside of the event listener's scope.
