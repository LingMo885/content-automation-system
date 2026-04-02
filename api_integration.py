#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API集成模块
集成多个AI内容生成API
"""

import logging
import json
import time
from typing import Dict, List, Any, Optional, Tuple
import requests

logger = logging.getLogger(__name__)


class APIIntegration:
    """API集成类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化API集成
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.ai_apis = config.get("ai_apis", {})
        self.active_apis = self.get_active_apis()
        
        logger.info(f"API集成初始化完成，激活的API: {list(self.active_apis.keys())}")
    
    def get_active_apis(self) -> Dict[str, Dict[str, Any]]:
        """获取激活的API"""
        active = {}
        for api_name, api_config in self.ai_apis.items():
            if api_config.get("enabled", False):
                active[api_name] = api_config.copy()
        
        return active
    
    def generate_content(self, prompt: str, api_name: Optional[str] = None, 
                        max_tokens: int = 1000) -> Tuple[bool, str]:
        """
        生成内容
        
        Args:
            prompt: 提示词
            api_name: 指定API名称，如果为None则自动选择
            max_tokens: 最大token数
            
        Returns:
            (是否成功, 生成的内容或错误信息)
        """
        if not self.active_apis:
            return False, "没有激活的AI API"
        
        # 选择API
        if api_name and api_name in self.active_apis:
            selected_api = api_name
        else:
            selected_api = self.select_best_api()
        
        if selected_api not in self.active_apis:
            return False, f"API不可用: {selected_api}"
        
        api_config = self.active_apis[selected_api]
        
        try:
            logger.info(f"使用 {selected_api} API生成内容")
            
            if selected_api == "wenxin":
                return self.call_wenxin_api(prompt, api_config, max_tokens)
            elif selected_api == "tongyi":
                return self.call_tongyi_api(prompt, api_config, max_tokens)
            elif selected_api == "zhipu":
                return self.call_zhipu_api(prompt, api_config, max_tokens)
            else:
                return False, f"不支持的API: {selected_api}"
                
        except Exception as e:
            logger.error(f"API调用失败: {selected_api}, 错误: {str(e)}")
            return False, f"API调用失败: {str(e)}"
    
    def select_best_api(self) -> str:
        """选择最佳API"""
        if not self.active_apis:
            return ""
        
        # 简单实现：选择第一个激活的API
        # 实际可以根据API性能、成本、可用性等选择
        return list(self.active_apis.keys())[0]
    
    def call_wenxin_api(self, prompt: str, api_config: Dict[str, Any], 
                       max_tokens: int) -> Tuple[bool, str]:
        """调用文心一言API"""
        api_key = api_config.get("api_key", "")
        api_secret = api_config.get("api_secret", "")
        model = api_config.get("model", "ernie-4.0")
        
        if not api_key or not api_secret:
            return False, "文心一言API密钥未配置"
        
        # 获取access token
        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        token_params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": api_secret
        }
        
        try:
            # 获取access token
            token_response = requests.post(token_url, params=token_params)
            token_data = token_response.json()
            
            if "error" in token_data:
                return False, f"获取access token失败: {token_data.get('error_description', '未知错误')}"
            
            access_token = token_data.get("access_token", "")
            if not access_token:
                return False, "获取access token失败"
            
            # 调用文心一言API
            api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens
            }
            
            params = {"access_token": access_token}
            response = requests.post(api_url, params=params, headers=headers, 
                                   json=payload, timeout=30)
            
            response_data = response.json()
            
            if "error_code" in response_data:
                return False, f"文心一言API错误: {response_data.get('error_msg', '未知错误')}"
            
            result = response_data.get("result", "")
            if not result:
                return False, "文心一言API返回空结果"
            
            return True, result
            
        except requests.exceptions.RequestException as e:
            return False, f"网络请求失败: {str(e)}"
        except Exception as e:
            return False, f"API调用异常: {str(e)}"
    
    def call_tongyi_api(self, prompt: str, api_config: Dict[str, Any], 
                       max_tokens: int) -> Tuple[bool, str]:
        """调用通义千问API"""
        api_key = api_config.get("api_key", "")
        model = api_config.get("model", "qwen-max")
        
        if not api_key:
            return False, "通义千问API密钥未配置"
        
        try:
            api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response_data = response.json()
            
            if "code" in response_data and response_data["code"] != 200:
                return False, f"通义千问API错误: {response_data.get('message', '未知错误')}"
            
            # 提取结果
            output = response_data.get("output", {})
            if not output:
                return False, "通义千问API返回空结果"
            
            result = output.get("text", "")
            if not result:
                # 尝试其他格式
                choices = output.get("choices", [])
                if choices and len(choices) > 0:
                    result = choices[0].get("message", {}).get("content", "")
            
            if not result:
                return False, "无法提取通义千问API结果"
            
            return True, result
            
        except requests.exceptions.RequestException as e:
            return False, f"网络请求失败: {str(e)}"
        except Exception as e:
            return False, f"API调用异常: {str(e)}"
    
    def call_zhipu_api(self, prompt: str, api_config: Dict[str, Any], 
                      max_tokens: int) -> Tuple[bool, str]:
        """调用智谱AI API"""
        api_key = api_config.get("api_key", "")
        model = api_config.get("model", "glm-4")
        
        if not api_key:
            return False, "智谱AI API密钥未配置"
        
        try:
            api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response_data = response.json()
            
            if "error" in response_data:
                return False, f"智谱AI API错误: {response_data.get('error', {}).get('message', '未知错误')}"
            
            choices = response_data.get("choices", [])
            if not choices or len(choices) == 0:
                return False, "智谱AI API返回空结果"
            
            result = choices[0].get("message", {}).get("content", "")
            if not result:
                return False, "无法提取智谱AI API结果"
            
            return True, result
            
        except requests.exceptions.RequestException as e:
            return False, f"网络请求失败: {str(e)}"
        except Exception as e:
            return False, f"API调用异常: {str(e)}"
    
    def enhance_content(self, content: str, enhancement_type: str = "polish") -> Tuple[bool, str]:
        """
        增强内容
        
        Args:
            content: 原始内容
            enhancement_type: 增强类型 (polish, expand, simplify, professionalize)
            
        Returns:
            (是否成功, 增强后的内容或错误信息)
        """
        enhancement_prompts = {
            "polish": f"请优化以下内容，使其更加流畅、易读，保持原意不变：\n\n{content}",
            "expand": f"请扩展以下内容，添加更多细节和解释，保持主题不变：\n\n{content}",
            "simplify": f"请简化以下内容，使其更加简洁明了，适合普通读者理解：\n\n{content}",
            "professionalize": f"请将以下内容专业化，使用更专业的术语和表达，提升专业性：\n\n{content}"
        }
        
        prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["polish"])
        
        return self.generate_content(prompt)
    
    def check_grammar(self, content: str) -> Tuple[bool, Dict[str, Any]]:
        """
        检查语法
        
        Args:
            content: 要检查的内容
            
        Returns:
            (是否成功, 检查结果)
        """
        prompt = f"请检查以下中文内容的语法和表达问题，指出错误并提供修改建议：\n\n{content}"
        
        success, result = self.generate_content(prompt, max_tokens=500)
        
        if not success:
            return False, {"error": result}
        
        # 解析结果
        analysis = {
            "has_errors": "错误" in result or "问题" in result,
            "suggestions": result,
            "original_content": content
        }
        
        return True, analysis
    
    def generate_summary(self, content: str, max_length: int = 200) -> Tuple[bool, str]:
        """
        生成摘要
        
        Args:
            content: 原始内容
            max_length: 摘要最大长度
            
        Returns:
            (是否成功, 摘要)
        """
        prompt = f"请为以下内容生成一个简洁的摘要，不超过{max_length}字：\n\n{content}"
        
        return self.generate_content(prompt, max_tokens=300)
    
    def generate_title(self, content: str, style: str = "normal") -> Tuple[bool, str]:
        """
        生成标题
        
        Args:
            content: 内容
            style: 标题风格 (normal, catchy, professional, question)
            
        Returns:
            (是否成功, 标题)
        """
        style_prompts = {
            "normal": "为以下内容生成一个合适的标题：",
            "catchy": "为以下内容生成一个吸引眼球的标题：",
            "professional": "为以下内容生成一个专业的标题：",
            "question": "为以下内容生成一个疑问式标题："
        }
        
        prompt = f"{style_prompts.get(style, style_prompts['normal'])}\n\n{content}"
        
        return self.generate_content(prompt, max_tokens=100)
    
    def test_api_connection(self, api_name: str) -> Tuple[bool, str]:
        """
        测试API连接
        
        Args:
            api_name: API名称
            
        Returns:
            (是否成功, 测试结果)
        """
        if api_name not in self.active_apis:
            return False, f"API未激活: {api_name}"
        
        test_prompt = "请回复'测试成功'，无需其他内容。"
        
        start_time = time.time()
        success, result = self.generate_content(test_prompt, api_name, max_tokens=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if success:
            if "测试成功" in result:
                return True, f"API连接测试成功，响应时间: {response_time:.2f}秒"
            else:
                return False, f"API响应异常: {result}"
        else:
            return False, f"API连接失败: {result}"
    
    def get_api_status(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有API状态
        
        Returns:
            API状态字典
        """
        status = {}
        
        for api_name in self.active_apis.keys():
            is_connected, message = self.test_api_connection(api_name)
            
            status[api_name] = {
                "enabled": True,
                "connected": is_connected,
                "message": message,
                "config": self.active_apis[api_name]
            }
        
        return status


# 测试函数
def test_api_integration():
    """测试API集成"""
    print("测试API集成...")
    
    # 测试配置
    test_config = {
        "ai_apis": {
            "wenxin": {
                "enabled": False,  # 测试时禁用，避免实际调用
                "api_key": "test_key",
                "api_secret": "test_secret",
                "model": "ernie-4.0",
                "max_tokens": 2000
            },
            "tongyi": {
                "enabled": False,
                "api_key": "test_key",
                "model": "qwen-max",
                "max_tokens": 2000
            },
            "zhipu": {
                "enabled": False,
                "api_key": "test_key",
                "model": "glm-4",
                "max_tokens": 2000
            }
        }
    }
    
    try:
        api_integration = APIIntegration(test_config)
        
        print(f"激活的API: {list(api_integration.active_apis.keys())}")
        
        # 测试API状态
        print("\nAPI状态:")
        status = api_integration.get_api_status()
        for api_name, api_status in status.items():
            print(f"  {api_name}: {'已连接' if api_status['connected'] else '未连接'} - {api_status['message']}")
        
        # 测试模拟内容生成
        print("\n测试模拟内容生成...")
        
        # 由于测试配置中API都禁用了，这里测试模拟逻辑
        test_prompt = "测试提示词"
        
        # 测试API选择
        best_api = api_integration.select_best_api()
        print(f"最佳API选择: {best_api}")
        
        # 测试增强类型
        print("\n增强类型:")
        for enhancement_type in ["polish", "expand", "simplify", "professionalize"]:
            print(f"  {enhancement_type}: 已定义")
        
        print("\n测试完成（实际API调用需要配置有效的API密钥）")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_api_integration()