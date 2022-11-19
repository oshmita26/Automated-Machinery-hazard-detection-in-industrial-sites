# Script to generate the dataset

import os
import cv2
from tqdm import tqdm
import imutils
import time

DIRECTORY = r'C:\Users\KIIT\Downloads\dataset_for_wabtech\Dataset'
BG_SIZE = 128
FRONT_SIZE = 50


def resize_images(dir, dim, dest):
    os.mkdir(dest)
    for i, f in enumerate(tqdm(os.listdir(dir))):
        img = cv2.imread(dir + "\\" + f, cv2.IMREAD_UNCHANGED)
        img = cv2.resize(
            img, (dim, dim), interpolation=cv2.INTER_CUBIC
        )
        cv2.imwrite(dest + "\\" + str(i) + ".png", img)


def generate_offset(BG, PNG, x_offset, y_offset):
    bg = BG
    png = PNG

    y1, y2 = y_offset, y_offset + png.shape[0]
    x1, x2 = x_offset, x_offset + png.shape[1]

    alpha_s = png[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        bg[y1:y2, x1:x2, c] = (alpha_s * png[:, :, c] + alpha_l * bg[y1:y2, x1:x2, c])

    return bg


def generate_left(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) - scale, int(BG_SIZE * 0.25))
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) - 2 * scale, int(BG_SIZE * 0.25))

    return img1, img2, img3


def generate_right(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) + scale, int(BG_SIZE * 0.25))
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) + 2 * scale, int(BG_SIZE * 0.25))

    return img1, img2, img3


def generate_up(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) - scale)
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) - 2 * scale)

    return img1, img2, img3


def generate_down(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) + scale)
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) + 2 * scale)

    return img1, img2, img3


def generate_mid_ver(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) - scale)
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25) + scale)

    return img1, img2, img3


def generate_mid_hor(BG, PNG, scale):
    img1 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25), int(BG_SIZE * 0.25))
    img2 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) - scale, int(BG_SIZE * 0.25))
    img3 = generate_offset(BG.copy(), PNG.copy(), int(BG_SIZE * 0.25) + scale, int(BG_SIZE * 0.25))

    return img1, img2, img3


def generate(bg, png, func, count):
    q1, q2, q3 = func(bg.copy(), png.copy(), 1)
    cv2.imwrite(DIRECTORY + "\\new\\frame1\\" + str(count) + "_scale1.png", q1)
    cv2.imwrite(DIRECTORY + "\\new\\frame2\\" + str(count) + "_scale1.png", q2)
    cv2.imwrite(DIRECTORY + "\\new\\frame3\\" + str(count) + "_scale1.png", q3)

    q1, q2, q3 = func(bg.copy(), png.copy(), 5)
    cv2.imwrite(DIRECTORY + "\\new\\frame1\\" + str(count) + "_scale5.png", q1)
    cv2.imwrite(DIRECTORY + "\\new\\frame2\\" + str(count) + "_scale5.png", q2)
    cv2.imwrite(DIRECTORY + "\\new\\frame3\\" + str(count) + "_scale5.png", q3)

    q1, q2, q3 = func(bg.copy(), png.copy(), 10)
    cv2.imwrite(DIRECTORY + "\\new\\frame1\\" + str(count) + "scale_10.png", q1)
    cv2.imwrite(DIRECTORY + "\\new\\frame2\\" + str(count) + "scale_10.png", q2)
    cv2.imwrite(DIRECTORY + "\\new\\frame3\\" + str(count) + "scale_10.png", q3)

    return count + 1


def merge_images(bg_size: int, front_size: int):
    print("Merging images: ")
    time.sleep(1)

    resize_images(DIRECTORY + "\Background", bg_size, DIRECTORY + "\BackgroundS")
    resize_images(DIRECTORY + "\pngs", front_size, DIRECTORY + "\pngsS")


def generate_movement():
    print("Moving images: ")
    time.sleep(1)

    os.mkdir(DIRECTORY + "\\" + "new")
    os.mkdir(DIRECTORY + "\\" + "new" + "\\" + "frame1")
    os.mkdir(DIRECTORY + "\\" + "new" + "\\" + "frame2")
    os.mkdir(DIRECTORY + "\\" + "new" + "\\" + "frame3")

    count = 0
    for f in tqdm(os.listdir(DIRECTORY + "\BackgroundS")):
        for p in os.listdir(DIRECTORY + "\pngsS"):
            bg = cv2.imread(DIRECTORY + "\BackgroundS\\" + f, cv2.IMREAD_UNCHANGED)
            png = cv2.imread(DIRECTORY + "\pngsS\\" + p, cv2.IMREAD_UNCHANGED)

            count = generate(bg.copy(), png.copy(), generate_up, count)
            count = generate(bg.copy(), png.copy(), generate_left, count)
            count = generate(bg.copy(), png.copy(), generate_down, count)
            count = generate(bg.copy(), png.copy(), generate_right, count)
            count = generate(bg.copy(), png.copy(), generate_mid_ver, count)
            count = generate(bg.copy(), png.copy(), generate_mid_hor, count)


def rotate(dir1, dir2, dir3, frame):
    img1 = cv2.imread(dir1 + "\\" + frame)
    img2 = cv2.imread(dir2 + "\\" + frame)
    img3 = cv2.imread(dir3 + "\\" + frame)

    for angle in range(0, 360, 45):
        cv2.imwrite(dir1 + "\\" + frame.split(".png")[0] + "_angle" + str(angle) + ".png",
                    imutils.rotate(img1.copy(), angle))
        cv2.imwrite(dir2 + "\\" + frame.split(".png")[0] + "_angle" + str(angle) + ".png",
                    imutils.rotate(img2.copy(), angle))
        cv2.imwrite(dir3 + "\\" + frame.split(".png")[0] + "_angle" + str(angle) + ".png",
                    imutils.rotate(img3.copy(), angle))


def generate_rotation():
    print("Rotating images: ")
    time.sleep(1)

    dir = DIRECTORY + "\\" + "new"
    for frame in tqdm(os.listdir(dir + "\\frame1\\")):
        rotate(dir + "\\frame1",
               dir + "\\frame2",
               dir + "\\frame3",
               frame
               )
        os.remove(dir + "\\frame1\\" + frame)
        os.remove(dir + "\\frame2\\" + frame)
        os.remove(dir + "\\frame3\\" + frame)


if __name__ == "__main__":
    merge_images(
        bg_size=BG_SIZE,
        front_size=FRONT_SIZE
    )
    generate_movement()
    generate_rotation()
