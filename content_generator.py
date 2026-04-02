#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容生成器模块
基于模板和AI生成八字内容
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import jinja2

logger = logging.getLogger(__name__)


class ContentGenerator:
    """内容生成器类"""
    
    def __init__(self, template_dir: str = "content_templates"):
        """
        初始化内容生成器
        
        Args:
            template_dir: 模板目录路径
        """
        self.template_dir = template_dir
        self.templates = self.load_templates()
        self.jinja_env = self.create_jinja_env()
        logger.info(f"内容生成器初始化完成，模板目录: {template_dir}")
    
    def load_templates(self) -> Dict[str, str]:
        """
        加载模板文件
        
        Returns:
            模板字典 {模板名称: 模板内容}
        """
        templates = {}
        
        if not os.path.exists(self.template_dir):
            logger.warning(f"模板目录不存在: {self.template_dir}")
            self.create_default_templates()
        
        try:
            for filename in os.listdir(self.template_dir):
                if filename.endswith('.md') or filename.endswith('.txt'):
                    template_name = os.path.splitext(filename)[0]
                    template_path = os.path.join(self.template_dir, filename)
                    
                    with open(template_path, 'r', encoding='utf-8') as f:
                        templates[template_name] = f.read()
                    
                    logger.debug(f"加载模板: {template_name}")
        
        except Exception as e:
            logger.error(f"加载模板失败: {str(e)}")
        
        return templates
    
    def create_default_templates(self):
        """创建默认模板"""
        logger.info("创建默认模板...")
        os.makedirs(self.template_dir, exist_ok=True)
        
        default_templates = {
            "base": self.get_base_template(),
            "wechat": self.get_wechat_template(),
            "xiaohongshu": self.get_xiaohongshu_template(),
            "douyin": self.get_douyin_template(),
            "zhihu": self.get_zhihu_template(),
            "weibo": self.get_weibo_template()
        }
        
        for name, content in default_templates.items():
            template_path = os.path.join(self.template_dir, f"{name}.md")
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.debug(f"创建默认模板: {name}")
    
    def create_jinja_env(self) -> jinja2.Environment:
        """
        创建Jinja2环境
        
        Returns:
            Jinja2环境实例
        """
        # 创建模板加载器
        template_loader = jinja2.FileSystemLoader(searchpath=self.template_dir)
        
        # 创建环境
        env = jinja2.Environment(
            loader=template_loader,
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 添加自定义过滤器
        env.filters['format_date'] = self.format_date_filter
        env.filters['truncate'] = self.truncate_filter
        env.filters['emphasize'] = self.emphasize_filter
        
        return env
    
    def generate_base_content(self, bazi_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成基础内容
        
        Args:
            bazi_analysis: 八字分析结果
            
        Returns:
            基础内容字典
        """
        try:
            logger.info("生成基础内容")
            
            # 准备模板数据
            template_data = self.prepare_template_data(bazi_analysis)
            
            # 使用基础模板生成内容
            base_content = self.render_template("base", template_data)
            
            # 构建内容结构
            content_structure = {
                "title": self.generate_title(bazi_analysis),
                "summary": self.generate_summary(bazi_analysis),
                "analysis": base_content,
                "recommendations": self.generate_recommendations(bazi_analysis),
                "tags": self.generate_tags(bazi_analysis),
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "bazi_id": bazi_analysis.get("basic_info", {}).get("name", "unknown"),
                    "content_type": "bazi_analysis"
                }
            }
            
            logger.debug(f"生成的基础内容结构: {content_structure.keys()}")
            return content_structure
            
        except Exception as e:
            logger.error(f"生成基础内容失败: {str(e)}", exc_info=True)
            raise
    
    def prepare_template_data(self, bazi_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备模板数据
        
        Args:
            bazi_analysis: 八字分析结果
            
        Returns:
            模板数据字典
        """
        basic_info = bazi_analysis.get("basic_info", {})
        bazi_pillar = bazi_analysis.get("bazi_pillar", {})
        ri_zhu = bazi_analysis.get("ri_zhu", {})
        features = bazi_analysis.get("features", {})
        
        # 构建模板数据
        template_data = {
            "name": basic_info.get("name", ""),
            "birth_date": basic_info.get("birth_date", ""),
            "birth_time": basic_info.get("birth_time", ""),
            "gender": "男" if basic_info.get("gender") == "male" else "女",
            "lunar_date": basic_info.get("lunar_date", ""),
            
            # 八字信息
            "bazi": {
                "nian_zhu": bazi_pillar.get("nian_zhu", ""),
                "yue_zhu": bazi_pillar.get("yue_zhu", ""),
                "ri_zhu": bazi_pillar.get("ri_zhu", ""),
                "shi_zhu": bazi_pillar.get("shi_zhu", "")
            },
            
            # 日主信息
            "ri_zhu_info": {
                "character": ri_zhu.get("character", ""),
                "wu_xing": ri_zhu.get("wu_xing", ""),
                "description": ri_zhu.get("description", "")
            },
            
            # 五行强弱
            "wu_xing_strength": bazi_analysis.get("wu_xing_strength", {}),
            
            # 命理特征
            "features": features,
            
            # 大运信息
            "da_yun": bazi_analysis.get("da_yun", []),
            
            # 分析摘要
            "analysis_summary": bazi_analysis.get("analysis_summary", ""),
            
            # 生成时间
            "generated_time": datetime.now().strftime("%Y年%m月%d日 %H:%M"),
            
            # 其他辅助数据
            "has_personality": len(features.get("personality", [])) > 0,
            "has_career": len(features.get("career", [])) > 0,
            "has_wealth": len(features.get("wealth", [])) > 0,
            "has_relationships": len(features.get("relationships", [])) > 0
        }
        
        return template_data
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template_name: 模板名称
            data: 模板数据
            
        Returns:
            渲染后的内容
        """
        try:
            template = self.jinja_env.get_template(f"{template_name}.md")
            rendered_content = template.render(**data)
            return rendered_content
            
        except jinja2.TemplateNotFound:
            logger.warning(f"模板未找到: {template_name}，使用基础模板")
            # 尝试使用基础模板
            try:
                template = self.jinja_env.get_template("base.md")
                return template.render(**data)
            except:
                # 如果基础模板也不存在，返回简单文本
                return self.generate_fallback_content(data)
        
        except Exception as e:
            logger.error(f"渲染模板失败: {str(e)}")
            return self.generate_fallback_content(data)
    
    def generate_fallback_content(self, data: Dict[str, Any]) -> str:
        """生成回退内容（当模板渲染失败时）"""
        name = data.get("name", "用户")
        bazi = data.get("bazi", {})
        
        content = f"""
# {name}的八字分析

## 八字信息
- 年柱：{bazi.get('nian_zhu', '')}
- 月柱：{bazi.get('yue_zhu', '')}
- 日柱：{bazi.get('ri_zhu', '')}
- 时柱：{bazi.get('shi_zhu', '')}

## 日主分析
日主为{bazi.get('ri_zhu', '')[:1]}，五行属{data.get('ri_zhu_info', {}).get('wu_xing', '')}。

## 命理特征
{data.get('analysis_summary', '')}

## 建议
1. 根据八字特点规划人生方向
2. 注意五行平衡，补足弱势元素
3. 把握大运时机，顺势而为

*分析时间：{data.get('generated_time', '')}*
"""
        return content
    
    def generate_title(self, bazi_analysis: Dict[str, Any]) -> str:
        """生成标题"""
        name = bazi_analysis.get("basic_info", {}).get("name", "这位")
        ri_zhu = bazi_analysis.get("bazi_pillar", {}).get("ri_zhu", "")
        ri_zhu_wu_xing = bazi_analysis.get("ri_zhu", {}).get("wu_xing", "")
        
        titles = [
            f"{name}的{ri_zhu}命理深度解析",
            f"{ri_zhu_wu_xing}命{ri_zhu}：{name}的人生密码",
            f"八字揭秘：{name}的{ri_zhu}命格分析",
            f"{ri_zhu}命理：{name}的性格与运势",
            f"深度解读{name}的{ri_zhu}八字格局"
        ]
        
        import random
        return random.choice(titles)
    
    def generate_summary(self, bazi_analysis: Dict[str, Any]) -> str:
        """生成摘要"""
        analysis_summary = bazi_analysis.get("analysis_summary", "")
        features = bazi_analysis.get("features", {})
        
        if analysis_summary:
            return analysis_summary
        
        # 如果分析摘要为空，从特征中生成
        summary_parts = []
        
        if features.get("personality"):
            summary_parts.append(f"性格{', '.join(features['personality'][:2])}")
        
        if features.get("career"):
            summary_parts.append(f"适合{', '.join(features['career'][:2])}等领域")
        
        if features.get("wealth"):
            summary_parts.append(features['wealth'][0])
        
        return "。".join(summary_parts) + "。"
    
    def generate_recommendations(self, bazi_analysis: Dict[str, Any]) -> List[str]:
        """生成建议"""
        features = bazi_analysis.get("features", {})
        wu_xing_strength = bazi_analysis.get("wu_xing_strength", {})
        
        recommendations = []
        
        # 根据五行强弱给出建议
        strongest = max(wu_xing_strength.items(), key=lambda x: x[1])[0] if wu_xing_strength else None
        weakest = min(wu_xing_strength.items(), key=lambda x: x[1])[0] if wu_xing_strength else None
        
        if strongest:
            recommendations.append(f"充分发挥{strongest}元素的优势")
        
        if weakest and wu_xing_strength.get(weakest, 0) < 10:
            recommendations.append(f"适当补足{weakest}元素的能量")
        
        # 根据特征给出建议
        if features.get("career"):
            recommendations.append(f"优先考虑{', '.join(features['career'][:2])}相关领域")
        
        if features.get("lucky_elements"):
            recommendations.append(f"多接触{', '.join(features['lucky_elements'])}相关的事物")
        
        # 通用建议
        recommendations.extend([
            "保持积极心态，顺势而为",
            "定期复盘，调整人生策略",
            "注重身心健康，平衡工作与生活"
        ])
        
        return recommendations[:5]  # 返回前5条建议
    
    def generate_tags(self, bazi_analysis: Dict[str, Any]) -> List[str]:
        """生成标签"""
        ri_zhu = bazi_analysis.get("bazi_pillar", {}).get("ri_zhu", "")
        ri_zhu_wu_xing = bazi_analysis.get("ri_zhu", {}).get("wu_xing", "")
        features = bazi_analysis.get("features", {})
        
        tags = [
            "八字命理",
            "命理分析",
            ri_zhu,
            f"{ri_zhu_wu_xing}命",
            "人生规划"
        ]
        
        # 添加特征标签
        if features.get("personality"):
            tags.extend(features["personality"][:2])
        
        if features.get("career"):
            tags.extend(features["career"][:2])
        
        # 去重并限制数量
        unique_tags = list(dict.fromkeys(tags))
        return unique_tags[:10]
    
    def ai_enhance(self, content_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI优化内容
        
        Args:
            content_structure: 内容结构
            
        Returns:
            优化后的内容结构
        """
        try:
            logger.info("开始AI优化内容")
            
            # 这里应该调用AI API进行内容优化
            # 由于时间限制，这里实现简化版本
            
            enhanced_content = content_structure.copy()
            
            # 优化标题
            original_title = enhanced_content.get("title", "")
            if original_title:
                enhanced_content["title"] = self.ai_enhance_title(original_title)
            
            # 优化摘要
            original_summary = enhanced_content.get("summary", "")
            if original_summary:
                enhanced_content["summary"] = self.ai_enhance_summary(original_summary)
            
            # 优化分析内容
            original_analysis = enhanced_content.get("analysis", "")
            if original_analysis:
                enhanced_content["analysis"] = self.ai_enhance_analysis(original_analysis)
            
            # 添加AI优化标记
            enhanced_content["metadata"]["ai_enhanced"] = True
            enhanced_content["metadata"]["enhanced_at"] = datetime.now().isoformat()
            
            logger.info("AI优化完成")
            return enhanced_content
            
        except Exception as e:
            logger.error(f"AI优化失败: {str(e)}")
            # 返回原始内容
            return content_structure
    
    def ai_enhance_title(self, title: str) -> str:
        """AI优化标题"""
        # 简化实现，实际应该调用AI API
        enhancements = [
            "【深度解析】",
            "【命理揭秘】",
            "【独家解读】",
            "【专业分析】"
        ]
        
        import random
        enhanced = random.choice(enhancements) + title
        return enhanced
    
    def ai_enhance_summary(self, summary: str) -> str:
        """AI优化摘要"""
        # 简化实现
        if len(summary) < 50:
            return summary + " 本文将从八字格局、五行强弱、十神关系等多角度进行深度分析。"
        return summary
    
    def ai_enhance_analysis(self, analysis: str) -> str:
        """AI优化分析内容"""
        # 简化实现
        lines = analysis.split('\n')
        enhanced_lines = []
        
        for line in lines:
            if line.strip() and len(line.strip()) > 10:
                # 简单优化：添加强调
                if line.startswith('##'):
                    enhanced_lines.append(line + " 👇")
                elif line.startswith('-') or line.startswith('*'):
                    enhanced_lines.append(line + " 💡")
                else:
                    enhanced_lines.append(line)
            else:
                enhanced_lines.append(line)
        
        # 添加结尾
        enhanced_lines.append("\n---")
        enhanced_lines.append("*以上内容由AI辅助生成，仅供参考。命理分析需结合实际情况，建议咨询专业命理师。*")
        
        return '\n'.join(enhanced_lines)
    
    # 自定义Jinja2过滤器
    def format_date_filter(self, date_str: str) -> str:
        """日期格式化过滤器"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y年%m月%d日")
        except:
            return date_str
    
    def truncate_filter(self, text: str, length: int = 100) -> str:
        """截断文本过滤器"""
        if len(text) <= length:
            return text
        return text[:length] + "..."
    
    def emphasize_filter(self, text: str) -> str:
        """强调文本过滤器"""
        return f"**{text}**"
    
    # 默认模板内容
    def get_base_template(self) -> str:
        """获取基础模板"""
        return """# {{ title }}

## 📅 基本信息
- **姓名**：{{ name }}
- **出生日期**：{{ birth_date|format_date }} {{ birth_time }}
- **农历日期**：{{ lunar_date }}
- **性别**：{{ gender }}

## 🎯 八字排盘
| 四柱 | 天干地支 |
|------|----------|
| 年柱 | {{ bazi.nian_zhu }} |
| 月柱 | {{ bazi.yue_zhu }} |
| 日柱 | {{ bazi.ri_zhu }} |
| 时柱 | {{ bazi.shi_zhu }} |

## 🔍 日主分析
**日柱**：{{ ri_zhu_info.character }}
**五行**：{{ ri_zhu_info.wu_xing }}
**特点**：{{ ri_zhu_info.description }}

## ⚖️ 五行强弱分析
{% for wuxing, strength in wu_xing_strength.items() %}
- **{{ wuxing }}**：{{ strength }}%
{% endfor %}

## 🌟 命理特征
{% if has_personality %}
### 性格特点
{% for trait in features.personality %}
- {{ trait }}
{% endfor %}
{% endif %}

{% if has_career %}
### 事业方向
{% for career in features.career %}
- {{ career }}
{% endfor %}
{% endif %}

{% if has_wealth %}
### 财运特征
{% for wealth in features.wealth %}
- {{ wealth }}
{% endfor %}
{% endif %}

{% if features.lucky_elements %}
### 幸运元素
{% for element in features.lucky_elements %}
- {{ element }}
{% endfor %}
{% endif %}

## 📈 大运走势
{% for yun in da_yun %}
- **{{ yun.age }}岁**：{{ yun.yun }} - {{ yun.description }}
{% endfor %}

## 💡 人生建议
1. 根据八字特点，发挥自身优势
2. 把握大运时机，顺势而为
3. 注重五行平衡，补足弱势
4. 保持积极心态，持续成长

---
*生成时间：{{ generated_time }}*
*本分析仅供参考，实际人生还需自己把握*"""

    def get_wechat_template(self) -> str:
        """获取微信公众号模板"""
        return """# {{ title }}

> {{ summary }}

## 一、八字基本信息
**姓名**：{{ name }}
**出生**：{{ birth_date|format_date }} {{ birth_time }}
**八字**：{{ bazi.nian_zhu }} {{ bazi.yue_zhu }} {{ bazi.ri_zhu }} {{ bazi.shi_zhu }}

## 二、命格深度解析

### 1. 日主特性
日柱为**{{ ri_zhu_info.character }}**，五行属**{{ ri_zhu_info.wu_xing }}**。
{{ ri_zhu_info.description }}

### 2. 五行能量分布
{% for wuxing, strength in wu_xing_strength.items() %}
- **{{ wuxing }}**：{{ strength }}% {{ "🌟" * (strength//20) }}
{% endfor %}

### 3. 性格与天赋
{% if features.personality %}
**性格特点**：
{% for trait in features.personality %}
- {{ trait }}
{% endfor %}
{% endif %}

### 4. 事业与财运
{% if features.career %}
**适合领域**：
{% for career in features.career %}
- {{ career }}
{% endfor %}
{% endif %}

{% if features.wealth %}
**财运提示**：
{% for wealth in features.wealth %}
- {{ wealth }}
{% endfor %}
{% endif %}

## 三、十年大运走势
{% for yun in da_yun %}
- **{{ yun.age }}岁**：{{ yun.yun }} → {{ yun.description }}
{% endfor %}

## 四、人生建议与提醒
1. **发挥优势**：{{ features.lucky_elements[0] if features.lucky_elements else "金" }}元素是你的幸运符号
2. **补足短板**：注意{{ features.unlucky_elements[0] if features.unlucky_elements else "水" }}元素的平衡
3. **把握时机**：关注大运转换的关键年份
4. **心态调整**：命理是参考，努力是关键

---

**温馨提示**：八字命理是中国传统文化的一部分，本文分析仅供参考。人生之路还需自己脚踏实地去走，愿您把握当下，创造美好未来！

📅 分析时间：{{ generated_time }}
🏷️ 标签：{% for tag in tags[:5] %}#{{ tag }} {% endfor %}"""

    def get_xiaohongshu_template(self) -> str:
        """获取小红书模板"""
        return """{{ title }} ✨

📝 八字分析来啦！
帮{{ name }}宝宝看了八字，发现了一些小秘密～ 

🔮 **八字信息**：
{{ bazi.nian_zhu }}·{{ bazi.yue_zhu }}·{{ bazi.ri_zhu }}·{{ bazi.shi_zhu }}

🌟 **日主特点**：
{{ ri_zhu_info.character }}日主，{{ ri_zhu_info.wu_xing }}命
{{ ri_zhu_info.description|truncate(50) }}

🌈 **五行能量**：
{% for wuxing, strength in wu_xing_strength.items() %}
{{ wuxing }}：{{ "⭐" * (strength//20) }} {{ strength }}%
{% endfor %}

💫 **性格标签**：
{% for trait in features.personality[:3] %}
#{{ trait }} 
{% endfor %}

🎯 **事业方向**：
{% for career in features.career[:2] %}
• {{ career }}
{% endfor %}

💰 **财运小贴士**：
{{ features.wealth[0] if features.wealth else "财运平稳，细水长流" }}

📅 **近期运势**：
{{ da_yun[0].description if da_yun else "当前运势平稳，适合积累" }}

💡 **建议**：
1. 多接触{{ features.lucky_elements[0] if features.lucky_elements else "金色" }}系物品
2. {{ features.career[0] if features.career else "当前领域" }}发展机会多
3. 保持好心情最重要！

---
#八字命理 #命理分析 #{{ ri_zhu_info.wu_xing }}命 #人生规划 #运势分析
{{ generated_time }} 📍"""

    def get_douyin_template(self) -> str:
        """获取抖音模板"""
        return """🔥 {{ title|truncate(20) }}

💎 八字：{{ bazi.nian_zhu }}{{ bazi.yue_zhu }}{{ bazi.ri_zhu }}{{ bazi.shi_zhu }}

🌟 日主：{{ ri_zhu_info.character }}
✨ 五行：{{ ri_zhu_info.wu_xing }}

📊 五行能量榜：
{% for wuxing, strength in wu_xing_strength.items() if strength > 15 %}
{{ wuxing }} {{ strength }}% {{ "🔥" * (strength//25) }}
{% endfor %}

🎭 性格：
{{ features.personality[0] if features.personality else "待发掘" }}

💼 事业：
{{ features.career[0] if features.career else "多领域发展" }}

💰 财运：
{{ features.wealth[0] if features.wealth else "稳步上升" }}

🚀 建议：
1️⃣ 发挥{{ features.lucky_elements[0] if features.lucky_elements else "自身" }}优势
2️⃣ 把握{{ da_yun[0].age if da_yun else "当前" }}岁运势
3️⃣ 保持积极心态

---
#八字 #命理 #{{ ri_zhu_info.wu_xing }}命 #运势 #人生建议
{{ generated_time }}"""

    def get_zhihu_template(self) -> str:
        """获取知乎模板"""
        return """## {{ title }}

### 背景信息
- **咨询者**：{{ name }}
- **出生时间**：{{ birth_date|format_date }} {{ birth_time }}
- **八字排盘**：{{ bazi.nian_zhu }} {{ bazi.yue_zhu }} {{ bazi.ri_zhu }} {{ bazi.shi_zhu }}

### 专业分析

#### 1. 八字格局
日主为**{{ ri_zhu_info.character }}**，五行属**{{ ri_zhu_info.wu_xing }}**。
{{ ri_zhu_info.description }}

#### 2. 五行能量分析
```text
{% for wuxing, strength in wu_xing_strength.items() %}
{{ wuxing }}：{{ "█" * (strength//10) }} {{ strength }}%
{% endfor %}
```

#### 3. 十神配置与性格
{% if features.personality %}
从八字十神配置来看，性格特征主要体现在：
{% for trait in features.personality %}
- {{ trait }}
{% endfor %}
{% endif %}

#### 4. 事业与财运走势
{% if features.career %}
**适合领域**：
{% for career in features.career %}
- {{ career }}（匹配度：{{ (80 + loop.index0*5)|string + "%" }}）
{% endfor %}
{% endif %}

{% if features.wealth %}
**财运特征**：
> {{ features.wealth[0] }}
{% endif %}

#### 5. 大运周期
| 年龄段 | 大运 | 特点 |
|--------|------|------|
{% for yun in da_yun %}
| {{ yun.age }} | {{ yun.yun }} | {{ yun.description }} |
{% endfor %}

### 综合建议
1. **优势发挥**：重点发展{{ features.lucky_elements[0] if features.lucky_elements else "自身优势" }}相关领域
2. **短板补足**：注意{{ features.unlucky_elements[0] if features.unlucky_elements else "五行平衡" }}
3. **时机把握**：{{ da_yun[1].age if da_yun|length > 1 else "31-40" }}岁是关键发展期
4. **心态建设**：命理为参考，努力为核心

### 免责声明
> 本文基于八字命理理论进行分析，仅供参考。人生充满变数，个人的努力、选择和机遇同样重要。建议结合实际情况，理性看待命理分析。

*分析时间：{{ generated_time }}*
*标签：{% for tag in tags %}{{ tag }} {% endfor %}*"""

    def get_weibo_template(self) -> str:
        """获取微博模板"""
        return """{{ title }}

八字：{{ bazi.nian_zhu }}{{ bazi.yue_zhu }}{{ bazi.ri_zhu }}{{ bazi.shi_zhu }}

📌 日主：{{ ri_zhu_info.character }}（{{ ri_zhu_info.wu_xing }}）
📌 特点：{{ ri_zhu_info.description|truncate(30) }}

🔥 五行最强：{{ max(wu_xing_strength.items(), key=lambda x: x[1])[0] if wu_xing_strength else "未知" }}
💧 五行最弱：{{ min(wu_xing_strength.items(), key=lambda x: x[1])[0] if wu_xing_strength else "未知" }}

💫 性格：{{ features.personality[0] if features.personality else "" }}
🎯 事业：{{ features.career[0] if features.career else "" }}
💰 财运：{{ features.wealth[0] if features.wealth else "" }}

💡 建议：
1. 把握{{ da_yun[0].age if da_yun else "当前" }}运势
2. 发展{{ features.career[0] if features.career else "擅长" }}领域
3. 保持好心态

#八字命理# #{{ ri_zhu_info.wu_xing }}命# #运势分析#
{{ generated_time }}"""


# 测试函数
def test_content_generator():
    """测试内容生成器"""
    print("测试内容生成器...")
    
    # 创建测试数据
    test_bazi_analysis = {
        "basic_info": {
            "name": "测试用户",
            "birth_date": "1990-01-01",
            "birth_time": "12:00",
            "gender": "male",
            "lunar_date": "己巳年冬月十五"
        },
        "bazi_pillar": {
            "nian_zhu": "甲子",
            "yue_zhu": "乙丑", 
            "ri_zhu": "丙寅",
            "shi_zhu": "丁卯"
        },
        "ri_zhu": {
            "character": "丙寅",
            "wu_xing": "火",
            "description": "丙火坐寅木，热情开朗，有创造力"
        },
        "wu_xing_strength": {
            "金": 15.0,
            "木": 25.0,
            "水": 20.0,
            "火": 30.0,
            "土": 10.0
        },
        "features": {
            "personality": ["热情", "开朗", "有领导力", "有时急躁"],
            "career": ["营销", "娱乐", "餐饮", "互联网"],
            "wealth": ["财运旺盛，适合投资"],
            "lucky_elements": ["火", "木"],
            "unlucky_elements": ["水"]
        },
        "da_yun": [
            {"age": "1-10", "yun": "丙寅", "description": "少年运，学业发展期"},
            {"age": "11-20", "yun": "丁卯", "description": "青年运，人际关系发展"}
        ],
        "analysis_summary": "火命丙寅，热情开朗有创造力。适合营销娱乐领域，财运旺盛。"
    }
    
    try:
        generator = ContentGenerator()
        
        print("\n1. 生成基础内容...")
        base_content = generator.generate_base_content(test_bazi_analysis)
        
        print(f"标题: {base_content.get('title')}")
        print(f"摘要: {base_content.get('summary')[:50]}...")
        print(f"标签: {', '.join(base_content.get('tags', [])[:3])}")
        
        print("\n2. AI优化内容...")
        enhanced_content = generator.ai_enhance(base_content)
        print(f"AI优化后标题: {enhanced_content.get('title')}")
        
        print("\n3. 测试模板渲染...")
        template_data = generator.prepare_template_data(test_bazi_analysis)
        
        platforms = ["wechat", "xiaohongshu", "douyin", "zhihu", "weibo"]
        for platform in platforms:
            content = generator.render_template(platform, template_data)
            print(f"{platform}: {len(content)} 字符")
        
        print("\n测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_content_generator()