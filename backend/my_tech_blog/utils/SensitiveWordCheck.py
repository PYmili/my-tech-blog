import os.path
from typing import List, Dict

from flashtext import KeywordProcessor

LEXICON_PATH = os.path.join(os.path.split(__file__)[0], 'lexicon', 'vocabulary')


class LexiconLoader:
    """词库加载器"""

    @staticmethod
    def load() -> Dict[str, List[str]]:
        """
        加载词库
        :return:
        """
        lexicon = {}
        for filename in os.listdir(LEXICON_PATH):
            # 文件路径
            filepath = os.path.join(LEXICON_PATH, filename)
            # 词库key
            key = filename.strip('.txt')
            lexicon[key] = []

            # 读取数据
            with open(filepath, 'r', encoding='utf-8') as rfp:
                for line in rfp.readlines():
                    lexicon[key].append(line.strip('\n'))

        return lexicon


# init
class Instance:
    """违禁词检查实例"""

    _processor = None  # 类变量存储单例处理器

    @classmethod
    def _init_processor(cls):
        """延迟初始化处理器（只在需要时加载）"""
        if cls._processor is not None:
            return

        cls._processor = KeywordProcessor()
        lexicon = LexiconLoader.load()

        for key, words in lexicon.items():
            for word in words:
                # 只需添加关键词，不需要替换标记
                cls._processor.add_keyword(word)

    @staticmethod
    def check(target: str) -> bool:
        """
        检查目标字符串是否包含违禁词
        :param target: 目标字符串
        :return: True表示包含违禁词，False表示不包含
        """
        Instance._init_processor()
        return bool(Instance._processor.extract_keywords(target))


if __name__ == '__main__':
    print(Instance.check('去你妈的！'))