## 2025-05-07 - Accessible Contrast in Dark Themes
**Learning:** In dark themes with vibrant accent colors (like Midnight's light teal #57c4c5), default white text can fail WCAG AA contrast requirements. Using the theme's background color (e.g., --pc-color-page) as text for active components provides much better legibility and contrast (9.2:1 vs 2.3:1).
**Action:** Always verify contrast ratios for primary action states across all supported themes, especially when flipping from light to dark modes.

## 2025-05-07 - Visual Feedback for Toggle Buttons
**Learning:** Buttons that act as state toggles (like a theme switcher) need clear visual differentiation beyond just ARIA attributes. Users rely on visual cues to understand the current system state.
**Action:** Style `aria-pressed="true"` states with distinct backgrounds or borders that match the system's active state patterns.

## 2026-07-22 - Visual Discovery of Keyboard Shortcuts
**Learning:** Keyboard shortcuts significantly boost user productivity, but they are often hidden features that users never discover. Providing platform-aware visual hints (like Ctrl+K on Windows/Linux or ⌘K on Mac/iOS) right next to the interactive label increases visual discovery of shortcuts while preserving high context readability.
**Action:** When implementing key-bound interactions, always include a platform-aware styled shortcut indicator (e.g., using a small badge with the appropriate key symbols) near the associated input or button.
