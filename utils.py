#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供各种辅助功能
"""

import os
import json
import logging
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import re

logger = logging.getLogger(__name__)


class Utils:
    """工具类"""
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """
        确保目录存在
        
        Args:
            directory: 目录路径
            
        Returns:
            是否成功
        """
        try:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"确保目录存在: {directory}")
            return True
        except Exception as e:
            logger.error(f"创建目录失败: {directory}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def read_json_file(file_path: str, default: Any = None) -> Any:
        """
        读取JSON文件
        
        Args:
            file_path: 文件路径
            default: 默认值
            
        Returns:
            JSON数据
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"文件不存在: {file_path}")
                return default
        except Exception as e:
            logger.error(f"读取JSON文件失败: {file_path}, 错误: {str(e)}")
            return default
    
    @staticmethod
    def write_json_file(file_path: str, data: Any, indent: int = 2) -> bool:
        """
        写入JSON文件
        
        Args:
            file_path: 文件路径
            data: 要写入的数据
            indent: 缩进
            
        Returns:
            是否成功
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            Utils.ensure_directory(directory)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            
            logger.debug(f"JSON文件写入成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"写入JSON文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def generate_id(prefix: str = "id", length: int = 8) -> str:
        """
        生成唯一ID
        
        Args:
            prefix: ID前缀
            length: 随机部分长度
            
        Returns:
            唯一ID
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return f"{prefix}_{timestamp}_{random_str}"
    
    @staticmethod
    def calculate_md5(content: str) -> str:
        """
        计算内容的MD5哈希值
        
        Args:
            content: 内容字符串
            
        Returns:
            MD5哈希值
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """
        截断文本
        
        Args:
            text: 原始文本
            max_length: 最大长度
            suffix: 后缀
            
        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        
        # 在句子边界处截断
        truncated = text[:max_length]
        
        # 查找最后一个句子结束符
        last_period = max(
            truncated.rfind('。'),
            truncated.rfind('.'),
            truncated.rfind('！'),
            truncated.rfind('!'),
            truncated.rfind('？'),
            truncated.rfind('?'),
            truncated.rfind('，'),
            truncated.rfind(','),
            truncated.rfind('；'),
            truncated.rfind(';')
        )
        
        if last_period > max_length * 0.7:  # 如果截断点附近有句子结束
            truncated = truncated[:last_period + 1]
        
        return truncated + suffix
    
    @staticmethod
    def count_chinese_chars(text: str) -> int:
        """
        统计中文字符数量
        
        Args:
            text: 文本
            
        Returns:
            中文字符数量
        """
        # 匹配中文字符
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        return len(chinese_pattern.findall(text))
    
    @staticmethod
    def count_english_words(text: str) -> int:
        """
        统计英文单词数量
        
        Args:
            text: 文本
            
        Returns:
            英文单词数量
        """
        # 匹配英文单词
        english_pattern = re.compile(r'\b[a-zA-Z]+\b')
        return len(english_pattern.findall(text))
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        提取话题标签
        
        Args:
            text: 文本
            
        Returns:
            话题标签列表
        """
        hashtag_pattern = re.compile(r'#(\w+)')
        return hashtag_pattern.findall(text)
    
    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """
        提取@提及
        
        Args:
            text: 文本
            
        Returns:
            @提及列表
        """
        mention_pattern = re.compile(r'@(\w+)')
        return mention_pattern.findall(text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        提取URL
        
        Args:
            text: 文本
            
        Returns:
            URL列表
        """
        url_pattern = re.compile(r'https?://\S+')
        return url_pattern.findall(text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        移除HTML标签
        
        Args:
            text: 文本
            
        Returns:
            清理后的文本
        """
        html_pattern = re.compile(r'<[^>]+>')
        return html_pattern.sub('', text)
    
    @staticmethod
    def remove_markdown_formatting(text: str) -> str:
        """
        移除Markdown格式
        
        Args:
            text: 文本
            
        Returns:
            清理后的文本
        """
        # 移除标题
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        # 移除粗体、斜体
        text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', text)
        # 移除代码块
        text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)
        # 移除链接
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # 移除引用
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        
        return text
    
    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """
        计算可读性分数（简化版）
        
        Args:
            text: 文本
            
        Returns:
            可读性分数（0-100）
        """
        if not text:
            return 0.0
        
        # 句子数量
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # 单词数量（中文字符+英文单词）
        chinese_chars = Utils.count_chinese_chars(text)
        english_words = Utils.count_english_words(text)
        total_words = chinese_chars + english_words
        
        if total_words == 0:
            return 0.0
        
        # 平均句子长度（词数）
        avg_sentence_length = total_words / len(sentences)
        
        # 长句比例（超过30词的句子）
        long_sentences = 0
        for sentence in sentences:
            sentence_words = Utils.count_chinese_chars(sentence) + Utils.count_english_words(sentence)
            if sentence_words > 30:
                long_sentences += 1
        
        long_sentence_ratio = long_sentences / len(sentences)
        
        # 计算可读性分数
        # 理想情况：平均句子长度15-25词，长句比例<20%
        sentence_score = 100 - abs(avg_sentence_length - 20) * 3
        long_sentence_score = 100 - long_sentence_ratio * 100
        
        # 综合分数
        readability_score = (sentence_score * 0.6 + long_sentence_score * 0.4)
        
        return max(min(readability_score, 100), 0)
    
    @staticmethod
    def generate_random_chinese_name() -> str:
        """
        生成随机中文姓名
        
        Returns:
            中文姓名
        """
        # 常见姓氏
        surnames = ["李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
                   "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]
        
        # 常见名字字符
        name_chars = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军",
                     "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞",
                     "平", "刚", "桂英", "华", "红", "文", "云", "兰", "飞", "鹏"]
        
        surname = random.choice(surnames)
        name = random.choice(name_chars)
        
        # 50%概率使用双字名
        if random.random() > 0.5:
            name += random.choice(name_chars)
        
        return surname + name
    
    @staticmethod
    def generate_random_birth_date(start_year: int = 1970, end_year: int = 2010) -> str:
        """
        生成随机出生日期
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            出生日期字符串（YYYY-MM-DD）
        """
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        
        # 处理不同月份的天数
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:  # 2月
            # 简单处理，不考虑闰年
            day = random.randint(1, 28)
        
        return f"{year:04d}-{month:02d}-{day:02d}"
    
    @staticmethod
    def generate_random_birth_time() -> str:
        """
        生成随机出生时间
        
        Returns:
            出生时间字符串（HH:MM）
        """
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        
        return f"{hour:02d}:{minute:02d}"
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        格式化日期时间
        
        Args:
            dt: 日期时间对象
            format_str: 格式字符串
            
        Returns:
            格式化后的字符串
        """
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
        """
        解析日期时间字符串
        
        Args:
            datetime_str: 日期时间字符串
            format_str: 格式字符串
            
        Returns:
            日期时间对象，解析失败返回None
        """
        try:
            return datetime.strptime(datetime_str, format_str)
        except ValueError:
            logger.warning(f"日期时间解析失败: {datetime_str}, 格式: {format_str}")
            return None
    
    @staticmethod
    def get_time_difference(start_time: datetime, end_time: datetime, 
                           unit: str = "hours") -> float:
        """
        计算时间差
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            unit: 单位（seconds, minutes, hours, days）
            
        Returns:
            时间差
        """
        diff = end_time - start_time
        diff_seconds = diff.total_seconds()
        
        if unit == "seconds":
            return diff_seconds
        elif unit == "minutes":
            return diff_seconds / 60
        elif unit == "hours":
            return diff_seconds / 3600
        elif unit == "days":
            return diff_seconds / 86400
        else:
            raise ValueError(f"不支持的unit: {unit}")
    
    @staticmethod
    def is_within_time_range(check_time: datetime, start_time: str, 
                            end_time: str, date_format: str = "%H:%M") -> bool:
        """
        检查时间是否在指定范围内
        
        Args:
            check_time: 检查的时间
            start_time: 开始时间字符串
            end_time: 结束时间字符串
            date_format: 时间格式
            
        Returns:
            是否在范围内
        """
        try:
            # 解析时间字符串
            start_dt = datetime.strptime(start_time, date_format)
            end_dt = datetime.strptime(end_time, date_format)
            
            # 创建检查时间的日期部分
            check_time_only = check_time.replace(year=1900, month=1, day=1)
            start_dt = start_dt.replace(year=1900, month=1, day=1)
            end_dt = end_dt.replace(year=1900, month=1, day=1)
            
            if start_dt <= end_dt:
                # 正常时间范围
                return start_dt <= check_time_only <= end_dt
            else:
                # 跨天时间范围
                return check_time_only >= start_dt or check_time_only <= end_dt
                
        except ValueError as e:
            logger.error(f"时间解析失败: {str(e)}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str, unit: str = "MB") -> float:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            unit: 单位（B, KB, MB, GB）
            
        Returns:
            文件大小
        """
        if not os.path.exists(file_path):
            return 0.0
        
        size_bytes = os.path.getsize(file_path)
        
        if unit == "B":
            return size_bytes
        elif unit == "KB":
            return size_bytes / 1024
        elif unit == "MB":
            return size_bytes / (1024 * 1024)
        elif unit == "GB":
            return size_bytes / (1024 * 1024 * 1024)
        else:
            raise ValueError(f"不支持的unit: {unit}")
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        获取文件扩展名
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件扩展名（小写）
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower().lstrip('.')
    
    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """
        判断是否为文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为文本文件
        """
        text_extensions = ['.txt', '.md', '.json', '.xml', '.html', '.css', '.js', 
                          '.py', '.java', '.cpp', '.c', '.h', '.csv', '.yml', '.yaml']
        
        ext = Utils.get_file_extension(file_path)
        return ext in text_extensions
    
    @staticmethod
    def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
        """
        备份文件
        
        Args:
            file_path: 文件路径
            backup_dir: 备份目录
            
        Returns:
            备份文件路径，失败返回None
        """
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在，无法备份: {file_path}")
            return None
        
        try:
            # 确保备份目录存在
            Utils.ensure_directory(backup_dir)
            
            # 生成备份文件名
            filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 复制文件
            import shutil
            shutil.copy2(file_path, backup_path)
            
            logger.info(f"文件备份成功: {file_path} -> {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"文件备份失败: {file_path}, 错误: {str(e)}")
            return None


# 测试函数
def test_utils():
    """测试工具函数"""
    print("测试工具函数...")
    
    utils = Utils()
    
    try:
        # 测试ID生成
        print("1. 测试ID生成:")
        id1 = Utils.generate_id("test")
        id2 = Utils.generate_id("test")
        print(f"  ID1: {id1}")
        print(f"  ID2: {id2}")
        print(f"  是否不同: {id1 != id2}")
        
        # 测试文本处理
        print("\n2. 测试文本处理:")
        test_text = "这是一个测试文本，包含#话题标签和@提及，还有https://example.com链接。"
        print(f"  原始文本: {test_text}")
        print(f"  话题标签: {Utils.extract_hashtags(test_text)}")
        print(f"  @提及: {Utils.extract_mentions(test_text)}")
        print(f"  URL: {Utils.extract_urls(test_text)}")
        
        # 测试可读性计算
        print("\n3. 测试可读性计算:")
        readable_text = "这是一个简单的句子。它很容易理解。"
        complex_text = "鉴于当前复杂多变的市场环境以及不可预测的外部因素，我们必须审慎评估各种潜在风险并制定相应的应对策略，以确保在充满挑战的形势下依然能够保持竞争优势并实现可持续发展目标。"
        print(f"  简单文本可读性: {Utils.calculate_readability_score(readable_text):.1f}")
        print(f"  复杂文本可读性: {Utils.calculate_readability_score(complex_text):.1f}")
        
        # 测试随机数据生成
        print("\n4. 测试随机数据生成:")
        print(f"  随机姓名: {Utils.generate_random_chinese_name()}")
        print(f"  随机出生日期: {Utils.generate_random_birth_date()}")
        print(f"  随机出生时间: {Utils.generate_random_birth_time()}")
        
        # 测试文件操作
        print("\n5. 测试目录确保:")
        test_dir = "test_directory"
        result = Utils.ensure_directory(test_dir)
        print(f"  创建目录 {test_dir}: {'成功' if result else '失败'}")
        
        # 测试JSON操作
        print("\n6. 测试JSON操作:")
        test_data = {"name": "测试", "value": 123}
        test_file = "test_data.json"
        
        write_result = Utils.write_json_file(test_file, test_data)
        print(f"  写入JSON文件: {'成功' if write_result else '失败'}")
        
        read_data = Utils.read_json_file(test_file)
        print(f"  读取JSON文件: {read_data}")
        
        # 清理测试文件
        import os
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_utils()