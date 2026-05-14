## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-07 - Robust Asynchronous UI Feedback
**Learning:** Temporary UI feedback states (e.g., "Copied" on a button) can lead to race conditions if the user interacts rapidly. Using a `Map` to track and clear pending timeouts ensures the UI always settles into the correct final state. Additionally, restoring `innerHTML` instead of `textContent` preserves nested elements like icons.
**Action:** When implementing temporary feedback, always clear existing timeouts and use a non-destructive restoration pattern that preserves accessibility (ARIA labels) and visual structure (nested HTML).
