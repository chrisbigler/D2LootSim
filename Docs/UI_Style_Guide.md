## D2 Loot Sim — UI Style Guide (2025)
### Destiny 2: Edge of Fate Expansion Theme

### Design Principles
- **Cosmic immersion**: Dark matter and Oort cloud inspired aesthetic with deep space themes.
- **Clarity first**: Clean hierarchy, generous spacing, legible typography with stellar contrast.
- **Dark-first**: Immersive sci‑fi dark theme reflecting the void between worlds.
- **Consistency**: Ship UI tokens and reuse components across the cosmic interface.

### Design Tokens - Edge of Fate Palette
- **Primary Palette** (Inspired by dark matter and cosmic themes)
  - Dark Matter Purple: `--brand-600: #6B46C1`, `--brand-700: #553C9A`, `--brand-800: #4C1D95`
  - Void Black: `--void-900: #0A0A0F`, `--void-800: #1A1A2E`, `--void-700: #16213E`
  - Cosmic Blue: `--cosmic-500: #3B82F6`, `--cosmic-600: #2563EB`, `--cosmic-700: #1D4ED8`
  - Stellar White: `--stellar-50: #F8FAFC`, `--stellar-100: #F1F5F9`, `--stellar-200: #E2E8F0`
- **Status Colors** (Enhanced with cosmic theme)
  - Success (Guardian Green): `--success-500: #10B981`, `--success-600: #059669`
  - Warning (Solar Orange): `--warning-500: #F59E0B`, `--warning-600: #D97706`  
  - Error (Crimson Alert): `--error-500: #EF4444`, `--error-600: #DC2626`
  - Info (Arc Blue): `--info-500: #06B6D4`, `--info-600: #0891B2`
- **Light mode** (Stellar theme - high contrast for accessibility)
  - `--bg: #F8FAFC`, `--surface: #FFFFFF`, `--surface-subtle: #F1F5F9`
  - `--text: #0F172A`, `--muted: #64748B`, `--border: #E2E8F0`
  - `--accent: #6B46C1`, `--accent-hover: #553C9A`
- **Dark mode** (Void theme - deep space immersion)
  - `--bg: #0A0A0F`, `--surface: #1A1A2E`, `--surface-subtle: #16213E`
  - `--text: #F8FAFC`, `--muted: #94A3B8`, `--border: #334155`
  - `--accent: #8B5CF6`, `--accent-hover: #A78BFA`

### Typography
- Use system-ui stack. Sizes: 24px h1, 16px body, 12–14px labels.
- Uppercase section labels with increased letter spacing for metadata.

### Components - Edge of Fate Design System
- **Buttons**: `.btn`, variants `.btn-primary` (Dark Matter Purple), `.btn-secondary` (Cosmic Blue), `.btn-success` (Guardian Green), `.btn-ghost` (transparent with Stellar borders).
- **Inputs**: `.input`, `.select` with 8–12px padding, 12px radius, Void backgrounds in dark mode, Stellar backgrounds in light mode.
- **Panels**: `.config-panel`, `.results-panel` use `--surface`, `--border`, cosmic-inspired soft shadows with purple tints.
- **Cards**: `.result-card` with Dark Matter Purple left accent (`--brand-600`).
- **Stats**: `.stats-grid` with `.stat-item` (subtle void backgrounds), `.stat-value` (Stellar White text), `.stat-label` (muted cosmic text).
- **Notices**: `.notice` + modifiers `.error` (Crimson Alert), `.success` (Guardian Green), `.warning` (Solar Orange), `.info` (Arc Blue).

### Layout
- Grid: `.main-content` uses 360px sidebar + fluid content.
- Responsive: collapse to single column <1200px; simplify grids <768px.

### Interactions - Cosmic UX
- **Hover effects**: Gentle lifts (translateY -1 to -2px) with cosmic glow shadows using Dark Matter Purple.
- **Focus rings**: 4px outline using `--accent` color with subtle purple glow for accessibility.
- **Active states**: Subtle cosmic pulse animation on interactions.
- **Keyboard shortcuts**: Cmd/Ctrl+1 runs single sim, Cmd/Ctrl+2 compares systems.

### Theming - Void/Stellar Toggle
- Root element carries `data-theme="dark|light"` with smooth transitions between Void (dark) and Stellar (light) themes.
- Theme preferences persist to `localStorage` (`theme-preference`).
- **Dark (Void) theme**: Deep space immersion with Dark Matter Purple accents.
- **Light (Stellar) theme**: High contrast stellar theme for accessibility.

### Accessibility - Guardian Standards
- **Contrast ratios**: Minimum 4.5:1 for normal text, 7:1 for enhanced readability.
- **Hit targets**: ≥ 44x44px for touch interfaces, ≥ 40x40px for desktop.
- **Labels**: Explicitly tied to inputs with proper ARIA relationships.
- **Color independence**: Never rely solely on color to convey information.
- **Focus management**: Clear focus indicators with cosmic-themed outlines.

### Content Guidelines - Expansion Voice
- Keep headings short and impactful. Use sentence case except for Destiny-specific terms.
- Prefer concise inline help using `.muted` text with subtle cosmic styling.
- Use terminology consistent with Destiny 2 universe (Guardian, Light, Void, Arc, Solar).
- Maintain scientific/space exploration tone befitting the Edge of Fate expansion.


