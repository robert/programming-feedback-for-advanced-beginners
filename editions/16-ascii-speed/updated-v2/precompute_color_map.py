import asciiart
import json

if __name__ == "__main__":
    color_map = {}
    for r in range(256):
        print(r)
        for g in range(256):
            for b in range(256):
                rgb = (r, g, b)
                col = asciiart.rgb_to_ansi(rgb)
                color_map[str(rgb)] = col

    asciiart.PrecomputedRgbToAnsiConverter.write_color_map(
        "./color_map.json",
        color_map,
    )

