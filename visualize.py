import cv2
import glob

if __name__ == "__main__":
    path = "/Users/tuananh/Downloads/TIES_DataGeneration/gentables/images/*.png"
    number = 0
    for image_path in glob.glob(path):
        if number == 100:
            image = cv2.imread(image_path)
            path_text = image_path.replace("images", "txt").replace(".png", ".txt")
            file = open(path_text, "r").read().split("\n")
            print(image_path)
            for box in file:
                if box == "":
                    continue
                box = list(map(int, box.split(',')))
                cv2.rectangle(image, (box[0]-2, box[1]-2), (box[2]+2, box[3]+2), thickness=2, color=(0, 255, 0))
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
        number += 1
    