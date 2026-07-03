## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-15 - Robust Temporary UI Feedback
**Learning:** When implementing temporary feedback (like a "Copied" state), capturing the original state (`innerHTML`, `aria-label`) at registration time rather than during the event ensures that rapid, successive interactions don't accidentally capture and "lock in" the temporary feedback state. Using `clearTimeout` within the handler further prevents race conditions.
**Action:** Always capture baseline state during component initialization and use `clearTimeout` to manage overlapping feedback timers.
