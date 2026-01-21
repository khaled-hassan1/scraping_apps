import requests
from bs4 import BeautifulSoup
import time

class GooglePlayScraper:
    def __init__(self, developer_url):
        self.base_url = "https://play.google.com"
        self.url = developer_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def get_app_description(self, app_url):
        """الدخول لصفحة التطبيق وجلب الوصف المختصر"""
        try:
            res = requests.get(app_url, headers=self.headers, timeout=10)
            app_soup = BeautifulSoup(res.content, 'html.parser')
            desc = app_soup.find("meta", attrs={"name": "description"})
            if desc:
                # تنظيف النص من علامات التنصيص التي قد تكسر كود Dart
                clean_desc = desc["content"].split(".")[0].replace("'", "\\'")
                return clean_desc
            return "وصف غير متوفر"
        except:
            return "تطبيق تعليمي على متجر جوجل بلاي"

    def scrape_and_save_to_file(self, filename="my_apps_data.dart"):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            apps = soup.find_all('div', class_='VfPpkd-EScbFb-JIbuQc')
            
            if not apps:
                print("❌ لم يتم العثور على تطبيقات. تأكد من صحة الرابط.")
                return

            print(f"✅ تم العثور على {len(apps)} تطبيق. جاري استخراج البيانات وحفظها في {filename}...")
            
            with open(filename, 'w', encoding='utf-8') as f:
                # كتابة ترويسة الملف
                f.write("class MyApps {\n")
                f.write("  static const List<AppData> apps = [\n")
                
                for app in apps:
                    link_tag = app.find('a', href=True)
                    if not link_tag: continue
                    
                    href = link_tag['href']
                    package_id = href.split('id=')[-1]
                    full_url = f"{self.base_url}{href}"

                    name_tag = app.find('span', class_='DdYX5')
                    name = name_tag.text.strip().replace("'", "\\'") if name_tag else "تطبيق بدون اسم"

                    img_tag = app.find('img', class_='stzEZd')
                    icon_url = img_tag['src'] if img_tag else "https://via.placeholder.com/150"
                    icon_url = icon_url.split('=')[0] + "=s256"

                    print(f"   ⏳ جلب بيانات: {name}...")
                    description = self.get_app_description(full_url)
                    
                    # كتابة كائن AppData داخل القائمة
                    f.write(f"    AppData(\n")
                    f.write(f"      id: '{package_id}',\n")
                    f.write(f"      name: '{name}',\n")
                    f.write(f"      description: '{description}',\n")
                    f.write(f"      iconUrl: '{icon_url}',\n")
                    f.write(f"      playStoreUrl: '{full_url}',\n")
                    f.write(f"    ),\n")
                    
                    time.sleep(1) # لتجنب الحظر من جوجل

                # إغلاق القائمة والكلاس
                f.write("  ];\n")
                f.write("}\n")
                
            print(f"\n✨ اكتملت العملية! تم إنشاء الملف بنجاح.")

        except Exception as e:
            print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    dev_link = "https://play.google.com/store/apps/developer?id=K.G.+Apps"
    scraper = GooglePlayScraper(dev_link)
    scraper.scrape_and_save_to_file()