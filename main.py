import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from ReplaceEncrypt import decrypt_and_replace, encrypt_and_replace
from KeyUtils import derive_key


class _BaseDropLabel(QtWidgets.QLabel):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:  # type: ignore[name-defined]
        if event.mimeData().hasUrls():
            event.acceptProposedAction()


class EncryptLabel(_BaseDropLabel):
    def __init__(self) -> None:
        super().__init__("Drop files here to encrypt")

    def dropEvent(self, event: QtGui.QDropEvent) -> None:  # type: ignore[name-defined]
        passphrase, ok = QtWidgets.QInputDialog.getText(
            self,
            "Passphrase",
            "Enter passphrase to derive encryption key:",
            QtWidgets.QLineEdit.Password,
        )
        if not ok or not passphrase:
            return

        key = derive_key(passphrase)
        for url in event.mimeData().urls():
            encrypt_and_replace(url.toLocalFile(), key)
        self.setText("File(s) encrypted & replaced!")


class DecryptLabel(_BaseDropLabel):
    def __init__(self) -> None:
        super().__init__("Drop files here to decrypt")

    def dropEvent(self, event: QtGui.QDropEvent) -> None:  # type: ignore[name-defined]
        passphrase, ok = QtWidgets.QInputDialog.getText(
            self,
            "Passphrase",
            "Enter passphrase to derive encryption key:",
            QtWidgets.QLineEdit.Password,
        )
        if not ok or not passphrase:
            return

        key = derive_key(passphrase)
        for url in event.mimeData().urls():
            decrypt_and_replace(url.toLocalFile(), key)
        self.setText("File(s) decrypted & replaced!")


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)
    layout.setSpacing(0)

    encrypt_label = EncryptLabel()
    decrypt_label = DecryptLabel()
    layout.addWidget(encrypt_label)
    layout.addWidget(decrypt_label)

    widget.resize(600, 400)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()