## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-14 - Layout Preservation for UI Enhancements
**Learning:** When adding elements (like a "Copy" button) to a flex container with `justify-between` (like `.command-card__bar`), existing items must be grouped in a sub-container (e.g., `.cluster`) to maintain their relative alignment while the new element is pushed to the far right.
**Action:** Always inspect the parent's layout strategy before inserting new UI elements to prevent unintended spacing shifts.
