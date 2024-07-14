import numpy as np
from solid import *
from solid import scad_render_to_file

# Braille dictionary (complete for demonstration)
braille_dict = {
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100',
    'f': '111000', 'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100',
    'k': '100010', 'l': '101010', 'm': '110010', 'n': '110110', 'o': '100110',
    'p': '111010', 'q': '111110', 'r': '101110', 's': '011010', 't': '011110',
    'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011', 'y': '110111',
    'z': '100111', ' ': '000000'
}

def text_to_braille(text):
    return [braille_dict.get(char, '000000') for char in text.lower()]

def generate_braille_stl(text, filename):
    braille_text = text_to_braille(text)
    unit_height = 0.1  # height of the Braille dots
    unit_radius = 0.05  # radius of the Braille dots
    dot_spacing = 0.2  # spacing between Braille dots
    line_spacing = 0.3  # spacing between lines of Braille
    char_spacing = 0.4  # spacing between Braille characters

    postcard_length = 6.0
    postcard_width = 4.0
    postcard_height = 0.1
    margin = 0.1  # margin from the edge

    braille_group = []
    x_offset = margin
    y_offset = margin

    for braille_char in braille_text:
        if x_offset + char_spacing >= postcard_length - margin:
            x_offset = margin
            y_offset += line_spacing

        if y_offset + dot_spacing * 2 >= postcard_width - margin:
            print("Warning: Text too long to fit on postcard")
            break

        dots = [(x_offset + dot_spacing * (i % 2),
                 y_offset + dot_spacing * (i // 2),
                 unit_height if braille_char[i] == '1' else 0)
                for i in range(6)]
        
        for dot in dots:
            if dot[2] > 0:
                translated_sphere = translate(dot)(sphere(r=unit_radius))
                braille_group.append(translated_sphere)
                # Debugging: Print coordinates and object info
                print(f"Adding dot at {dot}: {translated_sphere}")
        
        x_offset += char_spacing

    postcard = cube([postcard_length, postcard_width, postcard_height])
    braille_model = union()(postcard, *braille_group)
    
    # Generate and save SCAD file for visualization
    scad_filename = filename.replace('.stl', '.scad')
    scad_render_to_file(braille_model, scad_filename)

    # Use OpenSCAD to convert SCAD to STL
    import os
    os.system(f"openscad -o {filename} {scad_filename}")

# Example usage
text = "Hello World"
filename = "braille_postcard.stl"
generate_braille_stl(text, filename)
