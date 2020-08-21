import cv2


def refactor_img(img_path, size, to_gray=False):
    img = cv2.imread(img_path)
    img = cv2.resize(img, size)
    if to_gray:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(img_path, img)



