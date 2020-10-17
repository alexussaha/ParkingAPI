import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
from mrcnn.model import MaskRCNN
from pathlib import Path
import requests




# Конфигурация, которую будет использовать библиотека Mask-RCNN.
class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 1 + 80  # в датасете COCO находится 80 классов + 1 фоновый класс.
    DETECTION_MIN_CONFIDENCE = 0.6

class FreeParkFindModel:
# Фильтруем список результатов распознавания, чтобы остались только 11автомобили.

    # Корневая директория проекта.
    ROOT_DIR = Path(".")

    # Директория для сохранения логов и обученной модели.
    MODEL_DIR = ROOT_DIR / "logs"

    # Локальный путь к файлу с обученными весами.
    COCO_MODEL_PATH =  r"\resources\mask_rcnn_coco.h5"

    # Загружаем датасет COCO при необходимости.
    #mrcnn.utils.download_trained_weights(COCO_MODEL_PATH)

    # Директория с изображениями для обработки.
    IMAGE_DIR = ROOT_DIR / "images"

    # Видеофайл или камера для обработки — вставьте значение 0, если нужно использовать камеру, а не видеофайл.
    VIDEO_SOURCE = 'http://c001.sm0t.ru/'
    #'http://c001.sm0t.ru/'
    #'http://91.233.230.12/axis-cgi/jpg/image.cgi?resolution=640x480'
    #'http://91.233.230.14/jpg/image.jpg'

    def get_car_boxes(boxes, class_ids):
        car_boxes = []

        for i, box in enumerate(boxes):
            # Если найденный объект не автомобиль, то пропускаем его.
            if class_ids[i] in [3, 8, 6]:
                car_boxes.append(box)

        return np.array(car_boxes)


    def start():
        # Создаём модель Mask-RCNN в режиме вывода.
        model = MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=MaskRCNNConfig())

        # Загружаем предобученную модель.
        model.load_weights(COCO_MODEL_PATH, by_name=True)

        # Местоположение парковочных мест.
        parked_car_boxes = None

        #r = requests.get(VIDEO_SOURCE)

        #img = Image.open(io.BytesIO(r.content))

        # Загружаем видеофайл, для которого хотим запустить распознавание.
        video_capture = cv2.VideoCapture(VIDEO_SOURCE)
        #video_capture = cv2.VideoCapture(VIDEO_SOURCE)

        # Сколько кадров подряд с пустым местом мы уже видели.
        free_space_frames = 0



        # Проходимся в цикле по каждому кадру.
        #while video_capture.isOpened():
        while video_capture.isOpened():
            success, frame = video_capture.read()
            if not success:
                break

            # Конвертируем изображение из цветовой модели BGR в RGB.
            rgb_image = frame[:, :, ::-1]

            # Подаём изображение модели Mask R-CNN для получения результата.
            results = model.detect([rgb_image], verbose=0)

            # Mask R-CNN предполагает, что мы распознаём объекты на множественных изображениях.
            # Мы передали только одно изображение, поэтому извлекаем только первый результат.
            r = results[0]

            # Переменная r теперь содержит результаты распознавания:
            # - r['rois'] — ограничивающая рамка для каждого распознанного объекта;
            # - r['class_ids'] — идентификатор (тип) объекта;
            # - r['scores'] — степень уверенности;
            # - r['masks'] — маски объектов (что даёт вам их контур).

            if parked_car_boxes is None:
                # Это первый кадр видео — допустим, что все обнаруженные машины стоят на парковке.
                # Сохраняем местоположение каждой машины как парковочное место и переходим к следующему кадру.
                parked_car_boxes = get_car_boxes(r['rois'], r['class_ids'])
            else:
                # Мы уже знаем, где места. Проверяем, есть ли свободные.

                # Ищем машины на текущем кадре.
                car_boxes = get_car_boxes(r['rois'], r['class_ids'])

                # Смотрим, как сильно эти машины пересекаются с известными парковочными местами.
                overlaps = mrcnn.utils.compute_overlaps(parked_car_boxes, car_boxes)

                # Предполагаем, что свободных мест нет, пока не найдём хотя бы одно.
                free_space = False

                # Проходимся в цикле по каждому известному парковочному месту.
                for parking_area, overlap_areas in zip(parked_car_boxes, overlaps):

                    # Ищем максимальное значение пересечения с любой обнаруженной
                    # на кадре машиной (неважно, какой).
                    max_IoU_overlap = np.max(overlap_areas)

                    # Получаем верхнюю левую и нижнюю правую координаты парковочного места.
                    y1, x1, y2, x2 = parking_area

                    # Проверяем, свободно ли место, проверив значение IoU.
                    if max_IoU_overlap < 0.15:
                        # Место свободно! Рисуем зелёную рамку вокруг него.
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        # Отмечаем, что мы нашли как минимум оно свободное место.
                        free_space = True
                    else:
                        # Место всё ещё занято — рисуем красную рамку.
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

                    # Записываем значение IoU внутри рамки.
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255))

                # Если хотя бы одно место было свободным, начинаем считать кадры.
                # Это для того, чтобы убедиться, что место действительно свободно
                # и не отправить лишний раз уведомление.
                if free_space:
                    free_space_frames += 1
                else:
                    # Если всё занято, обнуляем счётчик.
                    free_space_frames = 0

                # Если место свободно на протяжении нескольких кадров, можно сказать, что оно свободно.
                if free_space_frames > 10:
                    # Отображаем надпись SPACE AVAILABLE!! вверху экрана.
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, f"SPACE AVAILABLE!", (10, 150), font, 3.0, (0, 255, 0), 2, cv2.FILLED)

                    # Отправляем сообщение, если ещё не сделали это.
            

                # Показываем кадр на экране.
                cv2.imshow('Video', frame)

            # Нажмите 'q', чтобы выйти.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Нажмите 'q', чтобы выйти.
        video_capture.release()
        cv2.destroyAllWindows()

