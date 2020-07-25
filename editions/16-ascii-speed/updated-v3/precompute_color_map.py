import asciiart
import json

if __name__ == "__main__":
    color_map = {}
    for r in range(256):
        print(r)
        color_map[r] = {}
        for g in range(256):
            color_map[r][g] = {}
            for b in range(256):
                col = asciiart.rgb_to_ansi((r, g, b))
                color_map[r][g][b] = col

    asciiart.PrecomputedRgbToAnsiConverterBytes.write_color_map(
        "./color_map.bin",
        color_map,
    )

