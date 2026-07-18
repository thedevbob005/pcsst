## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2025-05-15 - State Persistence and Race Conditions in Clipboard Copy Buttons
**Learning:** Copy buttons require both precise, accessible state announcements and robust asynchronous state tracking. When users rapidly click copy buttons, overlapping `setTimeout` calls can clear status feedback prematurely, causing confusing UI flashes. Managing previous timer state with `clearTimeout` ensures smooth, predictable feedback.
**Action:** When creating interactive feedback states with async timers, always clear any existing timeout references before scheduling a new one, and reset visual classes cleanly.
