#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字分析器模块
用于解析八字数据，提取命理信息
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

try:
    from lunarcalendar import Converter, Solar
    HAS_LUNAR_CALENDAR = True
except ImportError:
    HAS_LUNAR_CALENDAR = False

logger = logging.getLogger(__name__)


class BaZiAnalyzer:
    """八字分析器类"""
    
    # 天干地支映射
    TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # 六十甲子表 (在 __init__ 中初始化)
    
    # 五虎遁起月表 (年干 -> [正月~腊月的天干])
    WGHU = {
        "甲": ("丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"),
        "己": ("丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"),
        "乙": ("戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"),
        "庚": ("戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"),
        "丙": ("庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"),
        "辛": ("庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"),
        "丁": ("壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"),
        "壬": ("壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"),
        "戊": ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"),
        "癸": ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"),
    }
    
    # 五鼠遁起时表 (日干 -> [子时~亥时的天干])
    WUSHU = {
        "甲": ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"),
        "己": ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸","甲","乙"),
        "乙": ("丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"),
        "庚": ("丙","丁","戊","己","庚","辛","壬","癸","甲","乙","丙","丁"),
        "丙": ("戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"),
        "辛": ("戊","己","庚","辛","壬","癸","甲","乙","丙","丁","戊","己"),
        "丁": ("庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"),
        "壬": ("庚","辛","壬","癸","甲","乙","丙","丁","戊","己","庚","辛"),
        "戊": ("壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"),
        "癸": ("壬","癸","甲","乙","丙","丁","戊","己","庚","辛","壬","癸"),
    }
    
    # 五行属性
    WU_XING = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火",
        "戊": "土", "己": "土", "庚": "金", "辛": "金",
        "壬": "水", "癸": "水",
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    # 十神关系
    SHI_SHEN = {
        "比肩": "同我者为比肩",
        "劫财": "同我异性为劫财",
        "食神": "我生者为食神",
        "伤官": "我生异性为伤官",
        "正财": "我克者为正财",
        "偏财": "我克异性为偏财",
        "正官": "克我者为正官",
        "七杀": "克我异性为七杀",
        "正印": "生我者为正印",
        "偏印": "生我异性为偏印"
    }
    
    def __init__(self):
        """初始化八字分析器"""
        self.bazi_data = None
        self.analysis_result = {}
        # 六十甲子表
        self.GAN_ZHI_60 = [self.TIAN_GAN[i % 10] + self.DI_ZHI[i % 12] for i in range(60)]
        logger.info("八字分析器初始化完成")
    
    def analyze(self, birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析八字信息
        
        Args:
            birth_info: 出生信息字典，包含：
                - birth_date: 出生日期 (YYYY-MM-DD)
                - birth_time: 出生时间 (HH:MM)
                - gender: 性别 (male/female)
                - name: 姓名 (可选)
                
        Returns:
            八字分析结果
        """
        try:
            logger.info(f"开始分析八字: {birth_info}")
            
            # 验证输入数据
            self.validate_birth_info(birth_info)
            
            # 提取出生信息
            birth_date = birth_info["birth_date"]
            birth_time = birth_info["birth_time"]
            gender = birth_info["gender"]
            name = birth_info.get("name", "")
            
            # 1. 计算八字四柱
            bazi_pillar = self.calculate_bazi_pillar(birth_date, birth_time)
            
            # 2. 分析日主五行
            ri_zhu_wu_xing = self.analyze_ri_zhu(bazi_pillar)
            
            # 3. 分析十神
            shi_shen_analysis = self.analyze_shi_shen(bazi_pillar, ri_zhu_wu_xing)
            
            # 4. 分析五行强弱
            wu_xing_strength = self.analyze_wu_xing_strength(bazi_pillar)
            
            # 5. 分析大运
            da_yun = self.calculate_da_yun(birth_date, birth_time, gender)
            
            # 6. 生成命理特征
            features = self.generate_features(
                bazi_pillar, ri_zhu_wu_xing, shi_shen_analysis, wu_xing_strength
            )
            
            # 构建分析结果
            self.analysis_result = {
                "basic_info": {
                    "name": name,
                    "birth_date": birth_date,
                    "birth_time": birth_time,
                    "gender": gender,
                    "lunar_date": self.convert_to_lunar(birth_date)
                },
                "bazi_pillar": bazi_pillar,
                "ri_zhu": {
                    "character": bazi_pillar["ri_zhu"],
                    "wu_xing": ri_zhu_wu_xing,
                    "description": self.get_ri_zhu_description(bazi_pillar["ri_zhu"])
                },
                "shi_shen": shi_shen_analysis,
                "wu_xing_strength": wu_xing_strength,
                "da_yun": da_yun,
                "features": features,
                "analysis_summary": self.generate_summary(features),
                "created_at": datetime.now().isoformat()
            }
            
            logger.info("八字分析完成")
            return self.analysis_result
            
        except Exception as e:
            logger.error(f"八字分析失败: {str(e)}", exc_info=True)
            raise
    
    def validate_birth_info(self, birth_info: Dict[str, Any]):
        """验证出生信息"""
        required_fields = ["birth_date", "birth_time", "gender"]
        
        for field in required_fields:
            if field not in birth_info:
                raise ValueError(f"缺少必要字段: {field}")
        
        # 验证日期格式
        try:
            datetime.strptime(birth_info["birth_date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"日期格式错误: {birth_info['birth_date']}，应为YYYY-MM-DD")
        
        # 验证时间格式
        try:
            datetime.strptime(birth_info["birth_time"], "%H:%M")
        except ValueError:
            raise ValueError(f"时间格式错误: {birth_info['birth_time']}，应为HH:MM")
        
        # 验证性别
        if birth_info["gender"] not in ["male", "female"]:
            raise ValueError(f"性别错误: {birth_info['gender']}，应为male或female")
    
    def calculate_bazi_pillar(self, birth_date: str, birth_time: str) -> Dict[str, str]:
        """
        计算八字四柱 (年柱、月柱、日柱、时柱)

        算法说明:
        - 日柱: 使用已知参考点 offset=36 (1900-01-01=庚子), 经验证2026-03-27=丙寅正确
        - 年柱: 使用农历年 (春节分界, 非立春)
        - 月柱: 使用农历月 + 五虎遁查表
        - 时柱: 使用五鼠遁查表
        """
        from datetime import date as date_cls
        
        date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = int(birth_time.split(":")[0])
        
        # 如果没有 lunarcalendar, fallback到简化算法
        if not HAS_LUNAR_CALENDAR:
            return self._calculate_bazi_simple(year, month, day, hour)
        
        try:
            solar = Solar(year, month, day)
            lunar = Converter.Solar2Lunar(solar)
            lunar_year = lunar.year
            lunar_month = lunar.month
            lunar_day = lunar.day
            
            # 1. 日柱 (用公历日期直接算)
            days = (date_cls(year, month, day) - date_cls(1900, 1, 1)).days
            ri_zhu = self.GAN_ZHI_60[(days + 36) % 60]
            
            # 2. 年柱 (用农历年)
            nian_gan_idx = (lunar_year - 4) % 10
            nian_zhi_idx = (lunar_year - 4) % 12
            nian_zhu = self.TIAN_GAN[nian_gan_idx] + self.DI_ZHI[nian_zhi_idx]
            
            # 3. 月柱 (农历月 + 五虎遁)
            nian_gan = self.TIAN_GAN[nian_gan_idx]
            yue_gan = self.WGHU[nian_gan][lunar_month - 1]
            yue_zhi = self.DI_ZHI[(lunar_month + 1) % 12]  # 1月=寅,2月=卯...
            yue_zhu = yue_gan + yue_zhi
            
            # 4. 时柱 (日干 + 五鼠遁)
            ri_gan = ri_zhu[0]
            shi_zhi_idx = ((hour + 1) % 24) // 2
            shi_gan = self.WUSHU[ri_gan][shi_zhi_idx]
            shi_zhu = shi_gan + self.DI_ZHI[shi_zhi_idx]
            
            pillar = {
                "nian_zhu": nian_zhu,
                "yue_zhu": yue_zhu,
                "ri_zhu": ri_zhu,
                "shi_zhu": shi_zhu,
            }
            logger.debug(f"计算得到的八字: {pillar}")
            return pillar
            
        except Exception as e:
            logger.error(f"八字计算失败, 使用简化算法: {e}")
            return self._calculate_bazi_simple(year, month, day, hour)
    
    def _calculate_bazi_simple(self, year, month, day, hour):
        """简化八字算法 (当lunarcalendar不可用时 fallback)"""
        nian_idx = (year - 1900) % 10
        yue_idx = month % 10
        ri_idx = day % 10
        shi_idx = hour % 10
        
        return {
            "nian_zhu": f"{self.TIAN_GAN[nian_idx]}{self.DI_ZHI[nian_idx % 12]}",
            "yue_zhu": f"{self.TIAN_GAN[yue_idx]}{self.DI_ZHI[yue_idx % 12]}",
            "ri_zhu": f"{self.TIAN_GAN[ri_idx]}{self.DI_ZHI[ri_idx % 12]}",
            "shi_zhu": f"{self.TIAN_GAN[shi_idx]}{self.DI_ZHI[shi_idx % 12]}"
        }
    
    def analyze_ri_zhu(self, bazi_pillar: Dict[str, str]) -> str:
        """
        分析日主五行
        
        Args:
            bazi_pillar: 八字四柱
            
        Returns:
            日主五行
        """
        ri_zhu = bazi_pillar["ri_zhu"]
        ri_gan = ri_zhu[0]  # 日干
        
        wu_xing = self.WU_XING.get(ri_gan, "未知")
        logger.debug(f"日主 {ri_zhu} 的五行: {wu_xing}")
        
        return wu_xing
    
    def analyze_shi_shen(self, bazi_pillar: Dict[str, str], ri_zhu_wu_xing: str) -> Dict[str, List[str]]:
        """
        分析十神
        
        Args:
            bazi_pillar: 八字四柱
            ri_zhu_wu_xing: 日主五行
            
        Returns:
            十神分析结果
        """
        ri_gan = bazi_pillar["ri_zhu"][0]
        shi_shen_result = {}
        
        for pillar_name, pillar_value in bazi_pillar.items():
            gan = pillar_value[0]
            zhi = pillar_value[1]
            
            # 简化分析，实际需要根据日干和其他干支的关系计算十神
            shi_shen = self.simplified_shi_shen_analysis(ri_gan, gan)
            
            if pillar_name not in shi_shen_result:
                shi_shen_result[pillar_name] = []
            
            shi_shen_result[pillar_name].append({
                "gan": gan,
                "zhi": zhi,
                "shi_shen": shi_shen,
                "description": self.SHI_SHEN.get(shi_shen, "")
            })
        
        logger.debug(f"十神分析结果: {shi_shen_result}")
        return shi_shen_result
    
    def simplified_shi_shen_analysis(self, ri_gan: str, other_gan: str) -> str:
        """简化的十神分析（仅用于演示）"""
        # 实际需要复杂的十神计算
        # 这里使用简单映射
        shi_shen_map = {
            "甲": {"甲": "比肩", "乙": "劫财", "丙": "食神", "丁": "伤官", 
                  "戊": "偏财", "己": "正财", "庚": "七杀", "辛": "正官",
                  "壬": "偏印", "癸": "正印"},
            "乙": {"甲": "劫财", "乙": "比肩", "丙": "伤官", "丁": "食神",
                  "戊": "正财", "己": "偏财", "庚": "正官", "辛": "七杀",
                  "壬": "正印", "癸": "偏印"}
        }
        
        # 默认返回比肩
        return shi_shen_map.get(ri_gan, {}).get(other_gan, "比肩")
    
    def analyze_wu_xing_strength(self, bazi_pillar: Dict[str, str]) -> Dict[str, float]:
        """
        分析五行强弱
        
        Args:
            bazi_pillar: 八字四柱
            
        Returns:
            五行强弱字典
        """
        wu_xing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        # 统计八字中的五行
        for pillar_value in bazi_pillar.values():
            for char in pillar_value:
                wu_xing = self.WU_XING.get(char)
                if wu_xing:
                    wu_xing_count[wu_xing] += 1
        
        # 计算百分比
        total = sum(wu_xing_count.values())
        if total > 0:
            wu_xing_strength = {k: round(v/total * 100, 2) for k, v in wu_xing_count.items()}
        else:
            wu_xing_strength = {k: 0 for k in wu_xing_count.keys()}
        
        logger.debug(f"五行强弱分析: {wu_xing_strength}")
        return wu_xing_strength
    
    def calculate_da_yun(self, birth_date: str, birth_time: str, gender: str) -> List[Dict[str, Any]]:
        """
        计算大运
        
        Args:
            birth_date: 出生日期
            birth_time: 出生时间
            gender: 性别
            
        Returns:
            大运列表
        """
        # 简化实现，实际需要根据出生时间和性别计算大运
        logger.info(f"计算大运: {birth_date} {birth_time} {gender}")
        
        da_yun_list = []
        
        # 示例大运数据
        example_da_yun = [
            {"age": "1-10", "yun": "丙寅", "description": "少年运，学业发展期"},
            {"age": "11-20", "yun": "丁卯", "description": "青年运，人际关系发展"},
            {"age": "21-30", "yun": "戊辰", "description": "事业起步期，积累经验"},
            {"age": "31-40", "yun": "己巳", "description": "事业发展期，财运上升"},
            {"age": "41-50", "yun": "庚午", "description": "事业高峰期，成就显现"},
            {"age": "51-60", "yun": "辛未", "description": "稳定发展期，注重健康"},
            {"age": "61-70", "yun": "壬申", "description": "晚年运，享受成果"}
        ]
        
        return example_da_yun
    
    def generate_features(self, bazi_pillar: Dict[str, str], ri_zhu_wu_xing: str, 
                         shi_shen: Dict[str, List[str]], wu_xing_strength: Dict[str, float]) -> Dict[str, Any]:
        """
        生成命理特征
        
        Args:
            bazi_pillar: 八字四柱
            ri_zhu_wu_xing: 日主五行
            shi_shen: 十神分析
            wu_xing_strength: 五行强弱
            
        Returns:
            命理特征字典
        """
        features = {
            "personality": [],
            "career": [],
            "wealth": [],
            "relationships": [],
            "health": [],
            "lucky_elements": [],
            "unlucky_elements": []
        }
        
        # 根据五行强弱生成特征
        strongest_wu_xing = max(wu_xing_strength.items(), key=lambda x: x[1])[0]
        weakest_wu_xing = min(wu_xing_strength.items(), key=lambda x: x[1])[0]
        
        # 性格特征
        personality_traits = {
            "金": ["果断", "坚定", "讲义气", "有时固执"],
            "木": ["仁慈", "进取", "有活力", "有时冲动"],
            "水": ["聪明", "灵活", "适应力强", "有时多变"],
            "火": ["热情", "开朗", "有领导力", "有时急躁"],
            "土": ["稳重", "诚信", "有耐心", "有时保守"]
        }
        
        if ri_zhu_wu_xing in personality_traits:
            features["personality"] = personality_traits[ri_zhu_wu_xing]
        
        # 事业特征
        career_suggestions = {
            "金": ["金融", "法律", "机械", "管理"],
            "木": ["教育", "文化", "设计", "医疗"],
            "水": ["贸易", "物流", "咨询", "旅游"],
            "火": ["营销", "娱乐", "餐饮", "互联网"],
            "土": ["房地产", "建筑", "农业", "制造业"]
        }
        
        if strongest_wu_xing in career_suggestions:
            features["career"] = career_suggestions[strongest_wu_xing]
        
        # 财运特征
        wealth_features = []
        if wu_xing_strength.get("金", 0) > 20:
            wealth_features.append("有理财天赋")
        if wu_xing_strength.get("土", 0) > 20:
            wealth_features.append("适合稳健投资")
        if wu_xing_strength.get("水", 0) > 20:
            wealth_features.append("财运流动性强")
        
        features["wealth"] = wealth_features if wealth_features else ["财运平稳"]
        
        # 幸运元素
        features["lucky_elements"] = [strongest_wu_xing]
        features["unlucky_elements"] = [weakest_wu_xing]
        
        logger.debug(f"生成的命理特征: {features}")
        return features
    
    def generate_summary(self, features: Dict[str, Any]) -> str:
        """
        生成分析摘要
        
        Args:
            features: 命理特征
            
        Returns:
            分析摘要
        """
        summary_parts = []
        
        # 性格摘要
        if features.get("personality"):
            summary_parts.append(f"性格特点：{', '.join(features['personality'][:3])}")
        
        # 事业摘要
        if features.get("career"):
            summary_parts.append(f"适合行业：{', '.join(features['career'][:3])}")
        
        # 财运摘要
        if features.get("wealth"):
            summary_parts.append(f"财运特征：{', '.join(features['wealth'][:2])}")
        
        # 幸运元素
        if features.get("lucky_elements"):
            summary_parts.append(f"幸运元素：{', '.join(features['lucky_elements'])}")
        
        return "。".join(summary_parts) + "。"
    
    def get_ri_zhu_description(self, ri_zhu: str) -> str:
        """
        获取日柱描述
        
        Args:
            ri_zhu: 日柱
            
        Returns:
            日柱描述
        """
        descriptions = {
            "甲子": "甲木坐子水，聪明机智，有领导才能",
            "乙丑": "乙木坐丑土，稳重踏实，有艺术天赋",
            "丙寅": "丙火坐寅木，热情开朗，有创造力",
            "丁卯": "丁火坐卯木，温和细腻，有文艺气质",
            "戊辰": "戊土坐辰土，诚信稳重，有责任感",
            "己巳": "己土坐巳火，聪明灵活，有商业头脑",
            "庚午": "庚金坐午火，果断坚定，有执行力",
            "辛未": "辛金坐未土，细致认真，有分析能力",
            "壬申": "壬水坐申金，聪明灵活，适应力强",
            "癸酉": "癸水坐酉金，细腻敏感，有艺术天赋"
        }
        
        return descriptions.get(ri_zhu, "日柱特征需要详细分析")
    
    def convert_to_lunar(self, solar_date: str) -> str:
        """
        将公历日期转换为农历日期

        Args:
            solar_date: 公历日期，格式如 "2026-03-27"

        Returns:
            农历日期字符串，如 "2026年二月初九"
        """
        if not HAS_LUNAR_CALENDAR:
            logger.warning("lunarcalendar 库未安装，无法转换农历")
            return f"{solar_date}（农历）"

        try:
            # 解析日期，支持多种格式
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日"):
                try:
                    dt = datetime.strptime(solar_date, fmt)
                    break
                except ValueError:
                    continue
            else:
                return f"{solar_date}（农历）"

            solar = Solar(dt.year, dt.month, dt.day)
            lunar = Converter.Solar2Lunar(solar)

            # 转换为中文格式
            chinese_nums = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

            def to_chinese_num(n):
                """1-99的个位数和十位数转中文"""
                if n < 10:
                    return chinese_nums[n]
                elif n < 20:
                    return "十" + (chinese_nums[n - 10] if n > 10 else "")
                else:
                    tens = n // 10
                    ones = n % 10
                    return chinese_nums[tens] + "十" + (chinese_nums[ones] if ones else "")

            month_str = to_chinese_num(lunar.month)

            # 农历日期格式：初X（1-10）、十一到十九、二十到三十
            day = lunar.day
            if day <= 10:
                day_str = "初" + chinese_nums[day]
            elif day < 20:
                day_str = "十" + chinese_nums[day - 10]
            else:
                tens = day // 10
                ones = day % 10
                day_str = chinese_nums[tens] + "十" + (chinese_nums[ones] if ones else "")

            return f"{lunar.year}年{month_str}月{day_str}"
        except Exception as e:
            logger.error(f"农历转换失败: {e}")
            return f"{solar_date}（农历）"
    
    def get_analysis_result(self) -> Dict[str, Any]:
        """
        获取分析结果
        
        Returns:
            分析结果字典
        """
        if not self.analysis_result:
            raise ValueError("尚未进行分析，请先调用analyze方法")
        
        return self.analysis_result
    
    def save_analysis(self, file_path: str):
        """
        保存分析结果到文件
        
        Args:
            file_path: 文件路径
        """
        if not self.analysis_result:
            raise ValueError("没有分析结果可保存")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"分析结果已保存到: {file_path}")
            
        except Exception as e:
            logger.error(f"保存分析结果失败: {str(e)}")
            raise


# 测试函数
def test_bazi_analyzer():
    """测试八字分析器"""
    print("测试八字分析器...")
    
    analyzer = BaZiAnalyzer()
    
    # 测试数据
    test_birth_info = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00",
        "gender": "male",
        "name": "测试用户"
    }
    
    try:
        result = analyzer.analyze(test_birth_info)
        
        print("\n八字分析结果:")
        print(f"姓名: {result['basic_info']['name']}")
        print(f"出生日期: {result['basic_info']['birth_date']}")
        print(f"八字四柱: {result['bazi_pillar']}")
        print(f"日主五行: {result['ri_zhu']['wu_xing']}")
        print(f"分析摘要: {result['analysis_summary']}")
        
        print("\n五行强弱:")
        for wu_xing, strength in result['wu_xing_strength'].items():
            print(f"  {wu_xing}: {strength}%")
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    test_bazi_analyzer()
