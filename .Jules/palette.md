## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-07-04 - Layout grouping for secondary actions
**Learning:** When adding a secondary action (like a "Copy" button) to a header with `justify-between` and multiple existing text elements (title and annotation), simply adding the button disrupts the balance. Grouping the primary text elements in a `.cluster` container preserves their left-alignment while correctly pushing the new action to the far right.
**Action:** Use layout grouping primitives to maintain intended positioning when introducing new utility elements into existing component bars.
