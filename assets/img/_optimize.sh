#!/usr/bin/env bash
# Ottimizza immagini e video del prodotto HyperTrimmer.
# Strategia:
#   - immagini: genera WebP (cwebp) a dimensione "retina 2x" della resa effettiva
#               + PNG ottimizzato (pngquant) come fallback ridotto
#   - video:    genera MP4 H.264 (faststart, no audio) + WebM VP9
#               + poster JPG dal frame 1
# Originali preservati in _originals/

set -euo pipefail

PROD_DIR="$(cd "$(dirname "$0")" && pwd)/products/hypertrimmer"
REV_DIR="$(cd "$(dirname "$0")" && pwd)/reviews/hypertrimmer"

cwebp_q() {
  # cwebp_q SRC DST QUALITY MAX_DIM
  local src="$1" dst="$2" q="$3" max="$4"
  cwebp -quiet -q "$q" -m 6 -resize 0 0 -mt -metadata none "$src" -o "$dst.tmp"
  if [[ -n "${max:-}" && "$max" != "0" ]]; then
    cwebp -quiet -q "$q" -m 6 -resize "$max" 0 -mt -metadata none "$src" -o "$dst"
    rm -f "$dst.tmp"
  else
    mv "$dst.tmp" "$dst"
  fi
}

png_resize_quant() {
  # png_resize_quant SRC DST_PNG MAX_DIM QUALITY_RANGE
  local src="$1" dst="$2" max="$3" qrange="$4"
  local tmp="${dst}.resize.png"
  sips --resampleWidth "$max" "$src" --out "$tmp" >/dev/null
  pngquant --quality="$qrange" --strip --force --speed 1 --output "$dst" "$tmp"
  rm -f "$tmp"
}

echo "=== IMMAGINI PRODOTTO ==="
# hero.png — mostrato max 520x520 desktop, retina 1040
png_resize_quant "$PROD_DIR/_originals/hero.png" "$PROD_DIR/hero.png" 1040 70-90
cwebp -quiet -q 80 -m 6 -resize 1040 0 -mt -metadata none "$PROD_DIR/_originals/hero.png" -o "$PROD_DIR/hero.webp"
cwebp -quiet -q 78 -m 6 -resize 520 0 -mt -metadata none "$PROD_DIR/_originals/hero.png" -o "$PROD_DIR/hero-sm.webp"

# feature-2.png — mostrato 540x400, retina 1080
png_resize_quant "$PROD_DIR/_originals/feature-2.png" "$PROD_DIR/feature-2.png" 1080 70-90
cwebp -quiet -q 80 -m 6 -resize 1080 0 -mt -metadata none "$PROD_DIR/_originals/feature-2.png" -o "$PROD_DIR/feature-2.webp"

# package.png — mostrato 640x480, retina 1280
png_resize_quant "$PROD_DIR/_originals/package.png" "$PROD_DIR/package.png" 1280 70-90
cwebp -quiet -q 80 -m 6 -resize 1280 0 -mt -metadata none "$PROD_DIR/_originals/package.png" -o "$PROD_DIR/package.webp"

echo "=== IMMAGINI REVIEW (avatar grandi) ==="
# review-1..6.png — usate come avatar full-width della card, max ~400px → retina 800
for n in 1 2 3 4 5 6; do
  src="$REV_DIR/_originals/review-$n.png"
  png_resize_quant "$src" "$REV_DIR/review-$n.png" 800 65-85
  cwebp -quiet -q 78 -m 6 -resize 800 0 -mt -metadata none "$src" -o "$REV_DIR/review-$n.webp"
  # mini-avatar 24x24 per il rating del form (retina 48)
  cwebp -quiet -q 80 -m 6 -resize 96 0 -mt -metadata none "$src" -o "$REV_DIR/review-$n-mini.webp"
done

echo "=== EXPERT (160x160) ==="
# mostrato 160x160, retina 320
png_resize_quant "$REV_DIR/_originals/expert.png" "$REV_DIR/expert.png" 320 65-85
cwebp -quiet -q 80 -m 6 -resize 320 0 -mt -metadata none "$REV_DIR/_originals/expert.png" -o "$REV_DIR/expert.webp"

echo "=== POPUP (40x40) ==="
# popup-1..4.png — mostrati ~40px, retina 80px (lasciamo 96 di sicurezza)
for n in 1 2 3 4; do
  src="$REV_DIR/_originals/popup-$n.png"
  png_resize_quant "$src" "$REV_DIR/popup-$n.png" 96 65-85
  cwebp -quiet -q 80 -m 6 -resize 96 0 -mt -metadata none "$src" -o "$REV_DIR/popup-$n.webp"
done

echo "=== VIDEO ==="
# I video originali sono 720x1280 a ~9-12 Mbps con audio. Sono muted e in loop.
# Riduciamo a 540x960 (1.5x del display 540x400 con object-fit), CRF moderato, no audio.
for v in feature-1 feature-3; do
  src="$PROD_DIR/_originals/$v.mp4"
  echo "  -> $v.mp4 H.264"
  ffmpeg -y -loglevel error -i "$src" \
    -an -movflags +faststart \
    -vf "scale=540:-2:flags=lanczos" \
    -c:v libx264 -preset slow -crf 26 -profile:v high -level 4.0 -pix_fmt yuv420p \
    "$PROD_DIR/$v.mp4"
  echo "  -> $v.webm VP9"
  ffmpeg -y -loglevel error -i "$src" \
    -an -vf "scale=540:-2:flags=lanczos" \
    -c:v libvpx-vp9 -b:v 0 -crf 33 -row-mt 1 -tile-columns 2 -threads 4 \
    -deadline good -cpu-used 2 \
    "$PROD_DIR/$v.webm"
  echo "  -> $v-poster.jpg"
  ffmpeg -y -loglevel error -ss 0.2 -i "$src" -frames:v 1 \
    -vf "scale=540:-2:flags=lanczos" \
    -q:v 5 "$PROD_DIR/$v-poster.jpg"
  jpegoptim --strip-all --max=82 "$PROD_DIR/$v-poster.jpg" >/dev/null
done

echo "=== DONE ==="
