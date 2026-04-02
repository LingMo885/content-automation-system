#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件管理模块
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        # 系统配置
        "system": {

        
        # 微信公众号 API 配置
        "wechat_api": {
            "appid": "wxa05c024a3d75eaa0",
            "appsecret": "a98f98457262ba27bf68a7950f4a99d7",
            "access_token": "",
            "token_expires_at": 0,
            "enabled": True,
            "auto_publish": True,
            "publish_time": "09:00"
        },

            "name": "八字内容自动化生成系统",
            "version": "1.0.0",
            "debug": False,
            "log_level": "INFO"
        },
        
        # 目录配置
        "directories": {
            "template_dir": "content_templates",
            "output_dir": "output",
            "log_dir": "logs",
            "data_dir": "data"
        },
        
        # 平台配置
        "platforms": ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"],
        
        # AI API配置
        "ai_apis": {
            "wenxin": {
                "enabled": True,
                "api_key": "",
                "api_secret": "",
                "model": "ernie-4.0",
                "max_tokens": 2000
            },
            "tongyi": {
                "enabled": False,
                "api_key": "",
                "model": "qwen-max",
                "max_tokens": 2000
            },
            "zhipu": {
                "enabled": False,
                "api_key": "",
                "model": "glm-4",
                "max_tokens": 2000
            }
        },
        
        # 内容生成配置
        "content_generation": {
            "enable_ai_enhancement": True,
            "max_content_length": 5000,
            "min_content_length": 300,
            "default_language": "zh-CN",
            "enable_proofreading": True
        },
        
        # 质量评估配置
        "quality_evaluation": {
            "enable_auto_evaluation": True,
            "min_quality_score": 60,
            "evaluation_dimensions": [
                "relevance",
                "professionalism", 
                "readability",
                "attractiveness",
                "compliance"
            ],
            "weights": {
                "relevance": 0.25,
                "professionalism": 0.25,
                "readability": 0.20,
                "attractiveness": 0.20,
                "compliance": 0.10
            }
        },
        
        # 发布规划配置
        "publishing_planning": {
            "enable_auto_scheduling": True,
            "default_publishing_times": {
                "wechat": ["09:00", "12:00", "20:00"],
                "xiaohongshu": ["10:00", "14:00", "19:00"],
                "douyin": ["12:00", "18:00", "21:00"],
                "zhihu": ["08:00", "13:00", "19:00"],
                "weibo": ["09:00", "12:00", "18:00", "22:00"]
            },
            "min_interval_hours": 2,
            "max_daily_posts": {
                "wechat": 3,
                "xiaohongshu": 5,
                "douyin": 10,
                "zhihu": 3,
                "weibo": 10
            }
        },
        
        # 八字分析配置
        "bazi_analysis": {
            "enable_detailed_analysis": True,
            "include_ten_gods": True,
            "include_da_yun": True,
            "include_liu_nian": True,
            "analysis_depth": "standard"  # simple, standard, detailed
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        else:
            logger.info("使用默认配置")
        
        # 确保目录存在
        self.ensure_directories()
    
    def load_config(self, config_path: str):
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # 深度合并配置
            self.merge_config(self.config, loaded_config)
            logger.info(f"配置文件加载成功: {config_path}")
            
        except Exception as e:
            logger.warning(f"加载配置文件失败: {str(e)}，使用默认配置")
    
    def merge_config(self, base: Dict, update: Dict):
        """
        深度合并配置字典
        
        Args:
            base: 基础配置
            update: 更新配置
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self.merge_config(base[key], value)
            else:
                base[key] = value
    
    def ensure_directories(self):
        """确保所有必要的目录都存在"""
        dir_config = self.config.get("directories", {})
        
        for dir_key, dir_path in dir_config.items():
            if dir_key.endswith("_dir"):
                os.makedirs(dir_path, exist_ok=True)
                logger.debug(f"确保目录存在: {dir_path}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分隔符如 "system.name"
            default: 默认值
            
        Returns:
            配置值
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception:
            return default
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键，支持点分隔符
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        # 遍历到最后一个键的父级
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
    
    def save(self, config_path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            config_path: 配置文件路径，如果为None则使用初始化时的路径
        """
        save_path = config_path or self.config_path
        
        if not save_path:
            logger.warning("未指定配置文件路径，无法保存")
            return
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"配置保存成功: {save_path}")
            
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        获取配置字典
        
        Returns:
            配置字典
        """
        return self.config.copy()
    
    def validate(self) -> bool:
        """
        验证配置有效性
        
        Returns:
            是否有效
        """
        try:
            # 检查必要目录
            required_dirs = ["template_dir", "output_dir"]
            dir_config = self.config.get("directories", {})
            
            for dir_key in required_dirs:
                if dir_key not in dir_config:
                    logger.error(f"缺少必要目录配置: {dir_key}")
                    return False
            
            # 检查平台配置
            platforms = self.config.get("platforms", [])
            if not platforms:
                logger.error("未配置任何平台")
                return False
            
            # 检查AI API配置
            ai_apis = self.config.get("ai_apis", {})
            has_enabled_api = False
            
            for api_name, api_config in ai_apis.items():
                if api_config.get("enabled", False):
                    has_enabled_api = True
                    break
            
            if not has_enabled_api and self.config.get("content_generation", {}).get("enable_ai_enhancement", False):
                logger.warning("AI增强已启用但未配置任何AI API")
            
            return True
            
        except Exception as e:
            logger.error(f"配置验证失败: {str(e)}")
            return False
    
    def generate_sample_config(self, output_path: str = "config_sample.json"):
        """
        生成示例配置文件
        
        Args:
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
            
            logger.info(f"示例配置文件已生成: {output_path}")
            
        except Exception as e:
            logger.error(f"生成示例配置文件失败: {str(e)}")


# 单例配置实例
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    获取配置实例（单例模式）
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置实例
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = Config(config_path)
    
    return _config_instance


if __name__ == "__main__":
    # 测试配置模块
    config = Config()
    
    print("配置测试:")
    print(f"系统名称: {config.get('system.name')}")
    print(f"支持平台: {config.get('platforms')}")
    print(f"模板目录: {config.get('directories.template_dir')}")
    
    # 生成示例配置文件
    config.generate_sample_config()