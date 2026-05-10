## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-15 - Non-destructive UI State Updates
**Learning:** When updating button labels for temporary feedback (e.g., "Copied"), using `textContent` is destructive as it removes nested HTML like icons. Always use `innerHTML` or save the original HTML to restore the full component state. Similarly, when using temporary `aria-label` updates, ensure the original label is restored rather than blindly removed to maintain accessibility.
**Action:** Use a non-destructive pattern for temporary UI state changes that captures and restores the complete initial state (HTML and ARIA attributes).
