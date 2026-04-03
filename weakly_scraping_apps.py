import requests
from bs4 import BeautifulSoup
import time
import json

class GooglePlayScraper:
    def __init__(self, developer_url):
        self.base_url = "https://play.google.com"
        self.url = developer_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def get_app_description(self, app_url):
        """الدخول لصفحة التطبيق وجلب الوصف المختصر"""
        try:
            res = requests.get(app_url, headers=self.headers, timeout=10)
            app_soup = BeautifulSoup(res.content, "html.parser")
            desc = app_soup.find("meta", attrs={"name": "description"})
            if desc:
                return desc["content"].split(".")[0].strip()
            return "وصف غير متوفر"
        except:
            return "تطبيق تعليمي على متجر جوجل بلاي"

    def scrape_apps(self):
        """جلب بيانات التطبيقات"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, "html.parser")
            apps = soup.find_all("div", class_="VfPpkd-EScbFb-JIbuQc")

            if not apps:
                print("❌ لم يتم العثور على تطبيقات.")
                return []

            print(f"✅ تم العثور على {len(apps)} تطبيق. جاري استخراج البيانات...")
            apps_data = []
            for app in apps:
                link_tag = app.find("a", href=True)
                if not link_tag: continue

                href = link_tag["href"]
                package_id = href.split("id=")[-1]
                full_url = f"{self.base_url}{href}"

                name_tag = app.find("span", class_="DdYX5")
                name = name_tag.text.strip() if name_tag else "تطبيق بدون اسم"

                img_tag = app.find("img", class_="stzEZd")
                icon_url = img_tag["src"] if img_tag else ""
                if icon_url:
                    icon_url = icon_url.split("=")[0] + "=s256"

                print(f"   ⏳ جلب بيانات: {name}...")
                description = self.get_app_description(full_url)

                apps_data.append({
                    "id": package_id,
                    "name": name,
                    "description": description,
                    "iconUrl": icon_url,
                    "playStoreUrl": full_url,
                })
                time.sleep(1) 
            return apps_data
        except Exception as e:
            print(f"❌ حدث خطأ: {e}")
            return []

    def save_apps_to_json(self, apps_data, filename="apps_data.json"):
        """حفظ بيانات التطبيقات في ملف JSON (مسح القديم وكتابة الجديد)"""
        try:
            # هنا التعديل: نفتح الملف ونكتب البيانات الجديدة مباشرة بدون تحميل القديم
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(apps_data, f, ensure_ascii=False, indent=4)
            print(f"\n✨ تم بنجاح! الملف {filename} يحتوي الآن على البيانات الجديدة فقط.")
        except Exception as e:
            print(f"❌ حدث خطأ في الحفظ: {e}")

if __name__ == "__main__":
    dev_links = [
        "https://play.google.com/store/apps/developer?id=Asmaa+Zamel",
        "https://play.google.com/store/apps/developer?id=K.G.+Apps",
    ]

    all_apps_data = []
    
    # جمع كل البيانات الجديدة أولاً في قائمة واحدة
    for dev_link in dev_links:
        print(f"\n🔄 جاري السكراب من: {dev_link}")
        scraper = GooglePlayScraper(dev_link)
        apps_data = scraper.scrape_apps()
        all_apps_data.extend(apps_data)

    # حفظ القائمة النهائية (سوف تمسح محتوى الملف القديم تلقائياً)
    if all_apps_data:
        # استدعاء دالة الحفظ من أي كائن سكرابر أو جعلها دالة مستقلة
        final_scraper = GooglePlayScraper("") 
        final_scraper.save_apps_to_json(all_apps_data, "apps_data.json")
    else:
        print("⚠ لم يتم العثور على أي بيانات لحفظها.")
