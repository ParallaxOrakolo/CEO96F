from timeit import default_timer as now
import numpy as np
import pathlib
import cv2


def saveImages(dir_path, image_format, n_images, time, key_to_exit, key_to_save, camera_id):
    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    Breaks = False
    for x in range(n_images):
        t0 = now()
        while True:
            _, img = cap.read()
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            try:
                key = chr(key)
            except ValueError:
                pass
            if key == key_to_exit:
                print("Saindo...")
                Breaks = True
                break
            if not time:
                if key == key_to_save:
                    print("Salvando em:", f"{dir_path}{x}.{image_format}")
                    cv2.imwrite(f"{dir_path}{x}.{image_format}", img)
                    break
            else:
                if now() - t0 >= time:
                    print("Salvando em:", f"{dir_path}{x}.{image_format}")
                    cv2.imwrite(f"{dir_path}{x}.{image_format}", img)
                    cv2.waitKey(500)
                    break
        if Breaks:
            break
        cv2.destroyAllWindows()
        cap.release()


def calibrate_chessboard(dir_path, image_format, square_size, width, height):
    """Calibrate a camera using chessboard images."""
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    obj_p = np.zeros((height * width, 3), np.float32)
    obj_p[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    obj_p = obj_p * square_size

    # Arrays to store object points and image points from all the images.
    obj_points = []  # 3d point in real world space
    img_points = []  # 2d points in image plane.

    images = pathlib.Path(dir_path).glob(f'*.{image_format}')
    gray = cv2.cvtColor(cv2.imread(dir_path+'0.'+image_format), cv2.COLOR_BGR2GRAY)
    # Iterate through all images
    for name in images:
        img = cv2.imread(str(name))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        rets, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if rets:
            obj_points.append(obj_p)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)

            cv2.drawChessboardCorners(img, (width, height), corners2, rets)
            cv2.imshow('img', img)
            cv2.waitKey(100)

    # Calibrate camera
    rets, c_mat, dists, r_vectors, t_vectors = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    cv2.destroyAllWindows()
    return [rets, c_mat, dists, r_vectors, t_vectors]


def save_coefficients(matrix, c_dists, path):
    """Save the camera matrix and the distortion coefficients to given path/file."""
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write('K', matrix)
    cv_file.write('D', c_dists)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()


def load_coefficients(path):
    """Loads camera matrix and distortion coefficients."""
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


def Validate(original_dir_path, new_dir_path=None, image_format='jpg'):
    c_mtx, c_dist = load_coefficients('calibration_chessboard.yml')
    O_images = pathlib.Path(original_dir_path).glob(f'*.{image_format}')
    for name in O_images:
        original = cv2.imread(str(name))
        dst = cv2.undistort(original, c_mtx, c_dist, None, None)
        valid = np.concatenate((original, dst), axis=1)
        if not new_dir_path:
            cv2.imshow('valid', valid)
            cv2.waitKey(200)
        else:
            print("Salvando em:", new_dir_path+str(name)[len(original_dir_path):])
            cv2.imwrite(new_dir_path+str(name)[len(original_dir_path):], valid)


if __name__ == '__main__':
    # Parametros do Tabuleiro
    IMAGES_DIR = 'RawData/'
    IMAGES_FORMAT = 'jpg'
    SQUARE_SIZE = 2.2
    WIDTH = 7
    HEIGHT = 9

    # Parametros do Novo DataSet:
    CreateNewDataSet = True if input("Deseja criar um novo banco de imagens?:  [S/N]") in ['S',     's',
                                                                                           'Sim', 'sim'] else False

    NUMBER_OF_IMAGES = 30
    TIME = 1             # None to enable manual Mode
    EXIT_KEY = 'q'
    SAVE_KEY = 's'
    CAMERA_ID = 1
    # Cria um data set Novo:
    if CreateNewDataSet:
        saveImages(IMAGES_DIR,  IMAGES_FORMAT, NUMBER_OF_IMAGES, TIME, EXIT_KEY, SAVE_KEY, CAMERA_ID)

    # Calibrar
    ret, mtx, dist, r_vector, t_vector = calibrate_chessboard(
        IMAGES_DIR,
        IMAGES_FORMAT,
        SQUARE_SIZE,
        WIDTH,
        HEIGHT
    )
    # Salvar os coeficientes um arquivo
    save_coefficients(mtx, dist, "calibration_chessboard.yml")
    Validate(IMAGES_DIR, None, IMAGES_FORMAT)
