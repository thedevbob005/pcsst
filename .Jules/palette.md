## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-08-03 - Race-free Feedback for Ephemeral Action Buttons
**Learning:** Ephemeral state buttons (like a copy-to-clipboard button) require robust, race-free state management to prevent incorrect label restorations during rapid, repeated user clicks. Resolving timeout timers via stored listener references protects UI stability. Pairing dynamic `aria-label` announcements with existing design-system success indicators (like `.is-valid`) creates an exceptionally delightful and accessible user confirmation.
**Action:** Always capture initial text/accessibility states outside of the interaction closure, clear overlapping execution timeouts, and apply unified design system status styles for stateful micro-interactions.
