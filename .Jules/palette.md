## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-08-07 - Non-destructive Accessible Copy Buttons in Headers
**Learning:** Integrating copy utilities into component headers (like .command-card__bar) requires careful flexbox grouping to maintain visual alignment. Wrapping adjacent header text in a `div.cluster.cluster-tight` ensures the copy button is pushed correctly to the far right. Standardizing `aria-label` context ("Copy commands..." vs "Copy code...") also significantly improves screen-reader clarity.
**Action:** Always group header elements cleanly when inserting new interactive controls, and tailor the ARIA label's context based on the content type of the target container.
