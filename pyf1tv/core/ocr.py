import os
import tempfile
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import resources

import easyocr
import pytesseract as pt

from . import Image, utils


T = t.TypeVar('T')

RecogTargetType = t.Union[
    t.Literal['CHAR'], t.Literal['NUMBER'], t.Literal['WORD'],
    t.Literal['LINE'], t.Literal['TIME']]

TesseractOCRConfig = t.Dict[str, str]
EasyOCRConfig = t.List[str]


@dataclass
class OCRBase(t.Generic[T], ABC):
    """
    OCRBase implementations act as wrappers around specifics OCRs
    """
    
    config: T

    @abstractmethod
    def image_to_string(
        self,
        image: Image,
        config: t.Optional[T]
    ) -> str:
        """Extracts text from an given image"""
    
    def postprocess_text(self, text: str) -> str:
        return text.strip().lower()


@dataclass
class TesseractOCR(OCRBase[TesseractOCRConfig]):
    """Tesseract OCR v5 implementation"""
    
    config: TesseractOCRConfig

    def __post_init__(self):
        self._load_models()
    
    def _load_models(self):
        tmp_dir = tempfile.mkdtemp()
        data_module = 'pyf1tv.data.tesseract_models'
        for file_path in resources.files(data_module).iterdir():
            # Tesseract OCR model
            if file_path.name.endswith('.traineddata'):
                with resources.open_binary(data_module, file_path.name) as model_data:
                    # Write model data to temporary directory
                    with open(os.path.join(tmp_dir, file_path.name), 'wb') as file:
                        file.write(model_data.read())
        # Set new config
        self.config |= {'--tessdata-dir': tmp_dir}

    def image_to_string(
        self,
        image: Image,
        config: t.Optional[TesseractOCRConfig]
    ) -> str:
        if not config:
            config = {}
        text = pt.image_to_string(  # type: ignore
            image, config=utils.dict_to_string(self.config | config))
        return self.postprocess_text(t.cast(str, text))


@dataclass
class EasyOCR(OCRBase[EasyOCRConfig]):
    """EasyOCR Implementation"""

    config: EasyOCRConfig

    def image_to_string(
        self,
        image: Image,
        config: t.Optional[EasyOCRConfig]
    ) -> str:
        if not config:
            config = []
        result = easyocr.Reader([*self.config, *config]).readtext(image)  # type: ignore
        if len(t.cast(t.List[t.List[t.Any] | None], result)):
            return self.postprocess_text(t.cast(str, result[0][1]))
        return ''
    

TESSERACT_OCR = TesseractOCR({'--psm': '10', '--oem': '1', '-l': 'pyf1tv'})
EASY_OCR = EasyOCR(['en'])

OCRTable = t.Dict[RecogTargetType, t.Tuple[OCRBase[t.Any], t.Optional[t.Any]]]
ocr_table: OCRTable = {
    'CHAR': (TESSERACT_OCR, None),
    'NUMBER': (TESSERACT_OCR, None),
    'WORD': (EASY_OCR, None),
    'LINE': (TESSERACT_OCR, {'-l': 'eng'}),
    'TIME': (TESSERACT_OCR, {'-l': 'pyf1tv_time'}),
}

def image_to_string(image: Image, target: RecogTargetType):
    ocr, config = ocr_table[target]
    return ocr.image_to_string(image, config)
