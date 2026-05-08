## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-14 - Accessible Feedback for Transient Actions
**Learning:** Transient UI actions like "Copy to clipboard" require both visual and accessible confirmation. Using `aria-live="polite"` and updating `aria-label` ensures the success or failure is announced to screen readers. Managing timeouts properly prevents UI state desync during rapid interactions.
**Action:** Always pair transient text changes with `aria-live` and updated `aria-label` attributes. Capture original UI state outside the interaction loop to ensure reliable restoration.
