if __name__ == "__main__":

    import argparse
    from subprocess import call

    parser = argparse.ArgumentParser(description='Extract faces from given image')

    parser.add_argument('image_path', metavar = 'image_path',
                        help = 'image path');
    args = parser.parse_args()
    
    image_path = args.image_path;

    command = "python extract_faces_from_image.py " +  image_path

    call("python extract_faces_from_image.py test.jpg", shell=True)


