import sys
from PIL import Image

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc >= 2:
        image_path = sys.argv[1]
        dest_image_width: int = 0 if argc < 3 else int(sys.argv[2])
        image = Image.open(image_path)
        if dest_image_width > 0:
            dest_image_height = image.height * dest_image_width // image.width
            image = image.resize((dest_image_width, dest_image_height))

        output_image_gs2_data = []
        for y in range(0, image.height):
            for x in range(0, image.width):
                pixel = image.getpixel((x, y))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                a = 0
                if len(pixel) >= 4:
                    a = pixel[3]

                average = (r + g + b) / 3
                c = round((256 - average) / 256 * a / 256)
                output_image_gs2_data.append("11" if c else "00")
        # align to multiples of 4
        remainder = len(output_image_gs2_data) % 4
        for i in range(0, remainder):
            output_image_gs2_data.append("00")

        output_image_bytes = []
        index = 0
        output_image_gs2_data_len = len(output_image_gs2_data)
        while index < output_image_gs2_data_len:
            output_image_bytes.append(hex(int("0b{}{}{}{}".format(
                output_image_gs2_data[index + 3],
                output_image_gs2_data[index + 2],
                output_image_gs2_data[index + 1],
                output_image_gs2_data[index]
            ), 2)))
            index += 4
        print(f"Image:\n  width: {image.width}\n  height: {image.height}")
        print("Image data:")
        print(f"[{','.join(output_image_bytes)}]")
        print(f"Image data array length: {len(output_image_bytes)}")
        pass
    else:
        print("Usage: \n    python image2gs2.py logo.png [output_image_width]")
