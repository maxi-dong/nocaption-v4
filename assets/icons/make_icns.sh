#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

build_icon() {
  local base_png="$1"
  local name="$2"
  local iconset_dir="${name}.iconset"

  rm -rf "$iconset_dir"
  mkdir -p "$iconset_dir"

  sips -z 16 16     "$base_png" --out "$iconset_dir/icon_16x16.png" >/dev/null
  sips -z 32 32     "$base_png" --out "$iconset_dir/icon_16x16@2x.png" >/dev/null
  sips -z 32 32     "$base_png" --out "$iconset_dir/icon_32x32.png" >/dev/null
  sips -z 64 64     "$base_png" --out "$iconset_dir/icon_32x32@2x.png" >/dev/null
  sips -z 128 128   "$base_png" --out "$iconset_dir/icon_128x128.png" >/dev/null
  sips -z 256 256   "$base_png" --out "$iconset_dir/icon_128x128@2x.png" >/dev/null
  sips -z 256 256   "$base_png" --out "$iconset_dir/icon_256x256.png" >/dev/null
  sips -z 512 512   "$base_png" --out "$iconset_dir/icon_256x256@2x.png" >/dev/null
  sips -z 512 512   "$base_png" --out "$iconset_dir/icon_512x512.png" >/dev/null
  cp "$base_png" "$iconset_dir/icon_512x512@2x.png"

  iconutil -c icns "$iconset_dir"
  rm -rf "$iconset_dir"
}

build_icon "nocaption_v1_1024.png" "nocaption_v1"
build_icon "nocaption_v2_1024.png" "nocaption_v2"
