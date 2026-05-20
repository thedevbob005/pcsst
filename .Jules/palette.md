## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-05-20 - Preserving Documentation Code Formatting
**Learning:** Running global formatters (like Prettier) on HTML files containing `<code>` blocks with significant whitespace can flatten snippets into unreadable strings. Documentation code examples must remain authored with intent.
**Action:** Use targeted diffs or specific line formatting for documentation HTML instead of project-wide rewrites.

## 2026-05-20 - Non-destructive Feedback States
**Learning:** When providing temporary UI feedback (e.g., "Copied" on a button), using `innerHTML` restoration ensures that icons and nested structures are not lost. Using a `Map` to track timeouts prevents "flicker" or state abandonment during rapid interactions.
**Action:** Always store and restore `innerHTML` and `aria-label` for transient button states.
