import requests
from bs4 import BeautifulSoup
import time
import json

class GooglePlayScraper:
    def __init__(self, developer_url):
        self.base_url = "https://play.google.com"
        self.url = developer_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def get_app_description(self, app_url):
        try:
            res = requests.get(app_url, headers=self.headers, timeout=10)
            app_soup = BeautifulSoup(res.content, 'html.parser')
            desc = app_soup.find("meta", attrs={"name": "description"})
            if desc:
                # تنظيف النص ليكون صالحاً لملف JSON
                return desc["content"].split(".")[0].strip()
            return "وصف غير متوفر"
        except:
            return "تطبيق تعليمي على متجر جوجل بلاي"

    def scrape_and_save_json(self, filename="apps_data.json"):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # الكلاس البرمجي الخاص بعناصر التطبيقات في جوجل بلاي (قد يحتاج تحديث إذا غيرت جوجل تصميمها)
            apps = soup.find_all('div', class_='VfPpkd-EScbFb-JIbuQc')
            
            if not apps:
                print("❌ لم يتم العثور على تطبيقات. تأكد من صحة الرابط.")
                return

            apps_list = []
            print(f"✅ تم العثور على {len(apps)} تطبيق. جاري استخراج البيانات...")
            
            for app in apps:
                link_tag = app.find('a', href=True)
                if not link_tag: continue
                
                href = link_tag['href']
                package_id = href.split('id=')[-1]
                full_url = f"{self.base_url}{href}"

                name_tag = app.find('span', class_='DdYX5')
                name = name_tag.text.strip() if name_tag else "تطبيق بدون اسم"

                img_tag = app.find('img', class_='stzEZd')
                icon_url = img_tag['src'] if img_tag else ""
                if icon_url:
                    icon_url = icon_url.split('=')[0] + "=s256"

                print(f"   ⏳ جلب بيانات: {name}...")
                description = self.get_app_description(full_url)
                
                # إضافة البيانات للقائمة كقاموس (Dictionary)
                apps_list.append({
                    "id": package_id,
                    "name": name,
                    "description": description,
                    "iconUrl": icon_url,
                    "playStoreUrl": full_url
                })
                
                time.sleep(1)

            # حفظ البيانات في ملف JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(apps_list, f, ensure_ascii=False, indent=4)
                
            print(f"\n✨ اكتملت العملية! تم تحديث ملف {filename}")

        except Exception as e:
            print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    dev_link = "https://play.google.com/store/apps/developer?id=K.G.+Apps"
    scraper = GooglePlayScraper(dev_link)
    scraper.scrape_and_save_json()