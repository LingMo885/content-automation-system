#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布规划器模块
用于规划内容的发布时间和平台
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

logger = logging.getLogger(__name__)


class PublishingPlanner:
    """发布规划器类"""
    
    # 平台最佳发布时间
    PLATFORM_BEST_TIMES = {
        "wechat": [
            {"time": "07:00", "weight": 0.8, "description": "早晨通勤时间"},
            {"time": "12:00", "weight": 0.9, "description": "午休时间"},
            {"time": "18:00", "weight": 0.7, "description": "下班通勤时间"},
            {"time": "21:00", "weight": 1.0, "description": "晚间休闲时间"}
        ],
        "xiaohongshu": [
            {"time": "10:00", "weight": 0.9, "description": "上午活跃时间"},
            {"time": "14:00", "weight": 0.8, "description": "下午茶时间"},
            {"time": "19:00", "weight": 1.0, "description": "晚间黄金时间"},
            {"time": "22:00", "weight": 0.7, "description": "睡前时间"}
        ],
        "douyin": [
            {"time": "12:00", "weight": 0.9, "description": "午休高峰"},
            {"time": "18:00", "weight": 0.8, "description": "下班时间"},
            {"time": "21:00", "weight": 1.0, "description": "晚间高峰"},
            {"time": "23:00", "weight": 0.6, "description": "深夜时间"}
        ],
        "zhihu": [
            {"time": "08:00", "weight": 0.8, "description": "早晨学习时间"},
            {"time": "13:00", "weight": 0.7, "description": "午休阅读时间"},
            {"time": "19:00", "weight": 0.9, "description": "晚间深度阅读时间"},
            {"time": "22:00", "weight": 0.6, "description": "睡前思考时间"}
        ],
        "weibo": [
            {"time": "09:00", "weight": 0.8, "description": "上班摸鱼时间"},
            {"time": "12:00", "weight": 0.9, "description": "午休刷博时间"},
            {"time": "18:00", "weight": 0.8, "description": "下班路上时间"},
            {"time": "22:00", "weight": 0.7, "description": "睡前刷博时间"}
        ]
    }
    
    # 平台发布频率限制
    PLATFORM_FREQUENCY_LIMITS = {
        "wechat": {"daily_max": 3, "min_interval_hours": 4},
        "xiaohongshu": {"daily_max": 5, "min_interval_hours": 2},
        "douyin": {"daily_max": 10, "min_interval_hours": 1},
        "zhihu": {"daily_max": 3, "min_interval_hours": 6},
        "weibo": {"daily_max": 10, "min_interval_hours": 1}
    }
    
    # 内容类型与平台匹配度
    CONTENT_PLATFORM_MATCH = {
        "detailed_analysis": {"wechat": 0.9, "zhihu": 1.0, "xiaohongshu": 0.7, "douyin": 0.4, "weibo": 0.6},
        "quick_tips": {"wechat": 0.7, "zhihu": 0.8, "xiaohongshu": 0.9, "douyin": 0.8, "weibo": 0.9},
        "case_study": {"wechat": 0.8, "zhihu": 0.9, "xiaohongshu": 0.8, "douyin": 0.6, "weibo": 0.7},
        "trending_topic": {"wechat": 0.6, "zhihu": 0.7, "xiaohongshu": 0.9, "douyin": 1.0, "weibo": 1.0}
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化发布规划器
        
        Args:
            config_path: 配置文件路径
        """
        self.platform_best_times = self.PLATFORM_BEST_TIMES.copy()
        self.platform_frequency_limits = self.PLATFORM_FREQUENCY_LIMITS.copy()
        self.content_platform_match = self.CONTENT_PLATFORM_MATCH.copy()
        
        if config_path:
            self.load_config(config_path)
        
        # 发布历史记录
        self.publishing_history = []
        
        logger.info("发布规划器初始化完成")
    
    def load_config(self, config_path: str):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "platform_best_times" in config:
                self.platform_best_times.update(config["platform_best_times"])
            
            if "platform_frequency_limits" in config:
                self.platform_frequency_limits.update(config["platform_frequency_limits"])
            
            if "content_platform_match" in config:
                self.content_platform_match.update(config["content_platform_match"])
            
            logger.info(f"配置文件加载成功: {config_path}")
            
        except Exception as e:
            logger.warning(f"加载配置文件失败: {str(e)}，使用默认配置")
    
    def plan_publishing(self, platform_contents: Dict[str, str], 
                       quality_scores: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        规划内容发布
        
        Args:
            platform_contents: 各平台内容字典 {平台: 内容}
            quality_scores: 各平台质量评估结果
            
        Returns:
            发布计划
        """
        try:
            logger.info("开始规划内容发布")
            
            # 分析内容类型
            content_type = self.analyze_content_type(platform_contents)
            
            # 选择发布平台
            selected_platforms = self.select_publishing_platforms(
                platform_contents, quality_scores, content_type
            )
            
            # 规划发布时间
            publishing_schedule = self.schedule_publishing_times(
                selected_platforms, content_type
            )
            
            # 生成发布策略
            publishing_strategy = self.generate_publishing_strategy(
                publishing_schedule, quality_scores
            )
            
            # 构建发布计划
            publishing_plan = {
                "content_type": content_type,
                "selected_platforms": selected_platforms,
                "publishing_schedule": publishing_schedule,
                "publishing_strategy": publishing_strategy,
                "estimated_effect": self.estimate_publishing_effect(publishing_schedule, quality_scores),
                "plan_created_at": datetime.now().isoformat(),
                "plan_id": f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            # 保存到历史记录
            self.publishing_history.append({
                "plan_id": publishing_plan["plan_id"],
                "created_at": publishing_plan["plan_created_at"],
                "platforms": list(selected_platforms.keys())
            })
            
            logger.info(f"发布计划生成完成: {publishing_plan['plan_id']}")
            return publishing_plan
            
        except Exception as e:
            logger.error(f"发布规划失败: {str(e)}", exc_info=True)
            raise
    
    def analyze_content_type(self, platform_contents: Dict[str, str]) -> str:
        """
        分析内容类型
        
        Args:
            platform_contents: 各平台内容
            
        Returns:
            内容类型
        """
        # 获取一个平台的内容进行分析
        sample_content = next(iter(platform_contents.values()), "")
        
        if not sample_content:
            return "quick_tips"
        
        # 根据内容特征判断类型
        content_length = len(sample_content)
        has_detailed_analysis = any(keyword in sample_content for keyword in 
                                   ["深度分析", "详细解读", "专业分析", "全面解析"])
        has_case_study = any(keyword in sample_content for keyword in 
                            ["案例", "实例", "例子", "实际"])
        has_trending = any(keyword in sample_content for keyword in 
                          ["热门", "趋势", "最新", "潮流"])
        
        if content_length > 2000 and has_detailed_analysis:
            return "detailed_analysis"
        elif has_case_study:
            return "case_study"
        elif has_trending:
            return "trending_topic"
        elif content_length < 500:
            return "quick_tips"
        else:
            return "general_content"
    
    def select_publishing_platforms(self, platform_contents: Dict[str, str], 
                                   quality_scores: Dict[str, Dict[str, Any]], 
                                   content_type: str) -> Dict[str, Dict[str, Any]]:
        """
        选择发布平台
        
        Args:
            platform_contents: 各平台内容
            quality_scores: 质量评估结果
            content_type: 内容类型
            
        Returns:
            选择的平台及其信息
        """
        selected_platforms = {}
        
        # 获取内容类型与平台的匹配度
        type_match_scores = self.content_platform_match.get(content_type, {})
        
        for platform, content in platform_contents.items():
            # 检查内容是否为空
            if not content or len(content.strip()) < 50:
                logger.warning(f"平台 {platform} 内容过短，跳过")
                continue
            
            # 检查质量评分
            platform_quality = quality_scores.get(platform, {})
            overall_score = platform_quality.get("overall_score", 0)
            
            if overall_score < 60:
                logger.warning(f"平台 {platform} 质量评分过低 ({overall_score})，跳过")
                continue
            
            # 计算平台选择得分
            match_score = type_match_scores.get(platform, 0.5)
            quality_weight = overall_score / 100
            
            # 平台选择得分 = 匹配度 * 质量权重
            selection_score = match_score * quality_weight
            
            # 考虑平台限制
            frequency_limit = self.platform_frequency_limits.get(platform, {})
            daily_max = frequency_limit.get("daily_max", 3)
            
            # 检查今日已发布次数
            today_posts = self.get_today_posts_count(platform)
            if today_posts >= daily_max:
                logger.warning(f"平台 {platform} 今日已发布 {today_posts} 次，达到上限")
                continue
            
            # 平台信息
            platform_info = {
                "content": content,
                "content_length": len(content),
                "quality_score": overall_score,
                "selection_score": round(selection_score, 3),
                "match_score": match_score,
                "today_posts": today_posts,
                "daily_limit": daily_max,
                "min_interval": frequency_limit.get("min_interval_hours", 2)
            }
            
            selected_platforms[platform] = platform_info
        
        # 按选择得分排序
        sorted_platforms = dict(sorted(
            selected_platforms.items(),
            key=lambda x: x[1]["selection_score"],
            reverse=True
        ))
        
        # 限制平台数量
        max_platforms = min(5, len(sorted_platforms))
        selected = dict(list(sorted_platforms.items())[:max_platforms])
        
        logger.info(f"选择了 {len(selected)} 个平台: {list(selected.keys())}")
        return selected
    
    def schedule_publishing_times(self, selected_platforms: Dict[str, Dict[str, Any]], 
                                 content_type: str) -> List[Dict[str, Any]]:
        """
        规划发布时间
        
        Args:
            selected_platforms: 选择的平台
            content_type: 内容类型
            
        Returns:
            发布时间安排
        """
        schedule = []
        current_time = datetime.now()
        
        # 对平台进行排序（按选择得分）
        sorted_platforms = sorted(
            selected_platforms.items(),
            key=lambda x: x[1]["selection_score"],
            reverse=True
        )
        
        for i, (platform, platform_info) in enumerate(sorted_platforms):
            # 计算发布时间
            publish_time = self.calculate_publish_time(
                platform, content_type, i, current_time
            )
            
            # 检查时间间隔
            if i > 0:
                prev_time = schedule[-1]["scheduled_time"]
                min_interval = platform_info["min_interval"]
                
                time_diff = (publish_time - prev_time).total_seconds() / 3600
                if time_diff < min_interval:
                    # 调整时间以满足间隔要求
                    publish_time = prev_time + timedelta(hours=min_interval)
            
            # 构建时间安排
            time_slot = {
                "platform": platform,
                "scheduled_time": publish_time,
                "time_str": publish_time.strftime("%Y-%m-%d %H:%M"),
                "content_type": content_type,
                "content_length": platform_info["content_length"],
                "quality_score": platform_info["quality_score"],
                "selection_score": platform_info["selection_score"],
                "time_slot_score": self.evaluate_time_slot(platform, publish_time)
            }
            
            schedule.append(time_slot)
            
            # 更新当前时间
            current_time = publish_time
        
        return schedule
    
    def calculate_publish_time(self, platform: str, content_type: str, 
                              platform_index: int, base_time: datetime) -> datetime:
        """
        计算发布时间
        
        Args:
            platform: 平台名称
            content_type: 内容类型
            platform_index: 平台索引
            base_time: 基准时间
            
        Returns:
            发布时间
        """
        # 获取平台最佳时间
        best_times = self.platform_best_times.get(platform, [])
        
        if not best_times:
            # 默认时间：当前时间+平台索引小时
            return base_time + timedelta(hours=platform_index + 1)
        
        # 根据内容类型选择时间策略
        if content_type == "detailed_analysis":
            # 深度内容适合晚间发布
            preferred_times = [t for t in best_times if "晚间" in t["description"] or "晚上" in t["description"]]
        elif content_type == "quick_tips":
            # 快速提示适合白天发布
            preferred_times = [t for t in best_times if "午" in t["description"] or "白天" in t["description"]]
        else:
            preferred_times = best_times
        
        if not preferred_times:
            preferred_times = best_times
        
        # 根据权重选择时间
        weights = [t["weight"] for t in preferred_times]
        selected_time = random.choices(preferred_times, weights=weights, k=1)[0]
        
        # 解析时间
        time_str = selected_time["time"]
        hour, minute = map(int, time_str.split(':'))
        
        # 计算具体日期
        target_date = base_time.date()
        
        # 如果当前时间已经过了选择的时间，则安排到明天
        current_hour = base_time.hour
        if current_hour > hour or (current_hour == hour and base_time.minute > minute):
            target_date += timedelta(days=1)
        
        # 如果是第一个平台，可以安排在今天的最佳时间之后
        if platform_index == 0 and current_hour < hour:
            # 今天还有时间，安排在今天
            pass
        elif platform_index > 0:
            # 后续平台安排在下一天
            target_date += timedelta(days=platform_index)
        
        publish_time = datetime.combine(target_date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
        
        # 添加随机分钟偏移（0-15分钟）
        minute_offset = random.randint(0, 15)
        publish_time += timedelta(minutes=minute_offset)
        
        return publish_time
    
    def evaluate_time_slot(self, platform: str, publish_time: datetime) -> float:
        """
        评估时间槽质量
        
        Args:
            platform: 平台名称
            publish_time: 发布时间
            
        Returns:
            时间槽评分
        """
        hour = publish_time.hour
        weekday = publish_time.weekday()  # 0=周一, 6=周日
        
        # 获取平台最佳时间
        best_times = self.platform_best_times.get(platform, [])
        
        # 查找最接近的最佳时间
        best_score = 0.5  # 基础分
        
        for time_slot in best_times:
            slot_hour = int(time_slot["time"].split(':')[0])
            time_diff = abs(hour - slot_hour)
            
            if time_diff == 0:
                # 完全匹配最佳时间
                best_score = max(best_score, time_slot["weight"])
            elif time_diff <= 1:
                # 接近最佳时间
                best_score = max(best_score, time_slot["weight"] * 0.8)
            elif time_diff <= 2:
                # 较接近最佳时间
                best_score = max(best_score, time_slot["weight"] * 0.6)
        
        # 考虑工作日 vs 周末
        if weekday >= 5:  # 周末
            # 周末发布时间可以稍晚
            if 10 <= hour <= 23:
                best_score *= 1.1
        else:  # 工作日
            # 工作日避开工作时间
            if 9 <= hour <= 17:
                best_score *= 0.9
        
        return min(best_score, 1.0)
    
    def generate_publishing_strategy(self, publishing_schedule: List[Dict[str, Any]], 
                                    quality_scores: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成发布策略
        
        Args:
            publishing_schedule: 发布时间安排
            quality_scores: 质量评估结果
            
        Returns:
            发布策略
        """
        strategy = {
            "overall_strategy": "",
            "platform_strategies": {},
            "optimization_tips": [],
            "risk_warnings": []
        }
        
        # 分析整体策略
        if len(publishing_schedule) == 1:
            strategy["overall_strategy"] = "单平台重点发布，集中资源打造爆款"
        elif len(publishing_schedule) <= 3:
            strategy["overall_strategy"] = "多平台协同发布，覆盖不同用户群体"
        else:
            strategy["overall_strategy"] = "全平台矩阵发布，最大化内容曝光"
        
        # 生成各平台策略
        for schedule in publishing_schedule:
            platform = schedule["platform"]
            quality_info = quality_scores.get(platform, {})
            
            platform_strategy = {
                "publish_time": schedule["time_str"],
                "content_type": schedule["content_type"],
                "quality_grade": quality_info.get("quality_grade", "未知"),
                "key_strengths": quality_info.get("strengths", [])[:2],
                "main_improvements": quality_info.get("recommendations", [])[:2],
                "estimated_engagement": self.estimate_platform_engagement(platform, schedule)
            }
            
            strategy["platform_strategies"][platform] = platform_strategy
        
        # 生成优化建议
        optimization_tips = []
        
        # 时间优化
        time_scores = [s["time_slot_score"] for s in publishing_schedule]
        avg_time_score = sum(time_scores) / len(time_scores) if time_scores else 0
        
        if avg_time_score < 0.7:
            optimization_tips.append("部分发布时间可以进一步优化，选择平台活跃高峰")
        
        # 内容优化
        for platform, quality_info in quality_scores.items():
            if quality_info.get("overall_score", 0) < 70:
                optimization_tips.append(f"{platform}内容质量有待提升，建议优化后再发布")
        
        strategy["optimization_tips"] = optimization_tips[:3]
        
        # 风险警告
        risk_warnings = []
        
        # 检查发布时间冲突
        if len(publishing_schedule) > 1:
            time_diffs = []
            for i in range(1, len(publishing_schedule)):
                time1 = publishing_schedule[i-1]["scheduled_time"]
                time2 = publishing_schedule[i]["scheduled_time"]
                diff_hours = (time2 - time1).total_seconds() / 3600
                time_diffs.append(diff_hours)
            
            if any(diff < 1 for diff in time_diffs):
                risk_warnings.append("部分发布时间间隔过短，可能影响发布效果")
        
        # 检查内容合规性
        for platform, quality_info in quality_scores.items():
            compliance_score = quality_info.get("dimension_scores", {}).get("compliance", 100)
            if compliance_score < 80:
                risk_warnings.append(f"{platform}内容合规性需要注意")
        
        strategy["risk_warnings"] = risk_warnings[:3]
        
        return strategy
    
    def estimate_platform_engagement(self, platform: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """估算平台互动效果"""
        base_engagement = {
            "wechat": {"views": 500, "likes": 50, "shares": 20, "comments": 30},
            "xiaohongshu": {"views": 1000, "likes": 200, "collects": 100, "comments": 50},
            "douyin": {"views": 5000, "likes": 500, "shares": 200, "comments": 100},
            "zhihu": {"views": 800, "upvotes": 100, "collects": 50, "comments": 40},
            "weibo": {"views": 2000, "likes": 300, "reposts": 100, "comments": 80}
        }
        
        base = base_engagement.get(platform, {"views": 300, "likes": 30, "shares": 10, "comments": 20})
        
        # 根据质量评分调整
        quality_factor = schedule["quality_score"] / 100
        
        # 根据时间槽评分调整
        time_factor = schedule["time_slot_score"]
        
        # 根据内容类型调整
        content_type = schedule["content_type"]
        type_factors = {
            "detailed_analysis": 0.8,  # 深度内容传播较慢
            "quick_tips": 1.2,         # 快速提示传播较快
            "case_study": 1.0,
            "trending_topic": 1.5,     # 热门话题传播最快
            "general_content": 1.0
        }
        type_factor = type_factors.get(content_type, 1.0)
        
        # 计算调整后的互动
        adjusted = {}
        for metric, value in base.items():
            adjusted_value = value * quality_factor * time_factor * type_factor
            # 添加随机波动
            random_factor = random.uniform(0.8, 1.2)
            adjusted[metric] = int(adjusted_value * random_factor)
        
        return adjusted
    
    def estimate_publishing_effect(self, publishing_schedule: List[Dict[str, Any]], 
                                  quality_scores: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """估算发布效果"""
        total_views = 0
        total_engagement = 0
        platform_effects = {}
        
        for schedule in publishing_schedule:
            platform = schedule["platform"]
            engagement = self.estimate_platform_engagement(platform, schedule)
            
            platform_effects[platform] = {
                "estimated_views": engagement.get("views", 0),
                "estimated_engagement": sum([v for k, v in engagement.items() if k != "views"]),
                "engagement_rate": round(engagement.get("likes", 0) / max(engagement.get("views", 1), 1) * 100, 2)
            }
            
            total_views += engagement.get("views", 0)
            total_engagement += sum([v for k, v in engagement.items() if k != "views"])
        
        overall_engagement_rate = round(total_engagement / max(total_views, 1) * 100, 2) if total_views > 0 else 0
        
        return {
            "total_estimated_views": total_views,
            "total_estimated_engagement": total_engagement,
            "overall_engagement_rate": overall_engagement_rate,
            "platform_breakdown": platform_effects,
            "success_probability": self.calculate_success_probability(publishing_schedule, quality_scores)
        }
    
    def calculate_success_probability(self, publishing_schedule: List[Dict[str, Any]], 
                                     quality_scores: Dict[str, Dict[str, Any]]) -> float:
        """计算成功概率"""
        if not publishing_schedule:
            return 0.0
        
        # 基础概率
        base_probability = 0.6
        
        # 质量因素
        quality_scores_list = [quality_scores.get(s["platform"], {}).get("overall_score", 70) for s in publishing_schedule]
        avg_quality = sum(quality_scores_list) / len(quality_scores_list)
        quality_factor = avg_quality / 100
        
        # 时间因素
        time_scores = [s["time_slot_score"] for s in publishing_schedule]
        avg_time_score = sum(time_scores) / len(time_scores)
        
        # 平台数量因素
        platform_count = len(publishing_schedule)
        platform_factor = min(platform_count / 3, 1.2)  # 最多1.2倍
        
        # 计算最终概率
        probability = base_probability * quality_factor * avg_time_score * platform_factor
        
        return min(probability, 0.95)  # 最大95%
    
    def get_today_posts_count(self, platform: str) -> int:
        """获取今日已发布次数"""
        today = datetime.now().date()
        
        today_posts = 0
        for record in self.publishing_history:
            record_date = datetime.fromisoformat(record["created_at"]).date()
            if record_date == today and platform in record["platforms"]:
                today_posts += 1
        
        return today_posts
    
    def save_publishing_plan(self, publishing_plan: Dict[str, Any], file_path: str):
        """保存发布计划"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(publishing_plan, f, ensure_ascii=False, indent=2)
            
            logger.info(f"发布计划已保存到: {file_path}")
            
        except Exception as e:
            logger.error(f"保存发布计划失败: {str(e)}")
            raise
    
    def load_publishing_history(self, file_path: str):
        """加载发布历史"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.publishing_history = json.load(f)
            
            logger.info(f"发布历史加载成功: {file_path}")
            
        except Exception as e:
            logger.warning(f"加载发布历史失败: {str(e)}，使用空历史记录")
    
    def get_publishing_stats(self) -> Dict[str, Any]:
        """获取发布统计"""
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        today_count = 0
        week_count = 0
        platform_distribution = {}
        
        for record in self.publishing_history:
            record_date = datetime.fromisoformat(record["created_at"]).date()
            
            if record_date == today:
                today_count += 1
            
            if record_date >= week_ago:
                week_count += 1
            
            for platform in record["platforms"]:
                platform_distribution[platform] = platform_distribution.get(platform, 0) + 1
        
        return {
            "today_posts": today_count,
            "week_posts": week_count,
            "total_posts": len(self.publishing_history),
            "platform_distribution": platform_distribution,
            "avg_platforms_per_post": round(len(self.publishing_history) / max(sum(platform_distribution.values()), 1), 2)
        }


# 测试函数
def test_publishing_planner():
    """测试发布规划器"""
    print("测试发布规划器...")
    
    planner = PublishingPlanner()
    
    # 测试数据
    test_platform_contents = {
        "wechat": "微信公众号测试内容",
        "xiaohongshu": "小红书测试内容",
        "douyin": "抖音测试内容",
        "zhihu": "知乎测试内容",
        "weibo": "微博测试内容"
    }
    
    test_quality_scores = {
        "wechat": {"overall_score": 85, "quality_grade": "良好", "strengths": ["相关性高"], "recommendations": []},
        "xiaohongshu": {"overall_score": 78, "quality_grade": "合格", "strengths": ["吸引力强"], "recommendations": ["优化可读性"]},
        "douyin": {"overall_score": 65, "quality_grade": "待改进", "strengths": [], "recommendations": ["提升专业性"]},
        "zhihu": {"overall_score": 92, "quality_grade": "优秀", "strengths": ["专业性强"], "recommendations": []},
        "weibo": {"overall_score": 70, "quality_grade": "合格", "strengths": ["互动性好"], "recommendations": ["优化内容"]}
    }
    
    try:
        print("生成发布计划...")
        publishing_plan = planner.plan_publishing(test_platform_contents, test_quality_scores)
        
        print(f"\n计划ID: {publishing_plan['plan_id']}")
        print(f"内容类型: {publishing_plan['content_type']}")
        print(f"选择平台: {', '.join(publishing_plan['selected_platforms'].keys())}")
        
        print(f"\n整体策略: {publishing_plan['publishing_strategy']['overall_strategy']}")
        
        print("\n发布时间安排:")
        for schedule in publishing_plan["publishing_schedule"]:
            print(f"  {schedule['platform']}: {schedule['time_str']} (评分: {schedule['time_slot_score']:.2f})")
        
        print("\n预计效果:")
        effect = publishing_plan["estimated_effect"]
        print(f"  总浏览量: {effect['total_estimated_views']}")
        print(f"  总互动量: {effect['total_estimated_engagement']}")
        print(f"  互动率: {effect['overall_engagement_rate']}%")
        print(f"  成功概率: {effect['success_probability']*100:.1f}%")
        
        print("\n平台策略:")
        for platform, strategy in publishing_plan["publishing_strategy"]["platform_strategies"].items():
            print(f"  {platform}:")
            print(f"    发布时间: {strategy['publish_time']}")
            print(f"    质量等级: {strategy['quality_grade']}")
            print(f"    预计互动: {strategy['estimated_engagement']}")
        
        print("\n优化建议:")
        for tip in publishing_plan["publishing_strategy"]["optimization_tips"]:
            print(f"  - {tip}")
        
        print("\n风险警告:")
        for warning in publishing_plan["publishing_strategy"]["risk_warnings"]:
            print(f"  - {warning}")
        
        print("\n发布统计:")
        stats = planner.get_publishing_stats()
        print(f"  今日发布: {stats['today_posts']}")
        print(f"  本周发布: {stats['week_posts']}")
        print(f"  总发布数: {stats['total_posts']}")
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_publishing_planner()