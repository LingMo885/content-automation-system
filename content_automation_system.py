#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字内容自动化生成系统
主程序文件
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入自定义模块
from ba_zi_analyzer import BaZiAnalyzer
from content_generator import ContentGenerator
from platform_adapter import PlatformAdapter
from quality_evaluator import QualityEvaluator
from publishing_planner import PublishingPlanner
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContentAutomationSystem:
    """八字内容自动化生成系统主类"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化系统
        
        Args:
            config_path: 配置文件路径
        """
        self.config = Config(config_path)
        self.initialize_modules()
        logger.info("八字内容自动化生成系统初始化完成")
    
    def initialize_modules(self):
        """初始化所有模块"""
        # 八字分析器
        self.bazi_analyzer = BaZiAnalyzer()
        
        # 内容生成器
        template_dir = self.config.get("template_dir", "content_templates")
        self.content_generator = ContentGenerator(template_dir)
        
        # 平台适配器
        self.platform_adapter = PlatformAdapter()
        
        # 质量评估器
        self.quality_evaluator = QualityEvaluator()
        
        # 发布规划器
        self.publishing_planner = PublishingPlanner()
        
        logger.info("所有模块初始化完成")
    
    def process_bazi_content(self, birth_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理八字内容生成全流程
        
        Args:
            birth_info: 八字信息字典
            
        Returns:
            处理结果字典
        """
        try:
            logger.info(f"开始处理八字内容: {birth_info}")
            
            # 1. 八字分析
            logger.info("步骤1: 八字分析")
            bazi_analysis = self.bazi_analyzer.analyze(birth_info)
            
            if not bazi_analysis:
                raise ValueError("八字分析失败")
            
            # 2. 内容生成
            logger.info("步骤2: 内容生成")
            base_content = self.content_generator.generate_base_content(bazi_analysis)
            
            # 3. AI优化
            logger.info("步骤3: AI优化")
            enhanced_content = self.content_generator.ai_enhance(base_content)
            
            # 4. 多平台适配
            logger.info("步骤4: 多平台适配")
            platform_contents = {}
            platforms = self.config.get("platforms", ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"])
            
            for platform in platforms:
                platform_content = self.platform_adapter.adapt_content(
                    enhanced_content, platform
                )
                platform_contents[platform] = platform_content
            
            # 5. 质量评估
            logger.info("步骤5: 质量评估")
            quality_scores = {}
            for platform, content in platform_contents.items():
                score = self.quality_evaluator.evaluate(content, platform)
                quality_scores[platform] = score
            
            # 6. 发布规划
            logger.info("步骤6: 发布规划")
            publishing_schedule = self.publishing_planner.plan_publishing(
                platform_contents, quality_scores
            )
            
            # 7. 保存结果
            logger.info("步骤7: 保存结果")
            result = self.save_results(
                birth_info=birth_info,
                bazi_analysis=bazi_analysis,
                platform_contents=platform_contents,
                quality_scores=quality_scores,
                publishing_schedule=publishing_schedule
            )
            
            logger.info(f"八字内容处理完成: {result['result_id']}")
            return result
            
        except Exception as e:
            logger.error(f"处理八字内容时出错: {str(e)}", exc_info=True)
            raise
    
    def save_results(self, **kwargs) -> Dict[str, Any]:
        """
        保存处理结果
        
        Args:
            **kwargs: 各种结果数据
            
        Returns:
            保存结果
        """
        result_id = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建结果目录
        output_dir = self.config.get("output_dir", "output")
        result_dir = os.path.join(output_dir, result_id)
        os.makedirs(result_dir, exist_ok=True)
        
        # 保存八字分析结果
        if 'bazi_analysis' in kwargs:
            bazi_file = os.path.join(result_dir, "bazi_analysis.json")
            with open(bazi_file, 'w', encoding='utf-8') as f:
                json.dump(kwargs['bazi_analysis'], f, ensure_ascii=False, indent=2)
        
        # 保存平台内容
        if 'platform_contents' in kwargs:
            for platform, content in kwargs['platform_contents'].items():
                content_file = os.path.join(result_dir, f"{platform}_content.md")
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # 保存质量评估结果
        if 'quality_scores' in kwargs:
            quality_file = os.path.join(result_dir, "quality_scores.json")
            with open(quality_file, 'w', encoding='utf-8') as f:
                json.dump(kwargs['quality_scores'], f, ensure_ascii=False, indent=2)
        
        # 保存发布计划
        if 'publishing_schedule' in kwargs:
            schedule_file = os.path.join(result_dir, "publishing_schedule.json")
            with open(schedule_file, 'w', encoding='utf-8') as f:
                json.dump(kwargs['publishing_schedule'], f, ensure_ascii=False, indent=2)
        
        # 保存元数据
        metadata = {
            "result_id": result_id,
            "created_at": datetime.now().isoformat(),
            "birth_info": kwargs.get('birth_info', {}),
            "files": {
                "bazi_analysis": "bazi_analysis.json",
                "platform_contents": [f"{p}_content.md" for p in kwargs.get('platform_contents', {}).keys()],
                "quality_scores": "quality_scores.json",
                "publishing_schedule": "publishing_schedule.json"
            }
        }
        
        metadata_file = os.path.join(result_dir, "metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return metadata
    
    def batch_process(self, birth_info_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量处理八字内容
        
        Args:
            birth_info_list: 八字信息列表
            
        Returns:
            处理结果列表
        """
        results = []
        
        for i, birth_info in enumerate(birth_info_list):
            try:
                logger.info(f"处理第 {i+1}/{len(birth_info_list)} 个八字")
                result = self.process_bazi_content(birth_info)
                results.append(result)
            except Exception as e:
                logger.error(f"处理第 {i+1} 个八字时出错: {str(e)}")
                results.append({
                    "error": str(e),
                    "birth_info": birth_info
                })
        
        return results
    
    def generate_daily_content(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        生成每日内容
        
        Args:
            count: 生成内容数量
            
        Returns:
            生成结果列表
        """
        # 从配置或数据库中获取八字信息
        # 这里简化处理，随机生成八字信息
        import random
        from datetime import datetime, timedelta
        
        birth_info_list = []
        for i in range(count):
            # 随机生成出生日期（1980-2010年）
            year = random.randint(1980, 2010)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            
            birth_info = {
                "birth_date": f"{year}-{month:02d}-{day:02d}",
                "birth_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                "gender": random.choice(["male", "female"]),
                "name": f"测试用户{i+1}"
            }
            birth_info_list.append(birth_info)
        
        return self.batch_process(birth_info_list)


def main():
    """主函数"""
    print("=" * 60)
    print("八字内容自动化生成系统")
    print("=" * 60)
    
    try:
        # 初始化系统
        system = ContentAutomationSystem()
        
        # 示例八字信息
        example_birth_info = {
            "birth_date": "1990-01-01",
            "birth_time": "12:00",
            "gender": "male",
            "name": "张三"
        }
        
        print("\n1. 单次处理示例:")
        print(f"八字信息: {example_birth_info}")
        
        result = system.process_bazi_content(example_birth_info)
        print(f"处理完成! 结果ID: {result['result_id']}")
        print(f"结果保存在: output/{result['result_id']}/")
        
        print("\n2. 批量生成示例:")
        batch_results = system.generate_daily_content(count=3)
        print(f"批量生成完成! 共生成 {len(batch_results)} 个内容")
        
        print("\n3. 系统状态:")
        print(f"- 模板目录: {system.config.get('template_dir')}")
        print(f"- 支持平台: {', '.join(system.config.get('platforms', []))}")
        print(f"- 输出目录: {system.config.get('output_dir')}")
        
        print("\n系统运行完成!")
        
    except Exception as e:
        print(f"系统运行出错: {str(e)}")
        logger.error(f"系统运行出错: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()