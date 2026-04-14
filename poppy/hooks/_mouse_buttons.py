from ._mouse_button import MouseButton

class MouseButtons:
    @property
    def left(self) -> MouseButton: return MouseButton(0)
    @property
    def right(self) -> MouseButton: return MouseButton(1)
    @property
    def middle(self) -> MouseButton: return MouseButton(2)
    @property
    def x1(self) -> MouseButton: return MouseButton(3)
    @property
    def x2(self) -> MouseButton: return MouseButton(4)
    
mouseButtons = MouseButtons()