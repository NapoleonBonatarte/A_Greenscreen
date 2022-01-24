###
# Author: Tyler Windemuth
# Class: Csc 110
# Description: This program is a program that takes two (or three) ppm image files
#              and then uses these ppm files to put one ppm file over another, in
#              a way that is similar to a greenscreen. The program does this by taking
#              two input files, a color channel and channel difference. The program will then
#              go through and check the user input to make sure that the input is proper
#              then takes the inputs and uses the color channels to replace one imaage on top
#              of the other.


def get_image_dimensions_string(file_name):
    '''
    Given the file name for a valid PPM file, this function will return the
    image dimensions as a string. For example, if the image stored in the
    file is 150 pixels wide and 100 pixels tall, this function should return
    the string '150 100'.
    file_name: A string. A PPM file name.
    '''
    image_file = open(file_name, 'r')
    image_file.readline()
    return image_file.readline().strip('\n')


def load_image_pixels(file_name):
    ''' Load the pixels from the image saved in the file named file_name.
    The pixels will be stored in a 3d list, and the 3d list will be returned.
    Each list in the outer-most list are the rows of pixels.
    Each list within each row represents and individual pixel.
    Each pixels is representd by a list of three ints, which are the RGB values of that pixel.
    '''
    pixels = []
    image_file = open(file_name, 'r')

    image_file.readline()
    image_file.readline()
    image_file.readline()

    width_height = get_image_dimensions_string(file_name)
    width_height = width_height.split(' ')
    width = int(width_height[0])
    height = int(width_height[1])

    for line in image_file:
        line = line.strip('\n ')
        rgb_row = line.split(' ')
        row = []
        for i in range(0, len(rgb_row), 3):
            pixel = [int(rgb_row[i]), int(rgb_row[i+1]), int(rgb_row[i+2])]
            row.append(pixel)
        pixels.append(row)

    return pixels


def validate(channel, channel_difference, gs_file, fi_file):
    '''
    This functions validates inputs passed to it by checking if said
    inputs fall into the guidelines in the instructions
    :param channel: A string that should have only 1 character and equal a character in the
    color channel list
    :param channel_difference: A float that should be between 1 and 10
    :param gs_file: file name in string format
    :param fi_file: file name in string format
    :return:
    '''
    color_channel_list = ['r', 'g', 'b']  # color channels
    if not channel.lower() in color_channel_list:  # if channel is not in channel list quit program
        print('Channel must be r, g, or b. Will exit.')
        quit()
    if float(channel_difference) < 1.0 or float(
            channel_difference) > 10.0:  # if channel difference not between 1 and 10 quit program.
        print('Invalid channel difference. Will exit.')
        quit()

    if gs_file != 5:  # checks if files are being checked
        green_file = open(gs_file, 'r')
        back_file = open(fi_file,'r')
        green_data = green_file.readlines()
        back_data = back_file.readlines()
        green_file.close()
        back_file.close()
        if back_data[1][0] != green_data[1][0] or back_data[1][2] != green_data[1][2]:
            print('Images not the same size. Will exit.')  # ^ if file are of equal width
            quit()


def pixel_a(out,counter,channel, initial, second, third,width):
    '''
    This functions writes the output into the write file based off
    of the inputs passed to it.
    :param out: The file being written to.
    :param counter: an integer uses to determines if the write number
    of pixels are written to a file.
    :param channel: an integer that tells the functions what writing format
    to use.
    :param initial: an integer that contains the brightness of the R value
    of the pixel that will be written into the file.
    :param second: an integer that contains the brightness of the G value
    of the pixel that will be written into the file.
    :param third: an integer that contains the brightness of the B value
    of the pixel that will be written into the file.
    :param width: an integer of how wide the image file is.
    :return: the return is an integer called counter which is used
    to determine how many pixels to write to the out file.
    '''
    if channel == 0:  # r values changed
        counter += 1
        out.write(str(initial) + ' ' + str(second) + ' ' + str(third) + ' ')
    if channel == 1:  # g values changed
        counter += 1
        out.write(str(second) + ' ' + str(initial) + ' ' + str(third) + ' ')
    if channel == 2:  # b values changed
        counter += 1
        out.write(str(second) + ' ' + str(third) + ' ' + str(initial) + ' ')
    if counter == width:  # checks if proper amount of pixels inputted into file
        out.write('\n')
    return counter



def end_file(channel, channel_difference, initial_image, background_image, out_file):
    '''
    This function determines what to write to the outfile and
    calls the functions that write to the outfile, while also keeping track
    of the pixel count of out file.
    :param channel: A string that contains either an r,g, or b.
    This determines which color channel will be changed.
    :param channel_difference: A float that contains a value between 1 and 10
    that determines how the replacement algorithm will work.
    :param initial_image: Contains all of the information for the first image
    in the form of a list.
    :param background_image: Contains all of the information for the first image
    in the form of a list.
    :param out_file: a string that has the name of the file that the user
    wishes to user as their output file.
    :return:
    '''
    width = len(initial_image[0])
    if channel == 'r':  # sets channel lists
        channel,other_channel_one, other_channel_two = 0,1,2
    elif channel == 'g':
        channel,other_channel_one, other_channel_two = 1,0,2
    else:
        channel,other_channel_one, other_channel_two = 2,0,1
    out = open(out_file, 'w')
    out.write('P3\n')
    out.write(str(len(initial_image[0])) + ' ' + str(len(initial_image)) + '\n')
    out.write('255\n')
    for i in range(len(initial_image)):  # iterates through info in ppm file.
        counter = 0
        print(f'I {i}')
        for n in range(len(initial_image[i])):
            print(f'n {n}')
            initial = initial_image[i][n][channel]
            second = initial_image[i][n][other_channel_one]
            third = initial_image[i][n][other_channel_two]
            print(f'initial {initial}')
            print(f'second {second * channel_difference}')
            print(f'third {third * channel_difference}')
            if float((second * channel_difference)) >= initial or \
                    float((third * channel_difference)) >= initial:  # from picture a
                print('if')
                counter = pixel_a(out,counter,channel,initial,second,third,width)
            else:  # from picture b
                print('else')
                initial = background_image[i][n][channel]
                second = background_image[i][n][other_channel_one]
                third = background_image[i][n][other_channel_two]
                counter = pixel_a(out,counter,channel,initial,second,third,width)
    out.close()



def main():

    # Get the 5 input values from the user, as described in the PA specification
    # These input values will be validated later in main
    channel = input('Enter color channel\n')
    validate(channel,5,5,5)
    channel_difference = float(input('Enter color channel difference\n'))
    validate(channel, channel_difference, 5, 5)
    gs_file = input('Enter greenscreen image file name\n')
    fi_file = input('Enter fill image file name\n')
    validate(channel, channel_difference, gs_file, fi_file)
    out_file = input('Enter output file name\n')
    
    # Next, Do some valiation of the input values
    # The PA specification tells you what you need to validate
    validate(channel,channel_difference,gs_file,fi_file)
    if get_image_dimensions_string(fi_file) != get_image_dimensions_string(gs_file):
        quit('Dimension Error')

    # If the the input is valid, implement the greenscreen.
    # You should:
    #    * Load in the image data from the two input image files.
    #      Use the provided load_image_pixels functions for this!
    initial_image = load_image_pixels(gs_file)
    background_image = load_image_pixels(fi_file)
    #    * Generate a NEW image based on the two input values,
    #      using the greenscreen algorithm described in the specification
    end_file(channel,channel_difference,initial_image,background_image,out_file)
    print('Output file written. Exiting.')
    #    * Save the newly-generated image to a file
    # You probably will want to create other function(s) that you call from here.


main()
