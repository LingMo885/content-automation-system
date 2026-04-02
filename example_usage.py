#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字内容自动化生成系统使用示例
"""

import os
import sys
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def example_individual_analysis():
    """示例1: 个人八字分析"""
    print("=" * 60)
    print("示例1: 个人八字分析")
    print("=" * 60)
    
    from ba_zi_analyzer import BaZiAnalyzer
    
    # 创建八字分析器
    analyzer = BaZiAnalyzer()
    
    # 个人八字信息
    birth_info = {
        "birth_date": "1990-05-15",
        "birth_time": "08:30",
        "gender": "female",
        "name": "李小红"
    }
    
    print(f"分析对象: {birth_info['name']}")
    print(f"出生日期: {birth_info['birth_date']} {birth_info['birth_time']}")
    print(f"性别: {'男' if birth_info['gender'] == 'male' else '女'}")
    
    # 分析八字
    result = analyzer.analyze(birth_info)
    
    print(f"\n八字四柱: {result['bazi_pillar']}")
    print(f"日主: {result['ri_zhu']['character']} ({result['ri_zhu']['wu_xing']}命)")
    print(f"日主特点: {result['ri_zhu']['description']}")
    
    print("\n五行强弱:")
    for wuxing, strength in result['wu_xing_strength'].items():
        print(f"  {wuxing}: {strength}%")
    
    print(f"\n分析摘要: {result['analysis_summary']}")
    
    # 保存分析结果
    output_file = f"个人八字分析_{birth_info['name']}_{datetime.now().strftime('%Y%m%d')}.json"
    analyzer.save_analysis(output_file)
    print(f"\n分析结果已保存到: {output_file}")
    
    return result


def example_content_generation():
    """示例2: 内容生成"""
    print("\n" + "=" * 60)
    print("示例2: 内容生成")
    print("=" * 60)
    
    from ba_zi_analyzer import BaZiAnalyzer
    from content_generator import ContentGenerator
    
    # 分析八字
    analyzer = BaZiAnalyzer()
    birth_info = {
        "birth_date": "1985-08-20",
        "birth_time": "14:45",
        "gender": "male",
        "name": "王大明"
    }
    
    bazi_analysis = analyzer.analyze(birth_info)
    
    # 生成内容
    generator = ContentGenerator()
    content_structure = generator.generate_base_content(bazi_analysis)
    
    print(f"标题: {content_structure['title']}")
    print(f"摘要: {content_structure['summary']}")
    print(f"标签: {', '.join(content_structure['tags'][:5])}")
    
    print(f"\n内容长度: {len(content_structure['analysis'])} 字符")
    
    # AI优化内容
    enhanced_content = generator.ai_enhance(content_structure)
    print(f"优化后标题: {enhanced_content['title']}")
    
    # 生成各平台内容
    platforms = ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"]
    template_data = generator.prepare_template_data(bazi_analysis)
    
    print("\n各平台内容预览:")
    for platform in platforms:
        content = generator.render_template(platform, template_data)
        print(f"  {platform}: {len(content)} 字符")
    
    return content_structure


def example_quality_evaluation():
    """示例3: 质量评估"""
    print("\n" + "=" * 60)
    print("示例3: 内容质量评估")
    print("=" * 60)
    
    from quality_evaluator import QualityEvaluator
    
    # 测试内容
    test_content = """
# 王大明八字分析

## 基本信息
- 姓名：王大明
- 出生：1985年8月20日 14:45
- 八字：乙丑 甲申 辛卯 丙申

## 命理分析
辛金日主，聪明机智，有分析能力。五行金旺，适合从事金融、法律等行业。

## 性格特点
1. 细致认真
2. 有责任感
3. 有时固执

## 建议
发挥金元素优势，把握时机发展事业。
"""
    
    evaluator = QualityEvaluator()
    
    # 评估微信公众号内容
    print("评估微信公众号内容质量...")
    result = evaluator.evaluate(test_content, "wechat")
    
    print(f"综合得分: {result['overall_score']}")
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
    
    return result


def example_publishing_planning():
    """示例4: 发布规划"""
    print("\n" + "=" * 60)
    print("示例4: 发布规划")
    print("=" * 60)
    
    from publishing_planner import PublishingPlanner
    
    # 测试数据
    platform_contents = {
        "wechat": "微信公众号内容",
        "xiaohongshu": "小红书内容",
        "douyin": "抖音内容",
        "zhihu": "知乎内容",
        "weibo": "微博内容"
    }
    
    quality_scores = {
        "wechat": {"overall_score": 85, "quality_grade": "良好"},
        "xiaohongshu": {"overall_score": 78, "quality_grade": "合格"},
        "douyin": {"overall_score": 65, "quality_grade": "待改进"},
        "zhihu": {"overall_score": 92, "quality_grade": "优秀"},
        "weibo": {"overall_score": 70, "quality_grade": "合格"}
    }
    
    planner = PublishingPlanner()
    
    # 生成发布计划
    publishing_plan = planner.plan_publishing(platform_contents, quality_scores)
    
    print(f"计划ID: {publishing_plan['plan_id']}")
    print(f"内容类型: {publishing_plan['content_type']}")
    print(f"选择平台: {', '.join(publishing_plan['selected_platforms'].keys())}")
    
    print(f"\n整体策略: {publishing_plan['publishing_strategy']['overall_strategy']}")
    
    print("\n发布时间安排:")
    for schedule in publishing_plan["publishing_schedule"]:
        print(f"  {schedule['platform']}: {schedule['time_str']}")
    
    print("\n预计效果:")
    effect = publishing_plan["estimated_effect"]
    print(f"  总浏览量: {effect['total_estimated_views']}")
    print(f"  总互动量: {effect['total_estimated_engagement']}")
    print(f"  互动率: {effect['overall_engagement_rate']}%")
    print(f"  成功概率: {effect['success_probability']*100:.1f}%")
    
    return publishing_plan


def example_integrated_system():
    """示例5: 集成系统使用"""
    print("\n" + "=" * 60)
    print("示例5: 集成系统使用")
    print("=" * 60)
    
    from content_automation_system import ContentAutomationSystem
    
    # 创建测试配置
    test_config = {
        "system": {
            "name": "测试系统",
            "version": "1.0.0",
            "debug": False,
            "log_level": "INFO"
        },
        "directories": {
            "template_dir": "content_templates",
            "output_dir": "example_output",
            "log_dir": "example_logs"
        },
        "platforms": ["wechat", "xiaohongshu", "zhihu"],
        "ai_apis": {
            "wenxin": {"enabled": False},
            "tongyi": {"enabled": False},
            "zhipu": {"enabled": False}
        }
    }
    
    # 保存配置
    config_file = "example_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    
    # 初始化系统
    print("初始化系统...")
    system = ContentAutomationSystem(config_file)
    
    # 处理八字内容
    birth_info = {
        "birth_date": "1995-03-10",
        "birth_time": "09:15",
        "gender": "female",
        "name": "张美丽"
    }
    
    print(f"\n处理八字内容: {birth_info['name']}")
    result = system.process_bazi_content(birth_info)
    
    print(f"处理完成! 结果ID: {result['result_id']}")
    
    # 检查输出
    output_dir = os.path.join("example_output", result['result_id'])
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"生成文件: {len(files)} 个")
        for file in files[:3]:  # 显示前3个文件
            print(f"  - {file}")
    
    # 批量生成
    print("\n批量生成内容...")
    batch_results = system.generate_daily_content(count=2)
    print(f"批量生成完成! 共生成 {len(batch_results)} 个内容")
    
    # 清理
    import shutil
    if os.path.exists("example_output"):
        shutil.rmtree("example_output")
    if os.path.exists("example_logs"):
        shutil.rmtree("example_logs")
    if os.path.exists(config_file):
        os.remove(config_file)
    
    print("\n集成系统示例完成!")
    return result


def main():
    """主函数"""
    print("八字内容自动化生成系统使用示例")
    print("=" * 60)
    
    try:
        # 运行各个示例
        print("\n运行示例...")
        
        print("\n1. 个人八字分析示例")
        bazi_result = example_individual_analysis()
        
        print("\n2. 内容生成示例")
        content_result = example_content_generation()
        
        print("\n3. 质量评估示例")
        quality_result = example_quality_evaluation()
        
        print("\n4. 发布规划示例")
        publishing_result = example_publishing_planning()
        
        print("\n5. 集成系统示例")
        system_result = example_integrated_system()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成!")
        print("=" * 60)
        
        print("\n示例总结:")
        print(f"1. 八字分析: 成功分析 {bazi_result['basic_info']['name']} 的八字")
        print(f"2. 内容生成: 生成标题 '{content_result['title'][:20]}...'")
        print(f"3. 质量评估: 得分 {quality_result['overall_score']} ({quality_result['quality_grade']})")
        print(f"4. 发布规划: {len(publishing_result['selected_platforms'])} 个平台")
        print(f"5. 集成系统: 生成结果ID {system_result['result_id']}")
        
        print("\n🎉 示例运行成功!")
        print("\n下一步:")
        print("1. 配置 config.json 文件")
        print("2. 运行 python content_automation_system.py")
        print("3. 查看 output/ 目录中的结果")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 示例运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)