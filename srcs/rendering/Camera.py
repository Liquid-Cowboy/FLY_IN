from pygame import (Event, MOUSEWHEEL,
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP,
                    MOUSEMOTION)


class Camera():
    """
    Will handle how big the map is shown on the screen
    by evaluating mouse events (wheel scroll and left
    button hold). This will give the user a chance to
    examine parts of bigger and more complex maps.
    """
    def __init__(self):
        """
        Initiates basic offset atributes, a left button
        hold boolean and the current zoom amount.
        """
        self._x_offset: float = 0
        self._y_offset: float = 0
        self._dragging: bool = False
        self._zoom: float = 1.0

    def get_screen_coor(self, coor: tuple[int, int]) -> tuple[int, int]:
        """
        Will calculate the precise coordinates, given the current
        offsets and zoom amount. Mutates the x and y variables
        passed as arguments.
        """
        return (
            int((coor[0] + self._x_offset) * self._zoom),
            int((coor[1] + self._y_offset) * self._zoom)
        )

    def get_trans_nb(self, nb: int) -> int:
        return (int(nb * self._zoom))

    def move_camera(self, event: Event) -> None:
        """
        Will apply the changes to the class attributes
        based on the type of event passed.
        """
        if event.type == MOUSEWHEEL:
            self._zoom += event.y * 0.1
            self._zoom = max(0.1, min(self._zoom, 5.0))

        # if event.button == 1 it means we're clicking the
        # left button
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self._dragging = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self._dragging = False

        if event.type == MOUSEMOTION and self._dragging:
            # rel is the calculation of the mouses relative
            # position since last MOUSEMOTION event
            # rel[0] and rel[1] correspond to x and y
            # positions respectively
            self._x_offset += event.rel[0] / self._zoom
            self._y_offset += event.rel[1] / self._zoom
