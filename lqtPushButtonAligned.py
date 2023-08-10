__all__ = ("PushButtonAligned",)

import logging
from typing import Optional

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

logger = logging.getLogger(__name__)


class PushButtonAligned(QtWidgets.QPushButton):
    """
    A button on which you can set in which direction the text and its icon is aligned.

    The ``pin_icon...`` methods allow to pin the icon to border of the button, while the
    ``align_icon...`` align it relative to the text.

    Example::

        pin_icon_left, align_text_left
        ————————————————————————
        | [icon] text          |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

        pin_icon_left, align_text_right
        ————————————————————————
        | [icon]          text |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

        pin_icon_right, align_text_right
        ————————————————————————
        |          text [icon] |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

        align_icon_right
        ————————————————————————
        |     text [icon]      |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

    inspired from: https://stackoverflow.com/a/53417349/13806195
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_icon_pinned: bool = False
        self.text_h_alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignLeft
        self.icon_h_alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignLeft

        # 1. Create
        self._icon: QtGui.QIcon = super().icon()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.label_icon = QtWidgets.QLabel()
        self.label_text = QtWidgets.QLabel(super().text())

        # 2. Add
        self.layout.addStretch(0)
        self.layout.addWidget(self.label_icon)
        self.layout.addWidget(self.label_text)
        self.layout.addStretch(0)

        # 3. Modify
        self.layout.setContentsMargins(0, 0, 0, 0)
        for label in [self.label_text, self.label_icon]:
            label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.label_text.setObjectName(f"{self.__class__.__name__}:text")
        self.label_icon.setObjectName(f"{self.__class__.__name__}:icon")
        self.label_icon.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed,
        )
        super().setText("")
        self.setIcon(self._icon)
        super().setIcon(QtGui.QIcon())

        self.set_text_alignment(QtCore.Qt.AlignCenter)

    def icon(self) -> QtGui.QIcon:
        return self._icon

    def text(self) -> str:
        return self.label_text.text()

    def setContentsMargins(
        self,
        left: Optional[int],
        top: Optional[int],
        right: Optional[int],
        bottom: Optional[int],
    ):
        """

        Args:
            left: use existing margins if None, else override it
            top: use existing margins if None, else override it
            right: use existing margins if None, else override it
            bottom: use existing margins if None, else override it
        """
        margins = self.getContentsMargins()
        left = left if left is not None else margins[0]
        top = top if top is not None else margins[1]
        right = right if right is not None else margins[2]
        bottom = bottom if bottom is not None else margins[3]
        super().setContentsMargins(left, top, right, bottom)

    def setText(self, text: str):
        self.label_text.setText(text)

    def setIcon(self, icon: QtGui.QIcon):
        self._icon = icon
        self.label_icon.setPixmap(self.icon().pixmap(self.iconSize()))

    def setIconSize(self, size: QtCore.QSize):
        super().setIconSize(size)
        self.setIcon(self._icon)

    def sizeHint(self):
        base_hint = super().sizeHint()
        target_hint = self.layout.sizeHint()
        return QtCore.QSize(
            base_hint.width() + target_hint.width(),
            max(base_hint.height(), target_hint.height()),
        )

    def _update_layout(
        self,
        text_v_alignment: QtCore.Qt.AlignmentFlag = None,
    ):
        """
        Call an update on the icon relative to the current text position.
        """
        self.layout.removeWidget(self.label_icon)
        self.layout.removeWidget(self.label_text)
        text_v_alignment = text_v_alignment or QtCore.Qt.AlignVCenter

        if self.text_h_alignment == QtCore.Qt.AlignLeft:
            # [t][s][s]
            self.layout.insertWidget(0, self.label_text)

        elif self.text_h_alignment == QtCore.Qt.AlignRight:
            # [s][s][t]
            self.layout.insertWidget(-1, self.label_text)

        elif self.text_h_alignment == QtCore.Qt.AlignCenter:
            # [s][t][s]
            self.layout.insertWidget(1, self.label_text)

        else:
            raise ValueError(f"Unsupported value for {int(self.text_h_alignment)=}")

        logger.debug(
            f"[{self.__class__.__name__}][_update_layout](text)  {self._repr_layout()}"
        )

        self.label_text.setAlignment(self.text_h_alignment | text_v_alignment)

        if self.icon_h_alignment == QtCore.Qt.AlignLeft:
            if self.is_icon_pinned:
                self.layout.insertWidget(0, self.label_icon)
            else:
                text_index = self.layout.indexOf(self.label_text)
                self.layout.insertWidget(text_index, self.label_icon)

        elif self.icon_h_alignment == QtCore.Qt.AlignRight:
            if self.is_icon_pinned:
                self.layout.insertWidget(-1, self.label_icon)
            else:
                text_index = self.layout.indexOf(self.label_text)
                self.layout.insertWidget(text_index + 1, self.label_icon)

        else:
            raise ValueError(f"Unsupported value for {self.icon_h_alignment=}")

        logger.debug(
            f"[{self.__class__.__name__}][_update_layout](icon)    {self._repr_layout()}"
        )
        return

    def _repr_layout(self) -> str:
        """
        Return the layout structure as a string like ``[<>][i][t][<>]``.
        """

        layout_repr = ""
        for child_index in range(self.layout.count()):
            l_item = self.layout.itemAt(child_index)
            if l_item.spacerItem():
                layout_repr += "[<>]"
            else:
                layout_repr += f"[{l_item.widget().objectName().split(':')[-1][0]}]"

        return layout_repr

    def align_icon_left(self):
        """
        Align icon relative to the text.
        """
        self.icon_h_alignment = QtCore.Qt.AlignLeft
        self._update_layout()

    def align_icon_right(self):
        """
        Align icon relative to the text.
        """
        self.icon_h_alignment = QtCore.Qt.AlignRight
        self._update_layout()

    def align_text_left(self, margin=None):
        self.text_h_alignment = QtCore.Qt.AlignLeft
        self._update_layout(QtCore.Qt.AlignVCenter)

        self.setContentsMargins(margin, None, None, None)

    def align_text_right(self, margin=None):
        self.text_h_alignment = QtCore.Qt.AlignRight
        self._update_layout(QtCore.Qt.AlignVCenter)

        self.setContentsMargins(None, None, margin, None)

    def align_text_center(self):
        self.text_h_alignment = QtCore.Qt.AlignCenter
        self._update_layout(QtCore.Qt.AlignVCenter)

    def pin_icon_left(self, margin=None):
        """
        Align icon relative to the PushButton borders.
        """
        self.is_icon_pinned = True
        self.icon_h_alignment = QtCore.Qt.AlignLeft
        self._update_layout()
        self.setContentsMargins(margin, None, None, None)

    def pin_icon_right(self, margin=None):
        """
        Align icon relative to the PushButton borders.
        """
        self.is_icon_pinned = True
        self.icon_h_alignment = QtCore.Qt.AlignRight
        self._update_layout()
        self.setContentsMargins(None, None, margin, None)

    def set_text_alignment(
        self,
        alignment_h: QtCore.Qt.AlignmentFlag,
        alignment_v: Optional[QtCore.Qt.AlignmentFlag] = None,
    ):
        self.text_h_alignment = alignment_h
        self._update_layout(alignment_v)

    def unpin_icon(self):
        self.is_icon_pinned = False
        self._update_layout()
