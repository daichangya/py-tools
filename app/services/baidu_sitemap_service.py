import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import urlparse
import gzip
import io

# 创建日志记录器
logger = logging.getLogger(__name__)


class BaiduSitemapService:
    """百度sitemap推送服务类"""
    
    def __init__(self, api_key: str):
        """
        初始化百度sitemap服务
        
        Args:
            api_key: 百度搜索资源平台的API密钥
        """
        self.api_key = api_key
        self.push_url = "http://data.zz.baidu.com/urls"
        self.headers = {
            'Content-Type': 'text/plain',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_sitemap_content(self, sitemap_url: str) -> Optional[str]:
        """
        从URL获取sitemap内容
        
        Args:
            sitemap_url: sitemap文件的URL地址
            
        Returns:
            sitemap内容字符串，如果获取失败返回None
        """
        try:
            response = requests.get(sitemap_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 处理gzip压缩的sitemap
            if sitemap_url.endswith('.gz'):
                with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gzip_file:
                    return gzip_file.read().decode('utf-8')
            else:
                return response.text
                
        except requests.RequestException as e:
            logger.error(f"获取sitemap内容失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"处理sitemap内容时出错: {str(e)}")
            return None
    
    def parse_sitemap(self, sitemap_content: str) -> List[str]:
        """
        解析sitemap内容，提取所有URL
        
        Args:
            sitemap_content: sitemap内容字符串
            
        Returns:
            URL列表
        """
        urls = []
        
        try:
            root = ET.fromstring(sitemap_content)
            
            # 命名空间处理
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # 检查是否是sitemap索引文件
            if root.tag.endswith('sitemapindex'):
                # 处理sitemap索引文件
                for sitemap in root.findall('ns:sitemap', namespace):
                    loc = sitemap.find('ns:loc', namespace)
                    if loc is not None and loc.text:
                        # 递归获取子sitemap内容
                        sub_sitemap_content = self.fetch_sitemap_content(loc.text)
                        if sub_sitemap_content:
                            urls.extend(self.parse_sitemap(sub_sitemap_content))
            
            elif root.tag.endswith('urlset'):
                # 处理普通的urlset
                for url_elem in root.findall('ns:url', namespace):
                    loc = url_elem.find('ns:loc', namespace)
                    if loc is not None and loc.text:
                        urls.append(loc.text)
            
            else:
                logger.warning("未知的sitemap格式")
                
        except ET.ParseError as e:
            logger.error(f"解析sitemap XML时出错: {str(e)}")
        except Exception as e:
            logger.error(f"处理sitemap时发生未知错误: {str(e)}")
        
        return urls

    def push_to_baidu(self, urls: List[str]) -> Dict[str, Any]:
        """
        推送URL到百度搜索资源平台（支持分批推送）

        Args:
            urls: 要推送的URL列表

        Returns:
            推送结果字典
        """
        if not urls:
            return {
                "success": False,
                "message": "没有可推送的URL",
                "stats": {"total": 0, "success": 0, "failed": 0}
            }

        # 百度普通收录接口限制每次最多2000个URL
        BATCH_SIZE = 20
        results = []
        total_success = 0
        total_remain = 0

        # 分批推送URL
        for i in range(0, len(urls), BATCH_SIZE):
            batch_urls = urls[i:i + BATCH_SIZE]

            try:
                # 准备推送数据
                url_text = "\n".join(batch_urls)

                # 构建请求URL
                push_api_url = f"{self.push_url}?site={self._extract_domain(urls[0])}&token={self.api_key}"

                # 发送推送请求
                response = requests.post(push_api_url, data=url_text, headers=self.headers, timeout=30)
                response.raise_for_status()

                result = response.json()
                results.append(result)

                total_success += result.get('success', 0)
                total_remain += result.get('remain', 0)

            except requests.RequestException as e:
                # 打印 response.json() 的错误信息
                logger.error(f"推送请求失败: {response.json()} {str(e)}")
                error_msg = f"推送请求失败: {response.json()} {str(e)}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "message": error_msg,
                    "stats": {"total": len(urls), "success": 0, "failed": len(urls)}
                }
            except Exception as e:
                error_msg = f"推送过程中发生未知错误: {str(e)}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "message": error_msg,
                    "stats": {"total": len(urls), "success": 0, "failed": len(urls)}
                }

        return {
            "success": True,
            "message": f"推送成功，共分{len(results)}批处理",
            "data": results,
            "stats": {
                "total": len(urls),
                "success": total_success,
                "failed": len(urls) - total_success
            }
        }

    def _extract_domain(self, url: str) -> str:
        """
        从URL中提取域名
        
        Args:
            url: 完整的URL
            
        Returns:
            域名
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""
    
    def process_sitemap(self, sitemap_url: str) -> Dict[str, Any]:
        """
        完整的sitemap处理流程：获取->解析->推送
        
        Args:
            sitemap_url: sitemap文件的URL地址
            
        Returns:
            处理结果字典
        """
        # 1. 获取sitemap内容
        sitemap_content = self.fetch_sitemap_content(sitemap_url)
        if not sitemap_content:
            return {
                "success": False,
                "message": "获取sitemap内容失败",
                "stats": {"total": 0, "success": 0, "failed": 0}
            }
        
        # 2. 解析sitemap获取URL列表
        urls = self.parse_sitemap(sitemap_content)
        if not urls:
            return {
                "success": False,
                "message": "解析sitemap未找到有效URL",
                "stats": {"total": 0, "success": 0, "failed": 0}
            }
        
        # 3. 推送到百度
        push_result = self.push_to_baidu(urls)
        
        # 添加解析信息到结果中
        push_result["parsed_urls"] = len(urls)
        push_result["sitemap_url"] = sitemap_url
        
        return push_result