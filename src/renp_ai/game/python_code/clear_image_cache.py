import os
import glob

# Get the current script directory (python_code)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the cache directory relative to the python_code directory
cache_dir = os.path.join(current_dir, "..", "cache")

# Normalize the path to ensure it's correctly formatted
cache_dir = os.path.normpath(cache_dir)

# Define a whitelist of file names (without extensions)
whitelist = ["Mysterious_Forest"]


# Check if `log_message` is already defined
if 'log_message' not in globals():
    def log_message(message):
        # Write the message to the custom log file
        with open(os.path.join(config.gamedir, "log_custom.txt"), "a") as f:
            f.write(message + "\n")


def delete_unlisted_png_files(directory, whitelist):
    # print("Deleting unlisted .png files... from directory: ", directory)

    # Get all .png files in the directory
    png_files = glob.glob(os.path.join(directory, "*.png"))

    # Iterate through each .png file
    for filepath in png_files:
        # Extract the file name without the extension
        filename = os.path.basename(filepath).replace(".png", "")

        # If the file is not in the whitelist, delete it
        if filename not in whitelist:
            try:
                os.remove(filepath)
                log_message(f"Deleted: {filepath}")
            except Exception as e:
                log_message(f"Error deleting {filepath}: {str(e)}")


def print_cwd_with_game_dir():
    print(cache_dir)


if __name__ == "__main__":
    delete_unlisted_png_files(cache_dir, whitelist)
