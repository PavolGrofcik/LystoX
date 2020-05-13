"""
Controller class to represent an implementation of the business logic
"""
import os
import cv2
import copy as cp
import yaml
import logging
import pandas as pd
import qimage2ndarray as img_2_q
from model.directory import Directory
from model.image import Image

FILE_CONFIG = './resources/configs/config.yaml'
LOGGER_NAME = 'app_logger.'

logger = logging.getLogger(LOGGER_NAME + __name__)


class Controller:
    """
    Controller class is middle point between view and model
    All changes in model after user interactions are done
    using this class methods.

    Primary role is separation of concerns and ease off
    development with code readability of this application.
    """

    def __init__(self):
        self.dir = None
        self.Image = None
        self.Image_prev = None
        self.prev = None
        self.im_data = None
        self.im_data_cp = None
        self.qimage = None
        self.im_size = None
        self.new_name = None
        self.metadata = None
        self.config = None
        self.dst = None
        self.autosave = None
        self.original = None
        self.is_format = None
        self.labels = None
        self.load_config()
        logger.info('Controller initialization successful!')

    def load_config(self):
        """
        Method loads a config file
        :return: None
        """

        with open(FILE_CONFIG, 'r') as f:
            self.config = yaml.full_load(f)
            self.load_auto_save()
            self.load_labels_file()
        logger.debug(f'Config successfully loaded!')

    def load_cfg_directory(self):
        """
        Method directly loads directory from config file
        if config is specified

        :return: Booelan
        """

        if self.config is None:
            return False
        self.load_cfg_destination()

        if self.check_cfg_directory():
            self.dir = Directory(self.config['directory'][0],
                                 self.dst, self.labels)
            self.Image = self.dir.iter_act()
            self.initialize_images()
            self.load_metadata()
            logger.debug(f'Source config directory successfully loaded!')
            return True
        return False

    def check_cfg_directory(self):
        """
        Method checks if config path is valid
        path and declared directory is not
        empty

        :return: Boolean
        """

        if self.config and \
                self.config['directory'] is not None:
            dir = self.config['directory'][0]
            if os.path.exists(dir) and \
                    os.path.isdir(dir):
                dir = [x for x in os.listdir(dir) if \
                       os.path.exists(os.path.join(dir, x))]
                if len(dir) == 0:
                    return False
                else:
                    return True
            else:
                return False
        return False

    def load_cfg_destination(self):
        """
        Method loads destination from
        config file

        :return: None
        """

        if self.config:
            if self.config['destination'] is not None:
                self.dst = self.config['destination'][0]
                logger.debug(f'Destination config dir {self.dst}'
                             f' successfully loaded')

    def load_auto_save(self):
        """
        Method loads autosave option
        from a config file

        :return: None
        """

        if self.config and self.config['autosave']:
            option = self.config['autosave']['enabled']
            origin_opt = self.config['autosave']['original_img']
            format_opt = self.config['autosave']['format']
            if option is True or option is False:
                self.autosave = option
            if origin_opt is True or origin_opt is False:
                self.original = origin_opt
            if format_opt in Image.formats:
                self.is_format = format_opt
            logger.debug(f'Parameters autosave: {self.autosave}'
                         f', save original: {self.original}'
                         f', image format: {self.is_format}')

    def load_labels_file(self):
        """
        Method loads labels name of csv file

        :return: None
        """

        if self.config and self.config['metadata']:
            self.labels = self.config['metadata'][0]
            logger.debug(f'Metadata file: {self.labels}')

    def open_directory(self, path, is_file=False):
        """
        Method loads directory and first image in it after user input is given

        :param is_file: Boolean if user opened file
        :param path: Directory path
        :return: None
        """

        if is_file:
            self.dir = Directory('/'.join(path.split('/')[:-1]), self.dst)
            self.Image = self.dir.img_from_images(path.replace('/', '\\'))
        else:
            self.dir = Directory(path, self.dst)
            self.Image = self.dir.iter_act()
        logger.debug(f'Images successfully loaded!')

        if self.Image is not None:
            self.initialize_images()
            self.load_metadata()
            logger.debug(f'Metadata file successfully loaded!')

    def load_metadata(self):
        """
        Method loads metadata into pd.Dataframe
        if there is in loaded directory

        :return: Inplace
        """

        if self.dir is not None:
            self.metadata = self.dir.get_metadata()
            if self.metadata is not None:
                self.metadata = pd.read_csv(self.metadata)

    def set_dst_directory(self, path):
        """
        Method sets user given destination directory

        :param path: Path to directory
        :return: None
        """

        logger.debug(f'Destination directory path:  {path}')
        if self.dir is not None:
            self.dir.set_destination_directory(path)

    def initialize_images(self):
        """
        Method loads another image from loaded directory

        :return: None
        """

        if self.Image is not None:
            self.Image = self.Image.reload()
            self.Image_prev = cp.deepcopy(self.Image)
            self.Image_prev.name = self.Image_prev.name.split('.')[0] + '_mask' + self.Image_prev.format
            self.im_size = self.Image.get_shape()
            logger.debug(f'Image initialization successful!')

    def load_next_image(self, prev=False):
        """
        Method loads next image from open directory

        :return: None
        """

        if not prev:
            self.Image = self.dir.iter_next()
            self.initialize_images()
        else:
            self.Image = self.dir.iter_prev()
            self.initialize_images()

    def get_image_data(self, preview=False):
        """
        Method returns objects to build source and preview image

        :return: qimage data and qimage name
        """

        if self.Image is not None and self.Image_prev is not None:
            if preview:
                return self.np_array_to_qimage(self.Image_prev), self.Image_prev.get_image_name()
            else:
                return self.np_array_to_qimage(self.Image), self.Image.get_image_name()

    def np_array_to_qimage(self, Image=None):
        """
        Method that converts image numpy array to qimage object
        and BGR to RGB color space
        :return: QImage object
        """

        if Image is not None and \
                Image.img is not None:
            img = cv2.cvtColor(Image.img, cv2.COLOR_BGR2RGB)
            logger.debug(f'Image data to qimage data converted!')
            return img_2_q.array2qimage(img)

    def load_selected_image(self, image_num):
        """
        Method loads the image from the image_num
        if is the valid index in the loaded directory
        :param image_num: Index of the images
        :return: Boolean
        """

        image_num = self.parse_str_to_int(image_num)
        logger.debug(f'Image number to be loaded: {image_num}')

        if not isinstance(image_num, int):
            return False
        else:
            Image = self.dir.img_from_index(image_num)
            if Image:
                self.Image = Image
                self.initialize_images()
                return True
            return False

    def is_empty_directory(self):
        """
        Method tests whether loaded directory does not contain
        any supported images

        :return: Boolean
        """

        return self.dir.is_empty()

    def save_preview_image(self, name=None, format=None, dst=None):
        """
        Method first updates Image data (numpy array)
        and then saves the image.

        :return: None
        """

        if name is None or name == "":
            self.Image_prev.save(self.Image_prev.name, dst=self.dir.dst)
        else:
            if dst is not None:
                if format is not None:
                    self.Image_prev.save(name, format=format, dst=dst)
                else:
                    self.Image_prev.save(name, dst=dst)
            else:
                if format is not None:
                    self.Image_prev.save(name, format=format, dst=self.dir.dst)
                else:
                    self.Image_prev.save(name, dst=self.dir.dst)
        logger.debug(f'Image mask successfully saved!')

    def save_preview_mask(self, name=None, format=None):
        """
        Method saves preview mask to destination directory
        If metadata file is loaded, then it compares found
        cells vs number of cells in .csv file and saves on
        match/unmatch to proper destination directory.

        :param name: Name of preview mask
        :return:
        """

        if name is None or name == '':
            name = self.Image_prev.name
            logger.debug(f'Image mask name: {name}')

        if self.metadata is not None:
            if self.Image_prev.masked:
                if self.analyze_contours():
                    self.Image_prev.save(name, format, dst=self.dir.dst)
                else:
                    self.Image_prev.save(name, format, dst=self.dir.dst_diff)
            else:
                if not int(self.get_lymphocytes(self.Image.name)):
                    self.Image_prev.save(name, format, dst=self.dir.dst)
                else:
                    self.Image_prev.save(name, format, dst=self.dir.dst_diff)
        else:
            self.Image_prev.save(name, format, dst=self.dir.dst)
        logger.debug(f'Image mask successfully saved!')

    def save_source_image(self, name=None):
        """
        Method saves source image to destination directory

        :param name: Name of the source image
        :return: None
        """

        if name is None or name == '':
            name = self.Image.name
        self.Image.save_original(name, self.is_format, self.dir.dst_origin)
        logger.debug(f'Image original successfully saved!')

    def get_lymphocytes(self, img_name):
        """
        Method returns number of lymphocytes

        :param img_name: image_name
        :return: String of lymphocytes
        """

        if self.metadata is not None:
            img_name = img_name.split('.')[0]
            num = self.metadata[self.metadata['x'] == img_name]['y'].values[0]
            logger.debug(f'Lymphocytes count: {num}')
            return str(num)
        else:
            return 'No metadata found!'

    def get_img_index(self):
        """
        Method returns actual index of the image
        :return: str
        """

        return str(self.dir.get_img_seq(self.Image.path))

    def get_imgs_length(self):
        """
        Method returns a number of all loaded images
        :return: str
        """

        return '/ ' + str(self.dir.get_imgs_len())

    def highlight_borders(self):
        """
        Method highlights borders of the source image
        :return: None
        """

        if self.Image is not None:
            self.Image.highlight_borders()

    def fill_pixels(self, x, y):
        """
        Method highlights pixel in the
        source image

        :param x: x position of pixel
        :param y: y position of pixel
        :return: None
        """

        if self.Image is not None:
            self.Image.fill_4n_pixels(x, y)

    def threshold_image(self, threshold, neighbours):
        """
        Methods thresholds preview image

        :param threshold: threshold value
        :param neighbours: neighbours value
        :return: None
        """

        if self.Image_prev is not None:
            threshold = self.parse_str_to_int(threshold)
            neighbours = self.parse_str_to_int(neighbours)

            if threshold is not None and neighbours is not None:
                self.Image_prev.adaptive_threshold(threshold, neighbours)
        logger.debug(f'Image preview successfully thresholded!')

    def parse_str_to_int(self, input):
        """
        Method tries to parse user give input
        to int for next processing

        :param input: str value from user
        :return: parsed input or None
        """

        logger.debug(f'Input to parse: {input}')
        try:
            return int(input)
        except:
            return None

    def parse_listview_items(self, items):
        """
        Method parses items from listwidget
        to list of tuple

        :param items: List of str in listwidget
        :return: List of tuples or None
        """

        logger.debug(f'Items to parse: {items}')
        if items is not None:
            coords = []
            for item in items:
                item = item.split(' ')
                item = (int(item[1]), int(item[3]))
                # Scaling
                if self.Image.scaled:
                    x = item[0] / self.Image.sf_x if self.Image.sf_x < 1 \
                        else item[0] / self.Image.sf_x
                    y = item[1] / self.Image.sf_y if self.Image.sf_y < 1 \
                        else item[1] / self.Image.sf_y
                    item = (int(x), int(y))
                coords.append(item)
            return coords

    def parse_info_to_save_as(self, path, format):
        """
        Method parses parameters to correct format to
        save image

        :param path: Path where to be saved
        :param format: Format as to be saved
        :return: parsed name, path, format
        """

        name = path.split('/')[-1]
        path = '\\'.join(path.split('/')[:-1]) + '\\'
        logger.debug(f'Parsed name: {name}'
                     f' parsed path: {path}'
                     f' parsed format: {format}')

        return name, format, path

    def to_growing_region(self, coord_items, thresh, neigh):
        """
        Method process input arguments and
        invokes growing region in preview
        Image

        :param neigh: Number of neighbours
        :param thresh: Value of threshold
        :param coord_items: Coordinates X,Y - List of tuples
        :return: Inplace
        """

        logger.debug(f'Function args: {coord_items},'
                     f' {thresh}, {neigh}')
        coords = self.parse_listview_items(coord_items)
        thresh = self.parse_str_to_int(thresh)
        neigh = self.parse_str_to_int(neigh)
        if coords is not None:
            self.Image_prev.growing_region(coords, thresh, neigh)

    def to_morphological_open(self, x, y, element=None, size=None):
        """
        Method applies morphological opening
        to region with x,y position

        :param element: Structuring element
        :param size: Specified size of the element
        :param x: x positon of the object
        :param y: y position of the object
        :return: None
        """

        if size % 2 == 0:
            size = size + 1

        center = self.Image_prev.region_open(x, y, element, size)
        if center:
            rows = []
            for item in center:
                if self.Image.scaled:
                    x = item[0] * self.Image.sf_x if self.Image.sf_x < 1 \
                        else item[0] * self.Image.sf_x
                    y = item[1] * self.Image.sf_y if self.Image.sf_y < 1 \
                        else item[1] * self.Image.sf_y
                    item = (int(x), int(y))
                rows.append('X: ' + str(item[0]) + ' Y: ' + str(item[1]))
            logger.debug(f'Morphological open successful!')
            return rows

    def find_positions_not_in_mask(self, coords):
        """
        Method finds coordinates that does not
        belong to mask
        :param coords: list of item form listwidget
        :return: list of found coordinates
        """

        coords = self.parse_listview_items(coords)
        list = self.Image_prev.not_in_mask(coords)
        logger.debug(f'Image coords: {coords}, found: {list}')

        if len(list) > 0:
            rows = []
            for item in list:
                if self.Image.scaled:
                    x = item[0] * self.Image.sf_x if self.Image.sf_x < 1 \
                        else item[0] * self.Image.sf_x
                    y = item[1] * self.Image.sf_y if self.Image.sf_y < 1 \
                        else item[1] * self.Image.sf_y
                    item = (int(x), int(y))
                rows.append('X: ' + str(item[0]) + ' Y: ' + str(item[1]))
            return rows

    def merge_regions(self, coord_items):
        """
        Method merges regions together

        :param coord_items: list of coordinates
        :return: None
        """

        coords = self.parse_listview_items(coord_items)
        self.Image_prev.merge_regions(coords)
        logger.debug(f'Image regions merged successfully!')

    def find_centers(self):
        """
        Method finds new centers of regions
        :return: list of found centers
        """

        centers = []
        rows = []
        centers = self.Image_prev.find_centers()

        if len(centers) > 0:
            for item in centers:
                if self.Image.scaled:
                    x = item[0] * self.Image.sf_x if self.Image.sf_x < 1 \
                        else item[0] * self.Image.sf_x
                    y = item[1] * self.Image.sf_y if self.Image.sf_y < 1 \
                        else item[1] * self.Image.sf_y
                    item = (int(x), int(y))
                rows.append('X: ' + str(item[0]) + ' Y: ' + str(item[1]))
            logger.debug(f'Image regions centers found successfully!')
            return rows

    def delete_region(self, x, y, coords):
        """
        Method deletes selected region with position x,y

        :param x: x position of the region
        :param y: y position of the region
        :param coords: list of coordinates
        :return: list of other regions position
        """

        new = []
        coords = self.parse_listview_items(coords)

        rest = self.Image_prev.delete_region(x, y, coords)

        if len(rest) > 0:
            rows = []
            for item in rest:
                if self.Image.scaled:
                    x = item[0] * self.Image.sf_x if self.Image.sf_x < 1 \
                        else item[0] * self.Image.sf_x
                    y = item[1] * self.Image.sf_y if self.Image.sf_y < 1 \
                        else item[1] * self.Image.sf_y
                    item = (int(x), int(y))
                rows.append('X: ' + str(item[0]) + ' Y: ' + str(item[1]))
            logger.debug(f'Image region X: {x}, Y: {y} deleted successfully!')
            return rows
        return None

    def get_contours(self):
        """
        Method returns count of found contours
        :return: Str count of found contours
        """

        if not self.Image_prev.contours:
            self.Image_prev.find_countours()
        return str(len(self.Image_prev.contours))

    def analyze_contours(self):
        """
        Method analyzes number of contours and
        number of lymphocytes for the image
        :return: None
        """

        if self.metadata is not None:
            self.Image_prev.find_countours()
            num = int(self.get_lymphocytes(self.Image.name))
            if len(self.Image_prev.contours) == num or (num == 0 and len(self.Image_prev.contours) == 0):
                return True
            else:
                return False


if __name__ == '__main__':
    Cnt = Controller()
