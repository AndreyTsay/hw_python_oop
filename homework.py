from typing import List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return str(f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    HOUR_PER = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass

    def show_training_info(self) -> InfoMessage:
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message
    """Вернуть информационное сообщение о выполненной тренировке."""


class Running(Training):
    """Тренировка: бег."""
    CAL_M_S_MULT = 18
    CAL_M_S_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        calories = ((self.CAL_M_S_MULT
                    * self.get_mean_speed() + self.CAL_M_S_SHIFT)
                    * self.weight / self.M_IN_KM * self.duration
                    * self.HOUR_PER)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_WALK = 0.035
    CAL_SHIFT_WALK = 0.029
    PEREVOD_KM = 0.278
    HOUR_PER = 60
    ROST: float = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.CAL_WALK * self.weight + ((self.get_mean_speed()
                     * self.PEREVOD_KM) ** 2 / (self.height / self.ROST))
                     * self.CAL_SHIFT_WALK * self.weight)
                    * (self.duration * self.HOUR_PER))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CAL_SIW_1 = 1.1
    CAL_SIW_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool
                 * self.count_pool / super().M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.CAL_SIW_1)
                    * self.CAL_SIW_2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_d = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in type_d:
        return type_d.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
