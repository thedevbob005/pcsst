## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-07-12 - Resilient Micro-Interaction State Management
**Learning:** When implementing temporary UI feedback (like a "Copied" state on a button), capturing the initial `innerHTML` and `aria-label` during component registration (outside the event listener) is safer than capturing it inside the closure. This prevents rapid successive interactions from accidentally "capturing" the temporary feedback state as the original state if the timeout hasn't cleared yet.
**Action:** Always capture baseline component state during initialization/registration and use `clearTimeout` to handle race conditions in interactive feedback loops.
