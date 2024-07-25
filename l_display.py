import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import lxml.etree as ET
import os


def create_gui():
    """
    Create the graphical user interface (GUI) for editing MEI files.

    This function creates a GUI with an image display, text fields for editing,
    and buttons for navigating and saving changes.
    """
    mei_folder = "Liber Usualis - mei5"
    image_folder = "YOUR FOLDER HERE"
    index = 1

    # Find the first existing image file
    while True:
        image_file = f"liber_{index:04d}.jpg"
        image_path = os.path.join(image_folder, image_file)
        if os.path.exists(image_path):
            break
        index += 1
        if index > 2340:  # assume max 9999 images
            print("No image files found!")
            return

    # Create the GUI
    window = tk.Tk()
    window.title("MEI Editor")

    # Create a label to display the current index
    index_label = ttk.Label(window, text=f"Page {index:04d}")
    index_label.pack(fill="x", padx=5, pady=5)

    # Create a slider to change the size of the rectangles
    scale_slider = ttk.Scale(window, from_=0.1, to=5, orient="horizontal")
    scale_slider.set(1)  # Initial value
    scale_slider.pack(fill="x", padx=5, pady=5)
    # Create a label to display the current scale
    scale_label = ttk.Label(window, text=f"Scale: {scale_slider.get():.2f}")
    scale_label.pack(fill="x", padx=5, pady=5)

    # Function to update the image and MEI file based on the index
    def update_image(event=None):
        """
        Update the image and MEI file based on the current index.

        This function is called when the user navigates to a new page or adjusts the scale.
        It updates the image display, text fields, and scale label.
        """
        nonlocal index
        mei_file = f"{index:04d}_corr - mei5.mei"
        mei_path = os.path.join(mei_folder, mei_file)
        tree = ET.parse(mei_path)
        root = tree.getroot()

        image_file = f"liber_{index:04d}.jpg"
        image_path = os.path.join(image_folder, image_file)
        image = Image.open(image_path)
        image = image.resize(
            (image.width // 4, image.height // 4)
        )  # Scale the image down by the current scale
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Draw rectangles on the image based on the zone elements

        zones = root.findall(".//{http://www.music-encoding.org/ns/mei}zone")
        draw = ImageDraw.Draw(image)
        scale = scale_slider.get()  # Get the current scale from the slider
        i = -1
        colours = [
            "red",
            "yellow",
            "green",
            "brown",
            #           "scarlet"
            "black",
            #           "ochre"
            #           "peach"
            #           "ruby"
            "olive",
            "violet",
            #           "fawn"
            #           "lilac"
            "gold",
            "chocolate",
            #           "mauve"
            #           "cream"
            "crimson",
            "silver",
            #           "rose"
            "azure",
            #           "lemon"
            #           "russet"
            "grey",
            "purple",
            #           "white"
            "pink",
            "orange",
            "blue",
        ]
        for elem in root.findall(".//{http://www.music-encoding.org/ns/mei}l"):
            facs = elem.get("facs").strip("#")
            i += 1

            for zone in zones:

                if (
                    zone.get("{http://www.w3.org/XML/1998/namespace}id")
                    and zone.get("{http://www.w3.org/XML/1998/namespace}id") == facs
                ):
                    ulx, uly, lrx, lry = (
                        int(int(zone.get("ulx")) * scale) // 4,
                        int(int(zone.get("uly")) * scale) // 4,
                        int(int(zone.get("lrx")) * scale) // 4,
                        int(int(zone.get("lry")) * scale) // 4,
                    )
                    draw.rectangle(
                        [(ulx, uly), (lrx, lry)], outline=colours[i % len(colours)]
                    )

        photo = ImageTk.PhotoImage(image)

        # Update the image label
        image_label.config(image=photo)
        image_label.image = photo

        # Clear the text frame
        for widget in text_frame.winfo_children():
            widget.destroy()

        # Update the text fields
        text_fields.clear()
        for i, elem in enumerate(
            root.findall(".//{http://www.music-encoding.org/ns/mei}l")
        ):
            label = ttk.Label(
                text_frame, text=f"Line {i+1} ({colours[i%len(colours)]}):"
            )
            label.grid(row=i, column=0, padx=5, pady=5)
            # Create a colored frame to wrap the Entry widget
            text_field = ttk.Entry(text_frame, width=50)
            text_field.insert(0, elem.text)
            text_field.grid(row=i, column=1, padx=5, pady=5)
            text_fields.append(text_field)  # Function to increment the index
        index_label.config(text=f"Page: {index:04d}")
        scale_label.config(text=f"Scale: {scale_slider.get():.2f}")

    def increment_index():
        """
        Increment the index to display the next page.

        This function is called when the user clicks the "+" button or presses the right arrow key.
        """
        nonlocal index
        while True:
            index += 1
            image_file = f"liber_{index:04d}.jpg"
            image_path = os.path.join(image_folder, image_file)
            if os.path.exists(image_path):
                update_image()
                break
            elif index > 2341:  # assume max 2341 images
                index = 1
                update_image()
                break

    def decrement_index():
        """
        Decrement the index to display the previous page.

        This function is called when the user clicks the "-" button or presses the left arrow key.
        """
        nonlocal index
        while True:
            index -= 1
            if index < 1:
                image_file = "liber_0001.jpg"
                image_path = os.path.join(image_folder, image_file)
                if os.path.exists(image_path):
                    update_image()
                    break
                else:
                    index = 2341
            image_file = f"liber_{index:04d}.jpg"
            image_path = os.path.join(image_folder, image_file)
            if os.path.exists(image_path):
                update_image()
                break

    scale_slider.bind("<ButtonRelease-1>", lambda event: update_image())
    # Bind arrow keys to increment and decrement index
    window.bind("<Right>", lambda event: increment_index())
    window.bind("<Left>", lambda event: decrement_index())

    # Load the initial image
    mei_file = f"{index:04d}_corr - mei5.mei"
    mei_path = os.path.join(mei_folder, mei_file)
    tree = ET.parse(mei_path)
    root = tree.getroot()

    image_file = f"liber_{index:04d}.jpg"
    image_path = os.path.join(image_folder, image_file)
    image = Image.open(image_path)
    image = image.resize(
        (image.width // 4, image.height // 4)
    )  # Scale the image down by a factor of two

    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = ttk.Label(window, image=photo)
    image_label.image = photo
    image_label.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a canvas and a frame inside the canvas
    text_canvas = tk.Canvas(window, width=400, height=400)
    text_canvas.pack(side=tk.LEFT, fill="both", expand=True)

    text_frame = ttk.Frame(text_canvas)
    text_frame_id = text_canvas.create_window((0, 0), window=text_frame, anchor="nw")

    # Create a scrollbar and associate it with the canvas
    text_scrollbar = ttk.Scrollbar(window, orient="vertical", command=text_canvas.yview)
    text_scrollbar.pack(side=tk.LEFT, fill="y")

    text_canvas.configure(yscrollcommand=text_scrollbar.set)

    # Iterate over the <l> elements and create a text field for each one
    text_fields = []
    for i, elem in enumerate(
        root.findall(".//{http://www.music-encoding.org/ns/mei}l")
    ):
        label = ttk.Label(text_frame, text=f"Line {i+1}:")
        label.grid(row=i, column=0, padx=5, pady=5)

        text_field = ttk.Entry(text_frame, width=50)
        text_field.insert(0, elem.text)
        text_field.grid(row=i, column=1, padx=5, pady=5)
        text_fields.append(text_field)

    # Update the scroll region of the canvas
    text_frame.update_idletasks()
    text_canvas.configure(scrollregion=text_canvas.bbox("all"))

    # Add buttons to increment and decrement the index
    index_frame = ttk.Frame(window)
    index_frame.pack(fill="x")

    decrement_button = ttk.Button(index_frame, text="-", command=decrement_index)
    decrement_button.pack(side=tk.LEFT, padx=5, pady=5)

    increment_button = ttk.Button(index_frame, text="+", command=increment_index)
    increment_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Add a button to save the changes
    save_button = ttk.Button(
        index_frame,
        text="Save",
        command=lambda: save_changes(
            window, tree, text_fields, f"{mei_file[:-4]}_TEXT.mei"
        ),
    )
    save_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Start the GUI event loop
    window.mainloop()


def save_changes(window, tree, text_fields, filename):
    """
    Save the edited text fields to a new MEI file.

    This function is called when the user clicks the "Save" button.
    It updates the MEI file with the edited text fields and saves it to a new file.
    """
    # Iterate over the text fields and update the corresponding <l> elements
    for i, elem in enumerate(
        tree.findall(".//{http://www.music-encoding.org/ns/mei}l")
    ):
        elem.text = text_fields[i].get()

    # Create a new MEI file with the updated contents
    new_tree = ET.ElementTree(tree.getroot())
    new_tree.write(
        f"{filename[:-4]} new-text.mei", encoding="utf8", xml_declaration=True
    )


# Example usage
create_gui()
