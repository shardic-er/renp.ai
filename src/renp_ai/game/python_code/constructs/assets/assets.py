# game/python_code/constructs/assets.py

# Create default characters
default_characters = [Character(
    name="Unnamed Hero",
    description="A brave adventurer embarking on a mysterious journey.",
    # renpy_character=renpy.Character("Unnamed Hero", color="#ff0000")
)]

# Create a default location
default_location = Location(
    name="Mysterious Forest",
    description="A dense, fog-covered forest where the trees whisper secrets.",
    filepath="/cache/a_mystical_forest_at_dawn.png"  # Adjust to the correct path
)

# Create a default scene
default_scene = Scene(
    description="The journey begins in a mysterious forest at dusk.",
    location=default_location,
    characters=default_characters
)
