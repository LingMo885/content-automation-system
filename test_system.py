#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字内容自动化生成系统测试脚本
"""

import os
import sys
import logging
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_individual_modules():
    """测试各个模块"""
    print("=" * 60)
    print("八字内容自动化生成系统 - 模块测试")
    print("=" * 60)
    
    test_results = {}
    
    try:
        # 1. 测试八字分析器
        print("\n1. 测试八字分析器...")
        from ba_zi_analyzer import BaZiAnalyzer, test_bazi_analyzer
        test_results["bazi_analyzer"] = test_bazi_analyzer()
        
        # 2. 测试内容生成器
        print("\n2. 测试内容生成器...")
        from content_generator import ContentGenerator, test_content_generator
        test_results["content_generator"] = test_content_generator()
        
        # 3. 测试平台适配器
        print("\n3. 测试平台适配器...")
        from platform_adapter import PlatformAdapter, test_platform_adapter
        test_results["platform_adapter"] = test_platform_adapter()
        
        # 4. 测试质量评估器
        print("\n4. 测试质量评估器...")
        from quality_evaluator import QualityEvaluator, test_quality_evaluator
        test_results["quality_evaluator"] = test_quality_evaluator()
        
        # 5. 测试发布规划器
        print("\n5. 测试发布规划器...")
        from publishing_planner import PublishingPlanner, test_publishing_planner
        test_results["publishing_planner"] = test_publishing_planner()
        
        # 6. 测试工具函数
        print("\n6. 测试工具函数...")
        from utils import test_utils
        test_results["utils"] = test_utils()
        
        # 7. 测试API集成
        print("\n7. 测试API集成...")
        from api_integration import test_api_integration
        test_results["api_integration"] = test_api_integration()
        
        # 汇总测试结果
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        
        all_passed = True
        for module, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{module:20} {status}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("\n🎉 所有模块测试通过!")
        else:
            print("\n⚠️  部分模块测试失败，请检查日志")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integrated_system():
    """测试集成系统"""
    print("\n" + "=" * 60)
    print("八字内容自动化生成系统 - 集成测试")
    print("=" * 60)
    
    try:
        # 导入主系统
        from content_automation_system import ContentAutomationSystem
        
        # 创建测试配置
        test_config = {
            "system": {
                "name": "测试系统",
                "version": "1.0.0",
                "debug": True,
                "log_level": "INFO"
            },
            "directories": {
                "template_dir": "content_templates",
                "output_dir": "test_output",
                "log_dir": "test_logs",
                "data_dir": "test_data"
            },
            "platforms": ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"],
            "ai_apis": {
                "wenxin": {"enabled": False},
                "tongyi": {"enabled": False},
                "zhipu": {"enabled": False}
            },
            "content_generation": {
                "enable_ai_enhancement": False,
                "max_content_length": 5000
            }
        }
        
        # 保存测试配置
        config_file = "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, ensure_ascii=False, indent=2)
        
        print("1. 初始化系统...")
        system = ContentAutomationSystem(config_file)
        print(f"   系统名称: {system.config.get('system.name')}")
        print(f"   支持平台: {', '.join(system.config.get('platforms'))}")
        
        # 测试数据
        test_birth_info = {
            "birth_date": "1990-05-15",
            "birth_time": "08:30",
            "gender": "female",
            "name": "李小红"
        }
        
        print("\n2. 处理单个八字内容...")
        result = system.process_bazi_content(test_birth_info)
        print(f"   处理完成! 结果ID: {result['result_id']}")
        
        # 检查输出文件
        output_dir = os.path.join("test_output", result['result_id'])
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            print(f"   生成文件: {len(files)} 个")
            for file in files:
                print(f"     - {file}")
        
        print("\n3. 批量生成内容...")
        batch_results = system.generate_daily_content(count=2)
        print(f"   批量生成完成! 共生成 {len(batch_results)} 个内容")
        
        print("\n4. 测试系统状态...")
        print(f"   模板目录: {system.config.get('directories.template_dir')}")
        print(f"   输出目录: {system.config.get('directories.output_dir')}")
        print(f"   日志目录: {system.config.get('directories.log_dir')}")
        
        # 清理测试文件
        import shutil
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        if os.path.exists(config_file):
            os.remove(config_file)
        
        print("\n🎉 集成测试通过!")
        return True
        
    except Exception as e:
        print(f"\n❌ 集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_content_quality():
    """测试内容质量"""
    print("\n" + "=" * 60)
    print("八字内容自动化生成系统 - 内容质量测试")
    print("=" * 60)
    
    try:
        from ba_zi_analyzer import BaZiAnalyzer
        from content_generator import ContentGenerator
        from quality_evaluator import QualityEvaluator
        
        # 生成测试内容
        analyzer = BaZiAnalyzer()
        generator = ContentGenerator()
        evaluator = QualityEvaluator()
        
        test_birth_info = {
            "birth_date": "1985-08-20",
            "birth_time": "14:45",
            "gender": "male",
            "name": "王大明"
        }
        
        print("1. 生成八字分析...")
        bazi_analysis = analyzer.analyze(test_birth_info)
        print(f"   八字: {bazi_analysis['bazi_pillar']}")
        print(f"   日主: {bazi_analysis['ri_zhu']['character']}")
        print(f"   五行: {bazi_analysis['ri_zhu']['wu_xing']}")
        
        print("\n2. 生成基础内容...")
        base_content = generator.generate_base_content(bazi_analysis)
        print(f"   标题: {base_content.get('title')}")
        print(f"   摘要: {base_content.get('summary')[:50]}...")
        print(f"   标签: {', '.join(base_content.get('tags', [])[:3])}")
        
        print("\n3. 评估内容质量...")
        test_content = base_content.get("analysis", "")
        quality_result = evaluator.evaluate(test_content, "wechat")
        
        print(f"   综合得分: {quality_result['overall_score']}")
        print(f"   质量等级: {quality_result['quality_grade']}")
        
        print("\n4. 维度得分:")
        for dim_key, score in quality_result['dimension_scores'].items():
            dim_name = evaluator.EVALUATION_DIMENSIONS.get(dim_key, {}).get("name", dim_key)
            print(f"   {dim_name}: {score}")
        
        print("\n5. 改进建议:")
        for recommendation in quality_result['recommendations'][:3]:
            print(f"   - {recommendation}")
        
        if quality_result['overall_score'] >= 70:
            print("\n✅ 内容质量测试通过!")
            return True
        else:
            print("\n⚠️  内容质量有待提升")
            return False
        
    except Exception as e:
        print(f"\n❌ 内容质量测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_performance():
    """测试性能"""
    print("\n" + "=" * 60)
    print("八字内容自动化生成系统 - 性能测试")
    print("=" * 60)
    
    try:
        import time
        from ba_zi_analyzer import BaZiAnalyzer
        
        analyzer = BaZiAnalyzer()
        
        # 测试数据
        test_cases = []
        for i in range(5):
            test_cases.append({
                "birth_date": f"19{80+i}-{i+1:02d}-{i+10:02d}",
                "birth_time": f"{i+8:02d}:{i*10:02d}",
                "gender": "male" if i % 2 == 0 else "female",
                "name": f"测试用户{i+1}"
            })
        
        print("1. 单次分析性能...")
        start_time = time.time()
        result = analyzer.analyze(test_cases[0])
        end_time = time.time()
        print(f"   分析时间: {(end_time - start_time)*1000:.2f}ms")
        print(f"   分析结果: {result['bazi_pillar']}")
        
        print("\n2. 批量分析性能...")
        start_time = time.time()
        all_results = []
        for case in test_cases:
            result = analyzer.analyze(case)
            all_results.append(result)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(test_cases)
        print(f"   总时间: {total_time:.2f}s")
        print(f"   平均时间: {avg_time*1000:.2f}ms/个")
        print(f"   处理数量: {len(test_cases)} 个")
        
        if avg_time < 1.0:  # 平均分析时间小于1秒
            print("\n✅ 性能测试通过!")
            return True
        else:
            print("\n⚠️  性能有待优化")
            return False
        
    except Exception as e:
        print(f"\n❌ 性能测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("八字内容自动化生成系统 - 完整测试套件")
    print("=" * 60)
    
    # 创建测试输出目录
    os.makedirs("test_reports", exist_ok=True)
    
    test_summary = {
        "test_time": datetime.now().isoformat(),
        "modules": {},
        "overall": False
    }
    
    try:
        # 运行各个测试
        test_summary["modules"]["individual_modules"] = test_individual_modules()
        test_summary["modules"]["integrated_system"] = test_integrated_system()
        test_summary["modules"]["content_quality"] = test_content_quality()
        test_summary["modules"]["performance"] = test_performance()
        
        # 计算总体结果
        all_passed = all(test_summary["modules"].values())
        test_summary["overall"] = all_passed
        
        # 保存测试报告
        report_file = f"test_reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(test_summary, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("测试完成!")
        print("=" * 60)
        
        print("\n测试报告:")
        for test_name, result in test_summary["modules"].items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {test_name:20} {status}")
        
        if test_summary["overall"]:
            print("\n🎉 所有测试通过! 系统可以正常使用。")
            print(f"测试报告已保存到: {report_file}")
        else:
            print("\n⚠️  部分测试失败，请检查测试报告。")
            print(f"测试报告已保存到: {report_file}")
        
        return test_summary["overall"]
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)