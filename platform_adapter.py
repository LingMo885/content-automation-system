#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平台适配器模块
用于将内容适配到不同平台
"""

import logging
import re
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class PlatformAdapter:
    """平台适配器类"""
    
    # 平台配置
    PLATFORM_CONFIGS = {
        "wechat": {
            "name": "微信公众号",
            "max_length": 20000,
            "min_length": 300,
            "recommended_length": 1500,
            "allow_images": True,
            "allow_links": True,
            "allow_formatting": True,
            "emoji_limit": 20,
            "hashtag_limit": 5,
            "required_elements": ["title", "content"],
            "format_rules": {
                "title_max": 64,
                "paragraph_max": 500,
                "line_break": "\n\n"
            }
        },
        "xiaohongshu": {
            "name": "小红书",
            "max_length": 1000,
            "min_length": 100,
            "recommended_length": 500,
            "allow_images": True,
            "allow_links": False,
            "allow_formatting": True,
            "emoji_limit": 30,
            "hashtag_limit": 20,
            "required_elements": ["title", "content", "hashtags"],
            "format_rules": {
                "title_max": 30,
                "paragraph_max": 200,
                "line_break": "\n",
                "emoji_density": 0.1  # 每10个字符一个emoji
            }
        },
        "douyin": {
            "name": "抖音",
            "max_length": 300,
            "min_length": 20,
            "recommended_length": 100,
            "allow_images": False,
            "allow_links": False,
            "allow_formatting": False,
            "emoji_limit": 10,
            "hashtag_limit": 10,
            "required_elements": ["content", "hashtags"],
            "format_rules": {
                "line_break": "\n",
                "short_sentences": True,
                "attention_grabbing": True
            }
        },
        "zhihu": {
            "name": "知乎",
            "max_length": 50000,
            "min_length": 500,
            "recommended_length": 3000,
            "allow_images": True,
            "allow_links": True,
            "allow_formatting": True,
            "emoji_limit": 5,
            "hashtag_limit": 0,
            "required_elements": ["title", "content"],
            "format_rules": {
                "title_max": 100,
                "paragraph_max": 800,
                "line_break": "\n\n",
                "professional_tone": True
            }
        },
        "weibo": {
            "name": "微博",
            "max_length": 2000,
            "min_length": 50,
            "recommended_length": 300,
            "allow_images": True,
            "allow_links": True,
            "allow_formatting": True,
            "emoji_limit": 20,
            "hashtag_limit": 10,
            "required_elements": ["content", "hashtags"],
            "format_rules": {
                "line_break": "\n",
                "trending_topics": True,
                "interactive": True
            }
        }
    }
    
    # 平台特定的emoji集合
    PLATFORM_EMOJIS = {
        "wechat": ["📊", "🔍", "🌟", "💡", "📈", "🎯", "⚠️", "✅"],
        "xiaohongshu": ["✨", "🌟", "💫", "🎀", "💖", "👑", "🔥", "💎", "📝", "🔮"],
        "douyin": ["🔥", "💥", "🎯", "💰", "👑", "🌟", "💫", "⚡", "🎉", "💯"],
        "zhihu": ["📊", "🔍", "📈", "💡", "⚠️", "✅", "❓", "❗"],
        "weibo": ["🔥", "💥", "🎯", "💰", "🌟", "💫", "📈", "💡", "👀", "👍"]
    }
    
    def __init__(self):
        """初始化平台适配器"""
        self.platform_configs = self.PLATFORM_CONFIGS
        logger.info("平台适配器初始化完成")
    
    def adapt_content(self, content_structure: Dict[str, Any], platform: str) -> str:
        """
        将内容适配到特定平台
        
        Args:
            content_structure: 内容结构字典
            platform: 平台名称
            
        Returns:
            适配后的内容
        """
        try:
            logger.info(f"将内容适配到平台: {platform}")
            
            # 验证平台
            if platform not in self.platform_configs:
                raise ValueError(f"不支持的平台: {platform}")
            
            platform_config = self.platform_configs[platform]
            
            # 获取平台特定的模板内容
            platform_content = self.get_platform_template_content(content_structure, platform)
            
            # 应用平台适配规则
            adapted_content = self.apply_platform_rules(platform_content, platform_config)
            
            # 添加平台特定元素
            adapted_content = self.add_platform_elements(adapted_content, platform, content_structure)
            
            # 验证内容
            self.validate_content(adapted_content, platform_config)
            
            logger.debug(f"平台适配完成: {platform}, 长度: {len(adapted_content)}")
            return adapted_content
            
        except Exception as e:
            logger.error(f"平台适配失败: {str(e)}", exc_info=True)
            raise
    
    def get_platform_template_content(self, content_structure: Dict[str, Any], platform: str) -> str:
        """
        获取平台模板内容
        
        Args:
            content_structure: 内容结构
            platform: 平台名称
            
        Returns:
            模板内容
        """
        # 这里假设内容生成器已经生成了平台特定的内容
        # 实际实现中，应该从content_structure中获取或重新生成
        
        # 简化实现：使用基础内容
        base_content = content_structure.get("analysis", "")
        title = content_structure.get("title", "")
        summary = content_structure.get("summary", "")
        tags = content_structure.get("tags", [])
        
        # 根据平台生成不同格式的内容
        if platform == "wechat":
            return self.format_for_wechat(title, summary, base_content, tags)
        elif platform == "xiaohongshu":
            return self.format_for_xiaohongshu(title, summary, base_content, tags)
        elif platform == "douyin":
            return self.format_for_douyin(title, summary, base_content, tags)
        elif platform == "zhihu":
            return self.format_for_zhihu(title, summary, base_content, tags)
        elif platform == "weibo":
            return self.format_for_weibo(title, summary, base_content, tags)
        else:
            return base_content
    
    def format_for_wechat(self, title: str, summary: str, content: str, tags: List[str]) -> str:
        """格式化微信公众号内容"""
        formatted = f"# {title}\n\n"
        formatted += f"> {summary}\n\n"
        formatted += "---\n\n"
        formatted += content
        
        # 添加标签
        if tags:
            formatted += "\n\n---\n"
            formatted += "**相关标签**: "
            formatted += " ".join([f"#{tag}" for tag in tags[:5]])
        
        return formatted
    
    def format_for_xiaohongshu(self, title: str, summary: str, content: str, tags: List[str]) -> str:
        """格式化小红书内容"""
        # 小红书喜欢短标题和emoji
        short_title = title[:20] + "..." if len(title) > 20 else title
        formatted = f"{short_title} ✨\n\n"
        
        # 添加emoji装饰
        formatted += "📝 八字分析笔记来啦！\n\n"
        
        # 简化内容
        lines = content.split('\n')
        simplified = []
        for line in lines:
            if line.strip() and not line.startswith('#') and len(line) > 10:
                simplified.append(line[:100])  # 限制每行长度
        
        formatted += "\n".join(simplified[:10])  # 只取前10行
        
        # 添加标签
        if tags:
            formatted += "\n\n"
            for tag in tags[:10]:
                formatted += f"#{tag} "
        
        return formatted
    
    def format_for_douyin(self, title: str, summary: str, content: str, tags: List[str]) -> str:
        """格式化抖音内容"""
        # 抖音内容要非常简短
        short_title = title[:15] + "..." if len(title) > 15 else title
        formatted = f"{short_title}\n\n"
        
        # 提取关键信息
        key_points = []
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ["五行", "性格", "事业", "财运", "建议"]):
                key_points.append(line[:50])
        
        formatted += "\n".join(key_points[:5])
        
        # 添加标签
        if tags:
            formatted += "\n\n"
            for tag in tags[:5]:
                formatted += f"#{tag} "
        
        return formatted
    
    def format_for_zhihu(self, title: str, summary: str, content: str, tags: List[str]) -> str:
        """格式化知乎内容"""
        formatted = f"## {title}\n\n"
        formatted += f"**摘要**: {summary}\n\n"
        formatted += "---\n\n"
        formatted += content
        
        # 知乎格式要求更严格
        formatted = self.clean_formatting(formatted)
        
        # 添加专业标签
        if tags:
            formatted += "\n\n---\n"
            formatted += "**话题标签**: "
            formatted += "、".join(tags[:8])
        
        return formatted
    
    def format_for_weibo(self, title: str, summary: str, content: str, tags: List[str]) -> str:
        """格式化微博内容"""
        # 微博内容要吸引眼球
        formatted = f"{title}\n\n"
        
        # 提取亮点
        highlights = []
        lines = content.split('\n')
        for line in lines:
            if "🔥" in line or "🌟" in line or "💡" in line:
                highlights.append(line)
            elif len(line) < 100 and line.strip():
                highlights.append(line)
        
        formatted += "\n".join(highlights[:8])
        
        # 添加话题标签
        if tags:
            formatted += "\n\n"
            for tag in tags[:8]:
                formatted += f"#{tag}# "
        
        return formatted
    
    def apply_platform_rules(self, content: str, platform_config: Dict[str, Any]) -> str:
        """
        应用平台规则
        
        Args:
            content: 原始内容
            platform_config: 平台配置
            
        Returns:
            应用规则后的内容
        """
        adapted = content
        
        # 1. 长度调整
        max_length = platform_config.get("max_length", 10000)
        if len(adapted) > max_length:
            adapted = self.truncate_content(adapted, max_length)
        
        # 2. 格式清理
        if not platform_config.get("allow_formatting", True):
            adapted = self.remove_formatting(adapted)
        
        # 3. Emoji处理
        emoji_limit = platform_config.get("emoji_limit", 20)
        adapted = self.adjust_emoji_count(adapted, emoji_limit)
        
        # 4. 链接处理
        if not platform_config.get("allow_links", True):
            adapted = self.remove_links(adapted)
        
        # 5. 段落格式
        line_break = platform_config.get("format_rules", {}).get("line_break", "\n\n")
        if line_break != "\n\n":
            adapted = adapted.replace("\n\n", line_break)
        
        return adapted
    
    def truncate_content(self, content: str, max_length: int) -> str:
        """截断内容到指定长度"""
        if len(content) <= max_length:
            return content
        
        # 在句子边界处截断
        truncated = content[:max_length]
        
        # 查找最后一个句子结束符
        last_period = max(
            truncated.rfind('。'),
            truncated.rfind('.'),
            truncated.rfind('！'),
            truncated.rfind('!'),
            truncated.rfind('？'),
            truncated.rfind('?')
        )
        
        if last_period > max_length * 0.8:  # 如果截断点附近有句子结束
            truncated = truncated[:last_period + 1]
        
        truncated += "\n\n【内容过长，已截断】"
        return truncated
    
    def remove_formatting(self, content: str) -> str:
        """移除格式标记"""
        # 移除Markdown标记
        cleaned = re.sub(r'[#*_`~]', '', content)
        # 移除HTML标记
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        return cleaned
    
    def adjust_emoji_count(self, content: str, limit: int) -> str:
        """调整emoji数量"""
        # 统计emoji数量
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F'  # 表情符号
            r'\U0001F300-\U0001F5FF'  # 符号和象形文字
            r'\U0001F680-\U0001F6FF'  # 交通和地图符号
            r'\U0001F1E0-\U0001F1FF'  # 国旗
            r'\U00002702-\U000027B0'  # 装饰符号
            r'\U000024C2-\U0001F251]+',
            flags=re.UNICODE
        )
        
        emojis = emoji_pattern.findall(content)
        if len(emojis) <= limit:
            return content
        
        # 移除多余的emoji
        # 简单实现：保留前limit个emoji
        kept_emojis = set()
        result = []
        emoji_count = 0
        
        for char in content:
            if emoji_pattern.match(char):
                if char in kept_emojis or emoji_count < limit:
                    result.append(char)
                    if char not in kept_emojis:
                        kept_emojis.add(char)
                        emoji_count += 1
                # 跳过多余的emoji
            else:
                result.append(char)
        
        return ''.join(result)
    
    def remove_links(self, content: str) -> str:
        """移除链接"""
        # 移除Markdown链接
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # 移除URL
        content = re.sub(r'https?://\S+', '', content)
        return content
    
    def clean_formatting(self, content: str) -> str:
        """清理格式（用于知乎等专业平台）"""
        # 移除过多的emoji
        content = self.adjust_emoji_count(content, 5)
        # 确保段落之间有适当的间距
        content = re.sub(r'\n{3,}', '\n\n', content)
        # 移除多余的空格
        content = re.sub(r'[ \t]{2,}', ' ', content)
        return content
    
    def add_platform_elements(self, content: str, platform: str, content_structure: Dict[str, Any]) -> str:
        """
        添加平台特定元素
        
        Args:
            content: 内容
            platform: 平台名称
            content_structure: 内容结构
            
        Returns:
            添加元素后的内容
        """
        enhanced = content
        
        # 添加平台特定的emoji
        platform_emojis = self.PLATFORM_EMOJIS.get(platform, [])
        if platform_emojis:
            # 在适当位置添加emoji
            import random
            lines = enhanced.split('\n')
            enhanced_lines = []
            
            for line in lines:
                if line.strip() and len(line) > 20:
                    # 有一定概率在行首添加emoji
                    if random.random() < 0.3:
                        emoji = random.choice(platform_emojis)
                        line = f"{emoji} {line}"
                enhanced_lines.append(line)
            
            enhanced = '\n'.join(enhanced_lines)
        
        # 添加平台特定的结尾
        endings = {
            "wechat": "\n\n---\n*欢迎关注公众号，获取更多命理知识*",
            "xiaohongshu": "\n\n💖 喜欢就点个赞吧！",
            "douyin": "\n\n👉 关注我，了解更多八字知识",
            "zhihu": "\n\n*本文仅供参考，实际应用请咨询专业人士*",
            "weibo": "\n\n#八字命理# #运势分析#"
        }
        
        if platform in endings:
            enhanced += endings[platform]
        
        return enhanced
    
    def validate_content(self, content: str, platform_config: Dict[str, Any]) -> bool:
        """
        验证内容是否符合平台要求
        
        Args:
            content: 内容
            platform_config: 平台配置
            
        Returns:
            是否有效
        """
        try:
            # 检查长度
            min_length = platform_config.get("min_length", 0)
            max_length = platform_config.get("max_length", 10000)
            
            content_length = len(content)
            
            if content_length < min_length:
                logger.warning(f"内容过短: {content_length} < {min_length}")
                return False
            
            if content_length > max_length:
                logger.warning(f"内容过长: {content_length} > {max_length}")
                return False
            
            # 检查必要元素
            required_elements = platform_config.get("required_elements", [])
            
            if "title" in required_elements:
                # 检查是否有标题（以#开头或包含标题字样）
                if not re.search(r'^#+\s+.+', content, re.MULTILINE):
                    logger.warning("缺少标题")
                    return False
            
            if "hashtags" in required_elements:
                # 检查是否有话题标签
                if not re.search(r'#\w+', content):
                    logger.warning("缺少话题标签")
                    return False
            
            # 检查emoji数量
            emoji_pattern = re.compile(
                r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]',
                flags=re.UNICODE
            )
            
            emoji_count = len(emoji_pattern.findall(content))
            emoji_limit = platform_config.get("emoji_limit", 20)
            
            if emoji_count > emoji_limit:
                logger.warning(f"emoji过多: {emoji_count} > {emoji_limit}")
                return False
            
            logger.debug(f"内容验证通过: 长度={content_length}, emoji={emoji_count}")
            return True
            
        except Exception as e:
            logger.error(f"内容验证失败: {str(e)}")
            return False
    
    def get_platform_info(self, platform: str) -> Dict[str, Any]:
        """
        获取平台信息
        
        Args:
            platform: 平台名称
            
        Returns:
            平台信息字典
        """
        if platform not in self.platform_configs:
            raise ValueError(f"不支持的平台: {platform}")
        
        return self.platform_configs[platform].copy()
    
    def list_supported_platforms(self) -> List[str]:
        """
        列出支持的平台
        
        Returns:
            平台名称列表
        """
        return list(self.platform_configs.keys())
    
    def get_platform_stats(self, content: str, platform: str) -> Dict[str, Any]:
        """
        获取内容在特定平台上的统计信息
        
        Args:
            content: 内容
            platform: 平台名称
            
        Returns:
            统计信息字典
        """
        if platform not in self.platform_configs:
            raise ValueError(f"不支持的平台: {platform}")
        
        platform_config = self.platform_configs[platform]
        
        # 统计emoji
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]',
            flags=re.UNICODE
        )
        emojis = emoji_pattern.findall(content)
        
        # 统计话题标签
        hashtags = re.findall(r'#(\w+)', content)
        
        # 统计段落
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        
        stats = {
            "length": len(content),
            "paragraphs": len(paragraphs),
            "emojis": len(emojis),
            "hashtags": len(hashtags),
            "compliance": {
                "length_ok": platform_config["min_length"] <= len(content) <= platform_config["max_length"],
                "emoji_ok": len(emojis) <= platform_config["emoji_limit"],
                "hashtag_ok": len(hashtags) <= platform_config["hashtag_limit"]
            },
            "recommendations": []
        }
        
        # 生成建议
        if len(content) < platform_config["recommended_length"]:
            stats["recommendations"].append(f"内容偏短，建议达到{platform_config['recommended_length']}字左右")
        
        if len(content) > platform_config["recommended_length"] * 1.5:
            stats["recommendations"].append(f"内容偏长，建议精简到{platform_config['recommended_length']}字左右")
        
        if len(emojis) < 3 and platform in ["xiaohongshu", "douyin"]:
            stats["recommendations"].append("可以添加更多emoji增加吸引力")
        
        if len(hashtags) < 3 and platform in ["xiaohongshu", "douyin", "weibo"]:
            stats["recommendations"].append("可以添加更多话题标签增加曝光")
        
        return stats


# 测试函数
def test_platform_adapter():
    """测试平台适配器"""
    print("测试平台适配器...")
    
    adapter = PlatformAdapter()
    
    # 测试数据
    test_content_structure = {
        "title": "测试用户的八字命理深度分析",
        "summary": "这是一个测试摘要，用于平台适配测试。",
        "analysis": "## 八字分析\n\n这是一个测试内容，包含一些关键信息。\n\n### 五行分析\n金：20%\n木：30%\n水：15%\n火：25%\n土：10%\n\n### 性格特点\n- 热情开朗\n- 有创造力\n- 领导力强\n\n### 建议\n1. 发挥自身优势\n2. 把握时机\n3. 保持好心态",
        "tags": ["八字", "命理", "测试", "五行", "性格"]
    }
    
    try:
        print(f"支持的平台: {', '.join(adapter.list_supported_platforms())}")
        
        for platform in adapter.list_supported_platforms():
            print(f"\n--- 测试平台: {platform} ---")
            
            # 适配内容
            adapted_content = adapter.adapt_content(test_content_structure, platform)
            
            # 获取统计信息
            stats = adapter.get_platform_stats(adapted_content, platform)
            
            print(f"内容长度: {stats['length']}")
            print(f"段落数: {stats['paragraphs']}")
            print(f"emoji数: {stats['emojis']}")
            print(f"话题标签数: {stats['hashtags']}")
            print(f"合规性: {stats['compliance']}")
            
            if stats['recommendations']:
                print(f"建议: {stats['recommendations']}")
            
            # 显示前100个字符
            preview = adapted_content[:100] + "..." if len(adapted_content) > 100 else adapted_content
            print(f"预览: {preview}")
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_platform_adapter()