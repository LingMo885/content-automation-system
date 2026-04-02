#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
凌墨公众号自动发布系统
功能：
1. 读取飞书Bitable中的内容规划
2. 使用content-writer技能生成文章
3. 使用mxai技能生成配图
4. 调用微信公众号API发布到草稿箱
"""

import os
import sys
import json
import requests
import datetime
import subprocess
from pathlib import Path

# 配置信息
CONFIG = {
    "wechat_appid": "wxa05c024a3d75eaa0",
    "wechat_secret": "a98f98457262ba27bf68a7950f4a99d7",
    "feishu_app_token": "XalIb4esLa7oUjsTDvCcYA8tnoe",
    "feishu_table_id": "tblA4uIUEeh3oHH6",
    "workspace_path": "/Users/yyf/.openclaw/workspace",
    "output_dir": "/Users/yyf/.openclaw/workspace/content_automation_system/output",
    "access_token_file": "/Users/yyf/.openclaw/workspace/content_automation_system/wechat_token.json"
}

class WeChatAutoPublisher:
    def __init__(self):
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.setup_directories()
        
    def setup_directories(self):
        """创建必要的目录"""
        Path(CONFIG['output_dir']).mkdir(parents=True, exist_ok=True)
        
    def get_wechat_access_token(self):
        """获取微信公众号access_token"""
        token_file = CONFIG['access_token_file']
        
        # 检查token是否有效
        if os.path.exists(token_file):
            try:
                with open(token_file, 'r') as f:
                    token_data = json.load(f)
                    if datetime.datetime.now().timestamp() < token_data.get('expires_at', 0):
                        return token_data['access_token']
            except:
                pass
        
        # 获取新token
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={CONFIG['wechat_appid']}&secret={CONFIG['wechat_secret']}"
        response = requests.get(url)
        data = response.json()
        
        if 'access_token' in data:
            token_data = {
                'access_token': data['access_token'],
                'expires_at': datetime.datetime.now().timestamp() + data.get('expires_in', 7200) - 300
            }
            with open(token_file, 'w') as f:
                json.dump(token_data, f)
            return data['access_token']
        else:
            print(f"获取access_token失败: {data}")
            return None
    
    def get_today_content_plans(self):
        """获取今天的内容规划（模拟从飞书Bitable读取）"""
        # 这里模拟从飞书Bitable获取数据
        # 实际实现需要使用飞书API
        today_plans = [
            {
                "id": "recvflzIMdrHgq",
                "title": "八字基础知识：天干地支详解",
                "type": "知识科普",
                "status": "待处理"
            },
            {
                "id": "recvflzKMFrzgm",
                "title": "2026年4月生肖运势：属鼠人事业财运分析",
                "type": "运势",
                "status": "待处理"
            },
            {
                "id": "recvflzMSZEOm7",
                "title": "命例分析：从八字看婚姻感情走向",
                "type": "命例分析",
                "status": "待处理"
            }
        ]
        
        print(f"获取到 {len(today_plans)} 个今日内容规划")
        return today_plans
    
    def generate_content_with_skill(self, title, content_type):
        """使用content-writer技能生成文章内容"""
        # 这里调用content-writer技能
        # 实际实现需要调用相应的技能API或命令
        
        prompt = f"""
        请生成一篇关于{title}的微信公众号文章。
        
        要求：
        1. 文章类型：{content_type}
        2. 风格：专业易懂，适合命理爱好者阅读
        3. 结构：标题、引言、正文、结语
        4. 字数：800-1200字
        5. 包含适当的命理术语解释
        6. 结尾要有互动引导（如：欢迎留言分享你的八字）
        
        请用markdown格式输出。
        """
        
        # 模拟生成的内容
        content = f"""
# {title}

## 引言
{title}是八字命理中的重要内容，今天我们就来详细探讨这个话题。

## 正文内容
根据传统命理学的理论，{title.split('：')[0]}对于个人运势有着重要影响。在八字分析中，我们需要综合考虑天干地支、五行生克、十神关系等多个因素。

### 核心要点
1. **基础知识**：首先需要了解相关的基本概念
2. **分析方法**：掌握正确的分析方法和步骤
3. **实际应用**：如何将理论应用到实际命例中
4. **注意事项**：分析时需要注意的关键点

### 详细解析
{title}的具体内容需要根据个人的八字组合来进行分析。不同的八字格局会有不同的表现，需要结合大运流年进行综合判断。

## 结语
希望通过本文的介绍，大家对{title.split('：')[0]}有了更深入的了解。命理学的学习是一个循序渐进的过程，需要不断实践和总结。

**互动话题**：你对{title.split('：')[0]}有什么疑问或心得？欢迎在评论区留言分享！

---
*本文由凌墨命理工作室原创，转载请注明出处*
        """
        
        return content
    
    def generate_image_with_mxai(self, title, content_type):
        """使用mxai技能生成配图"""
        # 这里调用mxai技能生成图片
        # 实际实现需要调用相应的技能API或命令
        
        image_prompt = f"""
        为微信公众号文章生成配图：
        主题：{title}
        类型：{content_type}
        风格：中国风、传统、神秘、专业
        要求：适合命理/八字主题，有传统文化元素
        """
        
        # 模拟生成的图片信息
        image_info = {
            "url": f"https://example.com/images/{title.replace(' ', '_')}.jpg",
            "local_path": f"{CONFIG['output_dir']}/images/{self.today}/{title.replace(' ', '_')}.jpg",
            "prompt": image_prompt
        }
        
        # 创建图片目录
        image_dir = os.path.dirname(image_info["local_path"])
        os.makedirs(image_dir, exist_ok=True)
        
        # 这里应该调用mxai技能生成图片
        # 暂时创建一个占位文件
        with open(image_info["local_path"], 'w') as f:
            f.write(f"# 这里是{title}的配图\n生成时间：{datetime.datetime.now()}")
        
        return image_info
    
    def publish_to_wechat_draft(self, title, content, image_info):
        """发布到微信公众号草稿箱"""
        access_token = self.get_wechat_access_token()
        if not access_token:
            print("无法获取access_token，发布失败")
            return False
        
        # 构建文章数据
        article_data = {
            "articles": [{
                "title": title,
                "author": "凌墨",
                "digest": content[:100] + "...",
                "content": content,
                "content_source_url": "",
                "thumb_media_id": "",  # 需要先上传图片获取media_id
                "show_cover_pic": 1,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }]
        }
        
        # 调用微信草稿箱API
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
        response = requests.post(url, json=article_data)
        result = response.json()
        
        if result.get('errcode') == 0:
            print(f"文章 '{title}' 已成功发布到草稿箱")
            print(f"草稿ID: {result.get('media_id')}")
            return True
        else:
            print(f"发布失败: {result}")
            return False
    
    def update_content_status(self, content_id, status):
        """更新内容状态（模拟更新飞书Bitable）"""
        print(f"更新内容 {content_id} 状态为: {status}")
        # 实际实现需要调用飞书API更新记录
        return True
    
    def run_daily_publish(self):
        """执行每日发布流程"""
        print(f"=== 开始执行凌墨公众号自动发布 ({self.today}) ===")
        
        # 1. 获取今日内容规划
        content_plans = self.get_today_content_plans()
        
        if not content_plans:
            print("今日无内容规划，任务结束")
            return
        
        # 2. 处理每个内容
        for plan in content_plans:
            print(f"\n处理内容: {plan['title']} ({plan['type']})")
            
            # 2.1 生成文章内容
            print("生成文章内容...")
            content = self.generate_content_with_skill(plan['title'], plan['type'])
            
            # 保存文章到本地
            article_file = f"{CONFIG['output_dir']}/articles/{self.today}/{plan['title'].replace(' ', '_')}.md"
            os.makedirs(os.path.dirname(article_file), exist_ok=True)
            with open(article_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"文章已保存: {article_file}")
            
            # 2.2 生成配图
            print("生成配图...")
            image_info = self.generate_image_with_mxai(plan['title'], plan['type'])
            print(f"配图信息: {image_info['local_path']}")
            
            # 2.3 发布到微信草稿箱
            print("发布到微信公众号草稿箱...")
            success = self.publish_to_wechat_draft(plan['title'], content, image_info)
            
            # 2.4 更新状态
            if success:
                self.update_content_status(plan['id'], "已发布")
                print(f"✓ {plan['title']} 处理完成")
            else:
                self.update_content_status(plan['id'], "已生成")
                print(f"⚠ {plan['title']} 已生成但未发布")
        
        print(f"\n=== 凌墨公众号自动发布完成 ({self.today}) ===")
        
        # 生成执行报告
        self.generate_report(content_plans)
    
    def generate_report(self, content_plans):
        """生成执行报告"""
        report_file = f"{CONFIG['output_dir']}/reports/{self.today}_report.md"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        report_content = f"""
# 凌墨公众号自动发布执行报告
## 执行时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 处理内容统计
- 总内容数：{len(content_plans)}
- 处理时间：{self.today}

## 详细内容
{'-' * 50}

"""
        
        for plan in content_plans:
            report_content += f"""
### {plan['title']}
- 类型：{plan['type']}
- 状态：{plan['status']}
- 处理结果：已生成文章和配图

"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"执行报告已生成: {report_file}")

def main():
    """主函数"""
    publisher = WeChatAutoPublisher()
    publisher.run_daily_publish()

if __name__ == "__main__":
    main()