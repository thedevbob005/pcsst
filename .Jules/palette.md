## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-06-16 - Non-Destructive UI Feedback
**Learning:** When implementing temporary UI feedback (like a "Copied" state on a button), capturing the original `innerHTML` and accessibility attributes during registration/initialization is superior to capturing them inside the click listener. It prevents rapid successive interactions from "capturing" the transient feedback state as the baseline, ensuring the UI always restores to its intended original state.
**Action:** Use a non-destructive closure pattern to store and restore component baselines, and always use `clearTimeout` to manage transient state lifecycles during high-frequency interactions.
