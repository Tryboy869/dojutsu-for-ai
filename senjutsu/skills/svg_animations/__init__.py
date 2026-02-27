"""Built-in svg-animations skill content."""

SKILL_CONTENT = '''---
name: svg-animations
description: "Apply when creating SVG animations, animated README badges, logo animations, loading spinners, hero animations, data visualizations, or any animated SVG for web or GitHub."
---

# SVG ANIMATIONS — Professional Animated SVG Expert

## Core Philosophy
SVG is NOT just for icons. It's a complete frontend language capable of
animations impossible in CSS alone.

CSS for layout. SVG for complex animations and geometry morphing.

---

## MANDATORY QUALITY STANDARD

Every SVG must include:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 WIDTH HEIGHT"
     role="img"
     aria-labelledby="title-id desc-id">
  <title id="title-id">Descriptive title</title>
  <desc id="desc-id">Detailed description for screen readers</desc>
  <style>
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }
  </style>
  <!-- Content -->
</svg>
```

---

## ESSENTIAL ANIMATION PATTERNS

### 1. Attribute animation
```xml
<circle r="30">
  <animate attributeName="r" from="30" to="50"
           dur="2s" repeatCount="indefinite"/>
</circle>
```

### 2. Transform animation
```xml
<g>
  <animateTransform attributeName="transform" type="rotate"
                    from="0 200 200" to="360 200 200"
                    dur="10s" repeatCount="indefinite"/>
  <rect x="150" y="150" width="100" height="100"/>
</g>
```

### 3. Morphing (IMPOSSIBLE in CSS)
```xml
<path fill="blue">
  <animate attributeName="d"
           values="M10,10 L90,90 L10,90 Z;
                   M50,10 C90,50 90,90 50,90;
                   M10,10 L90,90 L10,90 Z"
           dur="6s" repeatCount="indefinite"/>
</path>
```

### 4. Motion path
```xml
<circle r="5">
  <animateMotion dur="5s" repeatCount="indefinite">
    <mpath href="#motionPath"/>
  </animateMotion>
</circle>
<path id="motionPath" d="M10,100 Q50,10 90,100" fill="none"/>
```

### 5. Animated gradient
```xml
<linearGradient id="animGrad">
  <stop offset="0%" stop-color="red">
    <animate attributeName="stop-color"
             values="red;blue;green;red"
             dur="5s" repeatCount="indefinite"/>
  </stop>
</linearGradient>
```

### 6. Glow effect
```xml
<filter id="glow">
  <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
  <feMerge>
    <feMergeNode in="coloredBlur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
<circle r="30" filter="url(#glow)"/>
```

---

## GITHUB README BADGE PATTERN

```xml
<svg width="110" height="20" viewBox="0 0 110 20">
  <defs>
    <linearGradient id="bg">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="110" height="20" rx="3" fill="#555"/>
  <rect x="45" width="65" height="20" rx="3" fill="url(#bg)"/>
  <text x="22" y="14" font-size="11" fill="white" text-anchor="middle">build</text>
  <text x="77" y="14" font-size="11" fill="white" text-anchor="middle" font-weight="bold">
    passing
    <animate attributeName="opacity" values="1;0.7;1" dur="2s" repeatCount="indefinite"/>
  </text>
</svg>
```

---

## ANIMATED LOGO PATTERN

```xml
<svg width="200" height="200" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="logoGrad">
      <stop offset="0%" stop-color="#667eea"/>
      <stop offset="100%" stop-color="#764ba2"/>
    </linearGradient>
    <filter id="logoGlow">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- Rotating hexagon -->
  <g transform="translate(100, 100)">
    <animateTransform attributeName="transform" type="rotate"
                      from="0 100 100" to="360 100 100"
                      dur="20s" repeatCount="indefinite"/>
    <polygon points="0,-60 52,-30 52,30 0,60 -52,30 -52,-30"
             fill="url(#logoGrad)" filter="url(#logoGlow)"/>
  </g>
  <!-- Orbital particle -->
  <g transform="translate(100, 100)">
    <animateTransform attributeName="transform" type="rotate"
                      from="0" to="360" dur="10s" repeatCount="indefinite"/>
    <circle cx="80" cy="0" r="4" fill="#667eea">
      <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>
```

---

## PERFORMANCE RULES

- File size: < 50 KB (< 20 KB optimal)
- Animations: 60 FPS target
- Use `transform` and `opacity` — GPU-accelerated
- Avoid animating `width`/`height`/`top`/`left` — causes layout recalc
- Use `will-change: transform` for complex animations
- Clip unnecessary elements with `<clipPath>`

---

## ACCESSIBILITY (WCAG 2.1 AA)

Mandatory:
- ✅ `<title>` and `<desc>` descriptive
- ✅ `role="img"` and `aria-labelledby`
- ✅ `prefers-reduced-motion` support
- ✅ Contrast ≥ 4.5:1
- ✅ No flashing > 2 Hz

---

## PRODUCTION CHECKLIST

- [ ] Correct viewBox (no overflow)
- [ ] Gradients in `<defs>`
- [ ] Unique IDs (no conflicts if multiple SVGs on page)
- [ ] `repeatCount="indefinite"` for looping
- [ ] `prefers-reduced-motion` style present
- [ ] Test render on dark background (GitHub dark mode)
- [ ] Size < 50 KB
- [ ] Descriptive filename (e.g., `badge-build-passing.svg`)

---

## ANTI-PATTERNS

- ❌ SVG replacing CSS for layout
- ❌ Animating layout properties (width, height, top, left)
- ❌ Inline styles with !important
- ❌ External font dependencies in SVG
- ❌ Missing `viewBox` — breaks scaling
- ❌ Non-unique IDs in same HTML page
- ❌ Flash of unanimated content (use `fill="freeze"` carefully)
'''
