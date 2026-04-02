#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动发布脚本
每天自动生成文章并发布到草稿箱
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
import requests
from datetime import datetime, date

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ba_zi_analyzer import BaZiAnalyzer
from lunarcalendar import Converter, Solar

class WechatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.access_token = None
        self.token_expires_at = 0
    
    def _load_config(self, config_path):
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "wechat_api": {
                "appid": "wxa05c024a3d75eaa0",
                "appsecret": "a98f98457262ba27bf68a7950f4a99d7",
                "enabled": True,
                "auto_publish": True,
                "publish_time": "09:00"
            }
        }
    
    def get_access_token(self, force_refresh=False):
        """获取Access Token"""
        api_config = self.config.get("wechat_api", {})
        
        # 检查是否需要刷新
        if not force_refresh and self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        appid = api_config.get("appid")
        appsecret = api_config.get("appsecret")
        
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            if "access_token" in result:
                self.access_token = result["access_token"]
                self.token_expires_at = time.time() + result.get("expires_in", 7200) - 300  # 提前5分钟过期
                print(f"✓ Access Token 获取成功")
                return self.access_token
            else:
                print(f"✗ 获取 Token 失败: {result}")
                return None
        except Exception as e:
            print(f"✗ 获取 Token 异常: {e}")
            return None
    
    def upload_image(self, image_path):
        """上传封面图到永久素材"""
        token = self.get_access_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': ('cover.jpg', f, 'image/jpeg')}
                resp = requests.post(url, files=files, timeout=30)
                result = resp.json()
                
                if "media_id" in result:
                    print(f"✓ 封面上传成功: {result.get('media_id')}")
                    return result.get("media_id")
                else:
                    print(f"✗ 封面上传失败: {result}")
                    return None
        except Exception as e:
            print(f"✗ 封面上传异常: {e}")
            return None
    
    def create_draft(self, title, content, thumb_media_id, author="凌墨", digest=""):
        """创建草稿箱文章"""
        token = self.get_access_token()
        if not token:
            return None
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
        
        payload = {
            "articles": [{
                "title": title,
                "author": author,
                "digest": digest or f"今日运势深度解析，{title}",
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }]
        }
        
        try:
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if "media_id" in result:
                print(f"✓ 草稿创建成功! media_id: {result.get('media_id')}")
                return result.get("media_id")
            else:
                print(f"✗ 草稿创建失败: {result}")
                return None
        except Exception as e:
            print(f"✗ 草稿创建异常: {e}")
            return None
    
    def generate_daily_article(self, target_date=None):
        """生成每日运势文章"""
        if target_date is None:
            target_date = date.today()
        
        analyzer = BaZiAnalyzer()
        date_str = target_date.strftime("%Y-%m-%d")
        
        # 获取八字信息
        pillar = analyzer.calculate_bazi_pillar(date_str, "08:00")
        lunar = analyzer.convert_to_lunar(date_str)
        
        ri_zhu = pillar["ri_zhu"]
        ri_gan = ri_zhu[0]  # 日干
        ri_zhi = ri_zhu[1]  # 日支
        
        # 获取五行信息
        wu_xing_map = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        gan_wu_xing = wu_xing_map.get(ri_gan, "木")
        
        zhi_wu_xing_map = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
        zhi_wu_xing = zhi_wu_xing_map.get(ri_zhi, "木")
        
        # 标题
        title = f"今日{ri_zhu} | 木火相生，这3个命格今日事业财运双爆发！"
        
        # 内容HTML
        content = self._build_article_html(date_str, lunar, ri_zhu, ri_gan, ri_zhi, gan_wu_xing, zhi_wu_xing)
        
        return title, content, f"今日{ri_zhu}，木火相生能量极佳！事业运最旺Top3命格是哪些？"
    
    def _build_article_html(self, date_str, lunar, ri_zhu, ri_gan, ri_zhi, gan_wx, zhi_wx):
        """构建文章HTML"""
        y, m, d = map(int, date_str.split('-'))
        solar = Solar(y, m, d)
        lunar_obj = Converter.Solar2Lunar(solar)
        lunar_str = f"{lunar_obj.year}年{lunar_obj.month}月{lunar_obj.day}日"
        
        # 根据日干生成内容
        if ri_gan in ["甲", "乙"]:
            luckiest = "日主为木的命格（甲、乙日生）"
            tips = ["利拓展业务，今日人脉关系处理得心应手", "利合作洽谈，双方容易达成共识", "宜积极行动，保守会错过好机会"]
        elif ri_gan in ["丙", "丁"]:
            luckiest = "日主为火的命格（丙、丁日生）"
            tips = ["利创新突破，适合提出新方案或新想法", "贵人运旺盛，容易得到上级或长辈支持", "谈判、签约等事宜顺利推进"]
        elif ri_gan in ["戊", "己"]:
            luckiest = "日主为土的命格（戊、己日生）"
            tips = ["今日利学习进修，提升专业能力", "利处理文案、策划等事务性工作", "财运稳定，不宜冒进，适合稳健理财"]
        elif ri_gan in ["庚", "辛"]:
            luckiest = "日主为金的命格（庚、辛日生）"
            tips = ["利财运拓展，正财收入稳定上涨", "利洽谈议价今日易占上风", "宜果断出击，机遇稍纵即逝"]
        else:  # 壬、癸
            luckiest = "日主为水的命格（壬、癸日生）"
            tips = ["今日利思考规划，灵感迸发", "利水路相关或贸易进出口业务", "贵人暗中相助，注意听取他人意见"]
        
        html = f"""<p style="text-align:center;"><strong>今日{ri_zhu} | 木火相生，这3个命格今日事业财运双爆发！</strong></p>
<p style="text-align:center;color:#b43c3c;">{lunar_str} · 今日运势深度解析</p>
<hr/>
<p style="text-align:center;">今日是{ri_zhu}日——木火相生，能量流通极佳的一天！</p>

<h2>一、今日五行能量速览</h2>
<table style="width:100%;border-collapse:collapse;">
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>公历日期</strong></td><td style="border:1px solid #ddd;padding:8px;">{date_str} {['星期一','星期二','星期三','星期四','星期五','星期六','星期日'][date(y,m,d).weekday()]}</td></tr>
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>农历日期</strong></td><td style="border:1px solid #ddd;padding:8px;">{lunar_str.replace('年', '年').replace('月', '月').replace('日', '日')}</td></tr>
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>日柱</strong></td><td style="border:1px solid #ddd;padding:8px;">{ri_zhu}</td></tr>
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>日干五行</strong></td><td style="border:1px solid #ddd;padding:8px;">{ri_gan}（{gan_wx}）</td></tr>
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>日支五行</strong></td><td style="border:1px solid #ddd;padding:8px;">{ri_zhi}（{zhi_wx}）</td></tr>
<tr><td style="border:1px solid #ddd;padding:8px;"><strong>今日主题</strong></td><td style="border:1px solid #ddd;padding:8px;">木火相生，文明之象，宜事业开疆</td></tr>
</table>

<h2>二、什么是{ri_zhu}日？</h2>
<p>{ri_zhu}，是日干"{ri_gan}"与日支"{ri_zhi}"的组合。</p>
<p><strong style="color:#c83c3c;">🔥 {ri_gan}（{gan_wx}）</strong> — 象征着创造、热情与领导力。今日能量充沛，做事自带正能量。</p>
<p><strong style="color:#3c783c;">🌱 {ri_zhi}（{zhi_wx}）</strong> — 象征着生长、进取与生命力。今日木气旺盛，代表新生和向上突破。</p>
<p><strong style="color:#b45014;">木火相生</strong> — 木能生火，火能照明。{ri_zhu}是能量流通极佳的组合，非常适合开始新项目、谈合作，做决策！</p>

<h2>三、今日事业财运分析</h2>
<h3>🏆 事业运最旺 Top 3</h3>

<p><strong>🥇 {luckiest}</strong></p>
<p>木火相生加持，今日事业爆发力极强！</p>
<ul>
<li>{tips[0]}</li>
<li>{tips[1]}</li>
<li>{tips[2]}</li>
</ul>

<h3>💰 今日财运提示</h3>
<p><strong>今日{ri_zhu}，木火通明，财气流通</strong></p>
<ul>
<li>正财方面：工作收入稳定，容易得到额外奖励或提成。</li>
<li>偏财方面：人脉带来财富机会，适合谈合作分成。</li>
<li>今日财位：正东（旺事业）、东南（旺积累）、正南（旺偏财）。</li>
<li>不宜：赌博、投机性理财。</li>
</ul>

<h2>四、今日感情运势</h2>
<p><strong>💕 今日感情运最旺：日主为火、木的命格</strong></p>
<ul>
<li>单身者：今日贵人运旺，容易通过社交认识新朋友。</li>
<li>有伴侣者：今日适合与伴侣共同规划事务，两人容易达成共识。</li>
<li>注意：今日火气较旺，与伴侣相处时注意语气。</li>
</ul>

<h2>五、今日健康提醒</h2>
<p>今日火气较旺，以下命格需注意：</p>
<ul>
<li>日主为火的命格（丙、丁日生）：容易上火、失眠。宜清淡饮食，多喝温水，早睡。</li>
<li>日主为金的命格（庚、辛日生）：呼吸系统需注意，易有咽喉肿痛、咳嗽等小问题。</li>
<li>日主为水的命格（壬、癸日生）：宜静心养神，避免过度劳累。</li>
</ul>

<h2>六、今日宜忌清单</h2>
<h3>✅ 今日宜</h3>
<ul>
<li>开疆拓土：今日利开启新项目、新计划</li>
<li>社交洽谈：贵人运强，宜拜访客户、谈合作</li>
<li>学习进修：印星加持，利读书、考试、报课</li>
<li>表白求婚：火木能量旺，感情升温的好时机</li>
</ul>

<h3>❌ 今日忌</h3>
<ul>
<li>急躁决策：火气旺时容易冲动，下午3点前不宜做重大决定</li>
<li>与人争执：火上加火，小事可能引发大冲突</li>
<li>赌博投机：财气流通但风险也高，不宜博彩</li>
<li>过度熬夜：火旺伤阴，注意休息，23点前入睡</li>
</ul>

<hr/>
<p><strong>💬 今日互动话题</strong></p>
<p>① 你是以上哪个命格？今天事业运/财运/感情运最旺的是哪个？</p>
<p>② 今天有什么计划？想开始做什么新项目？</p>
<p><strong>👇 留言区见！有具体命格想详细分析？发送你的出生年月日时，小墨帮你详细解读！</strong></p>
<p>更多命理干货、每日运势分析，关注我不迷路～</p>
<p>#{ri_zhu}日 #命理 #八字 #今日运势 #事业运 #财运 #感情运 #五行能量 #传统文化 #玄学</p>"""
        
        return html
    
    def publish_daily(self, image_path=None):
        """执行每日发布"""
        print(f"\n{'='*50}")
        print(f"📅 微信公众号每日发布 | {date.today()}")
        print(f"{'='*50}")
        
        # 1. 生成文章
        print("\n[1/4] 生成文章...")
        title, content, digest = self.generate_daily_article()
        print(f"  标题: {title}")
        
        # 2. 上传封面图
        print("\n[2/4] 上传封面图...")
        if image_path is None:
            # 默认封面图
            possible_paths = [
                "/Users/yyf/.openclaw/workspace/daily_content/{}/post_1_morning/cover_image.jpg".format(date.today().strftime("%Y-%m-%d")),
                "/Users/yyf/.openclaw/workspace/daily_content/2026-03-27/post_1_morning/cover_image.jpg",
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    image_path = p
                    break
        
        if image_path and os.path.exists(image_path):
            thumb_media_id = self.upload_image(image_path)
        else:
            print("  ⚠ 未找到封面图，跳过")
            thumb_media_id = None
        
        if not thumb_media_id:
            print("  ⚠ 封面图上传失败，使用默认")
            thumb_media_id = "P7pU8h-oLBTgbv4idTjk8fF-x362pPyYvsmykRm3I1EKtyDx4Rj5GHPKx1BNkrds"  # 2026-03-31 更新
        
        # 3. 创建草稿
        print("\n[3/4] 创建草稿...")
        media_id = self.create_draft(title, content, thumb_media_id, digest=digest)
        
        # 4. 完成
        print("\n[4/4] 完成!")
        print(f"\n{'='*50}")
        if media_id:
            print(f"✅ 发布成功! media_id: {media_id}")
            print(f"📝 请到微信公众号后台草稿箱查看并发布")
        else:
            print(f"❌ 发布失败，请检查日志")
        print(f"{'='*50}\n")
        
        return media_id is not None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信公众号每日发布')
    parser.add_argument('--date', '-d', help='目标日期 YYYY-MM-DD', default=None)
    parser.add_argument('--image', '-i', help='封面图路径', default=None)
    parser.add_argument('--config', '-c', help='配置文件路径', default=None)
    
    args = parser.parse_args()
    
    publisher = WechatPublisher(args.config)
    
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        title, content, digest = publisher.generate_daily_article(target_date)
        print(f"📅 生成 {args.date} 的文章:")
        print(f"  标题: {title}")
    else:
        success = publisher.publish_daily(args.image)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
