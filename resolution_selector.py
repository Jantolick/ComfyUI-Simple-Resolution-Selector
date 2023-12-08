import re

SDXL = "SDXL"
SD21 = "SD21"
SD15 = "SD15"

# Resolution presets
BASE_RESOLUTIONS = [
    (1024, 1024, SDXL, "1:1"),
    (640, 1536, SDXL, "5:12"),
    (512, 512, SD15, "1:1"),
    (768, 768, SD15, "1:1"),
    (512, 768, SD15, "2:3"),
    (768, 512, SD15, "3:2"),
    (768, 1344, SDXL, "3:7"),
    (256, 256, SD15, "1:1"),
    (832, 1216, SDXL, "13:19"),
    (512, 512, SD21, "1:1"),
    (768, 768, SD21, "1:1"),
    (768, 512, SD21, "3:2"),
    (512, 768, SD21, "2:3"),    
    (896, 1152, SDXL, "7:9"),    
    (1152, 896, SDXL, "9:7"),
    (1216, 832, SDXL, "19:13"),
    (1344, 768, SDXL, "21:12"),    
    (1536, 640, SDXL, "12:5"),    
]


class SimpleResolutionSelector:
    """
    A node to provide a drop-down list of resolutions and returns two int values (width and height).
    Filterable on base model type, resolution and/or ratio.
    """

    def __init__(self):        
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return a dictionary which contains config for all input fields.
        """

        # Sort the list by base model type, then width, then height, and finally ratio
        sorted_array = sorted(BASE_RESOLUTIONS, key=lambda x: (x[2], x[0], x[1], x[3]))

        # Create a list of resolution strings for the drop-down menu, filterable by base model type and ratio
        resolution_strings = [
            f"{name} {width} x {height} [{ratio}]" for width, height, name, ratio in sorted_array]
        
        return {
            "required": {
                "base_resolution": (resolution_strings,)
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "select_resolution"
    CATEGORY = 'utils'

    def select_resolution(self, base_resolution):
        """
        Returns the width and height based on the selected resolution.

        Args:
            base_resolution (str): Selected resolution string.

        Returns:
            Tuple[int, int]: Adjusted width and height.
        """
        try:            
            matches = re.findall(r'\d+ x \d+', base_resolution.split('[')[0])[0].split('x')            
            width, height = map(int, matches)
        except ValueError:
            raise ValueError("Invalid base_resolution format.")
        
        width = int(width)
        height = int(height)

        return width, height


NODE_CLASS_MAPPINGS = {
    "SimpleResolutionSelector": SimpleResolutionSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleResolutionSelector": "Simple Resolution Selector",
}
