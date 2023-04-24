import gradio as gr
import skimage
import scipy
import numpy
import scipy
import os

# Define the inputs that will be shown in the web GUI
inputs = [
    gr.File(),
    gr.Radio(["Otsu", "Li"], type="value", value="Otsu", label="Threshold method"),
    gr.Number(value=5, interactive=True, label="Object minimum size"),
    gr.Number(value=20, interactive=True, label="Object max size"),
]

# Define the output
output = [
    gr.File(label="Download output")
]

def example_function(image_path, threshold_method, min_size, max_size):
    """
    Example function that will threshold, label, and then filter objects
    based on size.

    This function also save the array and returns the file save path. The file
    save path will be read by gr.File and allow the user to download the
    analysed image.
    """

    # Load the image
    image = skimage.io.imread(image_path.name)

    # Threshold the image
    if threshold_method.casefold() == "otsu":
        th_image = image > skimage.filters.threshold_otsu(image)
    elif threshold_method.casefold() == "li":
        th_image = image > skimage.filters.threshold_li(image)
    else:
        raise NotImplementedError
    
    # Label the image
    labeled_image = skimage.measure.label(th_image)

    areas = scipy.ndimage.sum(
        numpy.ones(labeled_image.shape),
        labeled_image,
        numpy.array(list(range(0, labeled_image.max() + 1)), dtype=numpy.int32),
    )
    areas = numpy.array(areas, dtype=int)
    min_allowed_area = numpy.pi * (min_size * min_size) / 4
    max_allowed_area = numpy.pi * (max_size * max_size) / 4
    # area_image has the area of the object at every pixel within the object
    area_image = areas[labeled_image]
    labeled_image[area_image < min_allowed_area] = 0
    labeled_image[area_image > max_allowed_area] = 0

    # Construct filename from input
    base_filename = os.path.basename(image_path.name).split(".")[0]
    base_dir = os.path.dirname(image_path.name)
    output_filename = os.path.join(base_dir, base_filename + "_output.tiff")
    
    # Save file
    skimage.io.imsave(output_filename, labeled_image)

    # Return the file name
    return output_filename

demo = gr.Interface(
    fn=example_function, 
    inputs=inputs, 
    outputs=output,
    title="Simple ID objects"
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)