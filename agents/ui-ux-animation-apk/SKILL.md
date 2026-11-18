---
name: ui-ux-animation-apk
description: UI/UX Compose animation checklist khusus Synthetica Manager 6.0.0+ — transisi, motion, nyalitime entry/exit, edge-to-edge.
---

# UI/UX Animation APK (Synthetica Manager)

## Tujuan
Membuat UI yang terasa "premium" dan konsisten — bukan asal animated.
Referensi: `compose-animations`, `compose-state-and-effects`, `edge-to-edge`, `jetpack-compose-performance`.

## Checklist motion
1. **Enter/exit transisi** — setiap screen harus punya transisi masuk (`slideIn`/`fadeIn` + `slideOut`/`fadeOut`). Hindari `Instant` dan `None`.
2. **List animations** — item pertama list masuk stagger; gunakan `items()` + `animateItemPlacement()`.
3. **Shared element transition** — untuk item yang dipindah ke detail screen (`SharedTransitionLayout` di Navigation 3/2).
4. **Gesture-driven** — swipe-to-dismiss, swipe-back, pull-to-refresh — semua harus punya velocity & spring yang konsisten.
5. **Edge-to-edge** — `enableEdgeToEdge()` di MainActivity; `imePadding()`/`statusBarsPadding()`/`windowInsetsPadding()` di setiap screen; navigation bar transparan.
6. **Reduced motion** — `LocalInspectionMode` + `accessibleForKey` + `KeyTransition.Easing`; hargai `prefers-reduced-motion`.

## Checklist design tokens
- **No hardcoded colors** — gunakan `MaterialTheme.colorScheme` / tokens projek
- **No hardcoded dp** — gunakan `dimens` atau `MaterialTheme.typography` untuk teks, `space` token untuk layout
- **Icon konsistensi** — satu set icon (mis. `Icons.Rounded` only), jangan campur filled/outlined/rounded
- **Typography** — gunakan `MaterialTheme.typography` (`headlineSmall`, `titleMedium`, dll) — jangan sendiri
- **Elevation/containers** — `Surface`, `MaterialTheme.colorScheme` untuk surface tint, bukan warna mentah

## Checklist kecepatan animasi
- `spring(stiffness = Spring.StiffnessMediumLow)` untuk transisi layar yang menyenangkan
- `spring(dampingRatio = Spring.DampingRatioLowBouncy)` untuk gesture interaktif
- `tween(durationMillis = 250, easing = FastOutSlowInEasing)` untuk micro-interactions
- Test di **device mid-range** (joyeuse) — bukan hanya emulator — karena FPS dapat menjatuhkan perception of quality

## Caranya dijalankan
1. Baca screen saat ini, tandai semua efek yang tidak konsisten
2. Bandingkan dengan Material 3 motion spec
3. Terapkan satu per satu; build setiap tahap
4. Screenshot diff sebelum/sesudah (device) untuk evidence
5. Jalankan `./gradlew :app:assembleDebug` dan `adb install -r` → visual check

## Jangan
- Jangan tambah infinite animation di tempat yang bukan "live" — itu tidak profesioanl dan bisa degradasi FPS.
- Jangan animasikan `Modifier.fillMaxSize()` tanpa alasan (performa buruk).
- Jangan keras-headset animation tanpa respect to reduced-motion.
