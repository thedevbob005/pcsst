## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-05-11 - Robust Feedback for Async Actions
**Learning:** Temporary UI feedback for actions like "Copy to clipboard" can easily break if the user clicks multiple times or if the button contains nested HTML (like icons). Using a timeout tracking Map ensures that rapid clicks don't result in premature state restoration. Preserving `innerHTML` and `aria-label` instead of just `textContent` ensures that the button returns to its exact original visual and accessible state.
**Action:** When implementing temporary success/error states, use a non-destructive restoration pattern that captures both visual (HTML) and accessible (ARIA) state, and manage timeouts centrally to handle race conditions.
