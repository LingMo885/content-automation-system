#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容质量评估器模块
用于评估生成内容的质量
"""

import logging
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class QualityEvaluator:
    """内容质量评估器类"""
    
    # 评估维度配置
    EVALUATION_DIMENSIONS = {
        "relevance": {
            "name": "相关性",
            "weight": 0.25,
            "description": "内容与八字主题的相关程度",
            "max_score": 100
        },
        "professionalism": {
            "name": "专业性", 
            "weight": 0.25,
            "description": "命理知识的准确性和专业性",
            "max_score": 100
        },
        "readability": {
            "name": "可读性",
            "weight": 0.20,
            "description": "语言流畅度和易读性",
            "max_score": 100
        },
        "attractiveness": {
            "name": "吸引力",
            "weight": 0.20,
            "description": "内容的吸引力和传播性",
            "max_score": 100
        },
        "compliance": {
            "name": "合规性",
            "weight": 0.10,
            "description": "符合平台规范和政策",
            "max_score": 100
        }
    }
    
    # 关键词库
    KEYWORD_LIBRARY = {
        "bazi_terms": ["八字", "命理", "五行", "天干", "地支", "十神", "大运", "流年", "日主", "格局"],
        "professional_terms": ["分析", "解读", "深度", "专业", "准确", "科学", "传统", "文化"],
        "positive_words": ["优秀", "良好", "顺利", "成功", "吉祥", "幸福", "财富", "健康", "智慧"],
        "warning_words": ["注意", "避免", "谨慎", "调整", "改善", "平衡", "化解"],
        "platform_specific": {
            "wechat": ["公众号", "订阅", "分享", "收藏", "在看"],
            "xiaohongshu": ["笔记", "种草", "分享", "点赞", "收藏", "关注"],
            "douyin": ["短视频", "热门", "关注", "点赞", "评论", "分享"],
            "zhihu": ["回答", "问题", "赞同", "收藏", "关注", "专业"],
            "weibo": ["微博", "热搜", "话题", "转发", "评论", "点赞"]
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化质量评估器
        
        Args:
            config_path: 配置文件路径
        """
        self.evaluation_dimensions = self.EVALUATION_DIMENSIONS.copy()
        self.keyword_library = self.KEYWORD_LIBRARY.copy()
        
        if config_path:
            self.load_config(config_path)
        
        logger.info("质量评估器初始化完成")
    
    def load_config(self, config_path: str):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "evaluation_dimensions" in config:
                self.evaluation_dimensions.update(config["evaluation_dimensions"])
            
            if "keyword_library" in config:
                self.keyword_library.update(config["keyword_library"])
            
            logger.info(f"配置文件加载成功: {config_path}")
            
        except Exception as e:
            logger.warning(f"加载配置文件失败: {str(e)}，使用默认配置")
    
    def evaluate(self, content: str, platform: str) -> Dict[str, Any]:
        """
        评估内容质量
        
        Args:
            content: 要评估的内容
            platform: 内容发布的平台
            
        Returns:
            评估结果字典
        """
        try:
            logger.info(f"开始评估内容质量，平台: {platform}")
            
            # 初始化评估结果
            evaluation_result = {
                "overall_score": 0,
                "dimension_scores": {},
                "detailed_analysis": {},
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "metadata": {
                    "platform": platform,
                    "evaluated_at": datetime.now().isoformat(),
                    "content_length": len(content)
                }
            }
            
            # 评估各个维度
            dimension_scores = {}
            detailed_analysis = {}
            
            for dim_key, dim_config in self.evaluation_dimensions.items():
                dim_score, dim_analysis = self.evaluate_dimension(
                    content, platform, dim_key, dim_config
                )
                
                dimension_scores[dim_key] = dim_score
                detailed_analysis[dim_key] = dim_analysis
            
            # 计算综合得分
            overall_score = self.calculate_overall_score(dimension_scores)
            
            # 识别优势和弱点
            strengths, weaknesses = self.identify_strengths_weaknesses(dimension_scores, detailed_analysis)
            
            # 生成改进建议
            recommendations = self.generate_recommendations(dimension_scores, detailed_analysis, platform)
            
            # 构建最终结果
            evaluation_result.update({
                "overall_score": overall_score,
                "dimension_scores": dimension_scores,
                "detailed_analysis": detailed_analysis,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "recommendations": recommendations
            })
            
            # 质量等级
            evaluation_result["quality_grade"] = self.get_quality_grade(overall_score)
            
            logger.info(f"质量评估完成: 综合得分={overall_score}, 等级={evaluation_result['quality_grade']}")
            return evaluation_result
            
        except Exception as e:
            logger.error(f"质量评估失败: {str(e)}", exc_info=True)
            raise
    
    def evaluate_dimension(self, content: str, platform: str, 
                          dimension_key: str, dimension_config: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        评估单个维度
        
        Args:
            content: 内容
            platform: 平台
            dimension_key: 维度键
            dimension_config: 维度配置
            
        Returns:
            (得分, 详细分析)
        """
        if dimension_key == "relevance":
            return self.evaluate_relevance(content)
        elif dimension_key == "professionalism":
            return self.evaluate_professionalism(content)
        elif dimension_key == "readability":
            return self.evaluate_readability(content)
        elif dimension_key == "attractiveness":
            return self.evaluate_attractiveness(content, platform)
        elif dimension_key == "compliance":
            return self.evaluate_compliance(content, platform)
        else:
            # 默认评估
            return 70.0, {"message": "维度评估未实现"}
    
    def evaluate_relevance(self, content: str) -> Tuple[float, Dict[str, Any]]:
        """评估相关性"""
        analysis = {
            "keyword_matches": [],
            "topic_coverage": 0,
            "off_topic_content": []
        }
        
        # 检查八字相关关键词
        bazi_keywords = self.keyword_library.get("bazi_terms", [])
        found_keywords = []
        
        for keyword in bazi_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        analysis["keyword_matches"] = found_keywords
        
        # 计算主题覆盖率
        if bazi_keywords:
            coverage = len(found_keywords) / len(bazi_keywords) * 100
            analysis["topic_coverage"] = min(coverage, 100)
        else:
            analysis["topic_coverage"] = 0
        
        # 检查离题内容（简单实现）
        off_topic_patterns = [
            r'\d{11}',  # 手机号
            r'http[s]?://\S+',  # 链接
            r'@\w+',  # @提及
        ]
        
        off_topic = []
        for pattern in off_topic_patterns:
            matches = re.findall(pattern, content)
            off_topic.extend(matches)
        
        analysis["off_topic_content"] = off_topic
        
        # 计算得分
        score = analysis["topic_coverage"] * 0.7
        
        # 根据关键词数量调整
        keyword_score = min(len(found_keywords) * 10, 30)
        score += keyword_score
        
        # 扣除离题内容分数
        penalty = min(len(off_topic) * 5, 30)
        score = max(score - penalty, 0)
        
        return min(score, 100), analysis
    
    def evaluate_professionalism(self, content: str) -> Tuple[float, Dict[str, Any]]:
        """评估专业性"""
        analysis = {
            "professional_terms": [],
            "terminology_accuracy": 0,
            "logical_structure": True,
            "common_errors": []
        }
        
        # 检查专业术语
        professional_terms = self.keyword_library.get("professional_terms", [])
        found_terms = []
        
        for term in professional_terms:
            if term in content:
                found_terms.append(term)
        
        analysis["professional_terms"] = found_terms
        
        # 检查术语准确性（简化实现）
        # 实际应该检查八字术语的正确使用
        bazi_terms = self.keyword_library.get("bazi_terms", [])
        term_accuracy = 0
        
        for term in bazi_terms:
            if term in content:
                # 检查术语是否在合理上下文中
                # 这里简化处理
                term_accuracy += 5
        
        analysis["terminology_accuracy"] = min(term_accuracy, 100)
        
        # 检查逻辑结构
        # 检查是否有标题、段落、列表等结构
        has_title = bool(re.search(r'^#+\s+.+', content, re.MULTILINE))
        has_paragraphs = len([p for p in content.split('\n\n') if p.strip()]) >= 3
        has_lists = bool(re.search(r'^[*-]\s+.+', content, re.MULTILINE))
        
        analysis["logical_structure"] = has_title and has_paragraphs
        
        # 常见错误检查
        common_errors = []
        
        # 检查过于绝对的说法
        absolute_patterns = [
            r'一定[会|要|能]',
            r'绝对[会|要|能]',
            r'肯定[会|要|能]',
            r'必须[会|要|能]'
        ]
        
        for pattern in absolute_patterns:
            matches = re.findall(pattern, content)
            if matches:
                common_errors.append(f"过于绝对的说法: {matches[0]}")
        
        analysis["common_errors"] = common_errors
        
        # 计算得分
        score = 60  # 基础分
        
        # 专业术语加分
        score += min(len(found_terms) * 5, 20)
        
        # 术语准确性加分
        score += analysis["terminology_accuracy"] * 0.2
        
        # 逻辑结构加分
        if analysis["logical_structure"]:
            score += 10
        
        # 错误扣分
        score -= len(common_errors) * 5
        
        return max(min(score, 100), 0), analysis
    
    def evaluate_readability(self, content: str) -> Tuple[float, Dict[str, Any]]:
        """评估可读性"""
        analysis = {
            "sentence_length_stats": {},
            "paragraph_stats": {},
            "readability_metrics": {},
            "language_issues": []
        }
        
        # 分析句子长度
        sentences = re.split(r'[。！？.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            sentence_lengths = [len(s) for s in sentences]
            analysis["sentence_length_stats"] = {
                "count": len(sentences),
                "avg_length": sum(sentence_lengths) / len(sentences),
                "max_length": max(sentence_lengths),
                "min_length": min(sentence_lengths)
            }
        
        # 分析段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if paragraphs:
            paragraph_lengths = [len(p) for p in paragraphs]
            analysis["paragraph_stats"] = {
                "count": len(paragraphs),
                "avg_length": sum(paragraph_lengths) / len(paragraphs),
                "max_length": max(paragraph_lengths),
                "min_length": min(paragraph_lengths)
            }
        
        # 可读性指标
        total_chars = len(content)
        total_words = len(re.findall(r'\b\w+\b', content))
        
        if total_words > 0:
            # 平均词长
            avg_word_length = total_chars / total_words
            
            # 长句比例（超过50字的句子）
            long_sentences = [s for s in sentences if len(s) > 50]
            long_sentence_ratio = len(long_sentences) / len(sentences) if sentences else 0
            
            # 长段落比例（超过300字的段落）
            long_paragraphs = [p for p in paragraphs if len(p) > 300]
            long_paragraph_ratio = len(long_paragraphs) / len(paragraphs) if paragraphs else 0
            
            analysis["readability_metrics"] = {
                "avg_word_length": avg_word_length,
                "long_sentence_ratio": long_sentence_ratio,
                "long_paragraph_ratio": long_paragraph_ratio
            }
        
        # 语言问题检查
        language_issues = []
        
        # 检查重复词
        words = re.findall(r'\b\w{2,}\b', content)
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        repeated_words = [(word, count) for word, count in word_counts.items() if count > 5]
        if repeated_words:
            language_issues.append(f"词汇重复: {repeated_words[:3]}")
        
        # 检查标点使用
        punctuation_errors = []
        if content.count('，') < content.count(',') * 2:  # 中文内容应该多用中文标点
            punctuation_errors.append("标点使用不当")
        
        if punctuation_errors:
            language_issues.extend(punctuation_errors)
        
        analysis["language_issues"] = language_issues
        
        # 计算得分
        score = 70  # 基础分
        
        # 句子长度优化
        if sentences:
            avg_sentence_len = analysis["sentence_length_stats"]["avg_length"]
            if 15 <= avg_sentence_len <= 30:
                score += 10
            elif avg_sentence_len > 50:
                score -= 10
        
        # 段落长度优化
        if paragraphs:
            avg_paragraph_len = analysis["paragraph_stats"]["avg_length"]
            if 100 <= avg_paragraph_len <= 300:
                score += 10
            elif avg_paragraph_len > 500:
                score -= 10
        
        # 语言问题扣分
        score -= len(language_issues) * 5
        
        return max(min(score, 100), 0), analysis
    
    def evaluate_attractiveness(self, content: str, platform: str) -> Tuple[float, Dict[str, Any]]:
        """评估吸引力"""
        analysis = {
            "engagement_elements": [],
            "visual_elements": [],
            "emotional_appeal": 0,
            "call_to_action": False
        }
        
        # 互动元素检查
        engagement_patterns = {
            "questions": r'[？?].*[吗呢吧]|[你您].*[知道|觉得|认为]',
            "exclamations": r'[！!]',
            "invitations": r'欢迎|关注|点赞|分享|收藏|评论',
            "emojis": r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]'
        }
        
        for element_type, pattern in engagement_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                analysis["engagement_elements"].append(element_type)
        
        # 视觉元素检查
        visual_elements = []
        
        # 检查标题格式
        if re.search(r'^#+\s+.+', content, re.MULTILINE):
            visual_elements.append("标题")
        
        # 检查列表
        if re.search(r'^[*-]\s+.+', content, re.MULTILINE):
            visual_elements.append("列表")
        
        # 检查表格或结构化内容
        if '|' in content or '---' in content:
            visual_elements.append("表格")
        
        analysis["visual_elements"] = visual_elements
        
        # 情感吸引力
        positive_words = self.keyword_library.get("positive_words", [])
        warning_words = self.keyword_library.get("warning_words", [])
        
        positive_count = sum(1 for word in positive_words if word in content)
        warning_count = sum(1 for word in warning_words if word in content)
        
        # 平衡正面和提醒内容
        if positive_count > 0 and warning_count > 0:
            emotional_balance = min(positive_count / (positive_count + warning_count) * 100, 100)
        elif positive_count > 0:
            emotional_balance = 80
        elif warning_count > 0:
            emotional_balance = 60
        else:
            emotional_balance = 50
        
        analysis["emotional_appeal"] = emotional_balance
        
        # 行动号召检查
        cta_patterns = [
            r'关注[我|我们]',
            r'点赞[支持]',
            r'分享[给朋友]',
            r'收藏[本文]',
            r'评论[区]'
        ]
        
        has_cta = any(re.search(pattern, content) for pattern in cta_patterns)
        analysis["call_to_action"] = has_cta
        
        # 平台特定元素
        platform_specific = self.keyword_library.get("platform_specific", {}).get(platform, [])
        platform_elements = []
        
        for element in platform_specific:
            if element in content:
                platform_elements.append(element)
        
        if platform_elements:
            analysis["engagement_elements"].extend([f"platform_{e}" for e in platform_elements])
        
        # 计算得分
        score = 60  # 基础分
        
        # 互动元素加分
        engagement_score = len(analysis["engagement_elements"]) * 5
        score += min(engagement_score, 20)
        
        # 视觉元素加分
        visual_score = len(analysis["visual_elements"]) * 5
        score += min(visual_score, 15)
        
        # 情感吸引力加分
        score += analysis["emotional_appeal"] * 0.1
        
        # 行动号召加分
        if analysis["call_to_action"]:
            score += 10
        
        return max(min(score, 100), 0), analysis
    
    def evaluate_compliance(self, content: str, platform: str) -> Tuple[float, Dict[str, Any]]:
        """评估合规性"""
        analysis = {
            "platform_rules_violations": [],
            "content_restrictions": [],
            "safety_issues": [],
            "compliance_score": 0
        }
        
        # 平台特定规则检查
        platform_rules = {
            "wechat": [
                (r'微信[号|群]', "避免直接提及微信号"),
                (r'二维码', "谨慎使用二维码"),
                (r'诱导分享', "检查是否诱导分享")
            ],
            "xiaohongshu": [
                (r'联系方式', "避免直接联系方式"),
                (r'价格信息', "谨慎标注价格"),
                (r'广告推广', "检查是否硬广")
            ],
            "douyin": [
                (r'敏感词', "检查敏感词"),
                (r'联系方式', "避免直接联系方式"),
                (r'竞品提及', "避免提及竞品")
            ],
            "zhihu": [
                (r'广告内容', "检查广告内容"),
                (r'不实信息', "检查信息真实性"),
                (r'人身攻击', "检查攻击性语言")
            ],
            "weibo": [
                (r'敏感话题', "检查敏感话题"),
                (r'谣言', "检查不实信息"),
                (r'攻击性语言', "检查攻击性语言")
            ]
        }
        
        violations = []
        rules = platform_rules.get(platform, [])
        
        for pattern, description in rules:
            if re.search(pattern, content):
                violations.append(description)
        
        analysis["platform_rules_violations"] = violations
        
        # 内容限制检查
        restricted_patterns = [
            (r'赌博|赌场|彩票', "赌博相关内容"),
            (r'色情|淫秽|低俗', "色情低俗内容"),
            (r'暴力|血腥|恐怖', "暴力恐怖内容"),
            (r'政治敏感', "政治敏感内容"),
            (r'诈骗|骗局', "诈骗相关内容")
        ]
        
        restrictions = []
        for pattern, description in restricted_patterns:
            if re.search(pattern, content):
                restrictions.append(description)
        
        analysis["content_restrictions"] = restrictions
        
        # 安全检查
        safety_issues = []
        
        # 检查个人信息
        personal_info_patterns = [
            r'\d{11}',  # 手机号
            r'\d{18}',  # 身份证号
            r'\d{16}',  # 银行卡号
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # 邮箱
        ]
        
        for pattern in personal_info_patterns:
            matches = re.findall(pattern, content)
            if matches:
                safety_issues.append(f"个人信息泄露风险: {pattern}")
        
        analysis["safety_issues"] = safety_issues
        
        # 计算合规得分
        compliance_score = 100  # 基础分
        
        # 违规扣分
        compliance_score -= len(violations) * 20
        compliance_score -= len(restrictions) * 50  # 严重违规
        compliance_score -= len(safety_issues) * 30
        
        analysis["compliance_score"] = max(compliance_score, 0)
        
        return max(compliance_score, 0), analysis
    
    def calculate_overall_score(self, dimension_scores: Dict[str, float]) -> float:
        """计算综合得分"""
        total_score = 0
        total_weight = 0
        
        for dim_key, dim_config in self.evaluation_dimensions.items():
            weight = dim_config.get("weight", 0)
            score = dimension_scores.get(dim_key, 0)
            
            total_score += score * weight
            total_weight += weight
        
        if total_weight > 0:
            overall_score = total_score / total_weight
        else:
            overall_score = 0
        
        return round(overall_score, 2)
    
    def identify_strengths_weaknesses(self, dimension_scores: Dict[str, float], 
                                     detailed_analysis: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """识别优势和弱点"""
        strengths = []
        weaknesses = []
        
        # 根据维度得分识别
        for dim_key, score in dimension_scores.items():
            dim_name = self.evaluation_dimensions.get(dim_key, {}).get("name", dim_key)
            
            if score >= 80:
                strengths.append(f"{dim_name}优秀（{score}分）")
            elif score <= 60:
                weaknesses.append(f"{dim_name}待提升（{score}分）")
        
        # 从详细分析中提取具体点
        for dim_key, analysis in detailed_analysis.items():
            dim_name = self.evaluation_dimensions.get(dim_key, {}).get("name", dim_key)
            
            # 检查具体问题
            if dim_key == "readability" and analysis.get("language_issues"):
                weaknesses.append(f"{dim_name}: {', '.join(analysis['language_issues'][:2])}")
            
            if dim_key == "professionalism" and analysis.get("common_errors"):
                weaknesses.append(f"{dim_name}: {', '.join(analysis['common_errors'][:2])}")
            
            if dim_key == "attractiveness" and analysis.get("engagement_elements"):
                engagement_count = len(analysis["engagement_elements"])
                if engagement_count >= 3:
                    strengths.append(f"{dim_name}: 互动元素丰富")
                elif engagement_count == 0:
                    weaknesses.append(f"{dim_name}: 缺乏互动元素")
        
        return strengths[:3], weaknesses[:3]  # 各返回前3个
    
    def generate_recommendations(self, dimension_scores: Dict[str, float], 
                                detailed_analysis: Dict[str, Any], platform: str) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 根据低分维度生成建议
        for dim_key, score in dimension_scores.items():
            if score < 70:
                dim_name = self.evaluation_dimensions.get(dim_key, {}).get("name", dim_key)
                
                if dim_key == "relevance":
                    recommendations.append(f"增加八字相关关键词，提升{dim_name}")
                elif dim_key == "professionalism":
                    recommendations.append(f"检查命理术语准确性，提升{dim_name}")
                elif dim_key == "readability":
                    recommendations.append(f"优化句子长度和段落结构，提升{dim_name}")
                elif dim_key == "attractiveness":
                    recommendations.append(f"添加更多互动元素和视觉呈现，提升{dim_name}")
                elif dim_key == "compliance":
                    recommendations.append(f"检查平台规则遵守情况，提升{dim_name}")
        
        # 从详细分析中提取具体建议
        if "readability" in detailed_analysis:
            analysis = detailed_analysis["readability"]
            
            if analysis.get("sentence_length_stats", {}).get("avg_length", 0) > 50:
                recommendations.append("句子过长，建议拆分长句")
            
            if analysis.get("paragraph_stats", {}).get("avg_length", 0) > 400:
                recommendations.append("段落过长，建议拆分段落")
        
        if "attractiveness" in detailed_analysis:
            analysis = detailed_analysis["attractiveness"]
            
            if not analysis.get("call_to_action", False):
                recommendations.append("添加明确的行动号召，如'关注'、'点赞'等")
            
            if len(analysis.get("visual_elements", [])) < 2:
                recommendations.append("增加视觉元素，如列表、标题等")
        
        # 平台特定建议
        platform_suggestions = {
            "wechat": ["使用公众号特色格式", "添加公众号引导"],
            "xiaohongshu": ["添加更多emoji", "使用小红书特色标签"],
            "douyin": ["内容更加简短", "使用热门话题标签"],
            "zhihu": ["增加专业引用", "使用知乎特色格式"],
            "weibo": ["添加话题标签", "使用微博热门格式"]
        }
        
        if platform in platform_suggestions:
            recommendations.extend(platform_suggestions[platform][:2])
        
        return recommendations[:5]  # 返回前5条建议
    
    def get_quality_grade(self, score: float) -> str:
        """获取质量等级"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "合格"
        elif score >= 60:
            return "待改进"
        else:
            return "不合格"
    
    def save_evaluation(self, evaluation_result: Dict[str, Any], file_path: str):
        """保存评估结果"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"评估结果已保存到: {file_path}")
            
        except Exception as e:
            logger.error(f"保存评估结果失败: {str(e)}")
            raise


# 测试函数
def test_quality_evaluator():
    """测试质量评估器"""
    print("测试质量评估器...")
    
    evaluator = QualityEvaluator()
    
    # 测试内容
    test_content = """
# 张三的八字命理深度分析

## 基本信息
- 姓名：张三
- 出生：1990年1月1日 12:00
- 八字：甲子 乙丑 丙寅 丁卯

## 命理分析
丙火日主，热情开朗，有创造力。五行火旺，适合从事营销、娱乐等行业。

## 性格特点
1. 热情大方
2. 领导力强
3. 有时急躁

## 事业建议
发挥火元素优势，把握时机发展事业。

## 温馨提示
命理仅供参考，努力才是关键！

关注我，获取更多命理知识！
"""
    
    try:
        print("评估微信公众号内容...")
        result = evaluator.evaluate(test_content, "wechat")
        
        print(f"\n综合得分: {result['overall_score']}")
        print(f"质量等级: {result['quality_grade']}")
        
        print("\n维度得分:")
        for dim_key, score in result['dimension_scores'].items():
            dim_name = evaluator.EVALUATION_DIMENSIONS.get(dim_key, {}).get("name", dim_key)
            print(f"  {dim_name}: {score}")
        
        print("\n优势:")
        for strength in result['strengths']:
            print(f"  - {strength}")
        
        print("\n待改进:")
        for weakness in result['weaknesses']:
            print(f"  - {weakness}")
        
        print("\n建议:")
        for recommendation in result['recommendations']:
            print(f"  - {recommendation}")
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_quality_evaluator()