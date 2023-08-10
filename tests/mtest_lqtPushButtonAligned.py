import sys
import logging
from abc import abstractmethod

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

from lqtPushButtonAligned import PushButtonAligned

logger = logging.getLogger(__name__)


def show():
    app = QtWidgets.QApplication()

    class TestPushButtonAligned:
        test_name = ""
        expected = ""
        button_text = "This is a test button"

        def __init__(self):
            logger.debug(
                f"[{self.__class__.__name__}][{self.test_name}] expected {self.expected}"
            )
            self.widget = PushButtonAligned(self.get_icon(), self.button_text)
            self.setup()
            logger.debug(f"[{self.__class__.__name__}] Finished.\n")

        @staticmethod
        def get_icon() -> QtGui.QIcon:
            return QtWidgets.QApplication.style().standardIcon(
                QtWidgets.QStyle.SP_ArrowRight
            )

        @abstractmethod
        def setup(self):
            pass

    # PushButtonAligned:basic

    class Test1(TestPushButtonAligned):
        test_name = "default"
        expected = "|    [i]t    |"

        def setup(self):
            pass

    class Test2(TestPushButtonAligned):
        test_name = "pin_icon_left"
        expected = "|[i]    t    |"

        def setup(self):
            self.widget.pin_icon_left()

    class Test3(TestPushButtonAligned):
        test_name = "pin_icon_right"
        expected = "|    t    [i]|"

        def setup(self):
            self.widget.pin_icon_right()

    class Test4(TestPushButtonAligned):
        test_name = "align_text_left"
        expected = "|[i]t        |"

        def setup(self):
            self.widget.align_text_left()

    class Test5(TestPushButtonAligned):
        test_name = "align_text_right"
        expected = "|        [i]t|"

        def setup(self):
            self.widget.align_text_right()

    class Test6(TestPushButtonAligned):
        test_name = "align_icon_left"
        expected = "|    [i]t    |"

        def setup(self):
            self.widget.align_icon_left()

    class Test7(TestPushButtonAligned):
        test_name = "align_icon_right"
        expected = "|    t[i]    |"

        def setup(self):
            self.widget.align_icon_right()

    # PushButtonAligned:advanced

    class Test8(TestPushButtonAligned):
        test_name = "pin_icon_right(15)"
        expected = "|    t    [i] |"

        def setup(self):
            self.widget.pin_icon_right(15)

    class Test9(TestPushButtonAligned):
        test_name = "pin_icon_left(15)"
        expected = "| [i]    t    |"

        def setup(self):
            self.widget.pin_icon_left(15)

    class Test10(TestPushButtonAligned):
        test_name = "pin_icon_right(15), align_text_left"
        expected = "|t       [i] |"

        def setup(self):
            self.widget.pin_icon_right(15)
            self.widget.align_text_left()

    class Test11(TestPushButtonAligned):
        test_name = "pin_icon_right(15), align_text_right"
        expected = "|       t[i] |"

        def setup(self):
            self.widget.pin_icon_right(15)
            self.widget.align_text_right()

    class Test12(TestPushButtonAligned):
        test_name = "pin_icon_left, align_text_left"
        expected = "|[i]t        |"

        def setup(self):
            self.widget.pin_icon_left()
            self.widget.align_text_left()

    class Test13(TestPushButtonAligned):
        test_name = "pin_icon_left, align_text_right"
        expected = "|[i]        t|"

        def setup(self):
            self.widget.pin_icon_left()
            self.widget.align_text_right()

    class Test14(TestPushButtonAligned):
        test_name = "pin_icon_left, text AlignRight|AlignVCenter"
        expected = "|[i]        t|"

        def setup(self):
            self.widget.pin_icon_left()
            self.widget.set_text_alignment(QtCore.Qt.AlignRight, QtCore.Qt.AlignVCenter)

    class Test15(TestPushButtonAligned):
        test_name = "pin_icon_left, align_text_center"
        expected = "|[i]    t    |"

        def setup(self):
            self.widget.pin_icon_left()
            self.widget.align_text_center()

    class Test16(TestPushButtonAligned):
        test_name = "pin_icon_left, align_text_right(15)"
        expected = "|[i]       t |"

        def setup(self):
            self.widget.pin_icon_left()
            self.widget.align_text_right(15)

    class Test17(TestPushButtonAligned):
        test_name = "pin_icon_left(15), align_text_right(15)"
        expected = "| [i]      t |"

        def setup(self):
            self.widget.pin_icon_left(15)
            self.widget.align_text_right(15)

    class Test18(TestPushButtonAligned):
        test_name = "pin_icon_left(15), align_icon_right()"
        expected = "|    t    [i]|"

        def setup(self):
            self.widget.pin_icon_left(15)
            self.widget.align_icon_right()

    class Test19(TestPushButtonAligned):
        test_name = "pin_icon_left(15), pin_icon_right()"
        expected = "|    t    [i]|"

        def setup(self):
            self.widget.pin_icon_left(15)
            self.widget.pin_icon_right()

    class Test20(TestPushButtonAligned):
        test_name = "pin_icon_left(15), unpin_icon(), align_icon_right()"
        expected = "|    t[i]    |"

        def setup(self):
            self.widget.pin_icon_left(15)
            self.widget.unpin_icon()
            self.widget.align_icon_right()

    class Test21(TestPushButtonAligned):
        test_name = (
            "pin_icon_left(15), pin_icon_right(), align_text_left(), unpin_icon()"
        )
        expected = "|t[i]        |"

        def setup(self):
            self.widget.pin_icon_left(15)
            self.widget.pin_icon_right()
            self.widget.align_text_left()
            self.widget.unpin_icon()

    class Test22(TestPushButtonAligned):
        test_name = "align_text_left, pin_icon_right(15)"
        expected = "|t       [i] |"

        def setup(self):
            self.widget.align_text_left()
            self.widget.pin_icon_right(15)

    def to_qt_html(source_str: str) -> str:
        source_str = source_str.replace(" ", "&nbsp;")
        source_str = "<code>" + source_str + "</code>"
        return source_str

    layout = QtWidgets.QGridLayout()

    for class_index, test_class in enumerate(TestPushButtonAligned.__subclasses__()):
        test_class_instance = test_class()
        label_id = QtWidgets.QLabel(f"<b>{test_class.__name__}</b>")
        label_title = QtWidgets.QLabel(f"{test_class.test_name}")
        label_expected = QtWidgets.QLabel(to_qt_html(test_class.expected))
        layout.addWidget(label_id, class_index, 0)
        layout.addWidget(label_title, class_index, 1)
        layout.addWidget(test_class_instance.widget, class_index, 2)
        layout.addWidget(label_expected, class_index, 3)

    layout.setSpacing(25)
    layout.setColumnStretch(2, 3)

    window = QtWidgets.QWidget()
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    show()
